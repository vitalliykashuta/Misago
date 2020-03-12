import pytest

from ..get import get_post_by_id, get_posts_by_id, get_thread_posts_page


@pytest.mark.asyncio
async def test_post_can_be_get_by_id(post):
    assert post == await get_post_by_id(post.id)


@pytest.mark.asyncio
async def test_getting_post_by_nonexistent_id_returns_none(db):
    assert await get_post_by_id(1) is None


@pytest.mark.asyncio
async def test_posts_can_be_get_by_id(post):
    assert [post] == await get_posts_by_id([post.id])


@pytest.mark.asyncio
async def test_getting_posts_by_nonexistent_id_returns_empty_list(db):
    assert await get_posts_by_id([1]) == []


@pytest.mark.asyncio
async def test_thread_posts_page_can_be_get(thread, post):
    page = await get_thread_posts_page(thread, 10, 0, 1)
    assert post.thread_id == thread.id
    assert page.items == [post]


@pytest.mark.asyncio
async def test_none_is_returned_for_thread_posts_page_if_page_number_is_invalid(
    thread, post
):
    page = await get_thread_posts_page(thread, 10, 0, 100)
    assert page is None