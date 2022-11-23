import threading

from game import run_game
from ble import run_ble_client

if __name__ == "__main__":
    # two threads to run the game and the BLE client
    game_thread = threading.Thread(target=run_game)
    ble_thread = threading.Thread(target=run_ble_client, daemon=True)

    game_thread.start()
    # wait 2 seconds for the game to start
    game_thread.join(2)

    ble_thread.start()


