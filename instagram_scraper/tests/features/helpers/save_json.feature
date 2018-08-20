Feature: save json to a file

  Scenario: save json to file
    Given a json object to be saved
    When we save the json to a file
    Then calls open to write the json to the file