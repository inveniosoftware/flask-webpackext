# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

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
