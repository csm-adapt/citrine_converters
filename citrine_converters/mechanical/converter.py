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
    process_files(files)
    process_keywords(keywds)
    # Don't worry about the details, yet; these are placeholders.
    # TODO Determine whether *files* is .zip, .tgz, .pif, or .json

    # TODO Read files into System-level PIF record
    # TODO generate System from *parent*. What do we do if parent not provided?

    # TODO Analyze stress-strain curve

    # TODO return *PIF*


def process_files(filenames):
    """
    Accepts an string list of file names
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
        stress = sdata.properties[0].scalars
        stress_time = sdata.properties[0].conditions.scalars
        strain = sdata.properties[1].scalars
        strain_time = sdata.properties[1].conditions.scalars
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
        print(type(results))
        return results

    if len(filenames) == 2:
        with open(filenames[0], 'r') as stress_data:
            stress_d = pif.load(stress_data)
        with open(filenames[1], 'r') as strain_data:
            strain_d = pif.load(strain_data)
        stress = stress_d.properties[0].scalars
        stress_time = stress_d.properties[0].conditions.scalars
        strain = strain_d.properties[0].scalars
        strain_time = strain_d.properties[0].conditions.scalars
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
    else:
        assert False, \
            'Something is wrong with the input if statements failed'
