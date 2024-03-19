#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import string

# 3rd party imports
import numpy as np
import xarray as xr

# Local imports
from .. import pyrf

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"


__all__ = [
    "generate_timeline",
    "generate_data",
    "generate_ts",
    "generate_spectr",
    "generate_vdf",
]


def generate_timeline(
    f_s,
    n_pts: int = 10000,
    dtype="datetime64[ns]",
    ref_time: str = "2019-01-01T00:00:00.000000000",
):
    r"""Generate timeline for testings

    Parameters
    ----------
    f_s
    n_pts
    dtype
    ref_time

    Returns
    -------

    """
    ref_time = np.datetime64(ref_time)
    times = [ref_time + np.timedelta64(int(i * 1e9 / f_s), "ns") for i in range(n_pts)]
    times = np.array(times).astype(dtype)
    return times


def generate_data(n_pts, tensor_order: int = 0):
    r"""Generate data (numpy.ndarray) for testings

    Parameters
    ----------
    n_pts
    tensor_order

    Returns
    -------
    data
    """

    data = np.random.random((n_pts, *([3] * tensor_order)))

    return data


def generate_ts(f_s, n_pts, tensor_order: int = 0, attrs: dict = None):
    r"""Generate timeseries for testings

    Parameters
    ----------
    f_s
    n_pts
    tensor_order
    attrs

    Returns
    -------

    """
    if attrs is None:
        attrs = {}

    time = generate_timeline(f_s, n_pts)
    data = generate_data(n_pts, tensor_order=tensor_order)

    if tensor_order == 0:
        out = pyrf.ts_scalar(time, data, attrs=attrs)
    elif tensor_order == 1:
        out = pyrf.ts_vec_xyz(time, data, attrs=attrs)
    elif tensor_order == 2:
        out = pyrf.ts_tensor_xyz(time, data, attrs=attrs)
    else:
        coords = [time, *[np.arange(data.shape[i]) for i in range(1, tensor_order + 1)]]
        dims = ["time", *list(string.ascii_lowercase[8 : 8 + tensor_order])]
        out = xr.DataArray(data, coords=coords, dims=dims, attrs=attrs)

    out.time.attrs = {"UNITS": "I AM GROOT!!"}

    return out


def generate_spectr(f_s, n_pts, shape, attrs=None):
    r"""Generates spectrum for testings

    Parameters
    ----------
    f_s
    n_pts
    shape
    attrs

    Returns
    -------

    """
    out = pyrf.ts_spectr(
        generate_timeline(f_s, n_pts),
        np.arange(shape),
        np.random.random((n_pts, shape)),
        attrs=attrs,
    )
    return out


def generate_vdf(
    f_s,
    n_pts,
    shape,
    energy01: bool = False,
    species: str = "ions",
    units: str = "s^3/cm^6",
):
    r"""Generate skymap for testings

    Parameters
    ----------
    f_s
    n_pts
    shape
    energy01
    species

    Returns
    -------

    """
    times = generate_timeline(f_s, n_pts)

    phi = np.arange(shape[1])
    phi = np.tile(phi, (n_pts, 1))
    theta = np.arange(shape[2])
    data = np.random.random((n_pts, *shape))

    if energy01:
        energy0 = np.linspace(0, shape[0], shape[0], endpoint=False)
        energy1 = np.linspace(0, shape[0], shape[0], endpoint=False) + 0.5
        esteptable = np.arange(n_pts) % 2
        energy = np.tile(energy0, (n_pts, 1))
        energy[esteptable == 1, :] = np.tile(energy1, (np.sum(esteptable), 1))
    else:
        energy = np.linspace(0, shape[0], shape[0], endpoint=False)
        energy = np.tile(energy, (n_pts, 1))
        energy0 = energy[0, :]
        energy1 = energy[1, :]
        esteptable = np.zeros(n_pts)

    attrs = {"UNITS": units}
    glob_attrs = {
        "species": species,
        "delta_energy_plus": np.ones((n_pts, shape[0])),
        "delta_energy_minus": np.ones((n_pts, shape[0])),
    }

    out = pyrf.ts_skymap(
        times,
        data,
        energy,
        phi,
        theta,
        energy0=energy0,
        energy1=energy1,
        esteptable=esteptable,
        attrs=attrs,
        glob_attrs=glob_attrs,
    )
    return out
