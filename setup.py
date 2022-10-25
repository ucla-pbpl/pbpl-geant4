#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension, find_packages
import sys
import sysconfig
import subprocess
import shlex
import re as regex

with open('README.rst') as f:
    readme = f.read()

with open('HISTORY.rst') as f:
    history = f.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

geant4_cflags = subprocess.run(
    ['geant4-config', '--cflags'], capture_output=True).stdout.decode('utf-8')
pattern = regex.compile('-I(.+)')
geant4_include_dirs = [
    pattern.match(x)[1] for x in shlex.split(geant4_cflags)
    if pattern.match(x) is not None]
geant4_cflags = [
    x for x in shlex.split(geant4_cflags)
    if pattern.match(x) is None]

geant4_libflags = subprocess.run(
    ['geant4-config', '--libs'], capture_output=True).stdout.decode('utf-8')
pattern = regex.compile('-L(.+)')
geant4_lib_dirs = [
    pattern.match(x)[1] for x in shlex.split(geant4_libflags)
    if pattern.match(x) is not None]
pattern = regex.compile('-l(.+)')
geant4_libs = [
    pattern.match(x)[1] for x in shlex.split(geant4_libflags)
    if pattern.match(x) is not None]

setup(
    name='pbpl-geant4',
    version='0.1.0',
    description='Python package for running Geant4 simulations.',
    long_description=readme + '\n\n' + history,
    author='Brian Naranjo',
    author_email='brian.naranjo@gmail.com',
    url='https://github.com/bnara/pbpl-geant4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='UCLA PBPL Geant4 physics particle accelerator',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    ext_modules=[
        Extension(
            'pbpl.geant4.boost',
            ['src/boost.cpp',
             'src/ImportedMagneticField.cpp',
             'src/Particles.cpp',
             'src/PhysicsListEMstd.cpp',
             'src/PhysicsList.cpp',
             'src/pyCADMesh.cpp',
             'src/pyG4MultiSensitiveDetector.cpp',
             'src/pyG4MaterialPropertiesTable.cpp'],
            include_dirs=[
                *geant4_include_dirs,
                '/usr/include/hdf5/serial',
                '/opt/cadmesh/foo/install/include'],
            library_dirs=[
                *geant4_lib_dirs,
                '/opt/cadmesh/foo/install/lib'],
            libraries=[
                *geant4_libs,
                'boost_python3', 'boost_numpy3',
                'cadmesh', 'tet', 'assimp'],
            extra_compile_args=[
                *geant4_cflags])],
    entry_points = {
        'console_scripts' : [
            'pbpl-geant4-combine-deposition = pbpl.geant4.combine_deposition:main',
            'pbpl-geant4-convert-field = pbpl.geant4.convert_field:main',
            'pbpl-geant4-extrude-vrml = pbpl.geant4.extrude_vrml:main',
            'pbpl-geant4-mc = pbpl.geant4.mc:main',
            'pbpl-geant4-reduce-edep = pbpl.geant4.reduce_edep:main',
            'pbpl-geant4-sum-deposition = pbpl.geant4.sum_deposition:main'
        ] },
    # data_files=[
    #     ('share/lil-cpt',
    #      ['share/lil-cpt/lil-cpt.toml',
    #       'share/lil-cpt/lil_cpt.py',
    #       'share/lil-cpt/vis.mac']),
    #     ('share/lil-cpt/cad',
    #      ['share/lil-cpt/cad/lil-cpt.stl',
    #       'share/lil-cpt/cad/lil-cpt-magnet.stl']),
    #     ('share/lil-cpt/field',
    #      ['share/lil-cpt/field/B-field-2mm.h5',
    #       'share/lil-cpt/field/B-field-2mm.txt']),
    #     ('share/lil-cpt/cst',
    #      ['share/lil-cpt/cst/lil-cpt.mcs',
    #       'share/lil-cpt/cst/calc-enge.py'])],
    test_suite='tests',
    tests_require=test_requirements,
    namespace_packages=['pbpl']
)
