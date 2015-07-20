"""Structure example data for tests."""

# $Id: data_structures.py 22614 2015-07-15 18:14:53Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 13:14:53 -0500 (Wed, 15 Jul 2015) $
#
# This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.
#
# algebraixlib is free software: you can redistribute it and/or modify it under the terms of version
# 3 of the GNU Lesser General Public License as published by the Free Software Foundation.
#
# algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
# If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------
from algebraixlib.structure import CartesianProduct, GenesisSetA, GenesisSetM, GenesisSetN, PowerSet, Structure, Union
from algebraixlib.util.test import create_test_object

_print_examples = False


def _print_object_collection(name):
    if _print_examples:
        print('{name}:'.format(name=name))
        for key, val in sorted(globals()[name].items()):
            print('  "{key}": {val}'.format(key=key, val=val))


#: Two 'instances' of Structure. (They should be the same.)
empties = {key: create_test_object(Structure(), key, val) for key, val in {
    '{}': None,
    '{}-2': None
}.items()}
_print_object_collection('empties')


#: Two 'instances' of GenesisSetA. (They should be the same.)
setas = {key: create_test_object(GenesisSetA(), key, val) for key, val in {
    'A': None,
    'A-2': None
}.items()}
_print_object_collection('setas')


#: Two 'instances' of GenesisSetM. (They should be the same.)
setms = {key: create_test_object(GenesisSetM(), key, val) for key, val in {
    'M': None,
    'M-2': None
}.items()}
_print_object_collection('setms')

setns = {key: create_test_object(GenesisSetN(), key, val) for key, val in {
    'N': None,
    'N-2': None
}.items()}
_print_object_collection('setns')


#: Basic CartesianProduct instances.
basic_cps = {key: create_test_object(CartesianProduct(**val), key, val) for key, val in {
    'AxA': {'left': GenesisSetA(), 'right': GenesisSetA()},
    'AxM': {'left': GenesisSetA(), 'right': GenesisSetM()},
    'MxM': {'left': GenesisSetM(), 'right': GenesisSetM()},
    'Ax(AxA)': {'left': GenesisSetA(), 'right': CartesianProduct(GenesisSetA(), GenesisSetA())},
}.items()}
_print_object_collection('basic_cps')


#: Basic Union instances.
basic_unions = {key: create_test_object(Union(**val), key, val) for key, val in {
    'A': {'iterable': [GenesisSetA()]},
    'M': {'iterable': [Union([GenesisSetA()]), GenesisSetM()]},
    'M-2': {'iterable': [Union([Union([GenesisSetA()]), GenesisSetM()]), GenesisSetA()]},
    'M-3 U(AxA)': {'iterable': [Union([Union([GenesisSetA()]), GenesisSetM()]), basic_cps['AxA']]},
    'M-4 U(AxM)': {'iterable': [Union([Union([GenesisSetA()]), GenesisSetM()]), basic_cps['AxM']]},
    'M-4 U(AxM)-2': {'iterable': [
        Union([GenesisSetA()]),
        Union([Union([GenesisSetA()]), GenesisSetM()]),
        Union([Union([Union([GenesisSetA()]), GenesisSetM()]), GenesisSetA()]),
        Union([Union([GenesisSetA()]), basic_cps['AxA']]),
        Union([Union([Union([GenesisSetA()]), GenesisSetM()]), basic_cps['AxA']]),
        Union([Union([Union([GenesisSetA()]), GenesisSetM()]), basic_cps['AxM']]),
    ]},
    'AU(AxA)': {'iterable': [Union([GenesisSetA()]), basic_cps['AxA']]},
}.items()}
_print_object_collection('basic_unions')


#: Basic PowerSet instances.
basic_pss = {key: create_test_object(PowerSet(**val), key, val) for key, val in {
    'A': {'elements_struct': GenesisSetA()},
    'M': {'elements_struct': GenesisSetM()},
    'AxA': {'elements_struct': basic_cps['AxA']},
    'MxM': {'elements_struct': basic_cps['MxM']},
    'P(AxA)': {'elements_struct': PowerSet(basic_cps['AxA'])},
    'P(MxM)': {'elements_struct': PowerSet(basic_cps['MxM'])},
    'PP(AxA)': {'elements_struct': PowerSet(PowerSet(basic_cps['AxA']))},
    'PP(MxM)': {'elements_struct': PowerSet(PowerSet(basic_cps['MxM']))},
    'PPP(AxA)': {'elements_struct': PowerSet(PowerSet(PowerSet(basic_cps['AxA'])))},
    'PPP(MxM)': {'elements_struct': PowerSet(PowerSet(PowerSet(basic_cps['MxM'])))},
}.items()}
_print_object_collection('basic_pss')
