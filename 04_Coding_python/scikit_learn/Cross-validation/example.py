from sklearn.model_selection import StratifiedKFold, KFold, StratifiedShuffleSplit
import numpy as np

X, y = np.ones((50, 1)), np.hstack(([0] * 45, [1] * 5))


def make_stratified_k_fold():
    # skf = StratifiedKFold(n_splits=3)
    skf = StratifiedShuffleSplit(n_splits=3, test_size=0.5, random_state=0)
    for train, test in skf.split(X, y):
        print('train -  {}   |   test -  {}'.format(np.bincount(y[train]), np.bincount(y[test])))


def make_k_fold():
    kf = KFold(n_splits=3)
    for train, test in kf.split(X, y):
        print('train -  {}   |   test -  {}'.format(np.bincount(y[train]), np.bincount(y[test])))


if __name__ == '__main__':
    make_stratified_k_fold()
    print("---------------")
    make_k_fold()