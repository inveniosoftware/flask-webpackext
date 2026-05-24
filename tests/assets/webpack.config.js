/*
 * SPDX-FileCopyrightText: 2017 CERN.
 * SPDX-License-Identifier: BSD-3-Clause
 */
var path = require('path');

module.exports = {
  entry: './index.js',
  context: path.resolve(__dirname),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'build'),
  }
};
