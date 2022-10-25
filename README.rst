pbpl-geant4
============

.. image:: https://img.shields.io/pypi/v/pbpl-geant4.svg
        :target: https://pypi.python.org/pypi/pbpl-geant4

.. image:: https://img.shields.io/travis/bnara/pbpl-geant4.svg
        :target: https://travis-ci.org/bnara/pbpl-geant4

.. image:: https://readthedocs.org/projects/pbpl-geant4/badge/?version=latest
        :target: https://pbpl-geant4.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ucla-pbpl/pbpl-geant4/shield.svg
     :target: https://pyup.io/repos/github/ucla-pbpl/pbpl-geant4/
     :alt: Updates

Python package for running Geant4 simulations.

* Free software: MIT license
* Documentation: http://rodan.physics.ucla.edu/pbpl-geant4

Features
--------

* TODO
* Installation
  - Add following to pyG4TrackingManager.cc:
  .def("GetTrack", &G4TrackingManager::GetTrack,
    return_value_policy<reference_existing_object>())
* Testing
