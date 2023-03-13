import json

from eth_account.messages import encode_defunct
from web3 import Web3, HTTPProvider

from app.settings import WALLET_ADDRESS, CHAIN_ID, PRIVATE_KEY, REWARD_CONTRACT_ADDRESS, RPC_URL

f = open('./abi/Reward.json', 'r')
data = json.load(f)
abi = data['abi']
contract_address = REWARD_CONTRACT_ADDRESS
w3 = Web3(HTTPProvider(RPC_URL))


def get_contract():
    return w3.eth.contract(address=contract_address, abi=abi)


def recover_address(message, signature):
    message_hash = encode_defunct(text=message)
    return w3.eth.account.recover_message(message_hash, signature=signature)


def check_blockchain_reward(receiver, target_amount):
    contract = get_contract()
    current_reward_acc = contract.functions.rewardAccumulationMap(Web3.toChecksumAddress(receiver)).call()
    return target_amount - current_reward_acc
def transfer_reward(receiver, target_amount):
    contract = get_contract()
    current_reward_acc = contract.functions.rewardAccumulationMap(receiver).call()
    if target_amount <= current_reward_acc:
        return False
    transaction = contract.functions.reward(int(target_amount), receiver).buildTransaction(
        {'chainId': CHAIN_ID,
         "from": WALLET_ADDRESS,
         "gasPrice": w3.eth.gas_price,
         'nonce': w3.eth.getTransactionCount(WALLET_ADDRESS)
         })
    signed_txn = w3.eth.account.signTransaction(transaction, PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash.hex()
