import pytest
import numpy as np
from pypif import pif
import json
from citrine_converters.mechanical.converter import process_files


# note strain has been changed to be 0-100 for simplicity sakes
@pytest.fixture
def single_file():
    fname = {'stress': 'resources/expected_simple_stress_1.json',
             'strain': 'resource/expected_simple_stress_1.json'}
    expected = pif.System(
        properties=[
        pif.Property(name='stress',
                     scalars=list(np.linspace(0,100))),
        pif.Property(name='strain',
                     scalars = list(np.linspace(0,100))),
        pif.Property(name='time',
                     scalars = list(np.linspace(0,100)))
        ])
    #
    #         properties=
    #             pif.Property(
    #                 uid = 'single_file_stress',
    #                 name = 'stress',
    #                 scalars= list(np.linspace(0,100)),
    #                 conditions=pif.Value(
    #                     name='time',
    #                     scalars=list(np.linspace(0,100))
    #                 )
    #             )
    #     ),
    #     pif.System(
    #         pif.Property(
    #             uid = 'single_file_strain',
    #             name= 'strain',
    #             scalars = list(np.linspace(0,100)),
    #             conditions=pif.Value(
    #                 name='time',
    #                 scalars=list(np.linspace(0,100))
    #             )
    #
    #
    #         )
    #     )
    # ]
    #
@pytest.fixture
def generate_simple():
    with open('resources/simple_data.json') as r:
        data = json.load(r)
    stress = data['stress']
    strain = data['strain']
    time = data['time']
    results = pif.System(
        #names=None,
        properties=[
            pif.Property(name='stress',
                         scalars=list(stress),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(time))),

            pif.Property(name='strain',
                         scalars=list(strain),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(time)))
                    ])
    return results

@pytest.fixture
def generate_two_files():

    fname = {'stress': 'resources/expected_simple_stress.json',
             'strain': 'resources/expected_simple_strain.json'}
    expected = pif.System(
        properties=[
            pif.Property(name='stress',
                         scalars=list(np.linspace(0, 100)),
                         conditions=pif.Value(
                            name='time',
                            scalars=list(np.linspace(0, 100)))),
            pif.Property(name='strain',
                         scalars=list(np.linspace(0, 100)),
                         conditions=pif.Value(
                                name='time',
                                scalars=list(np.linspace(0, 100))))
        ])
        #     properties=
        #         pif.Property(
        #
        #             uid=None,
        #             name='stress',
        #             scalars=list(np.linspace(0, 100)),
        #             conditions=pif.Value(
        #                 name='time',
        #                 scalars=list(np.linspace(0, 100))
        #             )
        #         )
        # ),
        # pif.System(
        #     pif.Property(
        #         uid = None,
        #         name='strain',
        #         scalars=list(np.linspace(0, 100)),
        #         conditions=pif.Value(
        #             name='time',
        #             scalars=list(np.linspace(0, 100))
        #         )
        #     )
        # )]
    with open(fname['stress'], 'w') as ofs:
        pif.dump(expected.properties[0], ofs)#write the pif to the file in the resources folder
    with open(fname['strain'], 'w') as ofs:
        pif.dump(expected.properties[1], ofs)
    return {
        'filenames': fname,
        'expected': {
            'stress': expected.properties[0],
            'strain': expected.properties[1]
        }
    }

def test_process_two_filenames(generate_two_files,generate_simple):
    # create local variables and run fixtures
    pass
    info = generate_two_files
    #fname = info['filenames']
    expected = info['expected']
    # produce a new pif.System object with the stress and strain data
    #results = process_files([fname['stress'], fname['strain']])
    infor = generate_simple
    results = infor
    # compare the pifs
    assert results.uid is None, \
         'Result UID should be None'
    assert results.names is None, \
        'Result should not be named'
    assert results.classifications is None, \
        'Result should not have any classifications.'
    # TODO finish checking the attributes of the system object...
    assert len(results.properties) == 2\
           #len(expected['strain'].properties) + \
           #len(expected['stress'].properties), \
    'The length of the result and expected properties lists do not match.'
    # assert results.ids is None, \
    #     'Result ids should be None, but it is {}.'.format(results.ids)
    # assert results.source is None, \
    #     'Result source should be None, but it is {}.'.format(results.source)
    # assert results.quantity is None, \
    #     'Result quantity should be None, but it is {}.'.format(results.quantity)
    # assert results.preparation is None,\
    #     'Result preparation should be None, but it is {}.'.format(results.preparation)
    # assert results.subSystems is None,\
    #     'Results subSystem should be None, but it is {}.'.format(results.subSystems)
    # assert results.references is None,\
    #     'Results references should be None, but it is {}.'.format(results.references)
    # assert results.contacts is None, \
    #     'Results contacts should be None, but it is {}.'.format(results.contacts)
    # assert results.licenses is None,\
    #     'Results licenses should be None, but it is {}.'.format(results.licenses)
    # assert results.tags is None,\
    #     'Results tags should be None, but it is {}.'.format(results.tags)


def test_process_single_file(single_file,generate_simple):
    # TODO generate fname, expected, etc.
    pass

