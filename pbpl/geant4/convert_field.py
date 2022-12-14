#!/usr/bin/env python
import sys, os
import argparse
from argparse import RawDescriptionHelpFormatter
import numpy as np
import h5py
import re as regex
from pbpl.common.units import *

class CstAsciiConverter:
    name = 'cst-ascii'

    def check_format(filename):
        with open(filename, 'r') as f:
            try:
                line = f.readline()
            except:
                return False
            m = regex.search('x\s+\[(\S+)\]', line)
        if m:
            return True
        else:
            return False

    def convert(args):
        with open(args.input, 'r') as f:
            line = f.readline()
            m = regex.search('x\s+\[(\S+)\]', line)
            if m:
                length_unit = m.group(1)
                if length_unit == 'mm':
                    length_scale = 1e-3
                else:
                    raise ValueError(
                        "unfamiliar CST unit '{}'".format(length_unit))
            else:
                raise ValueError('unfamiliar CST header')
            m = regex.search('([BE])xRe\s+\[(\S+)\]', line)
            if m:
                field_type = m.group(1)
                field_unit = m.group(2)
                if field_unit in ['Vs/m^2', 'V.s/m^2']:
                    field_scale = 1.0
                else:
                    raise ValueError(
                        "unfamiliar CST unit '{}'".format(field_unit))
            else:
                raise ValueError('unfamiliar CST header')

        if args.double:
            dtype = np.float64
        else:
            dtype = np.float32

        # CST writes out grid in `X-major order' (i.e., Fortran order):
        #   X is fastest index, and Z is slowest index
        raw = np.loadtxt(args.input, skiprows=2, unpack=True, dtype=dtype)
        xvals, yvals, zvals = [
            np.sort(np.unique(x))*length_scale for x in raw[0:3]]
        def f2c(A):
            return A.reshape(3, len(xvals), len(yvals), len(zvals), order='F')
        pos = f2c(raw[0:3])
        if args.complex:
            # field = f2c(raw[3:6]) + 1j*f2c(raw[6:9])
            field = f2c(raw[[3,5,7]]) + 1j*f2c(raw[[6,8,10]])
            assert(False)
        else:
            # field = f2c(raw[3:6])
            field = f2c(raw[[3,5,7]])

        field *= field_scale

        if field_type == 'B':
            return xvals, yvals, zvals, field, None
        elif field_type == 'E':
            return xvals, yvals, zvals, None, field

def read_with_unit(fin, dataset_name):
    dset = fin[dataset_name]
    unit = dset.attrs['unit'].decode('utf-8')
    if unit == 'mm':
        unit_scale = mm
    else:
        raise ValueError(
            "unfamiliar CST unit '{}'".format(unit))
    return dset[:]*unit_scale

class CstHdfConverter:
    name = 'cst-hdf'

    def check_format(filename):
        try:
            with h5py.File(filename, 'r') as fin:
                cst_keys = (
                    'B-Field', 'Mesh line x', 'Mesh line y', 'Mesh line z')
                if set(cst_keys) == set(fin.keys()):
                    return True
        except:
            pass
        return False

    def convert(args):
        with h5py.File(args.input, 'r') as fin:
            xvals = read_with_unit(fin, 'Mesh line x')
            yvals = read_with_unit(fin, 'Mesh line y')
            zvals = read_with_unit(fin, 'Mesh line z')
            dset = fin['B-Field']
            val = dset[:]
            unit = dset.attrs['unit'].decode('utf-8')
            if unit in ['Vs/m^2', 'V.s/m^2']:
                unit_scale = tesla
            else:
                raise ValueError(
                    "unfamiliar CST unit '{}'".format(unit))
            field = unit_scale * np.array(
                (val['x']['re'], val['y']['re'], val['z']['re']),
                dtype=np.float32).transpose((0, 3, 2, 1))
        if args.double:
            dtype = np.float64
        else:
            dtype = np.float32

        return (
            xvals.astype(dtype),
            yvals.astype(dtype),
            zvals.astype(dtype),
            field.astype(dtype),
            None)

converters = [CstAsciiConverter, CstHdfConverter]
converters_dict = {x.name:x for x in converters}

def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description='Convert raw field data to pbpl-geant4 HDF5 format',
        epilog='Example:\n' +
        '  > pbpl-geant4-convert-field result.txt\n\n' +
        "Reads 'result.txt' and writes 'result.h5'")
    parser.add_argument(
        '--output', metavar='HDF5',# default=None,
        help='Specify output filename')
    parser.add_argument(
        '--complex', action='store_true',
        help='Store complex field (Store only real part by default)')
    parser.add_argument(
        '--double', action='store_true',
        help='Store double precision (Store single precision by default)')
    parser.add_argument(
        '--format', metavar='FORMAT', default=None,
        help='Force input format ' +
        '(Defaults to auto-detect.  Known formats: ' +
        ', '.join([x.name for x in converters]) + ')')
    parser.add_argument(
        'input', metavar='IN-FILE',
        help='Input filename')
    return parser


def get_args():
    parser = get_parser()
    args = parser.parse_args()
    if args.output == None:
        args.output = os.path.splitext(args.input)[0] + '.h5'
    return args


def create_dset(f, name, A):
    dset = f.create_dataset(
        name, shape=A.shape, dtype=A.dtype, compression='gzip')
    dset[:] = A


def main():
    args = get_args()

    format = None
    if args.format is None:
        for x in converters:
            if x.check_format(args.input):
                format = x.name
                break
        if format is None:
            raise ValueError(
                "Could not auto-detect format of '{}'".format(args.input))
    else:
        format = args.format
        if format not in converters_dict:
            raise ValueError(
                "unknown input format '{}'".format(format))
        if converters_dict[format].check_format(args.input) == False:
            raise ValueError(
                "'{}' is not recognized as format '{}'".format(
                    args.input, format))

    xvals, yvals, zvals, B_field, E_field = converters_dict[format].convert(
        args)

    with h5py.File(args.output, 'w') as f:
        f['xvals'] = xvals
        f['yvals'] = yvals
        f['zvals'] = zvals
        if B_field is not None:
            create_dset(f, 'B_field', B_field)
        if E_field is not None:
            create_dset(f, 'E_field', E_field)

if __name__ == '__main__':
    sys.exit(main())
