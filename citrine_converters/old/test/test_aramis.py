# -*- coding: utf-8 -*-

import os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, '..'))

import pytest
from pypif import pif
from citrine_converters.old.aramis import converter


EYSTRAIN="{}/data/aramis-ey_strain.csv".format(HERE)
MISES="{}/data/aramis-mises.csv".format(HERE)


@pytest.fixture
def generate_output():
    return False


@pytest.fixture
def aramis_ey_strain_no_time():
    with open('{}/data/aramis-ey_strain-no-time.json'.format(HERE)) as ifs:
        expected = ifs.read()
    return expected


@pytest.fixture
def aramis_ey_strain_with_time():
    with open('{}/data/aramis-ey_strain-with-time.json'.format(HERE)) as ifs:
        expected = ifs.read()
    return expected


@pytest.fixture
def aramis_mises_no_time():
    with open('{}/data/aramis-mises-no-time.json'.format(HERE)) as ifs:
        expected = ifs.read()
    return expected


@pytest.fixture
def aramis_mises_with_time():
    with open('{}/data/aramis-mises-with-time.json'.format(HERE)) as ifs:
        expected = ifs.read()
    return expected


def test_ey_strain_no_time(aramis_ey_strain_no_time, generate_output):
    pifs = converter(EYSTRAIN)
    if generate_output:
        with open('{}/data/aramis-ey_strain-no-time.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == aramis_ey_strain_no_time


def test_ey_strain_with_time(aramis_ey_strain_with_time, generate_output):
    pifs = converter(EYSTRAIN, timestep=0.5)
    if generate_output:
        with open('{}/data/aramis-ey_strain-with-time.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == aramis_ey_strain_with_time


def test_mises_no_time(aramis_mises_no_time, generate_output):
    pifs = converter(MISES)
    if generate_output:
        with open('{}/data/aramis-mises-no-time.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == aramis_mises_no_time


def test_mises_with_time(aramis_mises_with_time, generate_output):
    pifs = converter(MISES, timestep=0.5)
    if generate_output:
        with open('{}/data/aramis-mises-with-time.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == aramis_mises_with_time
