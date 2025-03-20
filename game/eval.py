from typing import TypeAlias
import algosdk as sdk
from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic
from algosdk import account, transaction as txn, encoding
from algosdk.v2client import algod
import algokit_utils as algorand
import os
import algokit_utils as au
from algokit_utils.models.account import SigningAccount
import algokit_utils.transactions.transaction_composer as att
import client as cl
from utils import (
    account_creation,
     display_info,
    box_abi,
    get_min_balance_required,
    sha256_encode,
    sha256_digest
)
os.system("algokit compile py --out-dir ./app app.py")
os.system(
        "algokit generate client app/Eval.arc32.json --output client.py"
    )

mnemonic = "ankle donate antique hospital any envelope brown school silly best term good pear cherry ball nest nation call lock donkey envelope human assume about useful"
private_key = sdk.mnemonic.to_private_key(mnemonic)
address = account.address_from_private_key(private_key)

print("Adresse de l'account: ", address)
print("Clé privée: ", private_key)

algorand = au.AlgorandClient.testnet()
leo = algorand.account.from_mnemonic(mnemonic=mnemonic)

factory = algorand.client.get_typed_app_factory(
        cl.EvalFactory, default_sender=leo.address
    )


evalId = 736038676
eval = factory.get_app_client_by_id(evalId)


result = eval.send.claim_algo(
      params=au.CommonAppCallParams(
          sender=leo.address,
          signer=leo.signer,
          box_references=[leo.public_key, b"q1" + leo.public_key]
      )
  )

ac = factory.get_app_client_by_id(evalId, default_sender=leo.address)
sp = algorand.get_suggested_params()

mbr_pay_txn = algorand.create_transaction.payment(
        au.PaymentParams(
            sender=leo.address,
            receiver=ac.app_address,
            amount=au.AlgoAmount(algo=0.2),
            extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
        )
    )

ac.send.opt_in_to_asset(
        cl.OptInToAssetArgs(
            mbr_pay = att.TransactionWithSigner(mbr_pay_txn, leo.signer),
            asset = 736069763
        ),
        send_params=au.SendParams(populate_app_call_resources=True)
    )

result = ac.send.sum(
        cl.SumArgs(
            array=bytes([1, 2])
        ),
        params=au.CommonAppCallParams(
            box_references=[leo.address],
            sender=leo.address,
            signer=leo.signer,
        ),
        send_params=au.SendParams(populate_app_call_resources=True)
)

result = ac.send.update_box(
        cl.UpdateBoxArgs(
            value="test"
        ),
        params=au.CommonAppCallParams(
            box_references=[leo.address],
            sender=leo.address,
            signer=leo.signer,
        ),
        send_params=au.SendParams(populate_app_call_resources=True)
)