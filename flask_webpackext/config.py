# SPDX-FileCopyrightText: 2017, 2018 CERN.
# SPDX-FileCopyrightText: 2024 Graz University of Technology.
# SPDX-License-Identifier: BSD-3-Clause

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
