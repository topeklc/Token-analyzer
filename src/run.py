# coding=utf8
from multiprocessing import Process, Queue
import subprocess
import logging

from src.analyzer.analyzer import Analyzer

logging.getLogger(__name__)

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
    return 6000 if 6000 not in using_ports else sorted(using_ports)[-1] + 1


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
        analyzer = Analyzer(account, token, chain, port)
        try:
            name, symbol = analyzer.check_name_and_symbol()
        except Exception as e:
            logging.error(f"Not able to get name and symbol due to {e}")
            name, symbol = None, None
        try:
            buy_tax = round(analyzer.check_buy_tax(0.01), 1)
        except Exception as e:
            logging.error(f"Not able to get buy tax due to {e}")
            buy_tax = None
        try:
            sell_tax = round(analyzer.check_sell_tax(), 1)
        except Exception as e:
            logging.error(f"Not able to get sell tax due to {e}")
            sell_tax = None
        try:
            total_supply = analyzer.get_total_supply()
        except Exception as e:
            logging.error(f"Not able to get total supply due to {e}")
            total_supply = None
        try:
            circulating_supply = analyzer.get_circulating_supply()
        except Exception as e:
            logging.error(f"Not able to get circulating supply due to {e}")
            circulating_supply = None
        try:
            marketcap = analyzer.get_marketcap()
        except Exception as e:
            logging.error(f"Not able to get marketcap due to {e}")
            marketcap = None
        try:
            owner = analyzer.get_owner()
            ownership = "Renouced!" if owner in analyzer.dead else owner
        except Exception as e:
            logging.error(f"Not able to get owner due to {e}")
            ownership = "Not able to get owner"
        try:
            subprocess.run(["fuser", "-k", f"{port}/tcp"])
            using_ports.remove(port)
        except Exception as e:
            logging.error(e)
        return name, symbol, buy_tax, sell_tax, total_supply, circulating_supply, marketcap, ownership

    except Exception as e:
        logging.error(f"Exception occurred: {e}", e)
        subprocess.run(["fuser", "-k", f"{port}/tcp"])
        logging.error("Something went wrong!")
