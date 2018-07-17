import pytest
import numpy as np
from pypif import pif
from citrine_converters.mechanical.converter import process_files



#what is pytest do
@pytest.fixture
def generate_two_files(input_filenames):
    fname = {'stress': 'resources/simple_stress.json',
            'strain': 'resources/simple_strain.json'}
    expected = [
        pif.System(
            properties=
                pif.Property(
                    name='stress',
                    scalars=list(np.linspace(0, 100)),
                    conditions=pif.Value(
                        name='time',
                        scalars=list(np.linspace(0, 100))
                    )
                )
        ),
        pif.System(
            pif.Property(
                name='strain',
                scalars=list(np.linspace(0, 1)),
                conditions={
                    'name': 'time',
                    'scalars': list(np.linspace(0, 100))}
            )
        )]
    with open(fname['stress'], 'w') as ofs:
        pif.dump(expected[0], ofs)#creates a pif object
    with open(fname['strain'], 'w') as ofs:
        pif.dump(expected[1], ofs)
    return {
        'filenames': fname,
        'expected': {
            'stress': expected[0],
            'strain': expected[1]
        }
    }

def test_process_two_filenames(generate_two_files):
    # create local variables and run fixtures
    info = generate_two_files
    fname = info['filenames']
    expected = info['expected']
    # produce a new pif.System object with the stress and strain data
    result = process_files([fname['stress'], fname['strain']])
    # compare the pifs
    assert results.uid is None, \
        'Result UID should be None, but it is {}.'.format(results.uid)
    assert result.names is None, \
        'Result should not be named'
    assert result.classifications is None, \
        'Result should not have any classifications.'
    # TODO finish checking the attributes of the system object...
    assert len(result.properties) == \
           len(expected['strain'].properties) + \
           len(expected['stress'].properties), \
        'The length of the result and expected properties lists do not match.'
    assert results.ids is None, \
        'Result ids should be None, but it is {}.'.format(results.ids)
    assert results.source is None, \
        'Result source should be None, but it is {}.'.format(results.source)
    assert results.quantity is None, \
        'Result quantity should be None, but it is {}.'.format(results.quantity)
    assert results.preparation is None,\
        'Result preparation should be None, but it is {}.'.format(results.preparation)
    assert results.subSystems is None,\
        'Results subSystem should be None, but it is {}.'.format(results.subSystems)
    assert results.references is None,\
        'Results references should be None, but it is {}.'.format(results.references)
    assert results.contacts is None, \
        'Results contacts should be None, but it is {}.'.format(results.contacts)
    assert results.licenses is None,\
        'Results licenses should be None, but it is {}.'.format(results.licenses)
    assert results.tags is None,\
        'Results tags should be None, but it is {}.'.format(results.tags)


def test_process_single_file(single_file, generate_simple):
    # TODO generate fname, expected, etc.
    pass

