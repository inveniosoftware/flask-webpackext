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

from pywebpack import WebpackProject

from .ext import FlaskWebpackExt
from .project import WebpackBundle, WebpackBundleProject, \
    WebpackTemplateProject
from .proxies import current_webpack, current_manifest
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
