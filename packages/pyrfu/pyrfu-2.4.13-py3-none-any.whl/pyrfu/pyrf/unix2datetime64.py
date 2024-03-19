#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


def unix2datetime64(time):
    r"""Converts unix time to datetime64 in ns units.

    Parameters
    ----------
    time : ndarray
        Time in unix format.

    Returns
    -------
    time_datetime64 : ndarray
        Time in datetime64 format.

    See Also
    --------
    pyrfu.pyrf.datetime642unix

    """

    # Make sure that time is in ns format
    time_unix = (time * 1e9).astype(np.int64)

    # Convert to unix
    time_datetime64 = time_unix.astype("datetime64[ns]")

    return time_datetime64
