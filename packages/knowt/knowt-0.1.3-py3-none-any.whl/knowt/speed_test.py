# timeit_benchmark.py
"""
>>> import numpy as np
... shape = (41531, 384)
... mmvecs = np.memmap('.knowt-data/corpus_hpr/sentences.embeddings.memmap', shape=shape, mode='r', dtype=np.float32)
>>> mmvecs
memmap([[-0.11991242, -0.01196034, -0.07994116, ...,  0.03639957,
          0.02800957, -0.01285664],
        ...,
        [ 0.00590789, -0.03429353,  0.06170199, ..., -0.02477657,
          0.01814286, -0.06049331]], dtype=float32)
>>> np.random.seed(1)
>>> v = np.random.randn(1, 384)
>>> from timeit import timeit
>>> mmvecs = mmvecs.T

>>> variables = dict(np=np, v=v, mmvecs=mmvecs)
>>> timeit(
...     'v.dot(mmvecs)',
...     globals=variables,
...     number=20)
0.6553003459994216
>>> timeit('v.dot(mmvecs)', globals=variables, number=1)
0.027156211001056363
>>> timeit.timeit('v.dot(mmvecs)', globals=dict(np=np, v=v, mmvecs=mmvecs), number=10)
0.31012663599904045
"""
import numpy as np
from timeit import timeit

np.random.seed(1)
v = np.random.randn(1, 384)

shape = (41531, 384)
mmvecs = np.memmap(
    '.knowt-data/sentences.embeddings.memmap',
    shape=shape,
    dtype=np.float32,
    mode='r')
variables = dict(np=np, v=v, vecs=mmvecs.T)

print('Running vectorized dot product on memmap file 1, 10, 20 times:')
timeit('v.dot(vecs)', globals=variables, number=1)
# 0.027156211001056363
timeit('v.dot(vecs)', globals=variables, number=10)
# 0.31012663599904045
dt_vectorized = timeit('v.dot(vecs)', globals=variables, number=20)
# 0.6553003459994216
print(f"dt_vectorized: {dt_vectorized}")


def do_dots():
    answers = np.zeros(shape[0])
    for i, vec in enumerate(vecs):
        answers[i] = sum((x1 * x2 for (x1, x2) in zip(v[0], vec)))
    return answers


print('Running for loop to calculate dot products 1, 10, 20 times:')
variables = dict(np=np, do_dots=do_dots, vecs=mmvecs, v=v)
print(timeit('do_dots()', globals=variables, number=1))
# 0.10109178899983817
timeit('do_dots()', globals=variables, number=10)
# 0.9936741420006001
dt_loop = timeit('do_dots()', globals=variables, number=20)
print(f"dt_loop: {dt_loop}")
# 1.961482011998669
print(f"dt_loop / dt_vectorized: {dt_loop / dt_vectorized}")
# 2.9932564876143073


print('Running vectorized dot product in RAM 1, 10, 20 times:')
vecs = np.array(mmvecs.T.copy().tolist())
variables = dict(vecs=vecs, v=v)
timeit('v.dot(vecs)', globals=variables, number=1)
# 0.0035433259999990696
timeit('v.dot(vecs)', globals=variables, number=10)
# 0.036666362000687514
dt_ram = timeit('v.dot(vecs)', globals=variables, number=20)
print(f"dt_ram: {dt_ram}")
# dt_ram: 0.10634478099927946
print(f"dt_vectorized / dt_ram: {dt_vectorized / dt_ram}")
# dt_vectorized / dt_ram: 5.91667026898266


def do_dots_ram():
    answers = np.zeros(shape[0])
    for i, vec in enumerate(vecs):
        answers[i] = sum((x1 * x2 for (x1, x2) in zip(v[0], vec)))
    return answers


print('Running for loop to calculate dot products 1, 10, 20 times:')
variables = dict(np=np, do_dots_ram=do_dots_ram, vecs=vecs.T, v=v)
print(timeit('do_dots_ram()', globals=variables, number=1))
# 0.07124039900008938
print(timeit('do_dots_ram()', globals=variables, number=10))
# 0.346967797000616
dt_loop_ram = timeit('do_dots_ram()', globals=variables, number=20)
print(f"dt_loop_ram: {dt_loop_ram}")
# dt_loop_ram: 0.671586558000854
print(f"dt_loop_ram / dt_vectorized: {dt_loop_ram / dt_ram}")
# dt_loop_ram / dt_vectorized: 6.315181165358781
