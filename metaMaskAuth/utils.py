import random
import string

from django.core.exceptions import BadRequest
from eth_account.messages import encode_defunct
from eth_keys.exceptions import BadSignature
from web3.auto import w3

from .api_settings import api_settings


def verify_singature(wallet, signature):
    try:
        print(f"nonce: {wallet.nonce}, signature: {signature}")
        print(
            "checking recover_message",
            w3.eth.account.recover_message(
                encode_defunct(text=wallet.nonce), signature=signature
            ),
            "with public_address",
            wallet.public_address,
        )
        if (
            w3.eth.account.recover_message(
                encode_defunct(text=wallet.nonce), signature=signature
            )
            == wallet.public_address
        ):
            return True
        else:
            raise BadRequest("Public address does not match.")

    except BadSignature:
        raise BadRequest("BadSignature!")


def generate_random():
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(api_settings.NONCE_LEN)  # type: ignore
    )
