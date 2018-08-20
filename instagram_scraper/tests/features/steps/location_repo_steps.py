from behave import given, when, then
from mock import MagicMock
from requests import Session, HTTPError

from instagram_scraper.repos import LocationRepo


@given('a location repo and session')
def location_repo(context):
    context.session = MagicMock(spec=Session)
    context.location_repo = LocationRepo(context.session)


@given('a query')
def step_impl(context):
    context.query = 'a search query'


@when('search for locations succeeds')
def step_impl(context):
    context.success = MagicMock()

    context.session.get.return_value.json.return_value = {'places': ['nyc']}

    context.location_repo.search(query=context.query,
                                 success=context.success,
                                 failure=None)


@then('calls the search location success callback with the location data')
def step_impl(context):
    context.success.assert_called_with(['nyc'])


@when('search for locations fails')
def step_impl(context):
    context.failure = MagicMock()

    context.error = HTTPError('error')
    context.session.get = MagicMock(side_effect=context.error)

    context.location_repo.search(query=context.query,
                                 success=None,
                                 failure=context.failure)


@then('calls the search location failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)
