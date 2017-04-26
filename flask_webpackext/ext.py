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

"""Webpack integration for Flask."""

from __future__ import absolute_import, print_function

from os.path import join

from pywebpack import FileStorage, ManifestLoader
from werkzeug.utils import import_string

from . import config
from ._compat import string_types
from .manifest import JinjaManifestLoader
from .proxies import current_manifest


class FlaskWebpackExt(object):
    """Flask-WebpackExt extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.add_template_global(current_manifest, name='webpack')
        app.extensions['flask-webpackext'] = _FlaskWebpackExtState(app)

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            'WEBPACKEXT_PROJECT_DISTDIR',
            join(app.static_folder, 'dist'),
        )
        app.config.setdefault(
            'WEBPACKEXT_PROJECT_DISTURL',
            join(app.static_url_path, 'dist'),
        )
        app.config.setdefault(
            'WEBPACKEXT_PROJECT_BUILDDIR',
            join(app.instance_path, 'assets'),
        )
        app.config.setdefault(
            'WEBPACKEXT_STORAGE_CLS',
            FileStorage
        )
        app.config.setdefault(
            'WEBPACKEXT_MANIFEST_LOADER',
            JinjaManifestLoader,
        )

        for k in dir(config):
            if k.startswith('WEBPACKEXT_'):
                app.config.setdefault(k, getattr(config, k))


class _FlaskWebpackExtState(object):
    """Flask webpack state object."""

    def __init__(self, app):
        """Initialize state."""
        self.app = app

    @property
    def manifest_loader(self):
        """Manifest loader."""
        loader = self.app.config['WEBPACKEXT_MANIFEST_LOADER']
        if isinstance(loader, string_types):
            return import_string(loader)
        return loader

    @property
    def manifest(self):
        """Manifest."""
        path = self.app.config['WEBPACKEXT_MANIFEST_PATH']
        if path:
            return self.manifest_loader().load(
                join(self.app.static_folder, path))
        return path

    @property
    def project(self):
        """Webpack project."""
        project = self.app.config['WEBPACKEXT_PROJECT']
        if isinstance(project, string_types):
            return import_string(project)
        return project

    @property
    def storage_cls(self):
        """Default storage class."""
        cls_ = self.app.config['WEBPACKEXT_STORAGE_CLS']
        if isinstance(cls_, string_types):
            return import_string(cls_)
        return cls_
