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

WEBPACKEXT_MANIFEST_LOADER = None
"""Manifest loader use to load manfest."""

WEBPACKEXT_MANIFEST_PATH = 'dist/manifest.json'
"""Path to manifest file relative to static folder."""

WEBPACKEXT_PROJECT = None
"""Webpack project."""

WEBPACKEXT_PROJECT_BUILDDIR = None
"""Directory where Webpack project should be copied to prior to build."""

WEBPACKEXT_PROJECT_DISTDIR = None
"""Directory where Webpack output files should be written to."""

WEBPACKEXT_PROJECT_DISTURL = None
"""URL path to where Webpack output files are accessible."""

WEBPACKEXT_STORAGE_CLS = None
"""Default storage class."""
