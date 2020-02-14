# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017, 2018 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

r"""Webpack integration for Flask.

A simple example
----------------

Let's create a basic Flask application inside ``app.py``. Jinja templates will
reside in the ``templates`` folder and the static files, to be included in the
template, in the ``instance/static`` folder:

.. code-block:: python

    from flask import Flask

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='instance/static'
    )

Let's add a template and an asset to our project:

.. code-block:: console

   src/
     js/
       main.js
   templates/
     index.html
   app.py

The asset will be a simple javascript file:

.. code-block:: javascript

   import $ from 'jquery'

   $(document).ready(function(){
     $("#msg").html("I am webpacked.");
   });

The content of the ``index.html`` we will define later.

To build our asset, let's create the Webpack configuration in
``src/webpack.config.js``:

.. code-block:: javascript

    var path = require('path');
    var config = require('./config');
    var ManifestPlugin = require('webpack-manifest-plugin');

    module.exports = {
        context: config.build.context,
        entry: {
            app: "./js/main.js",
        },
        output: {
            path: config.build.assetsPath,
            filename: 'js/[name].[chunkhash].js',
            publicPath: config.build.assetsURL
        },
        plugins: [
            new ManifestPlugin({
                fileName: 'manifest.json',
                stripSrc: true,
                publicPath: config.build.assetsURL
            })
        ]
    }

You might have noticed that an import of a file which we did not create has
been added, ``config.js``. This is because this file is generated by
Flask-WebpackExt when we run the ``flask webpack create`` command and it will
contain the following information::

    {
      "build": {
          // Absolute path to the directory where Webpack outputs files
          // will be written to.
          "assetsPath": "/private/tmp/testproject/instance/static/dist",

          // URL to access the built assets.
          "assetsURL": "/static/dist/",

          // Absolute path to the generated assets directory.
          "context": "/private/tmp/testproject/instance/assets",

          // Boolean which represents if Flask debug is on.
          "debug": false,

          // Absolute path to the generated static directory.
          "staticPath": "/private/tmp/testproject/instance/static",

          // URL to access the static files.
          "staticURL": "/static/"
      }
    }


This is really important since it is Flask, and only Flask, who knows where
the application path for assets is, so through this configuration we tell
Webpack where to move the bundles.

Also, we will need a ``package.json`` for the npm dependencies, with a run
script ``build`` that executes webpack, in ``src/package.json`` and will be
triggered by ``flask webpack build``:

.. code-block:: JSON

    {
        "private": true,
        "name": "example",
        "version": "0.0.1",
        "author": "myself",
        "license": "WTFPL",
        "description": "example",
        "scripts": {
            "build": "webpack --config webpack.config.js"
        },
        "dependencies": {
            "jquery": "^3.2.1"
        },
        "devDependencies": {
            "webpack-manifest-plugin": "^2.0.4"
        }
    }


We can now define, in ``app.py`` a :class:`~project.WebpackTemplateProject` to
integrate Webpack with our Flask application and build our assets:

.. code-block:: python

    from flask_webpackext.project import WebpackTemplateProject
    from flask_webpackext import FlaskWebpackExt

    project = WebpackTemplateProject(
        __name__,
        project_folder='src',
        config_path='config.json',
    )

    app.config.update(dict(
        WEBPACKEXT_PROJECT=project,
    ))

    # Initialize extension
    FlaskWebpackExt(app)

Since Flask-WebpackExt creates a new template global function called
``webpack`` to inject the assets in templates, we can use it to include the
assets in our template ``index.html``.

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
        </head>
        <body>
            <div id="msg"></div>
            {{ webpack['app.js'] }}
        </body>
    </html>

Finally, we will expose our template through a Flask view:

.. code-block:: python

    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

At this point we are ready to build the assets:

.. code-block:: console

    $ flask webpack buildall

The command will copy all files from the `src` folder to the application
instance folder designated for the Webpack project, download the npm packages
and run Webpack to build our assets.

Alternatively, we can execute each build step separately. To copy all sources
to the working directory:

.. code-block:: console

    $ flask webpack create

To run `npm install` command and download all dependencies:

.. code-block:: console

    $ flask webpack build

To run `npm run build` and execute what you have defined in the
`package.json`:

.. code-block:: console

    $ flask webpack install

Now you can run the application and see if the assets are loaded:

.. code-block:: console

   $ export FLASK_APP=app.py
   $ flask run
   $ firefox http://127.0.0.1:5000/

Assets for multiple Flask modules
---------------------------------

When working with large applications, assets are usually split in different
modules. Flask-WebpackExt uses `pywebpack`_ which allows to solve this problem
by using:

- :class:`~bundle.WebpackBundle` to declare the needed assets and npm
  dependencies for each module.
- :class:`~project.WebpackBundleProject` to gather all bundles under one
  Webpack project.

An example project with two modules could be structured as follows:

.. code-block:: console

  buildconfig/
    package.json
    webpack.config.js
  modules/
    module1/
      js/
      css/
    module2/
      js/
      css/
  templates/
    index.html
  app.py

Let's start with the definition of the first bundle ``bundle1``. ``bundle2``
would be similar:

.. code-block:: python

    from flask_webpackext import WebpackBundle
    bundle1 = WebpackBundle(
        __name__,
        './modules/module1/static',
        entry={
            'module1-app': './js/module1-app.js',
        },
        dependencies={
            'jquery': '^3.2.1'
        }
    )

We now define a :class:`~project.WebpackBundleProject` to put together all the
bundles and integrate with Flask:

.. code-block:: python

    from module1 import bundle1
    from module2 import bundle2
    from flask_webpackext import WebpackBundleProject

    myproject = WebpackBundleProject(
        __name__,
        project_folder='assets',
        config_path='src/config.json',
        bundles=[bundle1, bundle2],
    )

    app.config.update(dict(
        WEBPACKEXT_PROJECT=myproject,
    ))

    # ...

At this point, we can create the application and ``config.json`` will be
generated. The main difference with the previous ``config.json`` is that
Flask-WebpackExt now knows about the bundles, and it will add them under the
key ``entry``::

    {
        "build": {...},
        "entry": {
            "module1": "./js/module1.js",
            "module2": "./js/module2.js"
        }
    }

Because entries are now included in the ``config.json``, we can dynamically
load them into ``webpack.config.js``::

    var config = require('./config')

    module.exports = {
        context: config.build.context,
        entry: config.entry,
        ...
    };


Manifest
--------

Flask-WebpackExt can load the ``manifest.json`` created by webpack when
building the assets. You have to add the plugin in the ``webpack.config.js``
to generate it::

    ...
    var ManifestPlugin = require('webpack-manifest-plugin');

    module.exports = {
        ...
        plugins: [
            new ManifestPlugin({
                fileName: 'manifest.json',
                stripSrc: true,
                publicPath: config.build.assetsURL
            })
        ]
    };

The generated ``manifest.json`` will look like :

.. code-block:: javascript

    {
    "module1.js": "/static/dist/js/module1.4adb22699eb1a5698794.js",
    "module2.js": "/static/dist/js/module2.85e58794420201dc1426.js"
    }

By default, Flask-WebpackExt will look for the manifest file in
`WEBPACKEXT_MANIFEST_PATH` config variable, and if it exists, it will load the
file and make it available inside Jinja templates.

The injected asset in the generated html template will look similar to this::

    <script src="/static/dist/mymodule-app.8817a9d4faccbc712aa7.js"></script>

You can read more about it on `pywebpack`_ documentation.

.. _pywebpack: https://pywebpack.readthedocs.io
"""

from __future__ import absolute_import, print_function

from pywebpack import WebpackProject

from .bundle import WebpackBundle
from .ext import FlaskWebpackExt
from .project import WebpackBundleProject, WebpackTemplateProject
from .proxies import current_manifest, current_webpack
from .version import __version__

__all__ = (
    '__version__',
    'current_manifest',
    'current_webpack',
    'FlaskWebpackExt',
    'WebpackBundle',
    'WebpackBundleProject',
    'WebpackProject',
    'WebpackTemplateProject',
)
