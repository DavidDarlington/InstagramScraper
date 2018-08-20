Feature: get highlights

  Background: highlight repo
    Given a mock session and highlight repo

  Scenario: get highlights succeeds
    Given a user, observer, and highlight repo
    When get highlights succeeds
    Then calls the get highlights success callback with the highlights media

  Scenario: get highlights fails
    Given a user, observer, and highlight repo
    When get highlights fails
    Then calls the get highlights failure callback with the exception

  Scenario: no highlights
    Given a user, observer, and highlight repo
    When get highlights returns no media
    Then calls the get highlights empty callback