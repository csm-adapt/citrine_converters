import numpy as np
from pypif import pif
import pandas as pd

def converter(files=[], **keywds):
    """
    Summary
    =======

    Accepts PIF formatted stress and strain data and calculates the
    following mechanical information from these data:

        - elastic (Young's) modulus
        - elastic onset (strain)
        - yield strength
        - yield strain (plastic onset)
        - ultimate strength
        - necking onset (strain)
        - fracture strength
        - total elongation
        - ductility
        - toughness

    The input PIF files must contain "time" and "stress" fields (stress
    PIF) and "time" and "strain" fields (strain PIF).

    Input
    =====
    :param files:
        Option 1.
        Compressed zip/tarball with stress filename and strain
        filename. Only two files should be present in this compressed
        file. Both files should be *PIF* formatted files. The stress file is
        identified because it contains, at a minimum, a property called
        *stress*, with *time* as a condition of that property. The strain
        file is identified because it contains, at a minimum, a property
        called *strain* with *time* as a condition of that property.

        Option 2.
        Single *PIF*-formatted file that contains, at a minimum, two
        properties named "stress" and "strain", that each include "time"
        as a condition.
    :type files: string

    Keywords
    ========
    :param parent: *PIF*-formatted record of the sample whose stress-strain
        data was measured.
    :type parent: TODO Should this be a string? If a string, a filename or
        a PIF-formatted string? If not a string, a *pif.System* object?
    :units, string: unit convention used in this stress-strain data.
        Should be one of: {MPa, kip}

    Output
    ======
    PIF object.
    """
    result = pif.System(keywds.get('parent', pif.System()).as_dictionary())
    # TODO write out the function calls necessary to process these data.
    # process_files(files)
    # process_keywords(keywds)
    # Don't worry about the details, yet; these are placeholders.
    # TODO Determine whether *files* is .zip, .tgz, .pif, or .json

    # TODO Read files into System-level PIF record
    # TODO generate System from *parent*. What do we do if parent not provided?

    # TODO Analyze stress-strain curve

    # TODO return *PIF*


def process_files(filenames=[]):
    """
    Accepts a list of strings of file names the files should be pif
    formatted json files

    Accepts the filenames or file objects that contain the PIF-formatted
    stress and strain data. The results are integrated into *dst*, which
    is a `pif.System` object or None, in which case, a new System object
    is created.

    If multiple filenames are provided, then neither can have both stress
    and strain data.

    :param filenames:
    :return:
    """
# check if one or two files
    if len(filenames) == 1:
        with open(filenames[0], 'r') as data:
            sdata = pif.load(data)
        szprop = len(sdata.properties) == 2 # checks to see the length of properties
# -----------------------------Check for stress in the given file--------------------------------
        if 'stress' in [sdata.properties[0].name]:
            assert 'time' in [sdata.properties[0].conditions.name], \
                'Stress is dependent on time but time was not found'
            stress = sdata.properties[0].scalars
            stress_time = sdata.properties[0].conditions.scalars
        else:
            if not szprop:
                assert False, 'No stress data found in given file'

            if 'stress' in [sdata.properties[1].name]:
                assert 'time' in [sdata.properties[1].conditions.name], \
                    'Stress is dependent on time but time was not found'
                stress = sdata.properties[1].scalars
                stress_time = sdata.properties[1].conditions.scalars
            else:
                assert False, 'No stress data found in {}'.format(filenames[0])
# ---------------------------------Check for strain in the given file--------------------------------

        if 'strain' in [sdata.properties[0].name]:
            assert 'time' in sdata.properties[0].conditions.name, \
                'Strain is dependent on time but time was not found'
            strain = sdata.properties[0].scalars
            strain_time = sdata.properties[0].conditions.scalars
        else:
            if not szprop:
                assert False, 'No strain data found in given file'
            # test for swap is atleast getting here
            if 'strain' in [sdata.properties[1].name]: # this is returning false
                assert 'time' in [sdata.properties[1].conditions.name], \
                    'Strain is dependent on time but time was not found'
                strain = sdata.properties[1].scalars
                strain_time = sdata.properties[1].conditions.scalars
            else:
                assert False, 'No strain data found in {}'.format(filenames[0])

        res = pif.System(
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
        return res

    if len(filenames) == 2:
        with open(filenames[0], 'r') as stress_data:
            stress_d = pif.load(stress_data)
        with open(filenames[1], 'r') as strain_data:
            strain_d = pif.load(strain_data)
        stress = stress_d.properties[0].scalars
        stress_time = stress_d.properties[0].conditions.scalars
        strain = strain_d.properties[0].scalars
        strain_time = strain_d.properties[0].conditions.scalars
        res = pif.System(
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
        return res
    else:
        assert False, \
            'Something is wrong with the input if statements failed'
