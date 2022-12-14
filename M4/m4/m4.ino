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

#define BLE_UUID_ACCELEROMETER_SERVICE "22e04be7-f090-4c5a-9a32-4dbdb31b738b"

#define BLE_UUID_ACCELEROMETER_X "4f612f9d-1c08-47a9-862e-720b3294aeaa"
#define BLE_UUID_ACCELEROMETER_Y "4f612f9d-1c08-47a9-862e-720b3294aeab"
#define BLE_UUID_ACCELEROMETER_Z "4f612f9d-1c08-47a9-862e-720b3294aeac"
#define BLE_UUID_GYROSCOPE_X "4f612f9d-1c08-47a9-862e-720b3294aead"
#define BLE_UUID_GYROSCOPE_Y "4f612f9d-1c08-47a9-862e-720b3294aeae"
#define BLE_UUID_GYROSCOPE_Z "4f612f9d-1c08-47a9-862e-720b3294aeaf"

#define BLE_DEVICE_NAME "Koorong"
#define BLE_LOCAL_NAME "Koorong"

BLEService imuService(BLE_UUID_ACCELEROMETER_SERVICE);

BLEFloatCharacteristic accelerometerCharacteristicX(BLE_UUID_ACCELEROMETER_X, BLERead | BLENotify);
BLEFloatCharacteristic accelerometerCharacteristicY(BLE_UUID_ACCELEROMETER_Y, BLERead | BLENotify);
BLEFloatCharacteristic accelerometerCharacteristicZ(BLE_UUID_ACCELEROMETER_Z, BLERead | BLENotify);

BLEFloatCharacteristic gyroscopeCharacteristicX(BLE_UUID_GYROSCOPE_X, BLERead | BLENotify);
BLEFloatCharacteristic gyroscopeCharacteristicY(BLE_UUID_GYROSCOPE_Y, BLERead | BLENotify);
BLEFloatCharacteristic gyroscopeCharacteristicZ(BLE_UUID_GYROSCOPE_Z, BLERead | BLENotify);

float ax, ay, az, gx, gy, gz;

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

  // initialize BLE
  if (!BLE.begin())
  {
    Serial.println("Starting BluetoothÂ® Low Energy module failed!");
    while (1)
      ;
  }

  // set advertised local name and service UUID

  BLE.setLocalName(BLE_LOCAL_NAME);
  BLE.setAdvertisedServiceUuid(imuService.uuid());

//  Serial.print("BLE advertised service UUID: ");
//  Serial.println(imuService.uuid());
  BLE.setAdvertisedService(imuService);

  Serial.println(BLE.address());
  // add characteristics and service
  imuService.addCharacteristic(accelerometerCharacteristicX);
  imuService.addCharacteristic(accelerometerCharacteristicY);
  imuService.addCharacteristic(accelerometerCharacteristicZ);
  imuService.addCharacteristic(gyroscopeCharacteristicX);
  imuService.addCharacteristic(gyroscopeCharacteristicY);
  imuService.addCharacteristic(gyroscopeCharacteristicZ);

  BLE.addService(imuService);

  // start advertising
  BLE.advertise();

  Serial.println("BLE Peripheral");

  // set the initial value for characteristics
  accelerometerCharacteristicX.writeValue(0);
  accelerometerCharacteristicY.writeValue(0);
  accelerometerCharacteristicZ.writeValue(0);
  gyroscopeCharacteristicX.writeValue(0);
  gyroscopeCharacteristicY.writeValue(0);
  gyroscopeCharacteristicZ.writeValue(0);
}

void loop()
{
  BLEDevice central = BLE.central();

  // obtain and write accelerometer data

  if (IMU.accelerationAvailable())
  {
    IMU.readAcceleration(ax, ay, az);

    accelerometerCharacteristicX.writeValue(ax);
    accelerometerCharacteristicY.writeValue(ay);
    accelerometerCharacteristicZ.writeValue(az);

//    Serial.print("ax = ");
//    Serial.print(ax);
//    Serial.print(", ay = ");
//    Serial.print(ay);
//    Serial.print(", az = ");
//    Serial.println(az);
  }

  if (IMU.gyroscopeAvailable())
  {
    IMU.readGyroscope(gx, gy, gz);

    gyroscopeCharacteristicX.writeValue(gx);
    gyroscopeCharacteristicY.writeValue(gy);
    gyroscopeCharacteristicZ.writeValue(gz);

    Serial.print("Gx = ");
    Serial.println(gx);
    Serial.print("Gy = ");
    Serial.println(gy);
    Serial.print("Gz = ");
    Serial.println(gz);
  }


  delay(10);
}
