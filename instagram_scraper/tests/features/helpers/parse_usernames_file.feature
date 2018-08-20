Feature: parse a file containing usernames

  Scenario: parse a non-existent file
    Given we have a file that does not exist
    When we try to parse the file
    Then throws an error

  Scenario: parse an empty file
    Given we have an empty file
    When we try to parse the empty file
    Then returns an empty list


  Scenario: parse a file with a single user
    Given we have a file with a single user
    When we try to parse a file with a single user
    Then returns a list with a single user

  Scenario: parse a file with several users
    Given we have a file with several users
    When we try to parse a file with several users
    Then returns a list with several users