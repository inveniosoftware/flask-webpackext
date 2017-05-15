# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack integration for Flask."""

from __future__ import absolute_import, print_function

from .ext import FlaskWebpackExt
from .project import WebpackProject
from .proxies import current_webpack
from .version import __version__

__all__ = (
    '__version__',
    'current_webpack',
    'FlaskWebpackExt',
    'WebpackProject',
)
