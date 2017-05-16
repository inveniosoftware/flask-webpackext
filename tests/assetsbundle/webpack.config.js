var path = require('path');
var config = require('./config.json')

module.exports = {
  entry: config.entry,
  context: config.build.context,
  output: {
    filename: '[name].js',
    path: config.build.assetsPath,
  }
};
