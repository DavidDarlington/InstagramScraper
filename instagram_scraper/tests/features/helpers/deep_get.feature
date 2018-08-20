Feature: get nested dict property value using dot notation string

  Scenario: dict is empty
    Given an empty dict
    When we deep get
    Then returns None for the key value

  Scenario: dict is None
    Given a None dict
    When we deep get
    Then returns None for the key value

  Scenario: dict with nested keys
    Given an dict with nested keys
    When we deep get
    Then returns the value for the nested key


  Scenario: dict with missing nested key
    Given a dict with a missing nested key
    When we deep get
    Then returns None for the key value

  Scenario: dict with missing nested key and default
    Given a dict with a missing nested key and default
    When we deep get with a default
    Then returns the default as the value

  Scenario: dict with nested array index
    Given a dict with a nested array index
    When we deep get
    Then returns the nested key value

  Scenario: dict with nested negative array index
    Given a dict with a nested negative array index
    When we deep get
    Then returns the nested negative index key value