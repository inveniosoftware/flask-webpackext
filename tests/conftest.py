# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Pytest configuration."""

import shutil
import tempfile
from os import makedirs
from os.path import dirname, join

import pytest
from click.testing import CliRunner
from flask import Flask
from flask.cli import ScriptInfo

from flask_webpackext import (
    FlaskWebpackExt,
    WebpackBundle,
    WebpackBundleProject,
    WebpackProject,
    WebpackTemplateProject,
)


@pytest.fixture()
def tmpdir():
    """Temporary directory."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def instance_path(tmpdir):
    """Temporary instance path."""
    f = join(tmpdir, "instance")
    makedirs(f)
    return f


@pytest.fixture()
def static_folder(instance_path):
    """Static folder."""
    f = join(instance_path, "static")
    makedirs(f)
    return f


@pytest.fixture()
def manifest(static_folder):
    """Static folder."""
    src = join(dirname(__file__), "manifest.json")
    dst = join(static_folder, "dist/manifest.json")
    makedirs(dirname(dst))
    shutil.copyfile(src, dst)
    return dst


@pytest.fixture()
def app(instance_path, static_folder):
    """Flask application."""
    app_ = Flask("test", instance_path=instance_path, static_folder=static_folder)
    FlaskWebpackExt(app_)
    return app_


@pytest.fixture()
def appctx(app):
    """App in application context."""
    with app.app_context():
        yield app


@pytest.fixture()
def ext(app):
    """Extension instance."""
    return app.extensions["flask-webpackext"]


@pytest.fixture()
def project_assets_dir(tmpdir):
    """Temporary project assets dir."""
    src = join(dirname(__file__), "assets")
    dst = join(tmpdir, "project")
    shutil.copytree(src, dst)
    return dst


@pytest.fixture()
def project(app, project_assets_dir):
    """Webpack project."""
    project = WebpackProject(project_assets_dir)
    app.config.update(
        {
            "WEBPACKEXT_PROJECT": project,
        }
    )
    return project


@pytest.fixture()
def projecttpl(app):
    """Webpack project."""
    project = WebpackTemplateProject(__name__, "assets")
    app.config.update(
        {
            "WEBPACKEXT_PROJECT": project,
        }
    )
    return project


@pytest.fixture()
def bundles():
    """Webpack bundles."""
    return (
        WebpackBundle(__name__, "bundle1", entry={"app1": "./app1.js"}),
        WebpackBundle(__name__, "bundle2", entry={"app2": "./app2.js"}),
    )


@pytest.fixture()
def projectbundle(app, bundles):
    """Webpack bundle project."""
    project = WebpackBundleProject(__name__, "assetsbundle", bundles=bundles)
    app.config.update(
        {
            "WEBPACKEXT_PROJECT": project,
        }
    )
    return project


@pytest.fixture()
def cli_obj(app):
    """Script info."""
    return ScriptInfo(create_app=lambda: app)


@pytest.fixture()
def runner():
    """CLI Runner."""
    return CliRunner()
