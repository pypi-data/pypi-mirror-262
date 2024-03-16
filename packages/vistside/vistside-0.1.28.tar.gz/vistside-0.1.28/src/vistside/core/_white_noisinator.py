"""WhiteNoisinator class creates white noise"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import numpy as np
from icecream import ic

ic.configureOutput(includeContext=True)


def generateWhiteNoise(sample_length, fs) -> np.ndarray:
  """
  Generates white noise using Inverse Fourier Transform.

  Args:
      sample_length: The desired length of the white noise signal.
      fs: The sampling frequency.

  Returns:
      A NumPy array containing the white noise signal.
  """

  # Create random phases with uniform distribution
  phases = np.random.rand(sample_length) * 2 * np.pi

  # Constant amplitude spectrum
  amplitude = np.ones(sample_length)

  # Combine phases and amplitude
  spectrum = amplitude * np.exp(1j * phases)

  # Perform inverse Fourier Transform (IFFT)

  # Normalize the signal (optional)
  # white_noise = white_noise / np.std(white_noise)

  return np.real(np.fft.ifft(spectrum))


def linearInterpolation(x1, x2, y1, y2, x) -> np.ndarray | float:
  """Performs linear interpolation between two points."""
  return y1 + (x - x1) * (y2 - y1) / (x2 - x1)


def interpolateWhiteNoise(desired_length,
                          fs,
                          initial_sample_length=1000) -> np.ndarray:
  """
  Generates white noise and interpolates to a longer signal length.

  Args:
      desired_length: The desired length of the final white noise signal.
      fs: The sampling frequency.
      initial_sample_length: The number of samples for the initial white
      noise generation.

  Returns:
      A NumPy array containing the interpolated white noise signal.
  """

  # Generate initial white noise
  initNoise = generateWhiteNoise(initial_sample_length, fs)
  thisNoise = initNoise[~np.isnan(initNoise)]

  # Define interpolation function (choose your preferred method)

  # Upsample to desired length
  thisNoise = np.zeros(desired_length)
  for i in range(desired_length - 1):
    x = i / (desired_length - 1) * (
        initial_sample_length - 1)  # Scaled x value
    x1 = int(np.floor(x))
    x2 = int(np.ceil(x))
    y1 = initNoise[x1]
    y2 = initNoise[x2]
    thisNoise[i] = linearInterpolation(x1, x2, y1, y2, x)

  thisNoise[-1] = initNoise[-1]  # Set the last element directly
  # Normalize the signal
  ic(np.min(thisNoise), np.max(thisNoise))
  return thisNoise[~np.isnan(thisNoise)]

#
# # Example usage
# fs = 1000  # Sampling frequency
# desired_length = 10000  # Desired length of the final signal
#
# long_noise = generate_and_interpolate_white_noise(desired_length, fs)
#
# # Further processing (optional)
