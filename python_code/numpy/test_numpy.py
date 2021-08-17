import numpy as np


def create_matrix_2d_with_element_list():
    """List objects are mutable, so you're actually making a list with 12 references to one list.
     Use a list comprehension and make 12 distinct lists:
     https://stackoverflow.com/questions/17225694/python-appending-a-value-to-a-sublist"""
    # matrix = [[[]] * 9] * 9
    matrix = [[[] for i in range(9)] for j in range(9)]
    print(matrix)


def np_where_2d_input():
    all_ious = [[0, 0],
                [0, 0.96958],
                [0, 0],
                [0.94382, 0]]
    want_idx = np.where(np.array(all_ious) > 0.5)
    print(want_idx)
    # out want_idx = (array([1, 3]), array([1, 0]))


def test_filter_function():
    all_matches = np.array([
        np.array([0, 2, 0.9]),
        np.array([0, 1, 0.8]),
        np.array([1, 1, 0.9]),
        np.array([1, 2, 0.5]),
        np.array([0, 3, 0.5]),
    ])

    all_matches = all_matches[all_matches[:, 2].argsort()[::-1]]

    all_matches = all_matches[np.unique(all_matches[:, 1], return_index=True)[1]]

    all_matches = all_matches[all_matches[:, 2].argsort()[::-1]]

    all_matches = all_matches[np.unique(all_matches[:, 0], return_index=True)[1]]
    print(all_matches)


def test_np_unique():
    a = [1, 2, 6, 4, 2, 3, 2]
    u, indices = np.unique(a, return_inverse=True)
    print(u)
    print(indices)


def test_intersect1d():
    a = [1, 2, 3, 4, 5]
    b = [1, 2, 4, 3, 6, 7]
    c = np.intersect1d(a, b)
    print(c)


def test_setdiff1d():
    a = [1, 2, 3, 4, 5]
    b = [1, 2, 4, 3, 6, 7]
    c = np.setdiff1d(a, b)
    d = np.setdiff1d(b, a)
    print(c)
    print(d)


def test_cumsum():
    a = [1, 2, 3, 4, 5]
    # output [ 1  3  6 10 15]
    b = np.cumsum(a)
    print(b)


def test_np_diff():
    a = [1, 2, 4, 7, 0]
    # out [ 1  2  3 -7]
    b = np.diff(a, n=2)
    print(b)


def test_numpy_where():
    a = [1, 2, 4, 3, 6, 7]
    # out [0, 1, 3]
    b = np.where(np.array(a) < 4)
    print(np.array(a)[b])
    print(b)


def test():
    """
    Bài 1: a = [1, 2, 6, 4, 2, 3, 2] out =  [1 2 3 4 6]; [0 1 4 3 1 2 1]. Tìm những phần tử duy nhất, index
    Bài 2: a = [1, 2, 3, 4, 5]; b = [1, 2, 4, 3, 6, 7] out = [1 2 3 4]. Tìm phần tử giống nhau hai mảng
    Bài 3: a = [1, 2, 3, 4, 5]; b = [1, 2, 4, 3, 6, 7] out = [5], [6 7]. Tìm phần tử có trong a không có trong b, ngược lại.
    Bài 4: a = [1, 2, 3, 4, 5] out = [ 1  3  6 10 15]. Tính tổng tăng dần
    Bài 5: a = [1, 2, 4, 7, 0] out = [ 1  2  3 -7]. Tính độ khác nhau hai phần tử liên tiếp trong mảng.
    Bài 6: a = [1, 2, 4, 3, 6, 7] out = [0, 1, 3], [1 2 3], tìm  index,  phần tử < 4
    :return:
    """
    a = [1, 2, 3, 4, 5, 5, 7]
    b = [1, 2, 4, 3, 6, 7, 7]
    a = list(set(a))
    b = list(set(b))
    tronga = []
    for i in a:
        if i not in b:
            if i not in tronga:
                tronga.append(i)
        if i in b:
            b.remove(i)

    print(tronga, b)


if __name__ == '__main__':
    # test_filter_function()
    # np_where_2d_input()
    # create_matrix_2d_with_element_list()
    # test_np_unique()
    # test_intersect1d()
    # test_setdiff1d()
    # test_cumsum()
    # test_np_diff()
    # test_numpy_where()
    test()