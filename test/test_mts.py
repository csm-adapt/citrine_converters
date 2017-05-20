# -*- coding: utf-8 -*-

import os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, '..'))

import pytest
from pypif import pif
from citrine_converters.mts import converter


SOURCE="{}/data/mts-output.csv".format(HERE)


@pytest.fixture
def generate_output():
    return False


@pytest.fixture
def mts_no_stress():
    with open('{}/data/mts-no-stress.json'.format(HERE)) as ifs:
        expected = ifs.read()
    return expected


@pytest.fixture
def mts_with_stress():
    with open('{}/data/mts-with-stress.json'.format(HERE)) as ifs:
        expected = ifs.read()
    return expected


def test_file_only(mts_no_stress, generate_output):
    pifs = converter(SOURCE)
    if generate_output:
        with open('{}/data/mts-no-stress.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == mts_no_stress


def test_file_list(mts_no_stress, generate_output):
    pifs = converter([SOURCE])
    if generate_output:
        with open('{}/data/mts-no-stress.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == mts_no_stress


def test_stress(mts_with_stress, generate_output):
    area=12.9
    units='mm^2'
    pifs = converter(SOURCE, area=area, units=units)
    if generate_output:
        with open('{}/data/mts-with-stress.json'.format(HERE), 'w') as ofs:
            pif.dump(pifs, ofs, sort_keys=True)
        assert False
    pifs = pif.dumps(pifs, sort_keys=True)
    assert pifs == mts_with_stress
