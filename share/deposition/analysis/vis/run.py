#!/usr/bin/env python
import os
import toml
import sys

os.system('rm -f *wrl *h5')
print('### RUNNING GEANT4 (design.wrl) ###')
os.system('pbpl-geant4-mc deposition.toml vis.mac > /dev/null 2>&1')
#os.system('pbpl-compton-mc deposition.toml')# > /dev/null 2>&1')
os.system('pbpl-geant4-extrude-vrml g4_00.wrl --radius=0.000001 --num-points=8 --output=design.wrl')
#os.system('rm -f g4*wrl')
