import os
from algokit_utils import(
    AlgoAmount,
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PaymentParams,
)

from dotenv import load_dotenv

load_dotenv()
PASSPHRASE = os.environ.get("PASSPHRASE")

print("--------------------------------------------")
print("Processing account...")

algorand = AlgorandClient.testnet()

cuenta_1 = algorand.account.from_mnemonic(mnemonic=PASSPHRASE)

print(f"Esta es la cuenta con la que vamos a trabajar {cuenta_1.address}")

cuenta_1_info = algorand.account.get_information(cuenta_1)

print(f"El saldo de la cuenta es: {cuenta_1_info.amount.algo}")

cuenta_2 = algorand.account.random()
print(f"Esta es la cuenta 2 con la que vamos a trabajar {cuenta_2.address}")

pay_result = algorand.send.payment(
    PaymentParams(
        sender = cuenta_1.address,
        receiver = cuenta_2.address,
        amount=AlgoAmount(algo=0.5),
        static_fee= AlgoAmount (micro_algo=1_000)
    )
)
print(
    f"\nPay transaction confirmed with TxnID: {pay_result.tx_id}. \nView it on Lora at https://lora.algokit.io/testnet/transaction/{pay_result.tx_id}."
  )

create_asset_result = algorand.send.asset_create(
    AssetCreateParams(
      sender=cuenta_1.address,
      asset_name="Demo ACM",  # A human-readable name for the asset
      unit_name="DACM",  # A short ticker; this is not a unique identifier
      total=1000000,  # The true supply of indivisible units
      decimals=1,  # Used for displaying the asset amount off chain
      default_frozen=False,  # This asset can be transferred freely
      manager=cuenta_1.address,  # Account that can change the asset's config
      reserve=cuenta_1.address,  # Account to hold non-circulating supply
      freeze=cuenta_1.address,  # Account that can freeze asset holdings
      clawback=cuenta_1.address,  # Account that can revoke asset holdings
      note=b"Demo 29 de mayo",
      static_fee= AlgoAmount (micro_algo=1_000)
    )
  )
  # Store the Asset ID Alice created in a variable for later use in the script
  # This UInt64 Asset ID is a unique identifier for the asset on the chain
created_asset = create_asset_result.asset_id
print(
    f"\nAsset ID {created_asset} create transaction confirmed with TxnID: {create_asset_result.tx_id}."
  )
print(
    f"\nView it on Lora at https://lora.algokit.io/testnet/asset/{created_asset}."
  )

asset_info = algorand.asset.get_by_id(created_asset)
print(
    f"\nAsset information from algod's /v2/assets/{{asset-id}} REST API endpoint: {asset_info}."
  )
print(
    "\nLearn about and explore the algod REST API at https://dev.algorand.co/reference/rest-api/overview/#algod-rest-endpoints."
  )

cuenta_2_opt_in_result = algorand.send.asset_opt_in(
    AssetOptInParams(
      sender=cuenta_2.address,
      asset_id=created_asset,
      static_fee= AlgoAmount (micro_algo=1_000)
    )
  )
print(
    f"\nAsset opt-in transaction confirmed with TxnID: {cuenta_2_opt_in_result.tx_id}. \nView it on Lora at https://lora.algokit.io/testnet/transaction/{cuenta_2_opt_in_result.tx_id}."
  )


send_asset_result = algorand.send.asset_transfer(
    AssetTransferParams(
      sender=cuenta_1.address,
      receiver=cuenta_2.address,
      asset_id=created_asset,
      amount=3_000,  # The amount is in the smallest unit of the asset
      note=b"Have a few of my first ASA!",
      static_fee= AlgoAmount (micro_algo=1_000)
    )
  )
print(
    f"\nAsset transfer transaction confirmed with TxnID: {send_asset_result.tx_id}. \nView it on Lora at https://lora.algokit.io/testnet/transaction/{send_asset_result.tx_id}."
  )

cuenta_2_info = algorand.account.get_information(cuenta_2.address)
print(
    f"\Cuenta 2 's account information from algod's /v2/accounts/{{address}} REST API endpoint: \n{cuenta_2_info}."
  )
print(
    "\nLearn about and explore the algod REST API at https://dev.algorand.co/reference/rest-api/overview/#algod-rest-endpoints."
  )