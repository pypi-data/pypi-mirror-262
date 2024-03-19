#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np
import xarray as xr

# Local imports
from .ts_scalar import ts_scalar

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


def calc_sqrtq(p_xyz):
    r"""Computes agyrotropy coefficient as in [1]_

    .. math::

        Q = \frac{P_{12}^2 + P_{13}^2 + P_{23}^2}
        {P_\perp^2 + 2 P_\perp P_\parallel}


    Parameters
    ----------
    p_xyz : xarray.DataArray
        Time series of the pressure tensor

    Returns
    -------
    sqrt_q : xarray.DataArray
        Time series of the agyrotropy coefficient of the specie

    References
    ----------
    .. [1]  Swisdak, M. (2016), Quantifying gyrotropy in magnetic
            reconnection, Geophys. Res.Lett., 43, 43–49, doi:
            https://doi.org/10.1002/2015GL066980.

    Examples
    --------
    >>> from pyrfu import mms, pyrf

    Time interval

    >>> tint = ["2019-09-14T07:54:00.000","2019-09-14T08:11:00.000"]

    Spacecraft index

    >>> ic = 1

    Load magnetic field and electron pressure tensor

    >>> b_xyz = mms.get_data("b_gse_fgm_srvy_l2", tint, 1)
    >>> p_xyz_e = mms.get_data("pe_gse_fpi_fast_l2", tint, 1)

    Rotate electron pressure tensor to field aligned coordinates

    >>> p_fac_e_pp = mms.rotate_tensor(p_xyz_e, "fac", b_xyz, "pp")

    Compute agyrotropy coefficient

    >>> sqrt_q_e = pyrf.calc_sqrtq(p_fac_e_pp)

    """

    # Check input type
    assert isinstance(p_xyz, xr.DataArray), "p_xyz must be a xarray.DataArray"

    # Check import shape
    message = "p_xyz must be a time series of a tensor"
    assert p_xyz.data.ndim == 3 and p_xyz.shape[1] == 3 and p_xyz.shape[2] == 3, message

    # Parallel and perpendicular components
    p_para = p_xyz.data[:, 0, 0]
    p_perp = (p_xyz.data[:, 1, 1] + p_xyz.data[:, 2, 2]) / 2

    # Off-diagonal terms
    p_12, p_13, p_23 = [p_xyz.data[:, 0, 1], p_xyz.data[:, 0, 2], p_xyz.data[:, 1, 2]]

    sqrt_q = np.sqrt(p_12**2 + p_13**2 + p_23**2)
    sqrt_q /= np.sqrt(p_perp**2 + 2 * p_perp * p_para)
    sqrt_q = ts_scalar(p_xyz.time.data, sqrt_q)

    return sqrt_q
