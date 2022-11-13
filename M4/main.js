const express = require("express");

const app = express();
const port = 3000;

const noble = require("@abandonware/noble");

// let acceData = {
//   x: 0,
//   y: 0,
//   z: 0,
// };

let sensorData = {
  ax: 0,
  ay: 0,
  az: 0,
  gx: 0,
  gy: 0,
  gz: 0,
};

// let shifter = new Array(50).fill({
//   ax: 0,
//   ay: 0,
//   az: 0,
//   gx: 0,
//   gy: 0,
//   gz: 0,
// });

// const shifterLength = 100;

const gyThreshold = 150;

// function pushShifter(data) {
//   shifter.push(data);
//   if (shifter.length > shifterLength) {
//     shifter.shift();
//   }
// }

// function detect() {
//   // if gy rises to over threshold, and then false to -threshold, thats a lift
//   // if gy falls to under -threshold, and then true to threshold, thats a drop

//   let gy = shifter.map((data) => data.gy);
//   let gyMax = Math.max(...gy);
//   let gyMin = Math.min(...gy);

//   let gyMaxIndex = gy.indexOf(gyMax);
//   let gyMinIndex = gy.indexOf(gyMin);

//   console.log(gyMax, gyMin, gyMaxIndex, gyMinIndex);

//   if (gyMax > gyThreshold) {
//     // lift
//     console.log("lift");
//   }

//   if (gyMin < -gyThreshold) {
//     // drop
//     console.log("drop");
//   }
// }

const uuid_service = "3822";
const uuid_value_ax = "2101";
const uuid_value_ay = "2102";
const uuid_value_az = "2103";
const uuid_value_gx = "2201";
const uuid_value_gy = "2202";
const uuid_value_gz = "2203";

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
    uuid_value_ax,
    uuid_value_ay,
    uuid_value_az,
    uuid_value_gx,
    uuid_value_gy,
    uuid_value_gz,
  ]);

  // read data
  readData(characteristics);
});

// function debounce(fn, delay) {
//   let timer = null;
//   return function () {
//     let context = this;
//     let args = arguments;
//     clearTimeout(timer);
//     timer = setTimeout(function () {
//       fn.apply(context, args);
//     }, delay);
//   };
// }

// function detect(value) {
//   if (value > gyThreshold) {
//     console.log("gy rise");
//   }

//   if (value < -gyThreshold) {
//     console.log("gy fall");
//   }
// }

let y = 0;

//
// read data periodically
//
let readData = async (characteristics) => {
  let ax = await characteristics[0].readAsync();
  let ay = await characteristics[1].readAsync();
  let az = await characteristics[2].readAsync();
  let gx = await characteristics[3].readAsync();
  let gy = await characteristics[4].readAsync();
  let gz = await characteristics[5].readAsync();

  sensorData.ax = ax.readFloatLE(0);
  sensorData.ay = ay.readFloatLE(0);
  sensorData.az = az.readFloatLE(0);
  sensorData.gx = gx.readFloatLE(0);
  sensorData.gy = gy.readFloatLE(0);
  sensorData.gz = gz.readFloatLE(0);

  setTimeout(readData, 10, characteristics);
};

app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("index", {
    y: y,
  });
});

app.get("/data", (req, res) => {
  res.json(sensorData);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
