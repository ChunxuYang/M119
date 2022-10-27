// use noble to get arduino accelerometer data

const noble = require('@abandonware/noble');

const uuid_service = "1101"
const uuid_value_x = "2101"
const uuid_value_y = "2102"
const uuid_value_z = "2103"

noble.on('stateChange', async (state) => {
  if (state === 'poweredOn') {
    console.log("start scanning")
    await noble.startScanningAsync([uuid_service], false);
  }
});

noble.on('discover', async (peripheral) => {
  await noble.stopScanningAsync();
  await peripheral.connectAsync();
  const services = await peripheral.discoverServicesAsync([uuid_service]);
  const characteristics = await services[0].discoverCharacteristicsAsync([uuid_value_x, uuid_value_y, uuid_value_z]);

  // read data
  readData(characteristics);
});

//
// read data periodically
//
let readData = async (characteristics) => {
  let x = await characteristics[0].readAsync();
  let y = await characteristics[1].readAsync();
  let z = await characteristics[2].readAsync();

  console.log("x: " + x.readFloatLE(0) + ", y: " + y.readFloatLE(0) + ", z: " + z.readFloatLE(0));

  setTimeout(readData, 100, characteristics);
}

