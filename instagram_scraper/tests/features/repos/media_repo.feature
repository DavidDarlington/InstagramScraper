Feature: media repository

  Background: media repo setup
    Given a media repo

  Scenario: query media succeeds
    Given a user id and end cursor
    When query media succeeds
    Then returns the user's media data

  Scenario: query media fails
    Given  a user id and end cursor
    When query media fails
    Then raises the exception that caused the query media failure

  Scenario: get media details succeeds
    Given a short code
    When get media details succeeds
    Then returns the media details

  Scenario: get media details fails
    Given a short code
    When get media details fails
    Then raises the exception that caused the get media details failure