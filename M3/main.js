const express = require("express");

const app = express();
const port = 3000;

const noble = require("@abandonware/noble");

let sensorData = {
  x: 0,
  y: 0,
  z: 0,
};

const uuid_service = "3822";
const uuid_value_x = "2101";
const uuid_value_y = "2102";
const uuid_value_z = "2103";

noble.on("stateChange", async (state) => {
  if (state === "poweredOn") {
    console.log("start scanning");
    await noble.startScanningAsync([uuid_service], false);
  }
});

noble.on("discover", async (peripheral) => {
  console.log("peripheral discovered", peripheral.advertisement.localName);
  await noble.stopScanningAsync();
  await peripheral.connectAsync();
  const services = await peripheral.discoverServicesAsync([uuid_service]);
  const characteristics = await services[0].discoverCharacteristicsAsync([
    uuid_value_x,
    uuid_value_y,
    uuid_value_z,
  ]);

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

  sensorData.x = x.readFloatLE(0);
  sensorData.y = y.readFloatLE(0);
  sensorData.z = z.readFloatLE(0);

  setTimeout(readData, 10, characteristics);
};

app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("index");
});

app.get("/data", (req, res) => {
  res.json(sensorData);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
