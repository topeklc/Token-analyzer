import time
import os

from web3 import Web3

dire = os.path.dirname(__file__)


class Analyzer:
    dead = ["0x000000000000000000000000000000000000dEaD", "0x0000000000000000000000000000000000000000"]
    chains = {
        "ETH": {
            "router_address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "factory_address": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
            "main_wrapped_token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "usdc_decimals": 6,
            "rpc": "https://eth-mainnet.public.blastapi.io",
        },
        "BSC": {
            "router_address": "0x10ED43C718714eb63d5aA57B78B54704E256024E",
            "factory_address": "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
            "main_wrapped_token": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            "usdc": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
            "usdc_decimals": 18,
            "rpc": "https://bsc-dataseed.binance.org/",
        },
        "CRO": {
            "router_address": "0x145677FC4d9b8F19B5D56d1820c48e0443049a30",
            "factory_address": "0xd590cC180601AEcD6eeADD9B7f2B7611519544f4",
            "main_wrapped_token": "0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23",
            "usdc": "0xc21223249CA28397B4B6541dfFaEcC539BfF0c59",
            "usdc_decimals": 6,
            "rpc": "https://rpc.artemisone.org/cronos",
        },
        "Milkomeda": {
            "router_address": "0x9D2E30C2FB648BeE307EDBaFDb461b09DF79516C",
            "factory_address": "0xD6Ab33Ad975b39A8cc981bBc4Aaf61F957A5aD29",
            "main_wrapped_token": "0xAE83571000aF4499798d1e3b0fA0070EB3A3E3F9",
            "rpc": "https://rpc-mainnet-cardano-evm.c1.milkomeda.com",
        },
    }
    to_approve = (
        115792089237316195423570985008687907853269984665640564039457584007913129639935
    )
    router_abi = open(os.path.join(dire, "router_abi"), "r").read().replace("\n", "")
    factory_abi = open(os.path.join(dire, "factory_abi"), "r").read().replace("\n", "")
    token_abi = open(os.path.join(dire, "token_abi"), "r").read().replace("\n", "")
    pair_abi = open(os.path.join(dire, "pair_abi"), "r").read().replace("\n", "")

    def __init__(self, account, token, chain, port):
        self.web3 = Web3(Web3.HTTPProvider(f"HTTP://127.0.0.1:{port}"))
        self.account_pub = account[0]
        self.account_prv = account[1]
        self.main_wrapped_token = self.chains[f"{chain}"]["main_wrapped_token"]
        self.usdc = self.chains[f"{chain}"]["usdc"]
        self.usdc_decimals = self.chains[f"{chain}"]["usdc_decimals"]
        self.token = self.web3.toChecksumAddress(token)
        self.router_address = self.chains[f"{chain}"]["router_address"]
        self.factory_address = self.chains[f"{chain}"]["factory_address"]
        self.router = self.web3.eth.contract(
            address=self.router_address, abi=self.router_abi
        )
        self.factory = self.web3.eth.contract(
            address=self.factory_address, abi=self.factory_abi
        )
        self.contract_id = self.web3.toChecksumAddress(self.token)
        self.token_contract = self.web3.eth.contract(
            address=self.contract_id, abi=self.token_abi
        )
        self.main_wrapped_token_contract = self.web3.eth.contract(
            address=self.main_wrapped_token, abi=self.token_abi
        )
        self.token_decimals = self.token_contract.functions.decimals().call()
        self.pair_address = self.web3.toChecksumAddress(self.get_pair_address())
        self.pair_contract = self.web3.eth.contract(
            address=self.pair_address, abi=self.pair_abi
        )

    def approve_all(self):
        nonce = self.web3.eth.get_transaction_count(self.account_pub)
        tx = self.token_contract.functions.approve(
            self.router_address, self.to_approve
        ).buildTransaction(
            {
                "from": self.account_pub,
                "value": self.web3.toWei(0, "ether"),
                "gas": 10**6,
                "gasPrice": self.web3.toWei(70, "gwei"),
                "nonce": nonce,
            }
        )
        signed_txn = self.web3.eth.account.sign_transaction(tx, self.account_prv)
        self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    def buy(self, amount):
        tx = self.router.functions.swapExactETHForTokens(
            0,
            [self.main_wrapped_token, self.contract_id],
            self.account_pub,
            (int(time.time()) + 1000000),
        ).buildTransaction(
            {
                "from": self.account_pub,
                "value": self.web3.toWei(amount, "ether"),
                "gas": 10**6,
                "gasPrice": self.web3.toWei(70, "gwei"),
                "nonce": self.web3.eth.get_transaction_count(self.account_pub),
            }
        )
        signed_txn = self.web3.eth.account.sign_transaction(tx, self.account_prv)
        self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    def sell_all(self):
        nonce = self.web3.eth.get_transaction_count(self.account_pub)
        tx = self.router.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            self.token_contract.functions.balanceOf(self.account_pub).call(),
            0,
            [self.token, self.main_wrapped_token],
            self.account_pub,
            (int(time.time()) + 10000),
        ).buildTransaction(
            {
                "from": self.account_pub,
                "gas": 10**6,
                "gasPrice": self.web3.toWei(70, "gwei"),
                "nonce": nonce,
            }
        )
        signed_txn = self.web3.eth.account.sign_transaction(tx, self.account_prv)
        tx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        gas_used = self.web3.eth.get_transaction_receipt(tx)["gasUsed"]
        return self.web3.fromWei(gas_used * self.web3.toWei(70, "gwei"), "ether")

    def check_name_and_symbol(self):
        name = self.token_contract.functions.name().call()
        symbol = self.token_contract.functions.symbol().call()
        return name, symbol

    def get_pair_address(self):
        return self.factory.functions.getPair(
            self.main_wrapped_token, self.token
        ).call()

    def check_eth_balance(self):
        return self.web3.fromWei(self.web3.eth.get_balance(self.account_pub), "ether")

    def get_pool(self):
        main_wrapped_token = self.main_wrapped_token_contract.functions.balanceOf(self.pair_address).call() / 10**18
        token = self.token_contract.functions.balanceOf(self.pair_address).call() / 10**self.token_decimals
        return main_wrapped_token, token

    def get_total_supply(self):
        return (
            self.token_contract.functions.totalSupply().call()
            / 10 ** self.token_contract.functions.decimals().call()
        )

    def get_burned_supply(self):
        burned = sum([self.token_contract.functions.balanceOf(
                x
            ).call()
            / 10**self.token_decimals for x in self.dead])
        return burned

    def get_main_price(self):
        amount = self.web3.toWei(1, "Ether")
        amount_out = self.router.functions.getAmountsOut(
            amount, [self.main_wrapped_token, self.usdc]
        ).call()
        price = amount_out[1] / 10**self.usdc_decimals
        return price

    def get_token_price(self):
        main_wrapped_token, token = self.get_pool()
        return (main_wrapped_token / token) * self.get_main_price()

    def get_circulating_supply(self):
        return self.get_total_supply() - self.get_burned_supply()

    def get_marketcap(self):
        return self.get_circulating_supply() * self.get_token_price()

    def check_sell_tax(self):
        supposed_amount = (
            self.router.functions.getAmountsOut(
                self.token_contract.functions.balanceOf(self.account_pub).call(),
                [self.token, self.main_wrapped_token],
            ).call()[1]
            / 10**18
        )
        self.approve_all()
        balance_before_sell = self.check_eth_balance()
        fee = self.sell_all()
        balance_after_sell = self.check_eth_balance()
        return round(
            (
                1
                - (float(balance_after_sell) - float(balance_before_sell) + float(fee))
                / supposed_amount
            )
            * 100,
            2,
        )

    def check_buy_tax(self, amount):
        supposed_amount = self.router.functions.getAmountsOut(
            self.web3.toWei(amount, "Ether"), [self.main_wrapped_token, self.token]
        ).call()[1]
        self.buy(amount)
        real_amount = self.token_contract.functions.balanceOf(self.account_pub).call()
        return round((supposed_amount - real_amount) / supposed_amount * 100, 2)

    def get_owner(self):
        try:
            owner = self.token_contract.functions.getOwner().call()
        except:
            try:
                owner = self.token_contract.functions.owner().call()
            except:
                owner = "couldn't fetch owner"
        return owner

    def is_contract(self, address):
        return True if self.web3.eth.getCode(address) else False