# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Proxy to current extension."""

from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy

current_webpack = LocalProxy(
    lambda: current_app.extensions['flask-webpackext'])
"""Proxy to current extension."""

current_manifest = LocalProxy(
    lambda: current_app.extensions['flask-webpackext'].manifest)
"""Proxy to current manifest."""
