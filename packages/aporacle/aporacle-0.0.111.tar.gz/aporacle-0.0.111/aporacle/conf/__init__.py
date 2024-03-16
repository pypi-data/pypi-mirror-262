import os

import requests


def get_api_setup_data():
    try:
        with requests.Session() as session:
            response = session.get(url=f"http://{os.getenv('TSO_SETUP_URL')}/setup")
            response.raise_for_status()
            setup = response.json()
            return setup

    except Exception as e:
        raise


setup_data = get_api_setup_data()

# Data Service Streamers and APIs
WS = 'ws://'
WSS = 'wss://'
HTTP = 'http://'
HTTPS = 'https://'

tso_utilities_streamer_endpoint = setup_data["algorithms"]["streamers"]["utilities"]["url"]
tso_prepared_streamer_endpoint = setup_data["algorithms"]["streamers"]["prepared"]["url"]
tso_trades_streamer_endpoint = setup_data["algorithms"]["streamers"]["trades"]["url"]

# CHAIN VOTING ROUNDS
algorithm_prepared_data_buffer = 17
ml_predictions_buffer = 12
submission_commit_buffer = 7

# Web3 Providers
for chain in ['coston', 'songbird', 'flare']:
    try:
        web3_provider_list = setup_data["chains"][chain]["providers"]["rpc"]
        web3_websocket_list = setup_data["chains"][chain]["providers"]["ws"]
    except Exception as e:
        print(e)

test_web3_provider_list = [os.getenv("WEB3_PROVIDER")]
test_web3_websocket_list = [os.getenv("WEB3_WEBSOCKETS")]

# Chain Wallet Configuration
flare_reward_offers_manager_addresses = {}
for chain in ['coston', 'songbird', 'flare']:
    try:
        flare_reward_offers_manager_addresses[chain] \
            = setup_data["chains"][chain]["flare_reward_offers_manager_address"]
    except Exception as e:
        print(e)
