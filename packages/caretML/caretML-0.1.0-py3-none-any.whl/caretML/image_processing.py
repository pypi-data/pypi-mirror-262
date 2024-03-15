import numpy as np
from skimage.filters import canny
from skimage.morphology import binary_erosion, binary_dilation, disk
from skimage.filters import threshold_otsu, threshold_local
from scipy.signal import convolve2d
from numba import njit, prange

@njit(parallel=True)
def gaussian_noise(shape, mean=0, std=1):
    """Generate Gaussian noise with given shape, mean, and standard deviation."""
    return np.random.normal(mean, std, shape)

@njit(parallel=True)
def salt_and_pepper_noise(image, salt_prob=0.05, pepper_prob=0.05):
    """Apply salt-and-pepper noise to an image."""
    noisy_image = np.copy(image)
    salt = np.random.random(image.shape) < salt_prob
    pepper = np.random.random(image.shape) < pepper_prob
    noisy_image[salt] = 1
    noisy_image[pepper] = 0
    return noisy_image

def bilateral_filter(image, sigma_spatial=1, sigma_range=1):
    """Apply bilateral filter to an image."""
    from skimage.restoration import denoise_bilateral
    return denoise_bilateral(image, sigma_color=sigma_range, sigma_spatial=sigma_spatial)

def hough_transform(image, theta_resolution=1, rho_resolution=1):
    """Perform Hough transform on an edge-detected image."""
    from skimage.transform import hough_line
    edges = canny(image)
    h, theta, rho = hough_line(edges, theta=np.linspace(-np.pi / 2, np.pi / 2, theta_resolution),rho=np.arange(-np.max(image.shape), np.max(image.shape), rho_resolution))
    return h, theta, rho

def morphological_opening(image, selem_size=3):
    """Perform morphological opening on a binary image."""
    selem = disk(selem_size)
    return binary_erosion(binary_dilation(image, selem=selem), selem=selem)

def local_thresholding(image, block_size=51, method='gaussian'):
    """Perform local thresholding on an image."""
    if method == 'otsu':
        global_thresh = threshold_otsu(image)
    elif method == 'local':
        global_thresh = threshold_local(image, block_size, method='gaussian', mode='reflect')
    else:
        raise ValueError("Unsupported thresholding method. Choose 'otsu' or 'local'.")
    return image > global_thresh

def erosion(image, selem_size=3):
    """Perform binary erosion on an image."""
    selem = disk(selem_size)
    return binary_erosion(image, selem=selem)

def dilation(image, selem_size=3):
    """Perform binary dilation on an image."""
    selem = disk(selem_size)
    return binary_dilation(image, selem=selem)

def closing(image, selem_size=3):
    """Perform morphological closing on a binary image."""
    selem = disk(selem_size)
    return binary_dilation(binary_erosion(image, selem=selem), selem=selem)

@njit(parallel=True)
def sparse_matrix_multiplication(matrix1, matrix2):
    """
    Perform multiplication of two sparse matrices.

    Parameters:
        matrix1 (scipy.sparse matrix): First sparse matrix.
        matrix2 (scipy.sparse matrix): Second sparse matrix.

    Returns:
        scipy.sparse matrix: Result of the multiplication.
    """
    from scipy.sparse import csr_matrix
    return csr_matrix.dot(matrix1, matrix2)

@njit
def dynamic_time_warping(sequence1, sequence2, distance_function):
    """
    Perform dynamic time warping (DTW) between two sequences.

    Parameters:
        sequence1 (array_like): First sequence.
        sequence2 (array_like): Second sequence.
        distance_function (callable): Function to compute distance between elements of sequences.

    Returns:
        float: DTW distance between the two sequences.
    """
    n, m = len(sequence1), len(sequence2)
    dp = np.zeros((n + 1, m + 1))
    dp[0, 0] = 0
    for i in range(1, n + 1):
        dp[i, 0] = np.inf
    for j in range(1, m + 1):
        dp[0, j] = np.inf
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = distance_function(sequence1[i - 1], sequence2[j - 1])
            dp[i, j] = cost + min(dp[i - 1, j], dp[i, j - 1], dp[i - 1, j - 1])
    return dp[n, m]

@njit
def dynamic_programming(sequence1, sequence2, cost_function):
    """
    Perform dynamic programming to find the optimal alignment between two sequences.

    Parameters:
        sequence1 (array_like): First sequence.
        sequence2 (array_like): Second sequence.
        cost_function (callable): Function to compute cost of aligning two elements of sequences.

    Returns:
        list: List of tuples representing the optimal alignment.
    """
    n, m = len(sequence1), len(sequence2)
    dp = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        dp[i, 0] = i * cost_function(sequence1[i - 1], None)
    for j in range(1, m + 1):
        dp[0, j] = j * cost_function(None, sequence2[j - 1])
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = cost_function(sequence1[i - 1], sequence2[j - 1])
            dp[i, j] = cost + min(dp[i - 1, j], dp[i, j - 1], dp[i - 1, j - 1])
    alignment = []
    i, j = n, m
    while i > 0 and j > 0:
        if dp[i, j] == dp[i - 1, j - 1] + cost_function(sequence1[i - 1], sequence2[j - 1]):
            alignment.append((sequence1[i - 1], sequence2[j - 1]))
            i -= 1
            j -= 1
        elif dp[i, j] == dp[i - 1, j] + cost_function(sequence1[i - 1], None):
            alignment.append((sequence1[i - 1], None))
            i -= 1
        else:
            alignment.append((None, sequence2[j - 1]))
            j -= 1
    while i > 0:
        alignment.append((sequence1[i - 1], None))
        i -= 1
    while j > 0:
        alignment.append((None, sequence2[j - 1]))
        j -= 1
    return alignment[::-1]
