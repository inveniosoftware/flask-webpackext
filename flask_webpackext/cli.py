# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""CLI for Flask-WebpackExt."""

from __future__ import absolute_import, print_function

import click
from flask import current_app
from flask.cli import with_appcontext

from flask_webpackext import current_webpack


@click.group(chain=True)
@with_appcontext
def webpack():
    """Webpack commands."""


@webpack.command()
@with_appcontext
def create():
    """Create webpack project."""
    current_webpack.project.create()
    click.secho('Created webpack project.', fg='green')


@webpack.command()
@with_appcontext
def clean():
    """Remove created webpack project."""
    current_webpack.project.clean()


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
        click.secho(
            'Error: Invalid script name "{}".'.format(script), fg='red')
