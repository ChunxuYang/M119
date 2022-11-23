import threading

from game import run_game
from ble import run_ble_client
from central import run_central

if __name__ == "__main__":

    ble_thread = threading.Thread(target=run_central, daemon=True)
    ble_thread.start()
    run_game()




