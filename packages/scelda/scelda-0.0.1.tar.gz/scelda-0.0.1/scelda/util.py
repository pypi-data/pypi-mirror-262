import matplotlib.pyplot as plt
import muon as mu
import numpy as np
import os
import pyro
import random
import torch
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import NearestNeighbors

def set_seed(seed=9):
    """Initializes uniform random number generators.

    Parameters
    ----------
        seed : int, default=9
            Optional.
            Value to be used for all random number generation.

    Returns
    -------
        None
    """

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    pyro.set_rng_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

def map_labels(X_labels, Y_labels):
    """Maps predicted clustering labels to the given ground truth using linear
    sum assignment.
    
    Parameters
    ----------
        X_labels : numpy.ndarray, shape=(n_samples,)
            Ground truth cluster labels.
        Y_labels : numpy.ndarray, shape=(n_samples,)
            Predicted cluster labels.

    Returns
    -------
        labels : numpy.ndarray, shape=(n_samples,)
            TODO
    """

    scores = confusion_matrix(Y_labels, X_labels)
    row, col = linear_sum_assignment(scores, maximize=True)
    labels = np.zeros_like(X_labels)

    for i in row:
        labels[Y_labels == i] = col[i]

    return labels

def get_spatial(mdata, spatial_key='spatial', modality_key='morphological'):
    """TODO
    
    Parameters
    ----------
        mdata : TODO
            TODO
        spatial_key : str, default='spatial'
            Optional.
            TODO
        modality_key : str, default='physical'
            Optional.
            TODO
    
    Returns
    -------
        x : numpy.ndarray, shape=(n_samples,)
            TODO
        y : numpy.ndarray, shape=(n_samples,)
            TODO
    """

    try:
        x, y = mdata[modality_key].obsm[spatial_key].T
    except KeyError:
        x, y = mdata.obsm[spatial_key].T

    return x, y
    
def get_features(mdata, feature_key='protein', imagenet_key='imagenet'):
    """TODO

    Parameters
    ----------
        mdata : TODO
            TODO
        feature_key : str, default='protein'
            Optional.
            TODO
        imagenet_key : str, default='imagenet'
            Optional.
            TODO
    
    Returns
    -------
        features : numpy.ndarray, shape=(n_samples, n_features)
            TODO
    """

    try:
        features = mdata[feature_key].X
    except KeyError:
        features = mdata.X

    if imagenet_key:
        imagenet = mdata[imagenet_key].X
        features = np.hstack([features, imagenet])

    return features
    
def get_labels(mdata, label_key='celltype', modality_key='protein'):
    """TODO
    
    Parameters
    ----------
        mdata : TODO
            TODO
        label_key : str, default='celltype'
            Optional.
            TODO
        modality_key : str, default='protein'
            Optional.
            TODO

    Returns
    -------
        labels : numpy.ndarray, shape=(n_samples,)
            TODO
    """
    
    try:
        labels = mdata[modality_key].obs[label_key]
    except KeyError:
        labels = mdata.obs[label_key]

    return labels

def remove_lonely(data, labels, n_neighbors=12, threshold=225.):
    """Filters out samples that are too far removed from the data of interest
    according to the given threshold.

    Parameters
    ----------
        data : numpy.ndarray, shape=(n_samples, n_features)
            Collection of samples to be filtered.
        labels : numpy.ndarray, shape=(n_samples,)
            Component labels for each sample.
        n_neighbors : int, default=12
            Optional.
            TODO
        threshold : float, default=225.0
            Optional.
            TODO

    Returns
    -------
        data : numpy.ndarray, shape=(n_samples, n_features)
            TODO
        labels : numpy.ndarray, shape=(n_samples,)
            TODO
    """

    knn = NearestNeighbors(n_neighbors=n_neighbors).fit(data[:, :2])
    max_dist = knn.kneighbors()[0].max(-1)
    mask_idx, = np.where(max_dist > threshold)
    data = np.delete(data, mask_idx, axis=0)
    labels = np.delete(labels, mask_idx, axis=0)

    return data, labels

def read_anndata(filename, spatial_key='spatial', feature_key='protein', spatial_modality='morphological', imagenet_key='imagenet', label_key='celltype', label_modality='protein', n_neighbors=12, threshold=225., delineate=True, tensor=False):
    """Reads the specified annotated data object according to the format used by
    the NYGC Technology Innovation Laboratory.
    
    Parameters
    ----------
        filename : str
            TODO
        spatial_key : str, default='spatial'
            Optional.
            TODO
        spatial_modality : str, default='morphological'
            Optional.
            TODO
        feature_key : str, default='protein'
            Optional.
            TODO
        imagenet_key : str, default='imagenet'
            Optional.
            TODO
        label_key : str, default='protein:celltype'
            Optional.
            TODO
        label_modality : str, default='protein'
            Optional.
            TODO
        n_neighbors : int, default=12
            Optional.
            TODO
        threshold : float, default=225.0
            Optional.
            TODO
        delineate : bool, default=True
            Optional.
            TODO
        tensor : bool, default=False
            Optional.
            TODO

    Returns
    -------
        data : numpy.ndarray|torch.Tensor, shape=(n_samples, n_features)
            TODO
        labels : numpy.ndarray|torch.Tensor, shape=(n_samples,)
            TODO
    """

    mdata = mu.read(filename)
    x, y = get_spatial(mdata, spatial_key, spatial_modality)
    features = get_features(mdata, feature_key, imagenet_key)
    data = np.hstack([x[None].T, y[None].T, features])
    labels = get_labels(mdata, label_key, label_modality)
    _, labels = np.unique(labels, return_inverse=True)

    if threshold is not None:
        data, labels = remove_lonely(data, labels, n_neighbors, threshold)

    if delineate:
        data = np.hstack([np.zeros((data.shape[0], 1)), data])

    if tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    return data, labels

def read_anndatas(filenames, spatial_key='spatial', spatial_modality='morphological', feature_key='protein', imagenet_key='imagenet', label_key='celltype', label_modality='protein', n_neighbors=12, threshold=225., delineate=False, tensor=False):
    """Reads the specified annotated data object according to the format used by
    the NYGC Technology Innovation Laboratory.
    
    Parameters
    ----------
        filenames : list
            TODO
        spatial_key : str, default='spatial'
            Optional.
            TODO
        spatial_modality : str, default='morphological'
            Optional.
            TODO
        feature_key : str, default='protein'
            Optional.
            TODO
        imagenet_key : str, default='imagenet'
            Optional.
            TODO
        label_key : str, default='celltype'
            Optional.
            TODO
        label_modality : str, default='protein'
            Optional.
            TODO
        n_neighbors : int, default=12
            Optional.
            TODO
        threshold : float, default=225.0
            Optional.
            TODO
        delineate : bool, default=False
            Optional.
            TODO
        tensor : bool, default=False
            Optional.
            TODO

    Returns
    -------
        data : numpy.ndarray|torch.Tensor, shape=(n_samples, n_features)
            TODO
        labels : numpy.ndarray|torch.Tensor, shape=(n_samples,)
            TODO
    """

    data, labels = [], []

    for i, filename in enumerate(filenames):
        mdata = mu.read(filename)
        x, y = get_spatial(mdata, spatial_key, spatial_modality)
        features = get_features(mdata, feature_key, imagenet_key)
        data_i = np.hstack([x[None].T, y[None].T, features])
        labels_i = get_labels(mdata, label_key, label_modality)
        _, labels_i = np.unique(labels_i, return_inverse=True)

        if threshold is not None:
            data_i, labels_i = remove_lonely(data_i, labels_i, n_neighbors, threshold)

        data.append(np.hstack([i*np.ones((data_i.shape[0], 1)), data_i]))
        labels.append(labels_i)

    data, labels = np.vstack(data), np.hstack(labels)

    if tensor:
        return torch.tensor(data, dtype=torch.float32), torch.tensor(labels, dtype=torch.int32)
    return data, labels

def itemize(n, *items):
    """TODO
    
    Parameters
    ----------
        n : int
            TODO
        items : object
            TODO
    
    Yields
    ------
        items : tuple, shape=(n,)
            TODO
    """

    for i in items:
        yield i if isinstance(i, (list, tuple)) else (i,)*n

def format(ax, aspect='equal', show_ax=True):
    """TODO
    
    Parameters
    ----------
        ax : matplotlib.axis
            TODO
        aspect : str, default='equal'
            Optional.
            TODO
        show_ax : bool, default=True
            Optional.
            TODO

    Returns
    -------
        ax : matplotlib.axis
            TODO
    """

    ax.set_aspect(aspect)
    
    if not show_ax:
        ax.axis('off')

    return ax

def show_dataset(locs, labels, size=15, figsize=5, show_ax=True, colormap='tab10', filename=None):
    """TODO
    
    Parameters
    ----------
        locs : numpy.ndarray, shape=(n_samples, 2)
            TODO
        labels : numpy.ndarray, shape=(n_samples,)
            TODO
        size : int, default=15
            Optional.
            TODO
        show_ax : bool, default=True
            Optional.
            TODO
        figsize : int, default=10
            Optional.
            TODO
        colormap : str, default='tab20'
            Optional.
            TODO
        filename : str, default=None
            Optional.
            TODO

    Returns
    -------
        None
    """

    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(figsize=figsize)
    locs = locs[:, -2:].T
    color = plt.colormaps[colormap](labels)
    ax.scatter(*locs, s=size, c=color)
    ax = format(ax, aspect='equal', show_ax=show_ax)

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')

def show_datasets(locs, labels, size=15, figsize=10, show_ax=True, colormap='tab10', filename=None):
    """TODO
    
    Parameters
    ----------
        locs : numpy.ndarray, shape=(n_samples, 3)
            TODO
        labels : numpy.ndarray, shape=(n_samples,)
            TODO
        size : int, default=15
            Optional.
            TODO
        figsize : int, default=10
            Optional.
            TODO
        show_ax : bool, default=True
            Optional.
            TODO
        colormap : str, default='tab20'
            Optional.
            TODO
        filename : str, default=None
            Optional.
            TODO

    Returns
    -------
        TODO
    """
    
    n_datasets = np.unique(locs[:, 0]).shape[0]
    size, = itemize(n_datasets, size)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_datasets, figsize=figsize)
    axes = (ax,) if n_datasets == 1 else ax

    for i in range(n_datasets):
        idx = locs[:, 0].astype(np.int32) == i
        idx_locs = locs[idx, -2:].T
        color = plt.colormaps[colormap](labels[idx])
        axes[i].scatter(*idx_locs, s=size[i], c=color)
        format(axes[i], aspect='equal', show_ax=show_ax)

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')

    return fig, axes

def show_logs(*logs, size=15, figsize=10, show_ax=True, filename=None):
    """TODO
    
    Parameters
    ----------
        logs : tuple, shape=(n_logs,)
            TODO
        size : int, default=15
            Optional.
            TODO
        figsize : int, default=10
            Optional.
            TODO
        show_ax : bool, default=True
            Optional.
            TODO
        filename : str, default=None
            Optional.
            TODO

    Returns
    -------
        TODO
    """

    n_logs = len(logs)
    size, = itemize(n_logs, size)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_logs, figsize=figsize)
    axes = (ax,) if n_logs == 1 else ax

    for idx, log in enumerate(logs):
        x = np.arange(len(log))
        axes[idx].plot(x, log)
        format(axes[idx], aspect='equal', show_ax=show_ax)

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')

    return fig, axes

def show_logs(*logs, figsize=5, show_ax=True, filename=None):
    """TODO
    
    Parameters
    ----------
        logs : tuple, shape=(n_logs,)
            TODO
        figsize : int, default=10
            Optional.
            TODO
        show_ax : bool, default=True
            Optional.
            TODO
        filename : str, default=None
            Optional.
            TODO

    Returns
    -------
        TODO
    """

    n_logs = len(logs)
    figsize, = itemize(2, figsize)
    fig, ax = plt.subplots(1, n_logs, figsize=figsize)
    axes = (ax,) if n_logs == 1 else ax

    for idx, log in enumerate(logs):
        if len(log) == 2:
            axes[idx].set_title(log[0])
            log = log[1]

        x = np.arange(len(log))
        axes[idx].plot(x, log)
        axes[idx].set_box_aspect(1)

        if not show_ax:
            axes[idx].tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

    if filename is not None:
        fig.savefig(filename, bbox_inches='tight')

    return fig, axes
