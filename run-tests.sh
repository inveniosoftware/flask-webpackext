# -*- coding: utf-8 -*-
#
# This file is part of Flask-WebpackExt
# Copyright (C) 2017 CERN.
#
# Flask-WebpackExt is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

pydocstyle flask_webpackext tests docs && \
isort -rc -c -df && \
check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
