#!/usr/bin/env python
import Geant4 as g4
from Geant4.hepunit import *
import numpy as np

nm = 1e-6*mm

def spray():
    energy = 1*MeV
    while 1:
        x, y = np.random.uniform(-250*nm, 250*nm, 2).T
        yield 'e-', g4.G4ThreeVector(x,y,-500*nm), g4.G4ThreeVector(0,0,1), energy
