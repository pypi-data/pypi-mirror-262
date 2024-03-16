.. role:: underline
    :class: underline
.. role:: additions
    :class: additions
.. role:: deletions
    :class: deletions

======================
webchanges |downloads|
======================

**webchanges** checks web content and notifies you via email (or one of many other `supported services
<https://webchanges.readthedocs.io/en/stable/introduction.html#reporters-list>`__) if a change is detected.
**webchanges** can also check the output of local commands. The notification includes the changed URL or
command and a summary (diff) of what has changed.

**webchanges** *anonymously* alerts you of web changes.



Requirements
============
**webchanges** requires |support|.

You should use the latest version of `Python <https://www.python.org/downloads/>`__ if possible, but older
Python versions are supported for 3 years after being obsoleted by a new major release (3.x). For each major release,
only the latest bug and security fix version (3.x.y) is supported.


Installation
============
Install **webchanges** |pypi_version| |format| |status| |security| with:

.. code-block:: bash

   pip install webchanges


Running in Docker
=================
**webchanges** can be run in a `Docker <https://www.docker.com/>`__ container. Please see
`<https://github.com/yubiuser/webchanges-docker>`__ for one such implementation.


Documentation |readthedocs|
===========================
The documentation is hosted on `Read the Docs <https://webchanges.readthedocs.io/>`__.


Quick Start
============
Initialize
----------

#. Run the following command to create the default ``config.yaml`` (configuration) and ``jobs.yaml`` (jobs) files and
   open an editor to add your `jobs <https://webchanges.readthedocs.io/en/stable/jobs.html>`__:

   .. code-block:: bash

      webchanges --edit


#. Run the following command to change the default `configuration
   <https://webchanges.readthedocs.io/en/stable/configuration.html>`__, e.g. to receive change notifications
   ("`reports <https://webchanges.readthedocs.io/en/stable/reporters.html>`__")
   by `email <https://webchanges.readthedocs.io/en/stable/reporters.html#smtp>`__ and/or one of many other methods:

   .. code-block:: bash

      webchanges --edit-config


Run
---
To check the sources in your jobs and report on (e.g. display or via email) any changes found from the previous
execution, just run:

.. code-block:: bash

   webchanges

**webchanges** does not include a scheduler. We recommend using a system scheduler to automatically run **webchanges**
periodically:

- On Linux or macOS, you can use cron (if you have never used cron before, see
  `here <https://www.computerhope.com/unix/ucrontab.htm>`__); `crontab.guru <https://crontab.guru>`__ will build a
  schedule expression for you.
- On Windows, you can use the built-in `Windows Task Scheduler
  <https://en.wikipedia.org/wiki/Windows_Task_Scheduler>`__.


Code
====
|coveralls| |issues|

The code and issues tracker are hosted on `GitHub <https://github.com/mborsetti/webchanges>`__.


Contributing
============
We welcome any contribution no matter how small as both pull requests and `issue reports
<https://github.com/mborsetti/webchanges/issues>`__.

More information for developers and documentation contributors is `here
<https://webchanges.readthedocs.io/en/stable/contributing.html>`__, and our wishlist is `here
<https://github.com/mborsetti/webchanges/blob/main/WISHLIST.md>`__.


License
=======
|license|

Released under the `MIT License <https://opensource.org/licenses/MIT>`__ but redistributing modified source code from
`urlwatch 2.21 <https://github.com/thp/urlwatch/tree/346b25914b0418342ffe2fb0529bed702fddc01f>`__ dated 30 July 2020
licensed under a `BSD 3-Clause License
<https://raw.githubusercontent.com/thp/urlwatch/346b25914b0418342ffe2fb0529bed702fddc01f/COPYING>`__. See the complete
license `here <https://github.com/mborsetti/webchanges/blob/main/LICENSE>`__.


Compatibility with **urlwatch**
================================

This project is based on code from `urlwatch 2.21
<https://github.com/thp/urlwatch/tree/346b25914b0418342ffe2fb0529bed702fddc01f>`__ dated 30 July 2020. You can
easily upgrade from the current version of **urlwatch** (see `here
<https://webchanges.readthedocs.io/en/stable/migration.html>`__) using the same job and configuration files and
benefit from many HTML-focused improvements, including:

* Report links that are `clickable <https://pypi.org/project/webchanges/>`__!
* Original formatting such as **bolding / headers**, *italics*, :underline:`underlining`, list bullets (•) and
  indentation;
* :additions:`Added` and :deletions:`deleted` lines clearly highlighted by color and strikethrough, and long lines that
  wrap around;
* Correct rendering by email clients who override stylesheets (e.g. Gmail);
* Other legibility improvements;
* New filters such as `additions_only <https://webchanges.readthedocs.io/en/stable/diff_filters.html#additions-only>`__,
  which makes it easier to track content that was added without the distractions of the content that was deleted;
* New features such as ``--errors`` to catch jobs that no longer work;
* Much better `documentation <https://webchanges.readthedocs.io/>`__;
* More reliability and stability, including a ~30 percentage point increase in testing coverage;
* Many other additions, refinements and fixes (see `detailed information
  <https://webchanges.readthedocs.io/en/stable/migration.html#upgrade-details>`__).

Examples:

.. image:: https://raw.githubusercontent.com/mborsetti/webchanges/main/docs/html_diff_filters_example_1.png
    :width: 504

|

.. image:: https://raw.githubusercontent.com/mborsetti/webchanges/main/docs/html_diff_filters_example_3.png
    :width: 504




.. |support| image:: https://img.shields.io/pypi/pyversions/webchanges.svg
    :target: https://www.python.org/downloads/
    :alt: Supported Python versions
.. |pypi_version| image:: https://img.shields.io/pypi/v/webchanges.svg?label=
    :target: https://pypi.org/project/webchanges/
    :alt: PyPI version
.. |format| image:: https://img.shields.io/pypi/format/webchanges.svg
    :target: https://pypi.org/project/webchanges/
    :alt: Kit format
.. |downloads| image:: https://static.pepy.tech/badge/webchanges
    :target: https://www.pepy.tech/project/webchanges
    :alt: PyPI downloads
.. |license| image:: https://img.shields.io/pypi/l/webchanges.svg
    :target: https://pypi.org/project/webchanges/
    :alt: License at https://pypi.org/project/webchanges/
.. |issues| image:: https://img.shields.io/github/issues-raw/mborsetti/webchanges
    :target: https://github.com/mborsetti/webchanges/issues
    :alt: Issues at https://github.com/mborsetti/webchanges/issues
.. |readthedocs| image:: https://img.shields.io/readthedocs/webchanges/stable.svg?label=
    :target: https://webchanges.readthedocs.io/
    :alt: Documentation status
.. |CI| image:: https://github.com/mborsetti/webchanges/actions/workflows/ci-cd.yaml/badge.svg?event=push
    :target: https://github.com/mborsetti/webchanges/actions
    :alt: CI testing status
.. |coveralls| image:: https://coveralls.io/repos/github/mborsetti/webchanges/badge.svg?branch=main
    :target: https://coveralls.io/github/mborsetti/webchanges?branch=main
    :alt: Code coverage by Coveralls
.. |status| image:: https://img.shields.io/pypi/status/webchanges.svg
    :target: https://pypi.org/project/webchanges/
    :alt: Package stability
.. |security| image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
