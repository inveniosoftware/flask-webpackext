# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from flask_webpackext import FlaskWebpackExt


def test_version():
    """Test version import."""
    from flask_webpackext import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = FlaskWebpackExt(app)
    assert 'flask-webpackext' in app.extensions

    app = Flask('testapp')
    ext = FlaskWebpackExt()
    assert 'flask-webpackext' not in app.extensions
    ext.init_app(app)
    assert 'flask-webpackext' in app.extensions
