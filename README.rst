==================
 Flask-WebpackExt
==================

.. image:: https://img.shields.io/travis/inveniosoftware/flask-webpackext.svg
        :target: https://travis-ci.org/inveniosoftware/flask-webpackext

.. image:: https://img.shields.io/coveralls/inveniosoftware/flask-webpackext.svg
        :target: https://coveralls.io/r/inveniosoftware/flask-webpackext

.. image:: https://img.shields.io/github/tag/inveniosoftware/flask-webpackext.svg
        :target: https://github.com/inveniosoftware/flask-webpackext/releases

.. image:: https://img.shields.io/pypi/dm/flask-webpackext.svg
        :target: https://pypi.python.org/pypi/flask-webpackext

.. image:: https://img.shields.io/github/license/inveniosoftware/flask-webpackext.svg
        :target: https://github.com/inveniosoftware/flask-webpackext/blob/master/LICENSE

Webpack integration for Flask.

Flask-WebpackExt makes it easy to interface with your existing Webpack project
from Flask and does not try to manage Webpack for you. Flask-WebpackExt does
this via:

* **Manifests**: You tell Webpack to write a ``manifest.json`` using plugins
  such as `webpack-manifest-plugin
  <https://www.npmjs.com/package/webpack-manifest-plugin>`_,
  `webpack-yam-plugin
  <https://www.npmjs.com/package/webpack-yam-plugin>`_ or
  `webpack-bundle-tracker
  <https://www.npmjs.com/package/webpack-bundle-tracker>`_. Flask-WebpackExt
  reads the manifest and makes your compiled assets available in your Jinja
  templates.
* **CLI for NPM**: Flask-WebpackExt provides a Flask CLI so that e.g.
  ``flask webpack install`` will run ``npm install`` in your Webpack project.
  Similarly, ``flask webpack build`` will run ``npm run build``.

Optionally you can use Flask-WebpackExt to also:

* **Inject configuration:** Flask-WebpackExt will write a ``config.json`` into
  your Webpack project, which you can import in your Webpack configuration. You
  define what goes in the config e.g. Let Webpack know about output paths or
  dynamic entry points.
* **Collect bundles:** If your Webpack project is spread over multiple Python
  packages, Flask-WebpackExt can help you dynamically assemble the files into a
  Webpack project. This is useful if you don't know until runtime which
  packages are installed.

Further documentation is available on
https://flask-webpackext.readthedocs.io/
