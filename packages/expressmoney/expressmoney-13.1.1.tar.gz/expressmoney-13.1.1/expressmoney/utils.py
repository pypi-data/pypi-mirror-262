__all__ = ('timeit', 'get')

import time


def timeit(method):
    def wrapper(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return wrapper


def get(service: str, path: str, point_filter: str = None, read_pages: int = 1) -> list:
    from expressmoney.requests import Request
    data = list()
    pages_readed = 0
    next_page_is_exists = True
    while next_page_is_exists and (pages_readed < read_pages or read_pages == 0):
        page_path = f'{path}?page={pages_readed + 1}'
        if point_filter is not None:
            page_path = f'{page_path}&{point_filter}'
        response = Request(service=service, path=page_path).get()
        page_data = response.json().get('results')
        next_page_is_exists = True if response.json().get('next') is not None else False
        if page_data:
            data.extend(page_data)
        pages_readed += 1
    return data
