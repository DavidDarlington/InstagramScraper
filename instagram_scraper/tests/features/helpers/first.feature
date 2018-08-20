Feature: returns the first non-None value

  Scenario: list is empty
    Given an empty list
    When first is called
    Then returns None

  Scenario: list contains value
    Given a list with a value
    When first is called
    Then returns the value

  Scenario: list contains value with a default
    Given a list with a value and a default
    When first is called with a default
    Then returns the value

  Scenario: list contains None values
    Given a list of None values
    When first is called
    Then returns None

  Scenario: list contains None values with a default
    Given a list of None values and a default value
    When first is called with a default
    Then returns the default value