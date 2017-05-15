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

import pytest
from click.testing import CliRunner
from flask import Flask

from flask_webpackext import FlaskWebpackExt
from flask_webpackext.cli import webpack


def test_webpack(project):
    """Test webpack command."""
    runner = CliRunner()
    result = runner.invoke(webpack)
    assert result.exit_code == 0


@pytest.mark.parametrize('cmd', ['create', 'clean'])
def test_simple_create_clean(cmd, runner, project, cli_obj):
    """Test create/clean command on simple project."""
    result = runner.invoke(webpack, [cmd], obj=cli_obj)
    assert result.exit_code == 0
    assert 'Nothing to do' in result.output


def test_simple_chain(runner, project, cli_obj):
    """Test chaining commands."""
    result = runner.invoke(webpack, ['create', 'clean', ], obj=cli_obj)
    assert result.exit_code == 0
    assert 'Nothing to do' in result.output


def test_simple_install(project, project_assets_dir, runner, cli_obj):
    """Test install command on simple project."""
    node_dir = join(project_assets_dir, 'node_modules')
    assert not exists(node_dir)
    result = runner.invoke(webpack, ['install'], obj=cli_obj)
    assert result.exit_code == 0
    assert 'Installed webpack project.' in result.output
    assert exists(node_dir)

    # Test args passing
    result = runner.invoke(webpack, ['install', '--report'], obj=cli_obj)
    assert result.exit_code == 0


def test_simple_build(project, project_assets_dir, runner, cli_obj):
    """Test build comand on simple project."""
    bundle_js = join(project_assets_dir, 'build/bundle.js')
    assert not exists(bundle_js)
    result = runner.invoke(webpack, ['build'], obj=cli_obj)
    assert result.exit_code == 0
    assert 'Built webpack project.' in result.output
    assert exists(bundle_js)


def test_simple_run(project, project_assets_dir, runner, cli_obj):
    """Test run command."""
    bundle_js = join(project_assets_dir, 'build/bundle.js')
    assert not exists(bundle_js)
    result = runner.invoke(webpack, ['run', 'build'], obj=cli_obj)
    assert result.exit_code == 0
    assert 'Executed NPM script "build"' in result.output
    assert exists(bundle_js)


def test_simple_run_error(project, project_assets_dir, runner, cli_obj):
    """Test run command with invalid script."""
    result = runner.invoke(webpack, ['run', 'invalid'], obj=cli_obj)
    assert result.exit_code != 0


def test_simple_buildall(project, project_assets_dir, runner, cli_obj):
    """Test buildall command on simple project."""
    bundle_js = join(project_assets_dir, 'build/bundle.js')
    node_dir = join(project_assets_dir, 'node_modules')
    assert not exists(bundle_js)
    assert not exists(node_dir)
    result = runner.invoke(webpack, ['buildall'], obj=cli_obj)
    assert result.exit_code == 0
    assert exists(bundle_js)
    assert exists(node_dir)


def test_tpl_create(projecttpl, runner, cli_obj, app):
    """Test create command with template project."""
    pkgfile = join(app.instance_path, 'assets/package.json')
    assert not exists(pkgfile)
    result = runner.invoke(webpack, ['create'], obj=cli_obj)
    assert result.exit_code == 0
    assert 'Created webpack project.' in result.output
    assert exists(pkgfile)


def test_tpl_build(projecttpl, runner, cli_obj, app):
    """Test build command with template project."""
    bundle_js = join(app.instance_path, 'assets/build/bundle.js')
    assert not exists(bundle_js)
    result = runner.invoke(webpack, ['create', 'build'], obj=cli_obj)
    assert result.exit_code == 0
    assert exists(bundle_js)
