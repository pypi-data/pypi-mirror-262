#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np
import xarray as xr

# Local imports
from .ts_skymap import ts_skymap

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


def average_vdf(vdf, n_pts, method: str = "mean"):
    r"""Time averages the velocity distribution functions over `n_pts` in time.

    Parameters
    ----------
    vdf : xarray.DataArray
        Time series of the velocity distribution function.
    n_pts : int
        Number of points (samples) of the averaging window.
    method : {'mean', 'sum'}, Optional
        Method for averaging. Use 'sum' for counts. Default is 'mean'.

    Returns
    -------
    vdf_avg : xarray.DataArray
        Time series of the time averaged velocity distribution function.

    """

    # Check input type
    assert isinstance(vdf, xr.Dataset), "vdf must be a xarray.Dataset"

    assert n_pts % 2 != 0, "The number of distributions to be averaged must be an odd"

    n_vdf = len(vdf.time.data)
    times = vdf.time.data

    pad_value = np.floor(n_pts / 2)
    avg_inds = np.arange(pad_value, n_vdf - pad_value, n_pts, dtype=int)
    time_avg = times[avg_inds]

    energy_avg = np.zeros((len(avg_inds), vdf.data.shape[1]))
    phi_avg = np.zeros((len(avg_inds), vdf.data.shape[2]))
    vdf_avg = np.zeros((len(avg_inds), *vdf.data.shape[1:]))

    for i, avg_ind in enumerate(avg_inds):
        l_bound = int(avg_ind - pad_value)
        r_bound = int(avg_ind + pad_value)
        if method == "mean":
            vdf_avg[i, ...] = np.nanmean(vdf.data.data[l_bound:r_bound, ...], axis=0)
        elif method == "sum":
            vdf_avg[i, ...] = np.nansum(vdf.data.data[l_bound:r_bound, ...], axis=0)
        else:
            raise NotImplementedError("method not implemented feel free to do it!!")

        energy_avg[i, ...] = np.nanmean(
            vdf.energy.data[l_bound:r_bound, ...],
            axis=0,
        )
        phi_avg[i, ...] = np.nanmean(
            vdf.phi.data[l_bound:r_bound, ...],
            axis=0,
        )

    # Attributes
    glob_attrs = vdf.attrs  # Global attributes
    vdf_attrs = vdf.data.attrs  # VDF attributes
    coords_attrs = {k: vdf[k].attrs for k in ["time", "energy", "phi", "theta"]}

    # Get delta energy in global attributes for selected timestamps
    if "delta_energy_minus" in glob_attrs:
        glob_attrs["delta_energy_minus"] = glob_attrs["delta_energy_minus"][avg_inds, :]

    if "delta_energy_plus" in glob_attrs:
        glob_attrs["delta_energy_plus"] = glob_attrs["delta_energy_plus"][avg_inds, :]

    glob_attrs["esteptable"] = glob_attrs["esteptable"][: len(avg_inds)]

    vdf_avg = ts_skymap(
        time_avg,
        vdf_avg,
        energy_avg,
        phi_avg,
        vdf.theta.data,
        energy0=glob_attrs["energy0"],
        energy1=glob_attrs["energy1"],
        esteptable=glob_attrs["esteptable"][: len(avg_inds)],
        attrs=vdf_attrs,
        coords_attrs=coords_attrs,
        glob_attrs=glob_attrs,
    )

    return vdf_avg
