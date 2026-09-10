"""Shared pagination helper for management pages."""

import math

from streamlit_extras.pagination import pagination


PAGE_SIZE = 6


def paginate_items(items: list[dict], key: str, page_size: int = PAGE_SIZE) -> list[dict]:
    """Return the records belonging to the current page.

    Pagination is only displayed when the number of records is greater than
    one page, keeping short lists visually simple.
    """
    if len(items) <= page_size:
        return items

    total_pages = math.ceil(len(items) / page_size)
    page = pagination(num_pages=total_pages, key=key, width="stretch")
    start = (page - 1) * page_size
    return items[start : start + page_size]
