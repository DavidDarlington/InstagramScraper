Feature: location repository

  Background: location repo setup
    Given a location repo and session

  Scenario: search location succeeds
    Given a query
    When search for locations succeeds
    Then calls the search location success callback with the location data

  Scenario: search location fails
    Given a query
    When search for locations fails
    Then calls the search location failure callback with the exception
