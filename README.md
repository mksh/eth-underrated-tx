eth-underrated-tx
=================

Sends transaction with gas price sent to a ratio of the current one,
leading to underpriced transactions that can easily get stuck in mempool.

This is useful for testing Ethereum features like inclusion lists.

Usage
-----

```bash
pipenv sync
export PRIVATE_KEY="..."         # Eth wallet private key hex
pipenv run python3 main.py \ 
    --to 0x<address> \           # Where to send 
    --rpc-url http://rpc:8545 \  # Ethereum JSON-RPC server
    --no-dry-run                 # If this not present, only prints the plan
```
