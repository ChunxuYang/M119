import struct
from bleak import BleakClient, BleakScanner
import asyncio
from pyautogui import press

address_a = "58:bf:25:3a:e8:6e"
address_b = "58:bf:25:3a:e8:6e"

BLE_UUID_ACCELEROMETER_SERVICE = "22e04be7-f090-4c5a-9a32-4dbdb31b738b"

BLE_UUID_ACCELEROMETER_X = "4f612f9d-1c08-47a9-862e-720b3294aeaa"
BLE_UUID_ACCELEROMETER_Y = "4f612f9d-1c08-47a9-862e-720b3294aeab"
BLE_UUID_ACCELEROMETER_Z = "4f612f9d-1c08-47a9-862e-720b3294aeac"
BLE_UUID_GYROSCOPE_X = "4f612f9d-1c08-47a9-862e-720b3294aead"
BLE_UUID_GYROSCOPE_Y = "4f612f9d-1c08-47a9-862e-720b3294aeae"
BLE_UUID_GYROSCOPE_Z = "4f612f9d-1c08-47a9-862e-720b3294aeaf"


async def run(address):

    async with BleakClient(address) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))

        while True:
            ax = await client.read_gatt_char(BLE_UUID_ACCELEROMETER_X)
            ay = await client.read_gatt_char(BLE_UUID_ACCELEROMETER_Y)
            az = await client.read_gatt_char(BLE_UUID_ACCELEROMETER_Z)
            gx = await client.read_gatt_char(BLE_UUID_GYROSCOPE_X)
            gy = await client.read_gatt_char(BLE_UUID_GYROSCOPE_Y)
            gz = await client.read_gatt_char(BLE_UUID_GYROSCOPE_Z)

            ax = struct.unpack('f', ax)[0]
            ay = struct.unpack('f', ay)[0]
            az = struct.unpack('f', az)[0]
            gx = struct.unpack('f', gx)[0]
            gy = struct.unpack('f', gy)[0]
            gz = struct.unpack('f', gz)[0]

            if az > 0.9:
                print("move up")
                press('up')
            elif az < -0.9:
                print("move down")
                press('down')

            await asyncio.sleep(0.01)


def run_ble_client():
    asyncio.run(run(address_a))


if __name__ == "__main__":
    asyncio.run(run(address_a))
