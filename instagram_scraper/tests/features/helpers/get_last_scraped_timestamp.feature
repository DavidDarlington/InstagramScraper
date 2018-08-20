Feature: get last scraped timestamp from file

  Scenario: get last scraped timestamp from file
    Given a username with no parser
    When we get the timestamp from the file
    Then returns 0 as the timestamp

  Scenario: get last scraped timestamp from file
    Given a parser and a username
    When we get the timestamp from the file
    Then returns the last scraped timestamp


  Scenario: get last scraped timestamp fails
    Given a parser that fails with error and a username
    When we get the timestamp from the file
    Then returns 0 as the timestamp