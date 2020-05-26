const path = require("path");
const fs = require("fs-extra");

const assets = [
  "admin-lte/dist",
  "bootstrap/dist",
  "chosen-js",
  "bootstrap-datepicker",
  "eonasdan-bootstrap-datetimepicker/build",
  "bootstrap-chosen",
  "bootstrap-table/dist",
  "tablesorter",
  "jquery/dist",
  "moment/min",
];

const TARGET_DIR = "./itdagene/assets/lib";

for (const asset of assets) {
  fs.copy(
    path.resolve(__dirname, `./node_modules/${asset}`),
    path.resolve(__dirname, `${TARGET_DIR}/${asset}`),
    (err) => {
      if (err) {
        throw err;
      }
      console.log(`Successfully copied asset ${asset}`);
    }
  );
}
