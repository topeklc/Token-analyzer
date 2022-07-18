# coding=utf8
from multiprocessing import Process, Queue
import subprocess

from src.analyzer.analyzer import Analyzer

que = Queue()
using_ports = []


def run_ganache(port, chain):
    global que
    with subprocess.Popen(
        ["ganache-cli", "-p", f"{port}", "-f", f"{chain}"],
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    ) as p:
        for line in p.stdout:
            if line.startswith("(0)"):
                x = line.split()[1]
                que.put(x)


def get_free_port():
    return 6000 if 6000 not in using_ports else using_ports[-1] + 1


def run(token, chain):
    global que
    try:
        port = get_free_port()
        using_ports.append(port)
        p1 = Process(
            target=run_ganache,
            args=(
                port,
                f'{Analyzer.chains[f"{chain}"]["rpc"]}',
            ),
        )
        p1.start()
        account = []
        for _ in range(2):
            account.append(que.get())
        chain = Analyzer(account, token, chain, port)
        try:
            name, symbol = chain.check_name_and_symbol()
        except Exception as e:
            print("Not able to get name and symbol")
            name, symbol = None, None
        try:
            buy_tax = round(chain.check_buy_tax(0.01), 1)
        except Exception as e:
            print("Not able to get buy tax")
            buy_tax = None
        try:
            sell_tax = round(chain.check_sell_tax(), 1)
        except Exception as e:
            print("Not able to get sell tax")
            sell_tax = None
        try:
            total_supply = chain.get_total_supply()
        except Exception as e:
            print("Not able to get total supply")
            total_supply = None
        try:
            circulating_supply= chain.get_circulating_supply()
        except Exception as e:
            print("Not able to get circulating supply")
            circulating_supply = None
        try:
            marketcap = chain.get_marketcap()
        except Exception as e:
            print("Not able to get marketcap")
            marketcap = None
        try:
            owner = chain.get_owner()
            ownership = "Renouced!" if owner in chain.dead else owner
        except Exception as e:
            print("Not able to get owner")
            ownership = "Not able to get owner"
        try:
            subprocess.run(["fuser", "-k", f"{port}/tcp"])
            using_ports.remove(port)
        except Exception as e:
            print(e)
        return name, symbol, buy_tax, sell_tax, total_supply, circulating_supply, marketcap, ownership

    except Exception as e:
        print("Exception occurred: ", e)
        subprocess.run(["fuser", "-k", f"{port}/tcp"])
        print("Something went wrong!")
