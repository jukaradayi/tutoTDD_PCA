""" Compute PCA Transform on data stored in CSV format 
"""

import os
import ipdb
import argparse
import numpy as np


def generate_data(dim1, dim2):
    """Generate Random Data with size dim1 x dim2.
    Data are store in a numpy array
    """
    mat = np.random.rand(dim1, dim2)
    return mat


def read_csv_data(data_path):
    """ Read input data stored as csv

        Parameters
        ----------
        data_path : str
            path to the input .csv file.
            expecting data to be float without NaN.

        Returns
        -------
        np.array
            input data stored in numpy array
        
        Raises
        ------
        FileNotFoundError
            wrong data_path
    """
    if not os.path.isfile(data_path):
        raise FileNotFoundError(f'{data_path} file does not exist')

    # read csv input
    with open(data_path, 'r') as fin:
        mat = []
        for line_idx, line in enumerate(fin.readlines()):
            # skip header
            if line_idx == 0:
                continue
            row = line.strip().split(',')

            # store data as float
            mat.append([float(val) for val in row])

    return np.array(mat)

def substract_mean(mat):
    """Compute the mean over all the samples and substract it from the data
    See
    https://stackoverflow.com/questions/22053050/difference-between-numpy-array-shape-r-1-and-r

        Parameters
        ----------
        data : np.array
            dataset stored as a numpy array

        Returns 
        -------
        np.array
            dataset with zero mean
    """

    # Allocate array
    mu = np.zeros((mat.shape[1],))
    for row in mat:
        mu += row
    return mat - 1 / mat.shape[0] * mu


def get_covariance_matrix(centered_data):
    """ Compute the covariance matrix over the dataset
        The covariance matrix is computed as
            1/n_samples * (transpose(_mat) * _mat)
        where _mat is matrix data centered


        Parameters
        ----------
        data : np.array
            dataset stored as a numpy array.

        Returns
        -------
        np.array
            covariance matrix

        Raises
        ------
        AssertionError
            data has not been centered before computing covariance
    """

    dim1, _ = centered_data.shape
    return 1 / dim1 * np.matmul(np.transpose(centered_data), centered_data)


def eigenvectors(cov_mat):
    """ Compute eigenvectors on input dataset using numpy svd

        Parameters
        ----------
        cov_mat : np.array
            covariance matrix

        Returns
        -------
        2D np.array
            eigen vectors

        1D np.array
            eigen values
            
        Raises
        ------
        AssertionError
            cov_mat is not square matrix (wrong matrix ?)

    """

    # U, S, V = np.linalg.svd(cov_mat)
    e_vals, e_vecs = np.linalg.eig(cov_mat)

    return e_vals, e_vecs


def sort_values(e_vals, e_vecs):
    """ Sort eigen vectors and eigen values in decreasing order
        Select which dimensions to keep using some criterion
        (ex: threshold of how much data explained)
        TODO flip sign if negative ?

        Parameters
        ----------
        e_vals : np.array
            eigen values

        Returns
        -------
        1D np.array
            sorted index

    """

    index = np.flip(np.argsort(e_vals))

    # check if some values are negative ?
    for eigenval in e_vals:
        if eigenval < 0:
            print(eigenval)

    return index


def apply_transform(mat, e_vecs):
    """Apply transformation to input data"""
    # TODO : add number of components required 
    return np.matmul(mat, e_vecs)
def write_output():
    """Write transformed data"""

def whitening():
    """Make variance 1 along first component"""


def main():
    """Load input matrix or generate a random one,
    compute its covariance matrix, then compute its eigenvectors using numpy svd
    """
    parser = argparse.ArgumentParser(description='PCA')

    # input arguments
    parser.add_argument('-f', '--csv', type=str, 
            help='path to the input csv file')

    args = parser.parse_args()


    # read dataset 
    mat = read_csv_data(args.csv)

    # compute covariance matrix, its eigen vectors
    centered_data = substract_mean(mat)
    cov_mat = get_covariance_matrix(centered_data)
    e_val, e_vec = eigenvectors(cov_mat)

    # perform PCA
    projected_data = apply_transform(mat, e_vec)
    ipdb.set_trace()
if __name__ == "__main__":
    main()
