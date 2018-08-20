Feature: set last scraped timestamp for user to file

  Scenario: no parser
    Given no parser for last scraped timestamps
    When we set the timestamp to the file
    Then does not write to the timestamps file


  Scenario: file without users section
    Given a parser and a file without a users section
    When we set the timestamp to the file
    Then adds the users section
    And sets the timestamp for the user
    And writes the timestamp to the timestamps file

   Scenario: file with a users section
    Given a parser and a file with a users section
    When we set the timestamp to the file
    Then does not add the users section
    And sets the timestamp for the user
    And writes the timestamp to the timestamps file