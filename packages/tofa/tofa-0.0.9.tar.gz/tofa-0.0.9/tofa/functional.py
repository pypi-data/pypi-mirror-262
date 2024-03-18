"""Common useful functional subroutines.

There are potentially more useful functional primitives.
But here are included that are mostly used in prototyping and writing data loaders.
"""
import collections
from functools import partial, reduce
import itertools

Collection = (list, tuple, set, frozenset)
Mapping = (dict, collections.abc.Mapping)


# todo: tests


def accepts_collection(fn):
    """If iterator is passed to decorated function then result will be iterator,
    otherwise result will be of the same type as input collection."""

    def wrapper(arg, input, *args, return_iter=False, return_list=False, **kwargs):
        result_iter = fn(arg, input, *args, **kwargs)
        if return_iter:
            return result_iter
        if return_list:
            return list(result_iter)
        if isinstance(input, Collection):
            return type(input)(result_iter)
        return result_iter

    return wrapper


def accepts_collection_flip(fn):
    # todo:
    pass


# todo: maybe there is better name?
# candidates: map_, lmap, transform, value_map, ...
# same for filter
list_map = accepts_collection(map)


def key_map(mapping, fn):
    keys = list_map(mapping.keys(), fn)
    values = mapping.values()
    return type(mapping)(zip(keys, values))


def value_map(mapping, fn):
    keys = mapping.keys()
    values = list_map(mapping.values(), fn)
    return type(mapping)(zip(keys, values))


@accepts_collection
def map_index(iterable, index):
    return (item[index] for item in iterable)


def inverse_mapping(input):
    mapping_type = type(input)
    if isinstance(input, Collection):
        mapping_type = dict
        items = enumerate(input)
    else:
        items = input.items()
    return mapping_type((v, k) for k, v in items)


list_filter = accepts_collection(filter)
filter_false = accepts_collection(itertools.filterfalse)
take_while = accepts_collection(itertools.takewhile)
drop_while = accepts_collection(itertools.dropwhile)


def fold(reducer, collection, initial=None):
    return reduce(reducer, collection, initial)


@accepts_collection
def scan(reducer, collection, initial=None):
    # itertools.accumulate does not accepts initial value for python < 3.8
    if initial is None:
        initial, collection = head_tail(collection, return_iter=True)
    accumulator = initial
    for item in collection:
        accumulator = reducer(accumulator, item)
        yield accumulator


def first(iterable):
    return first(iter(iterable))


@accepts_collection
def take(n, iterable):
    return itertools.islice(iterable, n)


@accepts_collection
def drop(n, iterable):
    return itertools.islice(iterable, n, None)


def last(iterable):
    if isinstance(iterable, Collection):
        return iterable[-1]
    x = None
    for item in iterable:
        x = item
    return x


def take_last(n, iterable):
    if isinstance(iterable, Collection):
        return iterable[-n:]
    return iter(collections.deque(iterable, maxlen=n))


@accepts_collection
def drop_last(n, iterable):
    if isinstance(iterable, Collection):
        return iterable[:-n]
    return (item for item, _ in zip(iterable, drop(iterable, n)))


def get_nth(n, iterable):
    return next(itertools.islice(iterable, n, None))


head = first
tail = rest = partial(drop, n=1)


def head_tail(iterable, return_iter=False):
    head = first(iterable)
    tail = drop(iterable, 1, return_iter=return_iter)
    return head, tail


def split_at(n, iterable, return_iter=False):
    front = take(iterable, n, return_iter=return_iter)
    back = drop(iterable, n, return_iter=return_iter)
    return front, back


def consume(iter, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # from: https://docs.python.org/3/library/itertools.html#itertools-recipes
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iter, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iter, n, n), None)


@accepts_collection_flip
def flatten_once(iterable):
    return (item for sublist in iterable for item in sublist)


@accepts_collection_flip
def flatten_nested(iterable):
    for item in iterable:
        if isinstance(item, Collection):
            yield from flatten_nested(item)
        else:
            yield item


def sliding_window(iterable, n):
    # from: https://docs.python.org/3/library/itertools.html#itertools-recipes
    it = iter(iter)
    window = collections.deque(itertools.islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield window


def batched(iterable, n, drop_last=False):
    assert n > 0
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == n:
            yield batch
            batch = []
    if not drop_last and batch:
        yield batch


def group_by(iter, predicate):
    results = {}
    for item in iter:
        key = predicate(item)
        results.setdefault(key, []).append(item)


def partition(iter, predicate):
    results = [], []
    for item in iter:
        results[bool(predicate(item))].append(item)
    return results
