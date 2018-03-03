const path = require("path");
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");

// List of static assets to be copied to dist
const assets = [
  "animate.css",
  "bootstrap/dist",
  "chosen-js",
  "lightbox2",
  "bootstrap-datepicker",
  "font-awesome",
  "eonasdan-bootstrap-datetimepicker/build",
  "bootstrap-chosen",
  "bootstrap-table/dist",
  "tablesorter",
  "ionicons",
  "hover.css",
  "jquery/dist",
  "moment/min"
];

module.exports = {
  entry: {
    app: "./itdagene/assets/frontend/js/index.js"
  },
  output: {
    path: __dirname + "/itdagene/assets/frontend/",
    filename: "itdagene.js"
  },
  module: {
    rules: [
      {
        test: /\.styl$/,
        loader:
          "file-loader?name=[name].css!stylus-loader?paths=node_modules/bootstrap-stylus/stylus/"
      }
    ]
  },
  plugins: [
    new webpack.LoaderOptionsPlugin({
      options: {
        stylus: {
          use: [require("nib")()],
          import: ["~nib/lib/nib/index.styl"]
        }
      }
    }),

    new CopyWebpackPlugin(
      assets.map(asset => ({
        from: path.resolve(__dirname, `./node_modules/${asset}/`),
        toType: "dir",
        to: path.resolve(__dirname, `./itdagene/assets/lib/${asset}/`)
      }))
    )
  ]
};
