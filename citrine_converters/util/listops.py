def ensure_array_like(x):
    """
    Ensures that x is an array-like object, or wraps it in
    a list.

    :param x: Object that should be a list.
    :return: x wrapped in a list.
    """
    if hasattr(x, '__iter__') and not isinstance(x, str):
        return x
    else:
        return [x]


def replace_if_present_else_append(
        objlist,
        obj,
        cmp=lambda a, b: a == b,
        rename=None):
    """
    Add an object to a list of objects, if that obj does
    not already exist. If it does exist (`cmp(A, B) == True`),
    then replace the property in the property_list. The names
    are compared in a case-insensitive way.

    Input
    =====
    :objlist, list: list of objects.
    :obj, object: object to Add

    Options
    =======
    :cmp, (bool) cmp (A, B): compares A to B. If True, then the
        objects are the same and B should replace A. If False,
        then B should be appended to `objlist`.
    :param rename: Should A be renamed instead of overwritten? If not False,
        then rename should be a unary function that changes the name of A.
    :type rename: bool or unary function
    Output
    ======
    List is modified in place. A reference to the list is returned.
    """
    print(type (objlist))
    for i in range(len(objlist)):
        # was a matching object found in the list?
        if cmp(objlist[i], obj):
            # if so, should the old object be renamed?
            if rename is not None:
                newA = rename(objlist[i])
                # is the renamed object distinct from the object
                # (`obj`) that is to be added to the list?
                if cmp(newA, obj):
                    msg = '`rename` does not make {} unique.'.format(
                        str(objlist[i])[:32])
                    raise ValueError(msg)
                # now that we have newA, replace the original
                # object in the list with `obj`...
                objlist[i] = obj
                #... and replace_if_present_else_append newA.
                replace_if_present_else_append(
                    objlist, newA, cmp=cmp, rename=rename)
            # if the existing object should not be renamed,
            # simply replace.
            else:
                objlist[i] = obj
            # short circuit to exit the for loop and the function.
            return objlist
    # if we get here, then the property was not found. Append.
    objlist.append(obj)
    return objlist


def reassignment_error(original):
    """
    This function takes in the original value of a variable, checks and makes sure its value is None
    if it is not None, then the value is trying to be reassigned and an error is raised
    :param original: The original value of the variable
    :type any type
    :return: bool value
    """

    if (original == None):
        return False
    else:
        raise IOError("The variable '{}' was attempted to be reassigned".format(original))
        return True