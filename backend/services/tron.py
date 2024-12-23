from tronpy.tron import Tron


def get_tron_info(address: str):
    tron = Tron()
    account = tron.get_account(address)

    trx_balance = account.get("balance", 0) / 1000000
    bandwidth = account.get("bandwidth", 0)
    energy = account.get("energy", 0)

    return trx_balance, bandwidth, energy
