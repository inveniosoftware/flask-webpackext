var path = require('path')
var config = require('./config')
var webpack = require('webpack')
var ExtractTextPlugin = require('extract-text-webpack-plugin')
var OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin')
var ManifestPlugin = require('webpack-manifest-plugin')

cssLoader = {
  loader: 'css-loader',
  options: {
    minimize: process.env.NODE_ENV === 'production',
    sourceMap: true
  }
}

extractSass = new ExtractTextPlugin({
    filename: "css/[name].[contenthash].css",
});

var webpackConfig = {
  entry: {
     app: "./js/app.js",
     styles: "./scss/styles.scss",
  },
  context: config.build.context,
  output: {
    path: config.build.assetsPath,
    filename: 'js/[name].[chunkhash].js',
    chunkFilename: 'js/[id].[chunkhash].js',
    publicPath: config.build.assetsURL
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'eslint-loader',
        enforce: "pre",
        options: {
          formatter: require('eslint-friendly-formatter')
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: [
          cssLoader
        ]
      },
      {
        test: /\.scss$/,
        use: extractSass.extract({
          use: [
            cssLoader,
            {
              loader: "sass-loader",
              options: {
                sourceMap: true
              }
            }
          ]
        })
      },
      // Inline images smaller than 10k
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        loaders: 'url-loader',
        options: {
          limit: 10000,
          name: 'img/[name].[hash:7].[ext]'
        }
      },
      // Inline webfonts smaller than 10k
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'fonts/[name].[hash:7].[ext]'
        }
      }
    ]
  },
  // devtool: process.env.NODE_ENV === 'production' ? 'source-map' : 'cheap-source-map',
  plugins: [
    // Pragmas
    new webpack.DefinePlugin({
      'process.env': process.env.NODE_ENV
    }),
    // Automatically inject jquery
    new webpack.ProvidePlugin({
        jQuery: 'jquery/src/jquery',
        $: 'jquery/src/jquery',
        jquery: 'jquery/src/jquery',
        'window.jQuery': 'jquery/src/jquery'
    }),
    // Compress JavaScript
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false
      },
      sourceMap: true
    }),
    // Extract CSS into its own file
    extractSass,
    new ExtractTextPlugin({
      filename: 'css/[name].[contenthash].css'
    }),
    // Compress extracted CSS. We are using this plugin so that possible
    // duplicated CSS from different components can be deduped.
    new OptimizeCSSPlugin(),
    // Split vendor js into its own file
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      minChunks: function (module, count) {
        // Any required modules inside node_modules are extracted to vendor.
        return (
          module.resource &&
          /\.js$/.test(module.resource) &&
          module.resource.indexOf(
            path.join(__dirname, '../node_modules')
          ) === 0
        )
      }
    }),
    // Extract webpack runtime and module manifest to its own file in order to
    // prevent vendor hash from being updated whenever app bundle is updated.
    new webpack.optimize.CommonsChunkPlugin({
      name: 'manifest',
      chunks: ['vendor']
    }),
    // Write manifest file which Python will read.
    new ManifestPlugin({
      fileName: 'manifest.json',
      stripSrc: true,
      publicPath: config.build.assetsURL
    })
  ]
}

if (process.env.npm_config_report) {
  var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
  webpackConfig.plugins.push(new BundleAnalyzerPlugin())
}

module.exports = webpackConfig
