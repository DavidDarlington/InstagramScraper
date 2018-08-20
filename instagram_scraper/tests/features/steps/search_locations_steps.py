from behave import given, when, then
from hamcrest import assert_that, instance_of
from mock import MagicMock
from requests import RequestException

from instagram_scraper.use_cases import search_locations


@given('a query, observer, and location repo')
def step_impl(context):
    context.query = 'query'
    context.observer = MagicMock()
    context.location_repo = MagicMock()


@when('search locations succeeds with places')
def step_impl(context):
    def search_fake(**kwargs):
        places = [
            {'position': 2},
            {'position': 1},
            {'position': 3}
        ]
        kwargs['success'](places)

    context.location_repo.search.side_effect = search_fake

    search_locations(query=context.query,
                     observer=context.observer,
                     location_repo=context.location_repo)


@then('tells the observer search locations was successful with the sorted places by position')
def step_impl(context):
    context.observer.search_locations_success.assert_called_with([
        {'position': 1},
        {'position': 2},
        {'position': 3}
    ])


@when('search locations returns no places')
def step_impl(context):
    def search_fake(**kwargs):
        kwargs['success']([])

    context.location_repo.search.side_effect = search_fake

    search_locations(query=context.query,
                     observer=context.observer,
                     location_repo=context.location_repo)


@then('tells the observer no locations were found with an exception')
def step_impl(context):
    context.observer.no_locations_found.assert_called()

    no_locations_found = context.observer.no_locations_found
    actual_error = no_locations_found.call_args[0][0]
    assert_that(actual_error, instance_of(ValueError))


@when('search locations fails')
def step_impl(context):
    def search_fake(**kwargs):
        context.exception = MagicMock(spec=RequestException)
        kwargs['failure'](context.exception)

    context.location_repo.search.side_effect = search_fake

    search_locations(query=context.query,
                     observer=context.observer,
                     location_repo=context.location_repo)


@then('tells the observer search locations failed with the exception')
def step_impl(context):
    context.observer.search_locations_error(context.exception)
