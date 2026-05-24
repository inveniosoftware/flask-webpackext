# SPDX-FileCopyrightText: 2017 CERN.
# SPDX-License-Identifier: BSD-3-Clause

"""Module tests."""

from flask import Flask

from flask_webpackext import FlaskWebpackExt


def test_version():
    """Test version import."""
    from flask_webpackext import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = FlaskWebpackExt(app)
    assert "flask-webpackext" in app.extensions

    app = Flask("testapp")
    ext = FlaskWebpackExt()
    assert "flask-webpackext" not in app.extensions
    ext.init_app(app)
    assert "flask-webpackext" in app.extensions
