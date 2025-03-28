# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017, 2018 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Webpack project utilities for Flask-WebpackExt."""

from os.path import join

from flask import current_app
from flask.helpers import get_root_path
from pywebpack import WebpackBundleProject as PyWebpackBundleProject
from pywebpack import WebpackTemplateProject as PyWebpackTemplateProject
from pywebpack.helpers import cached

from .proxies import current_webpack


def flask_config():
    """Flask configuration injected in Webpack.

    :return: Dictionary which contains the information Flask-WebpackExt knows
        about a Webpack project and the absolute URLs for static files and
        assets. The dictionary consists of a key ``build`` with the following
        keys inside:

        * ``debug``: Boolean which represents if Flask debug is on.
        * ``context``: Absolute path to the generated assets directory.
        * ``assetsPath``: Absolute path to the generated static directory.
        * ``assetsURL``: URL to access the built files.
        * ``staticPath``: Absolute path to the generated static directory.
        * ``staticURL``: URL to access the static files..
    """
    assets_url = current_app.config["WEBPACKEXT_PROJECT_DISTURL"]
    if not assets_url.endswith("/"):
        assets_url += "/"
    static_url = current_app.static_url_path
    if not static_url.endswith("/"):
        static_url += "/"

    return {
        "build": {
            "debug": current_app.debug,
            "context": current_webpack.project.path,
            "assetsPath": current_app.config["WEBPACKEXT_PROJECT_DISTDIR"],
            "assetsURL": assets_url,
            "staticPath": current_app.static_folder,
            "staticURL": static_url,
        }
    }


def flask_allowed_copy_paths():
    """Get the allowed copy paths from the Flask application."""
    return [
        current_app.instance_path,
        current_webpack.project.path,
        current_app.static_folder,
        current_app.config["WEBPACKEXT_PROJECT_DISTDIR"],
    ]


class _PathStoragePackageMixin:
    """Mixin class for overriding various properties of the base ``WebpackProject``."""

    @property
    def path(self):
        """Get path to project."""
        return current_app.config["WEBPACKEXT_PROJECT_BUILDDIR"]

    @property
    def storage_cls(self):
        """Get storage class."""
        return current_webpack.storage_cls

    @property
    @cached
    def npmpkg(self):
        """Get API to the package for the configured package manager."""
        npm_pkg_cls = current_webpack.npm_pkg_cls
        return npm_pkg_cls(self.path)


class WebpackTemplateProject(_PathStoragePackageMixin, PyWebpackTemplateProject):
    """Flask webpack template project."""

    def __init__(
        self, import_name, project_folder=None, config=None, config_path=None, **kwargs
    ):
        """Initialize project.

        :param import_name: Name of the module where the
            WebpackTemplateProject class is instantiated. It is used to
            determine the absolute path to the ``project_folder``.
        :param project_folder: Relative path to the Webpack project.
        :param config: Dictionary which overrides the ``config.json`` file
            generated by Flask-WebpackExt. Use carefuly and only if you know
            what you are doing since ``config.json`` is the file that holds the
            key information to integrate Flask with Webpack.
        :param config_path: Path where Flask-WebpackExt is going to write the
            ``config.json``, this file is generated by
            :func:`flask_webpackext.project.flask_config`.
        :param kwargs: Keyword arguments to be passed to the super constructor.
        """
        project_template_dir = join(get_root_path(import_name), project_folder)
        super().__init__(
            None,
            project_template_dir=project_template_dir,
            config=config or flask_config,
            config_path=config_path,
            **kwargs,
        )


class WebpackBundleProject(_PathStoragePackageMixin, PyWebpackBundleProject):
    """Flask webpack bundle project."""

    def __init__(
        self,
        import_name,
        project_folder=None,
        bundles=None,
        config=None,
        config_path=None,
        allowed_copy_paths=None,
        **kwargs,
    ):
        """Initialize templated folder.

        :param import_name: Name of the module where the WebpackBundleProject
            class is instantiated. It is used to determine the absolute path
            to the ``project_folder``.
        :param project_folder: Relative path to the Webpack project which is
            going to aggregate all the ``bundles``.
        :param bundles: List of
            :class:`flask_webpackext.bundle.WebpackBundle`. This list can be
            statically defined if the bundles are known before hand, or
            dinamically generated using
            :func:`pywebpack.helpers.bundles_from_entry_point` so the bundles
            are discovered from the defined Webpack entrypoints exposed by
            other modules.
        :param config: Dictionary which overrides the ``config.json`` file
            generated by Flask-WebpackExt. Use carefuly and only if you know
            what you are doing since ``config.json`` is the file that holds the
            key information to integrate Flask with Webpack.
        :param config_path: Path where Flask-WebpackExt is going to write the
            ``config.json``, this file is generated by
            :func:`flask_webpackext.project.flask_config`.
        :param allowed_copy_paths: List of paths (absolute, or relative to
            the `config_path`) that are allowed for bundle copy instructions.
        :param kwargs: Keyword arguments to be passed to the super constructor.
        """
        project_template_dir = join(get_root_path(import_name), project_folder)
        super().__init__(
            None,
            project_template_dir=project_template_dir,
            bundles=bundles,
            config=config or flask_config,
            config_path=config_path,
            allowed_copy_paths=allowed_copy_paths or flask_allowed_copy_paths,
            **kwargs,
        )
