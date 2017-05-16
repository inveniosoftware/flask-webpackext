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

from os.path import exists, join


def test_project_path(app, projecttpl, appctx):
    """Test project path."""
    assert projecttpl.path == app.config['WEBPACKEXT_PROJECT_BUILDDIR']


def test_project_storage_cls(ext, projecttpl, appctx):
    """Test project path."""
    assert projecttpl.storage_cls == ext.storage_cls


def test_bundle_project(projectbundle, appctx, static_folder):
    """Test bundle project."""
    out = join(static_folder, 'dist')
    p = projectbundle

    # Test create()
    assert not exists(p.path)
    p.create()
    assert exists(p.path)
    for f in ['app1.js', 'app2.js', 'webpack.config.js', 'config.json']:
        assert exists(join(p.path, f))

    # Test build()
    files = ['app1.js', 'app2.js']
    assert all([not exists(join(out, f)) for f in files])
    p.build()
    assert all([exists(join(out, f)) for f in files])
