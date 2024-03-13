import base64
import hashlib
import hmac
import json
import logging
import os
from datetime import datetime
from http import HTTPStatus

import boto3
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import RespondToAuthChallengeResponseTypeDef
from pycognito import Cognito, aws_srp
from typing_extensions import TypedDict, Union

from fovus.config.config import Config
from fovus.constants.cli_constants import (
    CLIENT_ID,
    PATH_TO_CREDENTIALS_FILE,
    PATH_TO_DEVICE_INFORMATION_FILE,
    USER_POOL_ID,
)
from fovus.constants.fovus_api_constants import AUTHORIZATION_HEADER
from fovus.constants.util_constants import UTF8
from fovus.exception.user_exception import UserException

NOT_SIGNED_IN_EXCEPTION = UserException(
    HTTPStatus.BAD_REQUEST,
    None,
    "You are not signed in. Please run 'fovus --login' to login.",
)


class InvalidTokensException(Exception):
    pass


class CognitoTokens(TypedDict):
    id_token: str
    access_token: str
    refresh_token: str


class DeviceInformation(TypedDict):
    device_name: str
    device_key: str
    device_group_key: str
    device_password: str
    verifier: str
    salt: str


class FovusCognitoAdapter:
    _cognito_client: CognitoIdentityProviderClient
    _cognito: Cognito

    _device_information: DeviceInformation

    def __init__(
        self,
        cognito_tokens: Union[CognitoTokens, None] = None,
        device_information: Union[DeviceInformation, None] = None,
    ) -> None:
        user_pool_id = Config.get(USER_POOL_ID)
        client_id = Config.get(CLIENT_ID)
        user_pool_region = user_pool_id.split("_", maxsplit=1)[0]

        if cognito_tokens is None:
            cognito_tokens = self.load_credentials()

        if device_information is None:
            device_information = self.load_device_information()

        self._device_information = device_information

        self._cognito_client = boto3.client("cognito-idp", region_name=user_pool_region)

        self._cognito = Cognito(
            id_token=cognito_tokens["id_token"],
            access_token=cognito_tokens["access_token"],
            refresh_token=cognito_tokens["refresh_token"],
            user_pool_id=user_pool_id,
            client_id=client_id,
            user_pool_region=user_pool_region,
        )
        self._init_cognito()

    def get_tokens(self) -> tuple[str, str, str]:
        self._check_tokens()
        return (self._cognito.id_token, self._cognito.access_token, self._cognito.refresh_token)

    def get_claims(self) -> dict:
        claims = self._cognito.id_claims
        if claims is None:
            raise NOT_SIGNED_IN_EXCEPTION
        return claims

    def revoke_credentials(self) -> None:
        self._cognito_client.revoke_token(Token=self._cognito.refresh_token, ClientId=self._cognito.client_id)

    def get_authorization_header(self) -> dict:
        self._check_tokens()
        return {
            AUTHORIZATION_HEADER: self._cognito.id_token,
        }

    @staticmethod
    def sign_out():
        try:
            fovus_cognito_adapter = FovusCognitoAdapter()
            fovus_cognito_adapter.revoke_credentials()
            os.remove(PATH_TO_CREDENTIALS_FILE)
        except InvalidTokensException:
            logging.warning("Invalid tokens. Skipping revoking credentials.")
            os.remove(PATH_TO_CREDENTIALS_FILE)
        except UserException as exc:
            raise exc
        # pylint: disable=broad-except
        except BaseException:
            logging.exception("Failed to revoke token")
            os.remove(PATH_TO_CREDENTIALS_FILE)

    @staticmethod
    def load_credentials() -> CognitoTokens:
        try:
            with open(
                PATH_TO_CREDENTIALS_FILE,
                encoding=UTF8,
            ) as file:
                cognito_tokens = json.load(file)

            return cognito_tokens
        except FileNotFoundError as exc:
            raise NOT_SIGNED_IN_EXCEPTION from exc

    @staticmethod
    def save_credentials(cognito_tokens: CognitoTokens) -> None:
        with open(
            PATH_TO_CREDENTIALS_FILE,
            "w",
            encoding=UTF8,
        ) as file:
            json.dump(cognito_tokens, file)

    @staticmethod
    def load_device_information() -> DeviceInformation:
        try:
            with open(
                PATH_TO_DEVICE_INFORMATION_FILE,
                encoding=UTF8,
            ) as file:
                device_information = json.load(file)

            return device_information
        except FileNotFoundError as exc:
            raise NOT_SIGNED_IN_EXCEPTION from exc

    @staticmethod
    def save_device_information(device_information: DeviceInformation) -> None:
        with open(
            PATH_TO_DEVICE_INFORMATION_FILE,
            "w",
            encoding=UTF8,
        ) as file:
            json.dump(device_information, file)

    @staticmethod
    def generate_device_secrets(device_key: str, device_group_key: str) -> tuple[str, str, str]:
        # Source:
        # https://stackoverflow.com/questions/52499526/device-password-verifier-challenge-response-in-amazon-cognito-using-boto3-and-wa

        device_password = base64.standard_b64encode(os.urandom(40)).decode(UTF8)

        combined_string = f"{device_group_key}{device_key}:{device_password}"
        combined_string_hash = aws_srp.hash_sha256(combined_string.encode(UTF8))
        salt = aws_srp.pad_hex(aws_srp.get_random(16))

        x_value = aws_srp.hex_to_long(aws_srp.hex_hash(salt + combined_string_hash))
        g_long = aws_srp.hex_to_long(aws_srp.G_HEX)
        big_n = aws_srp.hex_to_long(aws_srp.N_HEX)
        verifier_device_not_padded = pow(g_long, x_value, big_n)
        verifier = aws_srp.pad_hex(verifier_device_not_padded)

        salt_str = base64.standard_b64encode(bytearray.fromhex(salt)).decode(UTF8)
        verifier_str = base64.standard_b64encode(bytearray.fromhex(verifier)).decode(UTF8)

        return salt_str, verifier_str, device_password

    # pylint: disable=too-many-locals
    @staticmethod
    def generate_password_claim(
        small_a_value: int,
        large_a_value: int,
        b_value: int,
        device_group_key: str,
        device_key: str,
        device_password: str,
        salt: str,
        secret_block_b64: str,
    ):
        # Source:
        # https://stackoverflow.com/questions/52499526/device-password-verifier-challenge-response-in-amazon-cognito-using-boto3-and-wa

        g_long = aws_srp.hex_to_long(aws_srp.G_HEX)
        big_n = aws_srp.hex_to_long(aws_srp.N_HEX)
        k = aws_srp.hex_to_long(aws_srp.hex_hash("00" + aws_srp.N_HEX + "0" + aws_srp.G_HEX))

        u_value = aws_srp.calculate_u(large_a_value, b_value)
        if u_value == 0:
            raise ValueError("U cannot be zero.")
        username_password = f"{device_group_key}{device_key}:{device_password}"
        username_password_hash = aws_srp.hash_sha256(username_password.encode("utf-8"))

        x_value = aws_srp.hex_to_long(
            aws_srp.hex_hash(aws_srp.pad_hex(base64.standard_b64decode(salt).hex()) + username_password_hash)
        )
        g_mod_pow_xn = pow(g_long, x_value, big_n)
        int_value2 = b_value - k * g_mod_pow_xn
        s_value = pow(int_value2, small_a_value + u_value * x_value, big_n)
        hkdf = aws_srp.compute_hkdf(
            bytearray.fromhex(aws_srp.pad_hex(s_value)),
            bytearray.fromhex(aws_srp.pad_hex(aws_srp.long_to_hex(u_value))),
        )

        timestamp = aws_srp.AWSSRP.get_cognito_formatted_timestamp(datetime.now())

        secret_block_bytes = base64.standard_b64decode(secret_block_b64)
        msg = (
            bytearray(device_group_key, "utf-8")
            + bytearray(device_key, "utf-8")
            + bytearray(secret_block_bytes)
            + bytearray(timestamp, "utf-8")
        )
        hmac_obj = hmac.new(hkdf, msg, digestmod=hashlib.sha256)
        signature_string = base64.standard_b64encode(hmac_obj.digest())

        return (secret_block_b64, signature_string.decode("utf-8"), timestamp)

    @staticmethod
    def respond_to_device_srp_challenge(
        response: RespondToAuthChallengeResponseTypeDef,
        device_information: DeviceInformation,
        cognito_client: CognitoIdentityProviderClient,
        client_id: str,
        username: str,
        user_pool_id: str,
        user_pool_region: str,
    ) -> RespondToAuthChallengeResponseTypeDef:
        aws_srp_client = aws_srp.AWSSRP("", "", user_pool_id, client_id, user_pool_region)

        srp_a = aws_srp_client.calculate_a()

        srp_response = cognito_client.respond_to_auth_challenge(
            ClientId=client_id,
            Session=response["Session"],
            ChallengeName="DEVICE_SRP_AUTH",
            ChallengeResponses={
                "DEVICE_KEY": device_information["device_key"],
                "USERNAME": username,
                "SRP_A": aws_srp.long_to_hex(srp_a),
            },
        )

        secret_block, signature, timestamp = FovusCognitoAdapter.generate_password_claim(
            aws_srp_client.small_a_value,
            aws_srp_client.large_a_value,
            aws_srp.hex_to_long(srp_response["ChallengeParameters"]["SRP_B"]),
            device_information["device_group_key"],
            device_information["device_key"],
            device_information["device_password"],
            device_information["salt"],
            srp_response["ChallengeParameters"]["SECRET_BLOCK"],
        )

        verifier_response = cognito_client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName="DEVICE_PASSWORD_VERIFIER",
            ChallengeResponses={
                "DEVICE_KEY": device_information["device_key"],
                "USERNAME": username,
                "PASSWORD_CLAIM_SIGNATURE": signature,
                "PASSWORD_CLAIM_SECRET_BLOCK": secret_block,
                "TIMESTAMP": timestamp,
            },
        )

        return verifier_response

    def _init_cognito(self) -> None:
        self._check_tokens()

        try:
            self._cognito.verify_tokens()
        except BaseException as exc:
            raise InvalidTokensException from exc

    def _refresh_tokens(self) -> None:
        refresh_response = self._cognito_client.initiate_auth(
            AuthFlow="REFRESH_TOKEN",
            ClientId=self._cognito.client_id,
            AuthParameters={
                "DEVICE_KEY": self._device_information["device_key"],
                "REFRESH_TOKEN": self._cognito.refresh_token,
            },
        )

        cognito_tokens: CognitoTokens = {
            "id_token": refresh_response["AuthenticationResult"]["IdToken"],
            "access_token": refresh_response["AuthenticationResult"]["AccessToken"],
            "refresh_token": self._cognito.refresh_token,
        }

        FovusCognitoAdapter.save_credentials(cognito_tokens)

        self._cognito = Cognito(
            id_token=cognito_tokens["id_token"],
            access_token=cognito_tokens["access_token"],
            refresh_token=cognito_tokens["refresh_token"],
            user_pool_id=self._cognito.user_pool_id,
            client_id=self._cognito.client_id,
            user_pool_region=self._cognito.user_pool_region,
        )
        self._init_cognito()

    def _check_tokens(self, refresh: bool = True) -> bool:
        try:
            if self._cognito.check_token(renew=False):
                if refresh:
                    self._refresh_tokens()
                else:
                    return False
            return True
        except BaseException as exc:
            raise InvalidTokensException from exc
