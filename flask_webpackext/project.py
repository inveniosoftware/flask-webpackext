# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack project utilities for Flask-WebpackExt."""

from __future__ import absolute_import, print_function

from os.path import join

from flask import current_app
from flask.helpers import get_root_path
from pywebpack import WebpackBundleProject, WebpackTemplateProject

from .proxies import current_webpack


def flask_config():
    """Flask configuration injected in Webpack."""
    assets_url = current_app.config['WEBPACKEXT_PROJECT_DISTURL']
    if assets_url[-1] != '/':
        assets_url += '/'
    static_url = current_app.static_url_path
    if static_url[-1] != '/':
        static_url += '/'

    return {
        'build': {
            'debug': current_app.debug,
            'context': current_webpack.project.path,
            'assetsPath': current_app.config['WEBPACKEXT_PROJECT_DISTDIR'],
            'assetsURL': assets_url,
            'staticPath': current_app.static_folder,
            'staticURL': static_url,
        }
    }


class WebpackProject(WebpackTemplateProject):
    """Flask webpack project."""

    def __init__(self, import_name, project_folder=None, config=None,
                 config_path=None,):
        """Initialize project."""
        super(WebpackProject, self).__init__(
            None,
            project_template=join(get_root_path(import_name), project_folder),
            config=config or flask_config,
            config_path=config_path,
        )

    @property
    def path(self):
        """Get path to project."""
        return current_app.config['WEBPACKEXT_PROJECT_BUILDDIR']

    @property
    def storage_cls(self):
        """Get storage class."""
        return current_webpack.storage_cls
