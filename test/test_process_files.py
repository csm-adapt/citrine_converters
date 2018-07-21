import pytest
import numpy as np
from pypif import pif
import pandas as pd
import json
from citrine_converters.mechanical.converter import process_files


@pytest.fixture
def generate_expected_one_file():
    fname = 'resources/simple_data.json'

    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, 100)
    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, 100)
    expected = pif.System(
        subSystems=None,
        properties=[
            pif.Property(name='stress',
                         scalars=list(stress),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(stress_time))),

            pif.Property(name='strain',
                         scalars=list(strain),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(strain_time)))
                    ])
    with open(fname, 'w') as data:
        pif.dump(expected, data)

    return {
        'file_name': fname,
        'expected': expected
    }

@pytest.fixture
def generate_expected_two_files():
    fname = {'stress': 'resources/simple_stress.json',
             'strain': 'resources/simple_strain.json'}
    expected = [  # makes an array of two pif systems
        pif.System(
            properties=[
                pif.Property(name='stress',
                             scalars=list(np.linspace(0, 1)),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, 100))))]),

        pif.System(
            properties=[
                pif.Property(name='strain',
                             scalars=list(np.linspace(0, 1)),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, 100))))])
        ]
    # dump the pifs into two seperate files
    with open(fname['stress'], 'w') as stress_file:
        pif.dump(expected[0], stress_file)
    with open(fname['strain'], 'w') as strain_file:
        pif.dump(expected[1], strain_file)

    return {
        'file_names': fname,
        'expected': {
            'stress': expected[0],
            'strain': expected[1]
        }
    }

@pytest.fixture
def generate_pif_one_file(file):
    with open(file, 'r') as data:
        Data = pif.load(data)
    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, 100)
    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, 100)
    results = pif.System(
        subSystems=None,
        properties=[

                pif.Property(name='stress',
                             scalars=list(stress),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(stress_time))),
                pif.Property(name='strain',
                             scalars=list(strain),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(strain_time)))
                    ])
    return results

@pytest.fixture
def generate_pif_two_files(file1, file2):
    with open(file1,'r') as stress_data:
        stress_d = pif.load(stress_data)
    with open(file2, 'r') as strain_data:
        strain_d = pif.load(strain_data)

# currently the pifs are generated from linspace but I am trying to
    #  figure out how to generate them from a pif formatted json(I would know how to do it if not pif formatted
    # json.load then stress= loadedfile['stress']
    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, 100)
    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, 100)
    results = pif.System(
        subSystems=None,
        properties=[

                pif.Property(name='stress',
                             scalars=list(stress),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(stress_time))),
                pif.Property(name='strain',
                             scalars=list(strain),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(strain_time)))
                    ])
    return results
def test_stress_strain_time_in():
    # This test it to check whether the function picks up the lack of one of these in its files
    pass

def test_process_single_file(generate_expected_one_file):
    einfo = generate_expected_one_file
    expected = einfo['expected']
    fname = einfo['file_name']
    results = generate_pif_one_file(fname)
    # compare the pifs
    assert results.uid is None, \
        'Result UID should be None'
    assert results.names is None, \
        'Result should not be named'
    assert results.classifications is None, \
        'Result should not have any classifications.'
    assert len(results.properties) == \
        len(expected.properties), \
        'The length of the result and expected properties lists do not match.'
    assert results.ids is None, \
        'Result ids should be None'
    assert results.source is None, \
        'Result source should be None'
    assert results.quantity is None, \
        'Result quantity should be None'
    assert results.preparation is None,\
        'Result preparation should be None'
    assert results.subSystems is None,\
        'Results subSystem should be None'
    assert results.references is None,\
        'Results references should be None'
    assert results.contacts is None, \
        'Results contacts should be None'
    assert results.licenses is None,\
        'Results licenses should be None'
    assert results.tags is None,\
        'Results tags should be None'

def test_process_two_filenames(generate_expected_two_files):
    # create local variables and run fixtures
    einfo = generate_expected_two_files
    expected = einfo['expected']
    fname = einfo['file_names']
    results = generate_pif_two_files(fname['stress'], fname['strain'])
    # compare the pifs
    assert results.uid is None, \
        'Result UID should be None'
    assert results.names is None, \
        'Result should not be named'
    assert results.classifications is None, \
        'Result should not have any classifications.'
    assert len(results.properties) == \
        len(expected['stress'].properties) + \
        len(expected['strain'].properties), \
        'The length of the result and expected properties lists do not match.'
    assert results.ids is None, \
        'Result ids should be None'
    assert results.source is None, \
        'Result source should be None'
    assert results.quantity is None, \
        'Result quantity should be None'
    assert results.preparation is None,\
        'Result preparation should be None'
    assert results.subSystems is None,\
        'Results subSystem should be None'
    assert results.references is None,\
        'Results references should be None'
    assert results.contacts is None, \
        'Results contacts should be None'
    assert results.licenses is None,\
        'Results licenses should be None'
    assert results.tags is None,\
        'Results tags should be None'
    #TODO add check to make sure time is in it




# def test_check_pif_values(generate_expected, generate_simple_two_files):
#     expected = generate_expected
#     results = generate_simple_two_files
#     assert results.properties[0] == expected.properties[0], \
#         'The expected pif and result pif differ in stress values'
#     assert results.properties[1] == expected.properties[1], \
#         'The expected pif and result pif differ in strain values'

