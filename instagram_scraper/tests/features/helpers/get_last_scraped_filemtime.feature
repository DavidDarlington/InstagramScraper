Feature: get the last modified time of the newest file within a directory

  Scenario: the directory does not contain jpg or mp4 files
    Given a directory
    When the directory does not contain jpg or mp4 files
    And we get the last modified time of the newest file
    Then returns 0 as the filemtime

  Scenario: the directory contains mp4 files
    Given a directory
    When the directory contains mp4 files
    And we get the last modified time of the newest file
    Then returns the filemtime of the latest file

   Scenario: the directory contains jpg files
    Given a directory
    When the directory contains jpg files
    And we get the last modified time of the newest file
    Then returns the filemtime of the latest file

    Scenario: the directory contains jpg and mp4 files
    Given a directory
    When the directory contains jpg files
    When the directory contains mp4 files
    And we get the last modified time of the newest file
    Then returns the filemtime of the latest file