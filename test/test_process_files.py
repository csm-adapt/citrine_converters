import pytest
import numpy as np
from pypif import pif
import random as rnd
from citrine_converters.mechanical.converter import process_files



@pytest.fixture
def generate_expected_one_file():
    """Generates the expected pif into one file"""
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

filee = 'resources/simple_data.json'

@pytest.fixture
def generate_expected_two_files():
    """Generates expected pif into two files"""
    fname = {'stress': 'resources/simple_stress.json',
             'strain': 'resources/simple_strain.json'}
    expected = [  # makes an array of two pif systems
        pif.System(
            properties=[
                pif.Property(name='stress',
                             scalars=list(np.linspace(0, 100)),
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
def generate_no_time_one_file():
    """Generates a file with no time included"""
    fname = 'resources/simple_data_no_time.json'

    stress = np.linspace(0, 100)
    strain = np.linspace(0, 100)
    expected = pif.System(
        subSystems=None,
        properties=[
            pif.Property(name='stress',
                         scalars=list(stress),
                         conditions=pif.Value(
                             name=None
                         )
                         ),

            pif.Property(name='strain',
                         scalars=list(strain),
                         )
                    ])
    with open(fname, 'w') as data:
        pif.dump(expected, data)

    return fname # only needs to return the file name since we wont calculate pifs with no time

@pytest.fixture
def generate_no_time_two_files():
    """Generates two files with no time included"""
    fname = {'stress': 'resources/simple_stress_no_time.json',
             'strain': 'resources/simple_strain_no_time.json'}
    expected = [  # makes an array of two pif systems
        pif.System(
            properties=[
                pif.Property(name='stress',
                             scalars=list(np.linspace(0, 100))
                             )]),

        pif.System(
            properties=[
                pif.Property(name='strain',
                             scalars=list(np.linspace(0, 1))
                             )])
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
def generate_no_stress_one_file():
    """Generates a file with no stress"""
    fname = 'resources/simple_data_no_stress.json'

    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, 100)
    expected = pif.System(
        subSystems=None,
        properties=[
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
def generate_no_strain_one_file():
    """Generates a file with no strain"""
    fname = 'resources/simple_data_no_strain.json'

    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, 100)
    expected = pif.System(
        subSystems=None,
        properties=[
            pif.Property(name=None,
                         scalars=list(stress),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(stress_time))),


            pif.Property(name='stress',
                         scalars=list(stress),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(stress_time))),
                    ])
    with open(fname, 'w') as data:
        pif.dump(expected, data)

    return {
        'file_name': fname,
        'expected': expected
    }

@pytest.fixture
def generate_differ_times_one_file():
    """Generates a file with differing time ending points"""
    fname = 'resources/differ_times.json'

    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, rnd.randint(1, 100))
    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, rnd.randint(1, 100)) # generates a random time interval
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

    return fname
@pytest.fixture
def generate_differ_times_two_files():
    """Generates differing ending times to see if the function catches it"""
    fname = {'stress': 'resources/simple_stress_differ_times.json',
             'strain': 'resources/simple_strain_differ_times.json'}
    expected = [  # makes an array of two pif systems
        pif.System(
            properties=[
                pif.Property(name='stress',
                             scalars=list(np.linspace(0, 100)),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, rnd.randint(1, 100)))))]),

        pif.System(
            properties=[
                pif.Property(name='strain',
                             scalars=list(np.linspace(0, 1)),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, rnd.randint(1, 100)))))])
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
def generate_swapped_stress_strain_one_file():
    """Swaps the stress and strain info in one file"""
    fname = 'resources/simple_swapped_data.json'

    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, 100)
    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, 100)
    expected = pif.System(
        subSystems=None,
        properties=[
            pif.Property(name='strain',
                         scalars=list(strain),
                         conditions=pif.Value(
                             name='time',
                             scalars=list(strain_time))),
            pif.Property(name='stress',
                         scalars=list(stress),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(stress_time)))

                    ])
    with open(fname, 'w') as data:
        pif.dump(expected, data)

    return {
        'file_name': fname,
        'expected': expected
    }

@pytest.fixture
def generate_swapped_stress_strain_two_files(strain, stress):
    """Swaps the file inputs"""
    return process_files(strain, stress)

@pytest.fixture
def generate_expected_pd_one_file():
    """Generates proper pd from expected pif"""
    pass

@pytest.fixture
def generate_expected_pd_two_files():
    """Generates proper pd from expected pif"""
    pass


@pytest.fixture
def generate_two_files_both_stress_strain():
    """Generates two files that have both stress and strain in each file"""
    pass

def test_differ_times_one_file(generate_differ_times_one_file):
    """Tests to see if function catches differing end time should throw an error"""
    fname = generate_differ_times_one_file
    with pytest.raises(Exception):
        process_files([fname])

"""Below test passes as expected"""
def test_time_not_in(generate_no_time_one_file):
    # This test it to check whether the function picks up the lack of one of these in its files
    fname = generate_no_time_one_file
    with pytest.raises(Exception):
        process_files([fname])

"""This test does not perform as expected(EDIT) after some time this test began to work magically"""
def test_stress_not_in(generate_no_stress_one_file):
    fname = generate_no_stress_one_file
    with pytest.raises(Exception):
        process_files([fname])


"""this test should fail when simple data is loaded in because an assertion should not be thrown but it is
issue does not lie with this test it works"""
def test_strain_not_in(generate_no_strain_one_file):
    fname = generate_no_strain_one_file
    with pytest.raises(Exception) as f:
        process_files([fname])
    # assert str(f.value) == 'stuff'  "got a coercing to unicode error"



def test_swapped_stress_strain_one_file(generate_swapped_stress_strain_one_file):
    einfo = generate_swapped_stress_strain_one_file
    expected = einfo['expected']
    fname = einfo['file_name']
    results = process_files([fname])
# Replaced the commented code below here with a modified copy
#  of the test_process_single_file code and everything worked???
    # info = generate_swapped_stress_strain_one_file
    # expected = info['expected']
    # fname = 'resources/simple_data.json' # info['file_name']
    # results = process_files([fname])
    A = results.properties[0].scalars
    B = expected.properties[0].scalars
    C = results.properties[1].scalars
    D = expected.properties[1].scalars
    assert np.array_equal(A, B), \
        'Result and expected pifs differ in stress values'
    assert np.array_equal(C, D), \
        'Result and expected pifs differ in strain values'

def test_process_single_file(generate_expected_one_file):
    einfo = generate_expected_one_file
    expected = einfo['expected']
    fname = einfo['file_name']
    results = process_files([fname])
    # compare the pifs
    A = results.properties[0].scalars
    B = expected.properties[0].scalars
    C = results.properties[1].scalars
    D = expected.properties[1].scalars
    assert np.array_equal(A, B), \
        'Result and expected pifs differ in stress values'
    assert np.array_equal(C, D), \
        'Result and expected pifs differ in strain values'
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
    results = process_files([fname['stress'], fname['strain']])
    # compare the pifs
    A = results.properties[0].scalars
    B = expected['stress'].properties[0].scalars
    C = results.properties[1].scalars
    D = expected['strain'].properties[0].scalars
    assert np.array_equal(A, B), \
        'Results and expected pifs differ in stress values'
    assert np.array_equal(C, D), \
        'Results snd expected pifs differ in strain values'
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

results = process_files(['resources/simple_data.json'])
"""The below lines are for testing why the function is returnning a type None to the test"""
# result = process_files(['resources/simple_data.json'])
# print('Type returned from function:')
# print(type(result))
"""
The above code does work when I pass the 'no time' json data to it, it raises an assertion error.
When I pass the time inlcuded data to it, everything works and it prints out the type two times
"""

