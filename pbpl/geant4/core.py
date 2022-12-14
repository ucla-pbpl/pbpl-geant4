# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial.transform import Rotation
from Geant4.hepunit import *

def build_transformation(spec, length_unit=1.0, angle_unit=1.0):
    result = np.identity(4)
    for operation, value in zip(*spec):
        translation = np.zeros(3)
        rotation = np.identity(3)
        if operation == 'TranslateX':
            translation = np.array((value*length_unit, 0, 0))
        elif operation == 'TranslateY':
            translation = np.array((0, value*length_unit, 0))
        elif operation == 'TranslateZ':
            translation = np.array((0, 0, value*length_unit))
        elif operation == 'RotateX':
            rotation = Rotation.from_euler('x', value*angle_unit).as_matrix()
        elif operation == 'RotateY':
            rotation = Rotation.from_euler('y', value*angle_unit).as_matrix()
        elif operation == 'RotateZ':
            rotation = Rotation.from_euler('z', value*angle_unit).as_matrix()
        elif operation == 'MirrorX':
            rotation = np.diag((-1,1,1)).astype(float)
        elif operation == 'MirrorY':
            rotation = np.diag((1,-1,1)).astype(float)
        elif operation == 'MirrorZ':
            rotation = np.diag((1,1,-1)).astype(float)
        else:
            assert(False)
        M = np.identity(4)
        M[:3,:3] = rotation
        M[:3,3] = translation
        result = M @ result
    return result

def transform(M, x):
    return (M[:3,:3] @ x.T).T + M[:3,3]

def in_volume(vol, x):
    return np.logical_and.reduce(
        (x[:,0]>=vol[0,0], x[:,0]<=vol[0,1],
         x[:,1]>=vol[1,0], x[:,1]<=vol[1,1],
         x[:,2]>=vol[2,0], x[:,2]<=vol[2,1]))

def gamma_to_edge(gamma):
    return 2*gamma**2/(2*gamma + electron_mass_c2)

def edge_to_gamma(edge):
    return 0.5*(edge + np.sqrt(edge**2 + 2*edge*electron_mass_c2))
