import numpy as np
# from citrine_converters import util
# import sys
# print('debug begin:')
# for p in sys.path:
#     print(p)

from citrine_converters.util.listops import ensure_array_like
from citrine_converters.util.listops import replace_if_present_else_append
from citrine_converters.util.listops import reassignment_error
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


def process_files(filenames, dst=None):
    """
    Accepts a list of strings of file names the files should be pif
    formatted json files

    Accepts the filenames or file objects that contain the PIF-formatted
    stress and strain data. The results are integrated into *dst*, which
    is a `pif.System` object or None, in which case, a new System object
    is created.

    If multiple filenames are provided, then neither can have both stress
    and strain data.

    :param dst: Destination for the stress and strain data.
    :type dst: pif.System
    :param filenames:
    :type filenames: string or array-like (of strings)
    :return: The pif.System object that contains stress and strain.
    """
    # ensure filenames is a list/array-like
    # ensure dst is a pif.System object, or create one
    # read stress and strain files
    filenames = ensure_array_like(filenames)
    if len(filenames) == 1:
        l, r = (filenames[0]), pif.System()
        with open(l, 'r') as dataLeft:
            left = pif.load(dataLeft)
    elif len(filenames) == 2:
        l, r = (filenames[0]), (filenames[1])
        with open(l, 'r') as dataLeft:
            left = pif.load(dataLeft)
        with open(r, 'r') as dataRight:
            right = pif.load(dataRight)
    else:
        raise IOError("One or two filenames must be supplied to process_files")

    # make sure dst is a pif.system()
    if type(dst) == pif.System():
        pass
    else:
        dst = pif.System(
            properties=[]
        )


    # assign stress and strain to None for checking if they are reassigned
    stress = None
    strain = None
    #TODO add a check to make sure time is included in found data, could do it after stress strain found
    try:
        if len(filenames) == 2:

    # check if left contains stress && right contains strain
            if any(p.name == "stress" for p in getattr(left, 'properties', [])) and \
                    any(p.name == "strain" for p in getattr(right, 'properties', [])):
                reassignment_error(stress) # checks to make sure stress is not being reassigned
                reassignment_error(strain) # checks to make sure strain is not being reassigned
                stress = left
                strain = right

    # check is right contains stress and left contains strain
            if any(p.name == "stress" for p in getattr(right, 'properties', [])) and \
                    any(p.name == "strain" for p in getattr(left, 'properties', [])):
                reassignment_error(stress) # checks to make sure stress is not being reassigned
                reassignment_error(strain) # checks to make sure strain is not being reassigned
                stress = right
                strain = left

    # check if stress and strain are in the left file only
        elif len(filenames) == 1:
            #TODO need a better way to check if stress strain are being reassigned for these ones

            stress = pif.System(properties=[pif.Property()])
            strain = pif.System(properties=[pif.Property()])
            if (left.properties[0].name == 'stress' and len(left.properties) == 2):

                stress.properties[0] = left.properties[0]
                if left.properties[1].name == 'strain':
                    strain.properties[0] = left.properties[1]
            elif (left.properties[0].name == 'strain' and len(left.properties) == 2):
                strain.properties[0] = left.properties[0]
                if left.properties[1].name == 'stress':
                    stress.properties[0] = left.properties[1]
            else:
                raise IOError("Either stress or strain is not provided in the single input file")
    # check if stress and strain have a time condition
    except IOError:
        raise IOError("Stress and strain can not be defined in two different places")


    try:
        if stress.properties[0].conditions.name == 'time' and strain.properties[0].conditions.name == 'time' \
                and stress.properties[0].conditions.scalars == strain.properties[0].conditions.scalars:
            pass
        else:
            assert False, "Time is non existent in stress or strain and/or the times do not match \
            between stress and strain"
    except IndexError:

        raise IOError("Stress or strain is missing a time component")







    # check if left file contains both stress and strain
    # check if left contains strain
    # check if right contains stress, error if left does also
    # check if right contains strain, error if left does also
    # ensure dst.properties exists
    dst.properties = getattr(dst, "properties", [])
    # add stress data to destination

    # print(type(dst.properties))

    # I think stress and strain are pif.system object when they should only be property

    replace_if_present_else_append(dst.properties, stress.properties[0],
                                   cmp=lambda a,b: a.name == b.name)
    # add strain data to destination
    replace_if_present_else_append(dst.properties, strain.properties[0],
                                   cmp=lambda a,b: a.name == b.name)
    return dst

