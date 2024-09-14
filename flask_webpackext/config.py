# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017, 2018 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack integration for Flask."""

WEBPACKEXT_MANIFEST_LOADER = None
"""Manifest loader use to load manifest. By default ``JinjaManifestLoader``.
"""

WEBPACKEXT_MANIFEST_PATH = "dist/manifest.json"
"""Path to manifest file relative to static folder."""

WEBPACKEXT_PROJECT = None
"""Webpack project."""

WEBPACKEXT_PROJECT_BUILDDIR = None
"""Directory where Webpack project should be copied to prior to build. By
default ``assets``.
"""

WEBPACKEXT_PROJECT_DISTDIR = None
"""Directory where Webpack output files should be written to. By default
``dist``.
"""

WEBPACKEXT_PROJECT_DISTURL = None
"""URL path to where Webpack output files are accessible. By default ``dist``.
"""

WEBPACKEXT_STORAGE_CLS = None
"""Default storage class. By default ``FileStorage``.
"""
