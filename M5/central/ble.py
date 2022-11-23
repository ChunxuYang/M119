from bleak import BleakClient
import asyncio

addressA = "00:00:00:00:00:00"
addressB = "00:00:00:00:00:00"

service_uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
accelerometer_x_characteristic_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
accelerometer_y_characteristic_uuid = "0000ffe2-0000-1000-8000-00805f9b34fb"
accelerometer_z_characteristic_uuid = "0000ffe3-0000-1000-8000-00805f9b34fb"
gyroscope_x_characteristic_uuid = "0000ffe4-0000-1000-8000-00805f9b34fb"
gyroscope_y_characteristic_uuid = "0000ffe5-0000-1000-8000-00805f9b34fb"
gyroscope_z_characteristic_uuid = "0000ffe6-0000-1000-8000-00805f9b34fb"


# create a new thread to run the BLE client
async def run_ble_client():
    client_a = BleakClient(addressA)
    client_b = BleakClient(addressB)
    await client_a.connect()
    await client_b.connect()

    # get accelerometer data and gyroscope data from clientA and clientB
    accelerometer_x_characteristic_a = await client_a.read_gatt_char(accelerometer_x_characteristic_uuid)
    accelerometer_y_characteristic_a = await client_a.read_gatt_char(accelerometer_y_characteristic_uuid)
    accelerometer_z_characteristic_a = await client_a.read_gatt_char(accelerometer_z_characteristic_uuid)
    gyroscope_x_characteristic_a = await client_a.read_gatt_char(gyroscope_x_characteristic_uuid)
    gyroscope_y_characteristic_a = await client_a.read_gatt_char(gyroscope_y_characteristic_uuid)
    gyroscope_z_characteristic_a = await client_a.read_gatt_char(gyroscope_z_characteristic_uuid)

    accelerometer_x_characteristic_b = await client_b.read_gatt_char(accelerometer_x_characteristic_uuid)
    accelerometer_y_characteristic_b = await client_b.read_gatt_char(accelerometer_y_characteristic_uuid)
    accelerometer_z_characteristic_b = await client_b.read_gatt_char(accelerometer_z_characteristic_uuid)
    gyroscope_x_characteristic_b = await client_b.read_gatt_char(gyroscope_x_characteristic_uuid)
    gyroscope_y_characteristic_b = await client_b.read_gatt_char(gyroscope_y_characteristic_uuid)
    gyroscope_z_characteristic_b = await client_b.read_gatt_char(gyroscope_z_characteristic_uuid)

    # print the data
    print("accelerometer_x_characteristic_a: ", accelerometer_x_characteristic_a)
    print("accelerometer_y_characteristic_a: ", accelerometer_y_characteristic_a)
    print("accelerometer_z_characteristic_a: ", accelerometer_z_characteristic_a)
    print("gyroscope_x_characteristic_a: ", gyroscope_x_characteristic_a)
    print("gyroscope_y_characteristic_a: ", gyroscope_y_characteristic_a)
    print("gyroscope_z_characteristic_a: ", gyroscope_z_characteristic_a)

    print("accelerometer_x_characteristic_b: ", accelerometer_x_characteristic_b)
    print("accelerometer_y_characteristic_b: ", accelerometer_y_characteristic_b)
    print("accelerometer_z_characteristic_b: ", accelerometer_z_characteristic_b)
    print("gyroscope_x_characteristic_b: ", gyroscope_x_characteristic_b)
    print("gyroscope_y_characteristic_b: ", gyroscope_y_characteristic_b)
    print("gyroscope_z_characteristic_b: ", gyroscope_z_characteristic_b)

    await client_a.disconnect()
    await client_b.disconnect()


def start_ble_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_ble_client())


if __name__ == "__main__":
    start_ble_client()
