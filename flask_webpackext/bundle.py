# SPDX-FileCopyrightText: 2018 CERN.
# SPDX-FileCopyrightText: 2024 Graz University of Technology.
# SPDX-License-Identifier: BSD-3-Clause

"""Webpack bundle APIs for Flask-WebpackExt."""

from os.path import join

from flask.helpers import get_root_path
from pywebpack import WebpackBundle as PyWebpackBundle


class WebpackBundle(PyWebpackBundle):
    """Flask webpack bundle."""

    def __init__(self, import_name, folder, **kwargs):
        """Initialize bundle.

        :param import_name: Name of the module where the WebpackBundle class
            is instantiated. It is used to determine the absolute path to the
            ``folder`` where the assets are located.
        :param folder: Relative path to the assets.
        :param kwargs: Keyword arguments directly passed to
            :class:`pywebpack.bundle.WebpackBundle`.
        """
        super().__init__(join(get_root_path(import_name), folder), **kwargs)
