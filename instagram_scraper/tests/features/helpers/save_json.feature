Feature: save json to a file

  Scenario: save json to file
    Given a json object to be saved
    When we save the json to a file and the dest exists
    Then calls open to write the json to the file

   Scenario: save json to file
    Given a json object to be saved
    When we save the json to a file and the dest does not exist
    Then creates the destination directory
    And calls open to write the json to the file