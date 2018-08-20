Feature: search locations

  Background: query, observer, and location repo
    Given a query, observer, and location repo

  Scenario: search locations succeeds
    When search locations succeeds with places
    Then tells the observer search locations was successful with the sorted places by position

  Scenario: search locations no matching places
    When search locations returns no places
    Then tells the observer no locations were found with an exception

  Scenario: search locations fails
    When search locations fails
    Then tells the observer search locations failed with the exception