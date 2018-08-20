Feature: story repository

  Background: session and story repo
    Given a session and story repo

  Scenario: find error
    Given user id
    When find stories fails
    Then calls the find stories failure callback with the exception

  Scenario: find no stories
    Given user id
    When find stories succeeds with no stories
    Then calls the find stories success callback with an empty list

  Scenario: find with stories
    Given user id
    When find stories succeeds with stories
    Then calls the find stories success callback with a list of stories