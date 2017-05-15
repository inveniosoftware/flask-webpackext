# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""CLI for Flask-WebpackExt."""

from __future__ import absolute_import, print_function

import click
from flask import current_app
from flask.cli import with_appcontext

from flask_webpackext import current_webpack


def _run(cmd, unavailable_msg, success_msg):
    project = current_webpack.project
    if not hasattr(project, cmd):
        click.secho(unavailable_msg, fg='yellow')
    else:
        getattr(current_webpack.project, cmd)()
        click.secho(success_msg, fg='green')


@click.group(chain=True)
@with_appcontext
def webpack():
    """Webpack commands."""


@webpack.command()
@with_appcontext
def create():
    """Create webpack project."""
    _run('create', 'Nothing to do for project.', 'Created webpack project.')


@webpack.command()
@with_appcontext
def clean():
    """Remove created webpack project."""
    _run('clean', 'Nothing to do for project.', 'Cleaned webpack project.')


@webpack.command(context_settings={'ignore_unknown_options': True})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def install(args):
    """Run NPM install."""
    current_webpack.project.install(*args)
    click.secho('Installed webpack project.', fg='green')


@webpack.command(context_settings={'ignore_unknown_options': True})
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def build(args):
    """Run NPM build-script."""
    current_webpack.project.build(*args)
    click.secho('Built webpack project.', fg='green')


@webpack.command()
@with_appcontext
def buildall():
    """Create, install and build webpack project."""
    current_webpack.project.buildall()
    click.secho('Created, installed and built webpack project.', fg='green')


@webpack.command(context_settings={'ignore_unknown_options': True})
@click.argument('script')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def run(script, args):
    """Run an NPM script."""
    try:
        current_webpack.project.run(script, *args)
        click.secho('Executed NPM script "{}".'.format(script), fg='green')
    except RuntimeError:
        raise click.BadParameter(
            '"{}" is not a valid NPM script.'.format(script))
