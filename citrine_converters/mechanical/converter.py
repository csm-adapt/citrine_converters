import numpy as np
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
    elif len(filenames) == 2:
        l, r = (filenames[0]), (filenames[1])
        with open(l, 'r') as dataLeft:
            left = pif.load(dataLeft)
        with open(r, 'r') as dataRight:
            right = pif.load(dataRight)
    else:
        raise IOError("One or two filenames must be supplied to process_files")


    if type(dst) == pif.System():
        pass
    else:
        dst = pif.System(
            properties=[]
        )

    print(type(dst))
    print('type of dst^^')

    # assign stress and strain to None for checking if they are reassigned
    stress = None
    strain = None
    #TODO add a check to make sure time is included in found data, could do it after stress strain found
    # check if left contains stress && right contains strain
    try:

        if any(p.name == "stress" for p in getattr(left, 'properties', [])) and \
                any(p.name == "strain" for p in getattr(right, 'properties', [])):
            if reassignment_error(stress):
                pass  # checks to make sure stress is not being reassigned
            if reassignment_error(strain):
                pass  # checks to make sure strain is not being reassigned
            stress = left
            strain = right

    # check is right contains stress and left contains strain
        if any(p.name == "stress" for p in getattr(right, 'properties', [])) and \
                any(p.name == "strain" for p in getattr(left, 'properties', [])):
            # ReassingmentError(stress) # checks to make sure stress is not being reassigned
            # ReassingmentError(strain) # checks to make sure strain is not being reassigned
            stress = right
            strain = left
    # check if stress and strain are in the left file only

    # check if stress and strain have a time condition
    except IOError:
        raise IOError("Stress and strain can not be defined in two different places")

    try:
        if stress.properties[0].conditions.name == 'time' and strain.properties[0].conditions.name == 'time':
            pass
    except IndexError:
        raise IOError("Stress or strain is missing a time component")







    # check if left file contains both stress and strain
    # check if left contains strain
    # check if right contains stress, error if left does also
    # check if right contains strain, error if left does also
    # ensure dst.properties exists
    # dst.properties = getattr(dst, "properties", [])
    # add stress data to destination
    print('dst type:')
    print(type(dst))
    print('end')
    replace_if_present_else_append(dst.properties, stress,
                                   cmp=lambda a, b: a.name == b.name)
    # add strain data to destination
    replace_if_present_else_append((dst.properties, strain),
                                   cmp=lambda a, b: a.name == b.name)
    # verify/validate input parameters
    return dst
#
# # check if one or two files
#     if len(filenames) == 1:
#         with open(filenames[0], 'r') as data:
#             sdata = pif.load(data)
#         szprop = len(sdata.properties) == 2 # checks to see the length of properties
# # -----------------------------Check for stress in the given file--------------------------------
#         if 'stress' in [sdata.properties[0].name]:
#             assert 'time' in [sdata.properties[0].conditions.name], \
#                 'Stress is dependent on time but time was not found'
#             stress = sdata.properties[0].scalars
#             stress_time = sdata.properties[0].conditions.scalars
#         else:
#             if not szprop:
#                 assert False, 'No stress data found in given file'
#
#             if 'stress' in [sdata.properties[1].name]:
#                 assert 'time' in [sdata.properties[1].conditions.name], \
#                     'Stress is dependent on time but time was not found'
#                 stress = sdata.properties[1].scalars
#                 stress_time = sdata.properties[1].conditions.scalars
#             else:
#                 assert False, 'No stress data found in {}'.format(filenames[0])
# # ---------------------------------Check for strain in the given file--------------------------------
#         if 'strain' in [sdata.properties[0].name]:
#             assert 'time' in sdata.properties[0].conditions.name, \
#                 'Strain is dependent on time but time was not found'
#             strain = sdata.properties[0].scalars
#             strain_time = sdata.properties[0].conditions.scalars
#         else:
#             if not szprop:
#                 assert False, 'No strain data found in given file'
#             # test for swap is atleast getting here
#             if ('strain' in [sdata.properties[1].name]): # this is returning false
#                 assert 'time' in [sdata.properties[1].conditions.name], \
#                     'Strain is dependent on time but time was not found'
#                 strain = sdata.properties[1].scalars
#                 strain_time = sdata.properties[1].conditions.scalars
#             else:
#                 assert False, 'No strain data found in {}'.format(filenames[0])
#
#         assert stress_time == strain_time, \
#             'Stress and Strain times must be equal'
#         res = pif.System(
#             subSystems=None,
#             properties=[
#                 pif.Property(name='stress',
#                              scalars=list(stress),
#                              conditions=pif.Value(
#                                  name='time',
#                                  scalars=list(stress_time))),
#                 pif.Property(name='strain',
#                              scalars=list(strain),
#                              conditions=pif.Value(
#                                  name='time',
#                                  scalars=list(strain_time)))
#             ])
#         return res
#
#     if len(filenames) == 2:
#         with open(filenames[0], 'r') as stress_data:
#             stress_d = pif.load(stress_data)
#         with open(filenames[1], 'r') as strain_data:
#             strain_d = pif.load(strain_data)
#         stress = stress_d.properties[0].scalars
#         stress_time = stress_d.properties[0].conditions.scalars
#         strain = strain_d.properties[0].scalars
#         strain_time = strain_d.properties[0].conditions.scalars
#         res = pif.System(
#             subSystems=None,
#             properties=[
#                 pif.Property(name='stress',
#                              scalars=list(stress),
#                              conditions=pif.Value(
#                                  name='time',
#                                  scalars=list(stress_time))),
#                 pif.Property(name='strain',
#                              scalars=list(strain),
#                              conditions=pif.Value(
#                                  name='time',
#                                  scalars=list(strain_time)))
#             ])
#         return res
#     else:
#         assert False, \
#             'Something is wrong with the input if statements failed'
