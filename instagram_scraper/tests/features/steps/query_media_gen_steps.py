from behave import given, when, then
from hamcrest import equal_to, assert_that
from mock import patch
from itertools import chain

from instagram_scraper.generators import query_media_gen


@given('a user and last scraped time')
def step_impl(context):
    context.user = {'id': 1, 'username': 'username'}
    context.last_scraped_time = 1


@when('the initial call to query media returns no media')
def step_impl(context):
    with patch('instagram_scraper.helpers.query_media') as query_media_fake:
        query_media_fake.return_value = (None, None)

        context.result = list(query_media_gen(user=context.user,
                                              last_scraped_time=context.last_scraped_time,
                                              media_repo=context.media_repo))


@when('query media succeeds with no more items')
def step_impl(context):
    with patch('instagram_scraper.helpers.query_media') as query_media_fake:
        context.media_items = [
            {'created_time': 2}
        ]

        query_media_fake.return_value = context.media_items, None

        context.result = list(query_media_gen(user=context.user,
                                              last_scraped_time=context.last_scraped_time,
                                              media_repo=context.media_repo))


@then('returns the list of items')
def step_impl(context):
    assert_that(context.result, equal_to(context.media_items))


@when('query media succeeds with more items')
def step_impl(context):
    with patch('instagram_scraper.helpers.query_media') as query_media_fake, \
            patch('instagram_scraper.helpers.get_timestamp') as get_timestamp_fake:
        context.media_lists = [
            [{'id': 6}, {'id': 5}, {'id': 4}],
            [{'id': 3}, {'id': 2}],
            [{'id': 1}]
        ]

        query_media_fake.side_effect = [
            (context.media_lists[0], 2),
            (context.media_lists[1], 1),
            (context.media_lists[2], None)
        ]

        get_timestamp_fake.return_value = 2

        context.result = list(query_media_gen(user=context.user,
                                              last_scraped_time=context.last_scraped_time,
                                              media_repo=context.media_repo))


@then('returns a list of media items from all query media calls')
def step_impl(context):
    expected = list(chain.from_iterable(context.media_lists))
    assert_that(context.result, equal_to(expected))


@when('query media succeeds with old items')
def step_impl(context):
    with patch('instagram_scraper.helpers.query_media') as query_media_fake, \
            patch('instagram_scraper.helpers.get_timestamp') as get_timestamp_fake:

        context.media_lists = [
            [{'id': 6}, {'id': 5}],
            [{'id': 4}, {'id': 3}]
        ]

        query_media_fake.side_effect = [
            (context.media_lists[0], 1),
            (context.media_lists[1], None)
        ]

        get_timestamp_fake.side_effect = [2, 2, 1, 0]

        context.result = list(query_media_gen(user=context.user,
                                              last_scraped_time=context.last_scraped_time,
                                              media_repo=context.media_repo))


@then('returns a list of the new media items')
def step_impl(context):
    expected = list(chain.from_iterable(context.media_lists))[:-2]
    assert_that(context.result, equal_to(expected))
