const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  entry: './web/static/css/base.less',
  output: {
    path: path.resolve(__dirname, 'web/static/css'),
    filename: 'bundle.js'
  },
  module: {
    rules: [{
      test: /\.less$/,
      use: ExtractTextPlugin.extract({
        fallback: "style-loader",
        use: ["css-loader", "less-loader"]
      })
    },
    {
      test: /\.(woff(2)?|ttf|eot|svg)$/,
      use: [{
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: '../fonts/'
        }
      }]
    },
    {
      test: /\.(png|jpg|jpeg|gif)$/,
      use: [{
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: '../images/'
        }
      }]
    }]
  },
  plugins: [
    new ExtractTextPlugin({
      filename: 'base.css'
    })
  ]
};