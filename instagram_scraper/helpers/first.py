def first(iterable, func=lambda L: L is not None, **kwargs):
    it = (el for el in iterable if func(el))

    if 'default' in kwargs:
        return next(it, kwargs['default'])

    try:
        return next(it)
    except StopIteration:
        return None

