from __future__ import annotations

import dataclasses
import functools
from typing import Callable, Iterable

from . import collectible
from .common import T, U


def create(objects: Iterable[T]) -> Proq[T]:
    return Proq(objects)


@dataclasses.dataclass
class Proq(collectible.Collectible[T]):
    items: Iterable[T]

    def map(self, f: Callable[[T], U]) -> Proq[U]:
        return Proq(map(f, self.items))

    def foreach(self, f: Callable[[T], U]) -> Proq[T]:
        def _foreach(item: T) -> T:
            f(item)
            return item

        return self.map(_foreach)

    def filter(self, f: Callable[[T], bool]) -> Proq[T]:
        return Proq(filter(f, self.items))

    def reduce(self, f: Callable[[T, T], T], initial: T | None = None) -> Proq[T]:
        if initial is None:
            return Proq(functools.reduce(f, self.items) for _ in range(1))
        return Proq(functools.reduce(f, self.items, initial) for _ in range(1))

    def collect_iter(self) -> Iterable[T]:
        yield from self.items


# class ProqPool(Generic[T, U]):
#     def __init__(self, pool: mp.Pool | None = None):
#         self._pool = pool or mp.Pool()


# class Proq(Generic[T]):
#     def __init__(self, q: mp.Queue | None = None, pool: mp.Pool | None = None):
#         self._q = q or mp.Queue()
#         self._pool = pool | mp.Pool()


# def long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(a: str) -> str:
#     return a


# def main():
#     proq = Proq()
#     proq.create("abc").map(
#         lambda a: long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(
#             a.upper()
#         )
#     ).map(
#         lambda a: long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(
#             a.lower()
#         )
#     ).map(
#         lambda a: long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(
#             a.capitalize()
#         )
#     )
#     (
#         proq.create("abc")
#         | (
#             lambda a: long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(
#                 a.upper()
#             )
#         )
#         | (
#             lambda a: long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(
#                 a.lower()
#             )
#         )
#         | (
#             lambda a: long_function_name_to_see_what_happens_aaaaaaaaaaaaaaaaaaaaaaaa(
#                 a.capitalize()
#             )
#         )
#     )


# # multiply by 3, keep even, count
# p = proq.create([1,2,3,4,5]).map(lambda x: x * 3).filter(lambda x: x % 2 == 0).count()

# p.run()

# pipeline = proq.pipeline().map(lambda x: x * 3).filter(lambda x: x % 2 == 0).count()
# pipeline.process([1,2,3,4,5])
# pipeline.apply([1,2,3,4,5])

# proq.make([1,2,3,4,5]) | proq.map()... | ...

# a = proq.make([1,2,3,4,5])
# b = proq.make([1,2,3,4,5])
# proq.join(a, b)

# proq.process([1,2,3,4,5])
# proq.pipeline().map(lambda x: x * 3).filter(lambda x: x % 2 == 0).count())


# a, b = proq.create().map().filter().sum().tee()


# q = proq.create()
# q.map(...)
# proq.Proq(inp1, inp2)
