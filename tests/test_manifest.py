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

import sys

import pytest
from flask import render_template_string
from pywebpack import ManifestLoader

from flask_webpackext.manifest import JinjaManifestLoader


def test_manifest_loading(appctx, ext, project, manifest):
    """Test manifest loading."""
    assert ext.manifest_loader == JinjaManifestLoader
    m = ext.manifest
    assert m.app
    assert m['app']


def test_manifest_rendering(appctx, ext, project, manifest):
    """Test manifest loading."""
    tpl = '{{ webpack.app }}'
    output = '<script src="/static/dist/app.js"></script>'
    assert render_template_string(tpl) == output


def test_manifest_loader_conf(app, ext, project, manifest):
    """Test manifest loading."""
    app.config.update({
        'WEBPACKEXT_MANIFEST_LOADER': 'pywebpack:ManifestLoader',
    })
    assert ext.manifest_loader == ManifestLoader


def test_manifest_nopath(app, ext):
    """Test no manifest path."""
    app.config['WEBPACKEXT_MANIFEST_PATH'] = None
    assert ext.manifest is None


def test_manifest_invalid_path(app, appctx, ext):
    """Test no manifest path."""
    app.config['WEBPACKEXT_MANIFEST_PATH'] = 'invalid/path.json'

    pytest.raises(
        FileNotFoundError if sys.version_info[0] == 3 else IOError,
        getattr, ext, 'manifest'
    )
