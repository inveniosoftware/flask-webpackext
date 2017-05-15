# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Minimal Flask application example.

First install Flask-WebpackExt, create the instance folder and export
environment variables:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ mkdir instance
   $ export FLASK_APP=app.py FLASK_DEBUG=1

Next, install and build the assets with webpack:

.. code-block:: console

   $ flask webpack buildall

Start the development server:

.. code-block:: console

   $ flask run

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/

"""

from __future__ import absolute_import, print_function

from flask import Flask, render_template

from flask_webpackext import FlaskWebpackExt, WebpackTemplateProject

# Create a Webpack project.
project = WebpackTemplateProject(
    __name__,
    project_folder='assets',
    config_path='build/config.json',
)

# Create Flask application
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='instance/static'
)
# Configure application
app.config.update(dict(
    WEBPACKEXT_PROJECT=project,
    # WEBPACKEXT_STORAGE_CLS='pywebpack:LinkStorage',
))

# Initialize extension
FlaskWebpackExt(app)


# Basic view
@app.route('/')
def index():
    """Frontpage."""
    return render_template('index.html')
