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

"""Proxy to current extension."""

from __future__ import absolute_import, print_function

from flask import current_app
from markupsafe import Markup
from pywebpack import Manifest, ManifestEntry, ManifestLoader


class JinjaManifestEntry(ManifestEntry):
    """Manifest entry which marks rendered strings as safe for Jinja."""

    def __html__(self):
        """Ensures that string is not escaped when included in Jinja."""
        return Markup(self.render())


class JinjaManifestLoader(ManifestLoader):
    """Factory which uses the Jinja manifest entry."""

    cache = {}

    def __init__(self, manifest_cls=Manifest, entry_cls=JinjaManifestEntry):
        """Initialize manifest loader."""
        super(JinjaManifestLoader, self).__init__(
            manifest_cls=manifest_cls,
            entry_cls=entry_cls
        )

    def load(self, filepath):
        """Load a manifest from a file."""
        if current_app.debug or filepath not in JinjaManifestLoader.cache:
            JinjaManifestLoader.cache[filepath] = \
                super(JinjaManifestLoader, self).load(filepath)
        return JinjaManifestLoader.cache[filepath]
