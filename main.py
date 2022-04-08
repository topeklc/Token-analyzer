import time
from web3 import Web3


to_approve = 115792089237316195423570985008687907853269984665640564039457584007913129639935

web3 = Web3(Web3.HTTPProvider("https://rpc-mainnet-cardano-evm.c1.milkomeda.com/"))
# tokens
wada = "0xAE83571000aF4499798d1e3b0fA0070EB3A3E3F9"
token = "0xdf2c385F007343a3cBe8C9EA21bb4dAd73b989B9"
# ABIs
router_abi = open('router_abi', 'r').read().replace('\n', '')
factory_abi = open('factory_abi', 'r').read().replace('\n', '')
token_abi = open('token_abi', 'r').read().replace('\n', '')
pair_abi = open('pair_abi', 'r').read().replace('\n', '')
# Router and Factory
router_address = "0x9D2E30C2FB648BeE307EDBaFDb461b09DF79516C"
factory_address = "0xD6Ab33Ad975b39A8cc981bBc4Aaf61F957A5aD29"
router = web3.eth.contract(address=router_address, abi=router_abi)
factory = web3.eth.contract(address=factory_address, abi=factory_abi)
# Token
contract_id = web3.toChecksumAddress(token)
token_contract = web3.eth.contract(address=contract_id, abi=token_abi)

print(contract_id)


def from_wei(value):
    return value / 1e18


def get_pair_address():
    return factory.functions.getPair(wada, token).call()

pair_id = web3.toChecksumAddress(get_pair_address())
pair_contract = web3.eth.contract(address=pair_id, abi=pair_abi)

def get_total_supply():
    return token_contract.functions.totalSupply().call() / 10 ** token_contract.functions.decimals().call()

def check_sell_tax():
    token_contract.functions.approve(
        router_address,
        to_approve
    ).call({'from': "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E"})


    print(router.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
                10000,
                100,
                [token, wada],
                "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E",
                (int(time.time()) + 10000)
            ).call({'from': "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E"}))


def check_buy_tax():
    for_1 = router.functions.swapExactETHForTokens(
        0,
        [wada, contract_id],
        "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E",
        (int(time.time()) + 1000000)
    ).call({'from': "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E", 'value': web3.toWei(1, 'ether')})
    print(router.functions.swapExactETHForTokens(
        0,
        [wada, contract_id],
        "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E",
        (int(time.time()) + 1000000)
    ).call({'from': "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E", 'value': web3.toWei(1, 'ether')}))

    print(router.functions.swapETHForExactTokens(
        for_1[1],
        [wada, contract_id],
        "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E",
        (int(time.time()) + 1000000)
    ).call({'from': "0x5e1De4B71Ba9FDf2F12Ad23530bE0E221687Eb8E", 'value': web3.toWei(1, 'ether')}))


    print(router.functions.getAmountsIn(web3.toWei(1, 'Ether'), [wada, token]).call())
    print(router.functions.getAmountsOut(web3.toWei(1, 'Ether'), [wada, token]).call())



check_buy_tax()

check_sell_tax()