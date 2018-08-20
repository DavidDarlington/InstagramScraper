Feature: get file extension

  Scenario: file with an extension
    Given a file with an extension
    When we get the file extension
    Then returns the file extension

  Scenario: file without extension
    Given a file without an extension
    When we get the file extension
    Then returns empty string

  Scenario: path with a file with an extension
    Given a path with a file with an extension
    When we get the file extension
    Then returns the file extension

  Scenario: path with a file without an extension
    Given a path with a file without an extension
    When we get the file extension
    Then returns empty string