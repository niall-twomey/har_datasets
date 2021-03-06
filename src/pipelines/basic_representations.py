from src.features import ecdf
from src.features import statistical_features
from src.transformers import body_grav_filter
from src.transformers import resample
from src.transformers import window
from src.utils.loaders import dataset_importer

__all__ = [
    "stat_feat",
    "ecdf_11",
    "ecdf_21",
]


def dataset_windowed(name, fs_new=33, win_len=2.56, win_inc=1.0):
    dataset = dataset_importer(name)
    resampled = resample(parent=dataset, fs_new=fs_new)
    filtered = body_grav_filter(parent=resampled)
    windowed = window(parent=filtered, win_len=win_len, win_inc=win_inc)
    return windowed


def stat_feat(name):
    windowed = dataset_windowed(name)
    feats = statistical_features(parent=windowed)
    return feats


def ecdf_caller(name, n_components):
    windowed = dataset_windowed(name)
    feats = ecdf(parent=windowed, n_components=n_components)
    return feats


def ecdf_11(name):
    return ecdf_caller(name, 11)


def ecdf_21(name):
    return ecdf_caller(name, 21)
