Feature: profile picture exists

  Scenario: profile pic file exists
    Given a dir and a profile picture url
    When the file exists and we call profile picture exists
    Then returns True for profile picture exists


  Scenario: profile pic file doesn't exist
    Given a dir and a profile picture url
    When the file doesn't exist and we call profile picture exists
    Then returns False for profile picture exists