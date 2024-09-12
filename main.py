#!/usr/bin/env python3
import argparse
import binascii
import os

import web3
import web3.eth
from web3.middleware import SignAndSendRawMiddlewareBuilder


def parse_amount(amount_string) -> int:
    return web3.Web3.to_wei(amount_string, "ether")


parser = argparse.ArgumentParser("Send underprised ETH transaction")
parser.add_argument(
    "-r", "--rpc-url", help="RPC url for web3 HTTP provider", required=True
)
parser.add_argument(
    "-k",
    "--private-key",
    default=os.environ.get("PRIVATE_KEY"),
    help="Private key in hex form",
)
parser.add_argument(
    "-t", "--to", required=True, help="Account where to send transaction"
)
parser.add_argument(
    "-a",
    "--amount",
    default="0.00939393",
    type=parse_amount,
    help="Amount (in ETH) to send. Accepts fractional amounts",
)
parser.add_argument(
    "-R",
    "--ratio",
    default="0.001",
    type=float,
    help="Ratio of gas price underrating to pay for transaction",
)
parser.add_argument(
    "--no-dry-run", action="store_true", help="Actually send transaction"
)


def main() -> None:
    args = parser.parse_args()
    assert args.private_key, "Private key should not be empty"

    w3 = web3.Web3(web3.Web3.HTTPProvider(args.rpc_url))
    acc = w3.eth.account.from_key(args.private_key)
    w3.middleware_onion.add(SignAndSendRawMiddlewareBuilder.build(acc))

    tx = {"to": args.to, "from": acc.address, "value": args.amount}
    gas_price = w3.eth.gas_price
    gas_price_underrate = int(gas_price * args.ratio)

    tx["gasPrice"] = gas_price_underrate

    print(
        f"Going to send {args.amount} wei to {args.to}, \n"
        f"price {gas_price}, "
        f"underrated price {gas_price_underrate}"
    )

    if args.no_dry_run:
        receipt = w3.eth.send_transaction(tx)
        print(f"Transaction sent, receipt is 0x{binascii.hexlify(receipt).decode()}")


if __name__ == "__main__":
    main()
