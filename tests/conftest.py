# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import shutil
import tempfile
from os.path import dirname, join

import pytest
from click.testing import CliRunner
from flask import Flask
from flask.cli import ScriptInfo

from flask_webpackext import FlaskWebpackExt, WebpackProject, \
    WebpackTemplateProject


@pytest.yield_fixture(scope='function')
def tmpdir():
    """Temporary directory."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture(scope='function')
def instance_path(tmpdir):
    """Temporary instance path."""
    return join(tmpdir, 'instance')


@pytest.fixture(scope='function')
def static_folder(instance_path):
    """Static folder."""
    return join(instance_path, 'static')


@pytest.fixture(scope='function')
def app(instance_path, static_folder):
    """Flask application."""
    app_ = Flask(
        'test',
        instance_path=instance_path,
        static_folder=static_folder
    )
    FlaskWebpackExt(app_)
    return app_


@pytest.fixture(scope='function')
def project_assets_dir(tmpdir):
    """Temporary project assets dir."""
    src = join(dirname(__file__), 'assets')
    dst = join(tmpdir, 'project')
    shutil.copytree(src, dst)
    return dst


@pytest.fixture(scope='function')
def project(app, project_assets_dir):
    """Webpack project."""
    project = WebpackProject(project_assets_dir)
    app.config.update({
        'WEBPACKEXT_PROJECT': project,
    })
    return project


@pytest.fixture(scope='function')
def projecttpl(app):
    """Webpack project."""
    project = WebpackTemplateProject(__name__, 'assets')
    app.config.update({
        'WEBPACKEXT_PROJECT': project,
    })
    return project


@pytest.fixture(scope='function')
def cli_obj(app):
    """Script info."""
    return ScriptInfo(create_app=lambda info: app)


@pytest.fixture(scope='function')
def runner():
    """CLI Runner."""
    return CliRunner()
