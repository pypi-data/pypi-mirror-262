from typing import Iterable, Protocol

from .common import T


class Collectible(Protocol[T]):
    def collect_iter(self) -> Iterable[T]:
        raise NotImplementedError(f"{self.__class__.__name__}.collect_iter()")

    def collect(self) -> list[T]:
        return list(self.collect_iter())

    def __iter__(self) -> Iterable[T]:
        return self.collect_iter()
