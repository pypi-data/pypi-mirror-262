# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
hdf5_wrapper.py
-----------------------
"""

import h5py
import numpy as np
import os
from numpy.core.defchararray import encode, decode


class hdf5_wrapper():
    """
    Class for reading/writing hdf5 files, which behaves similar to a native dict
    """

    def __init__(self, fname='', target='', mode='r'):
        """
        Initialize the hdf5_wrapper class
        Notes: If the fname is supplied (either by a positional or keyword argument),
                 the wrapper will open a hdf5 database from the filesystem.  The reccomended
                 options for the mode flag include 'r' for read-only and 'a' for read/write
                 access.  If write mode is enabled, and the fname does not point
                 to an existing file, a new database will be created.
                 If the target is supplied, then a new instance of the wrapper will
                 be created using an existing database handle.

        Args:
            fname (str): the filename of a new or existing hdf5 database
            target (str): the handle of an existing hdf5 dataset
            mode (str): the read/write behavior of the database (default='r')
        """

        self.mode = mode
        self.target = target
        if fname:
            self.target = h5py.File(os.path.expanduser(os.path.normpath(fname)), self.mode)

    def __getitem__(self, k):
        """
        Get a target from the database
        Note: The returned value depends on the type of the target:
                - An existing hdf5 group will return an instance of hdf5_wrapper
                - An existing array will return an numpy ndarray
                - If the target is not present in the datastructure and the
                    database is open in read/write mode, the wrapper will create a
                    new group and return an hdf5_wrapper
                - Otherwise, this will throw an error

        Args:
            k (str): name of target group or array

        Returns
            hdf5_wrapper.hdf5_wrapper, array
        """
        if (k not in self.target):
            if (self.mode in ['w', 'a']):
                self.target.create_group(k)
            else:
                raise ValueError(f'Entry does not exist in database: {k}')

        tmp = self.target[k]

        if isinstance(tmp, h5py._hl.group.Group):
            return hdf5_wrapper(target=tmp, mode=self.mode)
        elif isinstance(tmp, h5py._hl.dataset.Dataset):
            tmp = np.array(tmp)

            # Decode any string types
            if (tmp.dtype.kind in ['S', 'U', 'O']):
                tmp = decode(tmp)

            # Convert any 0-length arrays to native types
            if not tmp.shape:
                tmp = tmp[()]

            return tmp
        else:
            return tmp

    def __setitem__(self, k, value):
        """
        Write an object to the database if write-mode is enabled

        Args:
            k (str): the name of the object
            value (float, np.ndarray): the object to be written
        """

        if (self.mode in ['w', 'a']):
            if isinstance(value, dict):
                # Recursively add groups and their children
                if (k not in self.target):
                    self.target.create_group(k)
                new_group = self[k]
                for x in value:
                    new_group[x] = value[x]
            else:
                # Delete the old copy if necessary
                if (k in self.target):
                    del (self.target[k])

                # Add everything else as an ndarray
                tmp = np.array(value)
                if (tmp.dtype.kind in ['S', 'U', 'O']):
                    tmp = encode(tmp)
                self.target[k] = tmp
        else:
            raise ValueError(
                'Cannot write to an hdf5 opened in read-only mode!  This can be changed by overriding the default mode argument for the wrapper.'
            )

    def link(self, k, target):
        """
        Link an external hdf5 file to this location in the database

        Args:
            k (str): the name of the new link in the database
            target (str): the path to the external database
        """
        self.target[k] = h5py.ExternalLink(target, '/')

    def keys(self):
        """
        Get a list of groups and arrays located at the current level

        Returns
            list: a list of strings 
        """
        if isinstance(self.target, h5py._hl.group.Group):
            return list(self.target)
        else:
            raise ValueError('Object not a group!')

    def items(self):
        """
        Return the key-value pairs for entries at the current level

        Returns
            tuple: keys, values
        """
        tmp = self.keys()
        values = [self[k] for k in tmp]
        return zip(tmp, values)

    def __enter__(self):
        """
        Entry point for an iterator
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        End point for an iterator
        """
        self.target.close()

    def __del__(self):
        """
        Closes the database on wrapper deletion
        """
        try:
            if isinstance(self.target, h5py._hl.files.File):
                self.target.close()
        except:
            pass

    def close(self):
        """
        Closes the database
        """
        if isinstance(self.target, h5py._hl.files.File):
            self.target.close()

    def get_copy(self):
        """
        Copy the entire database into memory

        Returns
            dict: A copy of the database
        """
        tmp = {}
        self.copy(tmp)
        return tmp

    def copy(self, output):
        """
        Pack the contents of the current database level onto the target dict

        Args:
            output (dict): the dictionary to pack objects into
        """
        for k in self.keys():
            tmp = self[k]

            if isinstance(tmp, hdf5_wrapper):
                output[k] = {}
                tmp.copy(output[k])
            else:
                output[k] = tmp

    def compare_with_tolerance(self, fname, atol=1e-9):
        """
        Compare the current file with a second file

        Args:
            fname (str): Path of the target file
            atol (float): Maximum absolute tolerance for each entry

        Returns:
            int: Number of file comparison errors
        """
        if not os.path.isfile(fname):
            print(f'Could not find file to compare: {fname}')
            return 1

        try:
            other_file = hdf5_wrapper(fname)
            return compare_level_recursive(self, other_file, atol)

        except Exception as e:
            print('An exception occurred while comparing files')
            print(e)
            return 1


def compare_level_recursive(current, target, atol, path='/'):
    """
    Compare the current file with a second file

    Args:
        target (hdf5_wrapper): Wrapper to compare
        atol (float): Maximum absolute tolerance for each entry

    Returns:
        int: Number of file comparison errors
    """
    errors = 0
    current_keys = current.keys()
    target_keys = target.keys()
    current_only = [k for k in current_keys if k not in target_keys]
    target_only = [k for k in target_keys if k not in current_keys]
    valid_keys = [k for k in current_keys if k in target_keys]

    if len(current_only):
        tmp = ', '.join(current_only)
        print(f'Keys found in current file at {path}, but not target: {tmp}')
        errors += len(current_only)

    if len(target_only):
        tmp = ', '.join(target_only)
        print(f'Keys found in target file at {path}, but not current: {tmp}')
        errors += len(target_only)

    for k in valid_keys:
        kp = f'{path}/{k}'
        va = current[k]
        vb = target[k]

        if isinstance(va, hdf5_wrapper):
            if isinstance(vb, hdf5_wrapper):
                errors += compare_level_recursive(va, vb, atol, path=kp + '/')
            else:
                print(f'Directory structure mismatch: {kp}')

        elif isinstance(va, np.ndarray):
            Na = np.shape(va)
            Nb = np.shape(vb)

            if (Na != Nb):
                sa = ','.join(Na)
                sb = ','.join(Nb)
                print(f'Size mismatch for entry {kp}: current=({sa}), target=({sb})')
                errors += 1
                continue

            if va.dtype.kind != vb.dtype.kind:
                print(va.dtype.kind, vb.dtype.kind)
                print(f'Type mismatch for entry {kp}: current=({va.dtype}), target=({vb.dtype})')
                errors += 1
                continue

            if not va.size:
                continue

            if isinstance(va.flat[0], np.str_):
                Nc = np.sum(va != vb)
                if Nc:
                    print(f'String array {kp} contains {Nc} mismatches')
                    print('Current=', va)
                    print('Target=', vb)
                    errors += 1

            else:
                Ia = np.isclose(va, vb, atol=atol, equal_nan=True)
                if not np.all(Ia):
                    Ib = np.where(~Ia)
                    print(f'Array {kp} does not match')
                    print('Current=', va[Ib])
                    print('Target=', vb[Ib])
                    print('Indices=', Ib)
                    errors += 1

        else:
            if va.dtype.kind != vb.dtype.kind:
                print(f'Type mismatch for entry {kp}: current={va.dtype.kind}, target={vb.dtype.kind}')
                errors += 1
                continue

            if isinstance(va, np.str_):
                if (va != vb):
                    print(f'Values {kp} do not match')
                    print('Current=', va)
                    print('Target=', vb)

            else:
                if abs(va - vb) > atol:
                    print(f'Values {kp} do not match')
                    print('Current=', va)
                    print('Target=', vb)
                    errors += 1

    return errors
