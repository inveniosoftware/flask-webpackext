# SPDX-FileCopyrightText: 2017 CERN.
# SPDX-FileCopyrightText: 2024 Graz University of Technology.
# SPDX-License-Identifier: BSD-3-Clause

"""Proxy to current extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_webpack = LocalProxy(lambda: current_app.extensions["flask-webpackext"])
"""Proxy to current extension."""

current_manifest = LocalProxy(lambda: current_webpack.manifest)
"""Proxy to current manifest."""
