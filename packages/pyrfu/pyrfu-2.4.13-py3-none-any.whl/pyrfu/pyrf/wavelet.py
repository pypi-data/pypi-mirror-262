#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import logging
import os

# 3rd party imports
import numba
import numpy as np
import xarray as xr
from scipy import fft

# Local imports
from .calc_fs import calc_fs

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"

logging.captureWarnings(True)
logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


@numba.jit(nopython=True, fastmath=True)
def _ww(s_ww, scales_mat, sigma, frequencies_mat, f_nyq):
    # TODO : use nested for loop and math instead of numpy and test speed!!
    w_w = s_ww * np.exp(
        -sigma * sigma * ((scales_mat * frequencies_mat - f_nyq) ** 2) / 2,
    )
    w_w = w_w * np.sqrt(1)
    return w_w


@numba.jit(nopython=True, parallel=True, fastmath=True)
def _power_r(power, new_freq_mat):
    power2 = np.absolute((2 * np.pi) * np.conj(power) * power / new_freq_mat)
    return power2


@numba.jit(nopython=True, parallel=True, fastmath=True)
def _power_c(power, new_freq_mat):
    power2 = np.sqrt(np.absolute((2 * np.pi) / new_freq_mat)) * power
    return power2


def wavelet(inp, **kwargs):
    """Computes wavelet spectrogram based on fast FFT algorithm.
    Parameters
    ----------
    inp : xarray.DataArray
        Input quantity.
    **kwargs : dict
        Hash table of keyword arguments with :
            * fs : int or float
                Sampling frequency of the input time series.
            * f : list or ndarray
                Vector [f_min f_max], calculate spectra between frequencies
                f_min and f_max.
            * nf : int or float
                Number of frequency bins.
            * wavelet_width : int or float
                Width of the Morlet wavelet. Default 5.36.
            * linear : float
                Linear spacing between frequencies of df.
            * return_power : bool
                Set to True to return the power, False for complex wavelet
                transform. Default True.
            * cut_edge : bool
                Set to True to set points affected by edge effects to NaN,
                False to keep edge affect points. Default True
    Returns
    -------
    out : xarray.DataArray or xarray.Dataset
        Wavelet transform of the input.
    """

    # Unpack time and data
    data = inp.data

    f_s = kwargs.get("fs", calc_fs(inp))
    n_freqs = kwargs.get("nf", 200)
    wavelet_width = kwargs.get("wavelet_width", 5.36)
    cut_edge = kwargs.get("cut_edge", True)
    return_power = kwargs.get("return_power", True)

    if kwargs.get("linear"):
        linear_df = True
        if isinstance(kwargs["linear"], bool) and kwargs["linear"]:
            delta_f = 100
            logging.warning("Unknown input for linear delta_f set to 100")
        elif isinstance(kwargs["linear"], (int, float)):
            delta_f = kwargs["linear"]
        else:
            raise TypeError("linear keyword argument must be bool, float or int")
    else:
        delta_f = 100
        linear_df = False

    scale_min, scale_max = [0.01, 2]

    f_min, f_max = kwargs.get(
        "f",
        [0.5 * f_s / 10**scale_max, 0.5 * f_s / 10**scale_min],
    )

    f_nyq, scale_number, sigma = [f_s / 2, n_freqs, wavelet_width / (f_s / 2)]

    if linear_df:
        scale_number = np.floor(f_nyq / delta_f).astype(np.int64)

        f_min, f_max = [delta_f, scale_number * delta_f]

        scales = f_nyq / (np.linspace(f_max, f_min, scale_number))
    else:
        scale_min = np.log10(0.5 * f_s / f_max)
        scale_max = np.log10(0.5 * f_s / f_min)
        scales = np.logspace(scale_min, scale_max, scale_number)

    # Remove the last sample if the total number of samples is odd
    if len(data) / 2 != np.floor(len(data) / 2):
        time = inp.time.data[:-1]
        data = data[:-1, ...]
    else:
        time = inp.time.data

    # Check for NaNs
    scales[np.isnan(scales)] = 0

    # Find the frequencies for an FFT of all data
    freq = f_s * 0.5 * np.arange(1, 1 + len(data) / 2) / (len(data) / 2)

    # The frequencies corresponding to FFT
    frequencies = np.hstack([0, freq, -np.flip(freq[:-1])])

    # Get the correct frequencies for the wavelet transform
    new_freq = f_nyq / scales

    if len(inp.shape) == 1:
        out_dict, power2 = [None, np.zeros((len(inp.data), n_freqs))]
    elif len(inp.shape) == 2:
        out_dict, power2 = [{}, None]
    else:
        raise TypeError("Invalid shape of the inp")

    new_freq_mat, _ = np.meshgrid(new_freq, frequencies, sparse=True)

    _, frequencies_mat = np.meshgrid(scales, frequencies, sparse=True)

    # if scalar add virtual axis
    if len(inp.shape) == 1:
        data = data[:, np.newaxis]

    # go through all the data columns
    for i in range(data.shape[1]):
        # Make the FFT of all data
        data_col = data[:, i]

        # Wavelet transform of the data
        # Forward FFT
        s_w = fft.fft(data_col, workers=os.cpu_count())

        scales_mat, s_w_mat = np.meshgrid(scales, s_w, sparse=True)

        # Calculate the FFT of the wavelet transform
        w_w = _ww(s_w_mat, scales_mat, sigma, frequencies_mat, f_nyq)

        # Backward FFT
        power = fft.ifft(w_w, axis=0, workers=os.cpu_count())

        # Calculate the power spectrum
        if return_power:
            power2 = _power_r(power, np.tile(new_freq_mat, (len(power), 1)))
        else:
            power2 = _power_c(power, np.tile(new_freq_mat, (len(power), 1)))

        if cut_edge:
            censure = np.floor(2 * scales).astype(int)

            for j in range(scale_number):
                power2[: censure[j], j] = np.nan

                power2[len(data_col) - censure[j] : len(data_col), j] = np.nan

        if len(inp.shape) == 2:
            out_dict[inp.comp.data[i]] = (
                ["time", "frequency"],
                np.fliplr(power2),
            )

    if len(inp.shape) == 1:
        out = xr.DataArray(
            np.fliplr(power2),
            coords=[time, np.flip(new_freq)],
            dims=["time", "frequency"],
        )
    else:
        out = xr.Dataset(
            out_dict,
            coords={"time": time, "frequency": np.flip(new_freq)},
        )

    return out
