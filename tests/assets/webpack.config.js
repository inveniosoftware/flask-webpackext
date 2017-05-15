var path = require('path');

module.exports = {
  entry: './index.js',
  context: path.resolve(__dirname),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'build'),
  }
};
