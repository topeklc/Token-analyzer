# coding=utf8
from multiprocessing import Process, Queue
import subprocess
import logging

from src.analyzer.analyzer import Analyzer

logging.getLogger(__name__)

using_ports = []
que = Queue()


class Runner:
    def __init__(self, token: str, chain: str) -> None:
        self.analyzer = self.start_analyzer(token, chain)

    def start_analyzer(self, token, chain) -> Analyzer:
        global using_ports, que
        try:
            port = self.get_free_port()
            using_ports.append(port)
            p1 = Process(
                target=self.run_ganache,
                args=(
                    port,
                    f'{Analyzer.chains[f"{chain}"]["rpc"]}',
                ),
            )
            p1.start()
            account = []
            for _ in range(2):
                account.append(que.get())
            return Analyzer(account, token, chain, port)
        except Exception as e:
            logging.error(f"Exception occurred: {e}", e)
            subprocess.run(["fuser", "-k", f"{port}/tcp"])
            logging.error("Something went wrong!")

    @staticmethod
    def stop_analyzer() -> None:
        try:
            subprocess.run(["fuser", "-k", f"{port}/tcp"])
            using_ports.remove(port)
        except Exception as e:
            logging.error(e)

    @staticmethod
    def run_ganache(port: int, chain: str) -> None:
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

    @staticmethod
    def get_free_port() -> int:
        return 6000 if 6000 not in using_ports else sorted(using_ports)[-1] + 1

    def get_name_symbol(self) -> tuple[str, str] | tuple[None, None]:
        try:
            return self.analyzer.check_name_and_symbol()
        except Exception as e:
            logging.error(f"Not able to get name and symbol due to {e}")
            return None, None

    def get_buy_tax(self) -> float | None:
        try:
            return round(self.analyzer.check_buy_tax(0.01), 1)
        except Exception as e:
            logging.error(f"Not able to get buy tax due to {e}")
            return None

    def get_sell_tax(self) -> float | None:
        try:
            return round(self.analyzer.check_sell_tax(), 1)
        except Exception as e:
            logging.error(f"Not able to get sell tax due to {e}")
            return None

    def get_total_supply(self) -> float | None:
        try:
            return self.analyzer.get_total_supply()
        except Exception as e:
            logging.error(f"Not able to get total supply due to {e}")
            return None

    def get_circulating_supply(self) -> float | None:
        try:
            return self.analyzer.get_circulating_supply()
        except Exception as e:
            logging.error(f"Not able to get circulating supply due to {e}")
            return None

    def get_marketcap(self) -> float | None:
        try:
            return self.analyzer.get_marketcap()
        except Exception as e:
            logging.error(f"Not able to get marketcap due to {e}")
            return None

    def get_owner(self) -> str:
        try:
            owner = self.analyzer.get_owner()
            return "Renouced!" if owner in analyzer.dead else owner
        except Exception as e:
            logging.error(f"Not able to get owner due to {e}")
            return "Not able to get owner"

    def get_all_data(self) -> dict:
        name, symbol = self.get_name_symbol()
        return {'name': name, 'symbol': symbol, 'total supply': self.get_total_supply(),
                'criculating supply': self.get_circulating_supply(), 'marketcap': self.get_marketcap(),
                "ownership": self.get_owner(), 'buy tax': self.get_buy_tax(), 'sell tax': self.get_sell_tax()}
