const path = require("path");
const webpack = require("webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const Assets = require("./assets");

module.exports = {
  entry: {
    app: "./itdagene/assets/frontend/js/index.js"
  },
  output: {
    path: __dirname + "/itdagene/assets/frontend/",
    filename: "itdagene.js"
  },
  module: {
    loaders: [
      {
        test: /\.styl$/,
        loader:
          "file-loader?name=itdagene.css!stylus-loader?paths=node_modules/bootstrap-stylus/stylus/"
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
      Assets.map(asset => {
        return {
          from: path.resolve(__dirname, `./node_modules/${asset}/`),
          toType: "dir",
          to: path.resolve(__dirname, `./itdagene/assets/lib/${asset}/`)
        };
      })
    )
  ]
};
