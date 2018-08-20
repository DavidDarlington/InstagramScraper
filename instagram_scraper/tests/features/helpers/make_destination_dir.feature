Feature: make the destination directory

  Scenario: directory does not exists
    Given a destination path to make
    When we make the destination directory
    Then makes the destination directory

  Scenario: directory already exists when making the directory
    Given a destination path to make
    When we make the destination directory and it already exists
    Then returns None

  Scenario: making directory fails due to error
    Given a destination path to make
    When we make the destination directory and it fails due to error
    Then raises an os error from makedirs