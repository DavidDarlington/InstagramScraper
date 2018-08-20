Feature: get the destination directory

   Scenario: destination is current directory
    Given the destination is the current directory and retain username is false
    When we get the destination directory
    Then returns ./username

   Scenario: destination is not the current directory and retain username is false
    Given the destination is not the current directory and retain username is false
    When we get the destination directory
    Then returns the destination directory

   Scenario: destination is not the current directory and retain username is true
    Given the destination is not the current directory and retain username is true
    When we get the destination directory
    Then returns the destination directory/username