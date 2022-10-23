/*
 * @author: Chunxu Yang
 * @date: 2022-10-22
 * @description: This is the second part of the second assignment of M2.
 * @description: This program is used to send the acceleration data to the ble.
 * @cite this code is based on the code from the provided website.
 * @cite https://github.com/ucla-hci/m119/blob/main/m2b_peripheral/m2b_peripheral.ino
 */

#include <ArduinoBLE.h>
#include <Arduino_LSM6DS3.h>

#define BLE_UUID_ACCELEROMETER_SERVICE "1101"
#define BLE_UUID_ACCELEROMETER_X "2101"
#define BLE_UUID_ACCELEROMETER_Y "2102"
#define BLE_UUID_ACCELEROMETER_Z "2103"

#define BLE_DEVICE_NAME "Koorong"
#define BLE_LOCAL_NAME "Koorong"

BLEService accelerometerService(BLE_UUID_ACCELEROMETER_SERVICE);

BLEFloatCharacteristic accelerometerCharacteristicX(BLE_UUID_ACCELEROMETER_X, BLERead | BLENotify);
BLEFloatCharacteristic accelerometerCharacteristicY(BLE_UUID_ACCELEROMETER_Y, BLERead | BLENotify);
BLEFloatCharacteristic accelerometerCharacteristicZ(BLE_UUID_ACCELEROMETER_Z, BLERead | BLENotify);

float x, y, z;

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;

  // initialize IMU
  if (!IMU.begin())
  {
    Serial.println("Failed to initialize IMU!");
    while (1)
      ;
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println("Hz");

  // initialize BLE
  if (!BLE.begin())
  {
    Serial.println("Starting Bluetooth® Low Energy module failed!");
    while (1)
      ;
  }

  // set advertised local name and service UUID

  BLE.setLocalName(BLE_LOCAL_NAME);
  BLE.setAdvertisedServiceUuid(accelerometerService.uuid());

  Serial.print("BLE advertised service UUID: ");
  Serial.println(accelerometerService.uuid());
  BLE.setAdvertisedService(accelerometerService);

  // add characteristics and service
  accelerometerService.addCharacteristic(accelerometerCharacteristicX);
  accelerometerService.addCharacteristic(accelerometerCharacteristicY);
  accelerometerService.addCharacteristic(accelerometerCharacteristicZ);

  BLE.addService(accelerometerService);

  // start advertising
  BLE.advertise();

  Serial.println("BLE Accelerometer Peripheral");

  // set the initial value for characteristics
  accelerometerCharacteristicX.writeValue(0);
  accelerometerCharacteristicY.writeValue(0);
  accelerometerCharacteristicZ.writeValue(0);
}

void loop()
{
  BLEDevice central = BLE.central();

  // obtain and write accelerometer data

  if (IMU.accelerationAvailable())
  {
    IMU.readAcceleration(x, y, z);

    accelerometerCharacteristicX.writeValue(x);
    accelerometerCharacteristicY.writeValue(y);
    accelerometerCharacteristicZ.writeValue(z);

    Serial.print("x = ");
    Serial.print(x);
    Serial.print(", y = ");
    Serial.print(y);
    Serial.print(", z = ");
    Serial.println(z);
  }

  // poll central for characteristic updates

  if (central)
  {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
  }

  delay(100);
}