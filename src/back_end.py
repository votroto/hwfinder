import os

from GioAsyncSubprocess import AsyncSubprocess


def ignore(*x):
    pass


def arp_to_model(line):
    weights = {"REACHABLE": 600, "STALE": 400}

    ip, reach = line.strip().split()
    return [ip, weights.get(reach, 400)]


def populate_store(store, models):
    store.clear()
    for model in models:
        store.append(model)


def handle_row_activated(self, p, d, liststore):
    self_id = liststore[p][0]
    os.system(f"xdg-open 'http://{self_id}'")


def handle_search(d, pulser):
    search_cmd = ["scripts/broadcast_ping.sh"]

    def stop(*x):
        pulser.stop_pulsing()

    pulser.start_pulsing()
    p = AsyncSubprocess(search_cmd, ignore, stop)
    p.run()


def fetch_arp(store):
    search_cmd = ["scripts/query_poseidons.sh"]
    arp = []

    def finish(x, y):
        populate_store(store, map(arp_to_model, arp))

    p = AsyncSubprocess(search_cmd, arp.append, finish)
    p.run()

    return True
