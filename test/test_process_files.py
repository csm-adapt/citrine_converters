import pytest
import numpy as np
from pypif import pif
import random as rnd
from citrine_converters.mechanical.converter import process_files
"""
README
Format:
TEST NAME
-Description
PASS/FAIL
**note numbers correspond to order of tests. Tests Start on line 441
1.	test_stress_strain_both_files
-The tests generates simple data that has stress and strain defined in one file. The test passes the function two files
with both stress and strain data contained in each.
PASS
2.	test_stress_redefined
-This test generates one file with stress defined twice and no strain defined.
PASS
3.	test_strain_redefined
-This test generates one file with strain defined twice and no stress defined.
PASS
4.	test_differ_times_one_file
-This test generates one file with differing times
PASS
5.	test_differ_times_two_files
-This test generates two files with differing end times
PASS
6.	test_time_not_in
-This test generates one file with no time at all in it
PASS
7.	test_stress_not_in
-This test generates one file with no stress given
PASS
8.	test_strain_not_in
-This test generates one file with no strain given
PASS
9.	test_time_not_in_two_files
-This test generates two files with no time included 
PASS
10.	test_stress_not_in_two_files
-This test passes two identical files that only contain strain data
PASS
11.	test_strain_not_in_two_files
-This test passes in two identical files that only contain stress data
PASS
12.	test_swapped_stress_strain_one_file
-This test generates one file but with stress and strain swapped in order.
PASS
13.	test_swapped_stress_strain_two_files
-This test swaps the file input
PASS
14.	test_process_single_file
-This tests generates an expected pif, and then compares it to the function generated pif (from one file)
PASS
15.	 test_process_two_filenames
-This test generates an expected pif, and then compares it to the functions generated pif (from two files)
PASS
16.	test_bad_number_of_files
-This test inputs three files and zero files into the function to make sure it throws an assertion error
PASS

"""

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
files = {'stress': 'resources/simple_stress.json',
             'strain': 'resources/simple_strain.json'}
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

    # from StringIO import StringIO
    # sio = StringIO()
    # pif.dump(expected, sio)
    #
    # return {
    #     'StringIO': sio,
    #     'expected': expected
    # }

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

    return fname
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
def generate_two_files_both_stress_strain():
    """Generates two files that have both stress and strain in each file"""
    fname = {'stress': 'resources/double_stress.json',
             'strain': 'resources/double_strain.json'}
    expected = [  # makes an array of two pif systems
        pif.System(
            properties=[
                pif.Property(name='stress',
                             scalars=list(np.linspace(0, 100)),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, 100)))),
                pif.Property(name='strain',
                             scalars=list(np.linspace(0, 1)),
                             conditions=pif.Value(
                                 name='time',
                                 scalars=list(np.linspace(0, 100))))]),

        pif.System(
            properties=[
                pif.Property(name='stress',
                             scalars=list(np.linspace(0, 100)),
                             conditions=pif.Value(
                                 name='time',
                                 scalars=list(np.linspace(0, 100)))),
                pif.Property(name='strain',
                             scalars=list(np.linspace(0, 1)),
                             conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, 100))))
        ])]

    # dump the pifs into two seperate files
    with open(fname['stress'], 'w') as stress_file:
        pif.dump(expected[0], stress_file)
    with open(fname['strain'], 'w') as strain_file:
        pif.dump(expected[1], strain_file)

    return fname


@pytest.fixture
def generate_stress_redefined():
    fname = 'resources/stress_redefined.json'

    stress = np.linspace(0, 100)
    stress_time = np.linspace(0, 100)
    strain = np.linspace(0, 100)
    strain_time = np.linspace(0, 100)
    expected = pif.System(
        subSystems=None,
        properties=[
            pif.Property(name='stress',
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

    return fname

@pytest.fixture
def generate_strain_redefined():
    fname = 'resources/strain_redefined.json'

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
            pif.Property(name='strain',
                         scalars=list(stress),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(stress_time)))

                    ])
    with open(fname, 'w') as data:
        pif.dump(expected, data)

    return fname


# ---------------------------Begin Tests---------------------------

# NUM 1
def test_stress_strain_both_files(generate_two_files_both_stress_strain):
    """Inputs data with stress/strain defined twice"""
    fname = generate_two_files_both_stress_strain
    with pytest.raises(Exception):
        process_files([fname[0],fname[1]])

# NUM 2
def test_stress_redefined(generate_stress_redefined):
    """Inputs one file with stress defined twice and no strain"""
    fname = generate_stress_redefined
    try:
        process_files([fname])
        raise Exception, 'The redefined stress data and lack of strain data was not caught'
    except IOError:
        pass

# NUM 3
def test_strain_redefined(generate_strain_redefined):
    """Inputs one file with strain defined twice and no stress"""
    fname = generate_strain_redefined
    try:
        process_files([fname])
        raise Exception, 'The redefined strain data and lack of stress data was not caught'
    except IOError:
        pass

# NUM 4
def test_differ_times_one_file(generate_differ_times_one_file):
    """Tests to see if function catches differing end time should throw an error"""
    fname = generate_differ_times_one_file
    with pytest.raises(Exception):
        process_files([fname])

# NUM 5
def test_differ_times_two_files(generate_differ_times_two_files):
    """Inputs two files with differing time data"""
    fname = generate_differ_times_two_files
    with pytest.raises(Exception):
        process_files([fname[0], fname[1]])

# NUM 6
def test_time_not_in(generate_no_time_one_file):
    # This test it to check whether the function picks up the lack of one of these in its files
    fname = generate_no_time_one_file
    with pytest.raises(Exception):
        process_files([fname])

# NUM 7
def test_stress_not_in(generate_no_stress_one_file):
    """Input file has no stress"""
    fname = generate_no_stress_one_file
    with pytest.raises(Exception):
        process_files([fname])


# NUM 8
def test_strain_not_in(generate_no_strain_one_file):
    """Input file has no strain"""
    fname = generate_no_strain_one_file
    with pytest.raises(Exception) as f:
        process_files([fname])

# NUM 9
def test_time_not_in_two_files(generate_no_time_two_files):
    """Two file input with no time data"""
    fname = generate_no_time_two_files
    with pytest.raises(Exception):
        process_files([fname[0], fname[1]])
        # process_files(['resources/simple_stress.json', 'resources/simple_strain.json'])
#         above comment is for testing
# NUM 10
def test_stress_not_in_two_files(generate_no_stress_one_file):
    """Two file input with no stress"""
    fname = generate_no_stress_one_file
    with pytest.raises(Exception):
        process_files([fname, fname])

# NUM 11
def test_strain_not_in_two_files(generate_no_strain_one_file):
    """Two file input with no strain"""
    fname = generate_no_strain_one_file
    with pytest.raises(Exception):
        process_files([fname, fname])

# NUM 12
def test_swapped_stress_strain_one_file(generate_swapped_stress_strain_one_file):
    """Input swapped stress strain into function"""
    einfo = generate_swapped_stress_strain_one_file
    expected = einfo['expected']
    fname = einfo['file_name']
    results = process_files([fname])
    A = results.properties[0].scalars
    B = expected.properties[0].scalars
    C = results.properties[1].scalars
    D = expected.properties[1].scalars
    assert np.array_equal(A, B), \
        'Result and expected pifs differ in stress values'
    assert np.array_equal(C, D), \
        'Result and expected pifs differ in strain values'

# NUM 13
def test_swapped_stress_strain_two_files(generate_expected_two_files):
    """Swaps file input"""
    # create local variables and run fixtures
    einfo = generate_expected_two_files
    expected = einfo['expected']
    fname = einfo['file_names']
    results = process_files([fname['strain'], fname['stress']])
    # compare the pifs
    A = results.properties[0].scalars
    B = expected['stress'].properties[0].scalars
    C = results.properties[1].scalars
    D = expected['strain'].properties[0].scalars
    assert np.array_equal(A, B), \
        'Results and expected pifs differ in stress values'
    assert np.array_equal(C, D), \
        'Results snd expected pifs differ in strain values'
    assert getattr( results, 'uid', None) is None, \
        'Result UID should be None'
    assert getattr(results, 'names', None) is None, \
        'Result should not be named'
    assert getattr(results, 'classifications', None) is None, \
        'Result should not have any classifications.'
    assert len(results.properties) == \
        len(expected['stress'].properties) + \
        len(expected['strain'].properties), \
        'The length of the result and expected properties lists do not match.'
    assert getattr(results, "ids", None) is None, \
        'Result ids should be None'
    assert getattr(results, 'source', None) is None, \
        'Result source should be None'
    assert getattr(results, 'quantity', None) is None, \
        'Result quantity should be None'
    assert getattr(results, 'preparation', None) is None,\
        'Result preparation should be None'
    assert getattr(results, "subSystems", None) is None, \
        'Results subSystem should be None'
    assert getattr(results, 'references', None) is None,\
        'Results references should be None'
    assert getattr(results, 'contacts', None) is None, \
        'Results contacts should be None'
    assert getattr(results, 'licenses', None) is None,\
        'Results licenses should be None'
    assert getattr(results,'tags', None) is None,\
        'Results tags should be None'

# NUM 14
def test_process_single_file(generate_expected_one_file):
    """Tests process_files with one file input"""
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
    assert getattr( results, 'uid', None) is None, \
        'Result UID should be None'
    assert getattr(results, 'names', None) is None, \
        'Result should not be named'
    assert getattr(results, 'classifications', None) is None, \
        'Result should not have any classifications.'
    assert len(results.properties) == \
        len(expected.properties), \
        'The length of the result and expected properties lists do not match.'
    assert getattr(results, "ids", None) is None, \
        'Result ids should be None'
    assert getattr(results, 'source', None) is None, \
        'Result source should be None'
    assert getattr(results, 'quantity', None) is None, \
        'Result quantity should be None'
    assert getattr(results, 'preparation', None) is None,\
        'Result preparation should be None'
    assert getattr(results, "subSystems", None) is None, \
        'Results subSystem should be None'
    assert getattr(results, 'references', None) is None,\
        'Results references should be None'
    assert getattr(results, 'contacts', None) is None, \
        'Results contacts should be None'
    assert getattr(results, 'licenses', None) is None,\
        'Results licenses should be None'
    assert getattr(results,'tags', None) is None,\
        'Results tags should be None'

# NUM 15
def test_process_two_filenames(generate_expected_two_files):
    """Tests process_files with two file inputs"""
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
    assert getattr( results, 'uid', None) is None, \
        'Result UID should be None'
    assert getattr(results, 'names', None) is None, \
        'Result should not be named'
    assert getattr(results, 'classifications', None) is None, \
        'Result should not have any classifications.'
    assert len(results.properties) == \
        len(expected['stress'].properties) + \
        len(expected['strain'].properties), \
        'The length of the result and expected properties lists do not match.'
    assert getattr(results, "ids", None) is None, \
        'Result ids should be None'
    assert getattr(results, 'source', None) is None, \
        'Result source should be None'
    assert getattr(results, 'quantity', None) is None, \
        'Result quantity should be None'
    assert getattr(results, 'preparation', None) is None,\
        'Result preparation should be None'
    assert getattr(results, "subSystems", None) is None, \
        'Results subSystem should be None'
    assert getattr(results, 'references', None) is None,\
        'Results references should be None'
    assert getattr(results, 'contacts', None) is None, \
        'Results contacts should be None'
    assert getattr(results, 'licenses', None) is None,\
        'Results licenses should be None'
    assert getattr(results,'tags', None) is None,\
        'Results tags should be None'

def test_bad_number_of_files():
    """Inputs 3 files and 0 files"""
    with pytest.raises(Exception):
        process_files(['resources/simple_data.json', 'resources/simple_data.json', 'resources/simple_data.json'])
    with pytest.raises(Exception):
        process_files([])



