# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages
import versioneer

setup(
    name="q2-sourmash",
    #version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="C. Titus Brown",
    author_email="contact@luizirber.org",
    description="Compute and compare minhash signatures for DNA datasets using sourmash",
    license='BSD-3-Clause',
    url="https://qiime2.org",
    entry_points={
        'qiime2.plugins':
        ['q2-sourmash=q2_sourmash.plugin_setup:plugin']
    },
    package_data={'q2_sourmash': ['citations.bib']},
    zip_safe=False,
)
