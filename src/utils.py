import datetime
import math

import numpy as np


def sum_chunk(x: np.array, chunk_size: int, axis: int = -1) -> np.array:
    """Reshaping the 2D array into a 3D array, then collapse the extra dimension with np.sum. Generalizing it to n-dimensional arrays, could do something like this:

    Args:
        x (np.array): precipitation data
        chunk_size (int): Number of columns to be added
        axis (int, optional): dimension of the data. Defaults to -1.

    Returns:
        np.array: Precipitation data array after taking the sum of every 3 points
    """
    shape = x.shape
    if axis < 0:
        axis += x.ndim
    shape = shape[:axis] + (-1, chunk_size) + shape[axis + 1 :]
    x = x.reshape(shape)
    return x.sum(axis=axis + 1)


def time_convert(year, month, day, hour, minute):
    """Compute the time in seconds since 01-01-1970. 
    """
    t = datetime.datetime(year, month, day, hour, minute)
    return (t - datetime.datetime(1970, 1, 1)).total_seconds()


# Function to filter out values greater than 0.2
def filter_prec(sat_data, obs_data, prec_cutoff_val):
    """generate new time series for sateliite data and observation data  when both the satellite data and observation data  has precipitation value greater than the prec_cutoof_val at the same time.
    """
    sat_data_filter = []
    obs_data_filter = []
    for a, b in zip(sat_data, obs_data):
        if a >= prec_cutoff_val and b >= prec_cutoff_val:
            sat_data_filter.append(a)
            obs_data_filter.append(b)

    sat_data_filter = np.asarray(sat_data_filter, dtype=np.float32)
    obs_data_filter = np.asarray(obs_data_filter, dtype=np.float32)
    return sat_data_filter, obs_data_filter

def rmse(x, x_obs):
    """Compute the root mean squared error of two data sets. 
    """
    return np.sqrt(np.mean(np.square(x - x_obs)))


def variance(data, ddof=0):
    """Compute the variance. 
    """
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data):
    """Compute the standard deviation. 
    """
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev