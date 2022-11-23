import threading

from game import run_game
from ble import run_ble_client

if __name__ == "__main__":
    # two threads to run the game and the BLE client
    game_thread = threading.Thread(target=run_game)
    ble_thread = threading.Thread(target=run_ble_client)
