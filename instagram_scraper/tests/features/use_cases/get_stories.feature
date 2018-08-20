Feature: get stories

  Background: story repo
    Given a mock session and story repo

  Scenario: get stories succeeds
    Given a user, observer, and story repo
    When get stories succeeds
    Then calls the get stories success callback with the stories

  Scenario: get stories fails
    Given a user, observer, and story repo
    When get stories fails
    Then calls the get stories failure callback with the exception

  Scenario: no stories
    Given a user, observer, and story repo
    When get stories returns no stories
    Then calls the get stories empty callback