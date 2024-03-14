import os

from aporacle.intervaled_data_symbol import get_api_setup_data

setup_data = get_api_setup_data()


# Web3 Providers
web3_provider_list = [os.getenv("WEB3_PROVIDER")]
web3_websocket_list = [os.getenv("WEB3_WEBSOCKETS")]

test_web3_provider_list = [os.getenv("WEB3_PROVIDER")]
test_web3_websocket_list = [os.getenv("WEB3_WEBSOCKETS")]

# Wallet Tests
flare_systems_manager_address = os.getenv("FLARE_SYSTEMS_MANAGER_ADDRESS")
submission_address = os.getenv("SUBMISSION_ADDRESS")
asset_manager = os.getenv("ASSET_MANAGER_ADDRESS")

relay_address = os.getenv("RELAY_ADDRESS")
ftso_inflation_configurations_address = os.getenv("FTSO_INFLATION_CONFIGURATIONS_ADDRESS")
ftso_feed_publisher_address = os.getenv("FTSO_FEED_PUBLISHER_ADDRESS")

# Chain configurations
chain = os.getenv("CHAIN")
chain_voting_round_duration = int(os.getenv("CHAIN_VOTING_ROUND_DURATION"))