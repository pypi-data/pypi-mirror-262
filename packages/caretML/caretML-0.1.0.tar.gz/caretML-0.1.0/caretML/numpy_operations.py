import numpy as np

def matrix_multiply(a, b):
    """
    Perform matrix multiplication.

    Parameters:
        a (ndarray): First matrix.
        b (ndarray): Second matrix.

    Returns:
        ndarray: Result of matrix multiplication.
    """
    if a.shape[1] != b.shape[0]:
        raise ValueError("Matrix dimensions are not compatible for multiplication.")
    result = np.zeros((a.shape[0], b.shape[1]))
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            for k in range(a.shape[1]):
                result[i, j] += a[i, k] * b[k, j]
    return result

def matrix_inverse(matrix):
    """
    Compute the inverse of a matrix.

    Parameters:
        matrix (ndarray): Input matrix.

    Returns:
        ndarray: Inverse of the input matrix.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Input matrix must be square.")
    determinant = np.linalg.det(matrix)
    if determinant == 0:
        raise ValueError("Matrix is singular, cannot compute inverse.")
    adjugate = np.linalg.inv(matrix)
    return adjugate / determinant

def svd(matrix):
    """
    Perform Singular Value Decomposition (SVD) on a matrix.

    Parameters:
        matrix (ndarray): Input matrix.

    Returns:
        tuple: Tuple containing U, S, and V^T matrices.
    """
    if matrix.shape[0] < matrix.shape[1]:
        raise ValueError("SVD requires a matrix with more rows than columns.")
    if np.linalg.matrix_rank(matrix) < min(matrix.shape):
        raise ValueError("Matrix is not full rank, SVD cannot be computed.")
    m, n = matrix.shape
    u = np.zeros((m, m))
    s = np.zeros((m, n))
    v_transpose = np.zeros((n, n))
    eig_vals, eig_vecs = np.linalg.eig(matrix @ matrix.T)
    eig_vals_sorted_indices = np.argsort(eig_vals)[::-1]
    for i in range(m):
        u[:, i] = eig_vecs[:, eig_vals_sorted_indices[i]]
    u = u[:, :n]
    s_diag = np.sqrt(np.abs(eig_vals[eig_vals_sorted_indices[:n]]))
    np.fill_diagonal(s, s_diag)
    v = matrix.T @ u / s_diag
    return u, s, v.T

# Add more advanced numpy operations below
