Feature: highlight repository

  Background: session and highlight repo
    Given a session and highlight repo

  Scenario: find error
    Given user id
    When find highlights fails
    Then calls the find highlights failure callback with the exception

  Scenario: find no highlights
    Given user id
    When find highlights succeeds with no highlights
    Then calls the find highlights success callback with an empty list

  Scenario: find with highlights
    Given user id
    When find highlights succeeds with highlights
    Then calls the find highlights success callback with a list of highlights

  Scenario: find highlight media error
    Given a list of highlight reel ids
    When find highlight media fails
    Then calls the find highlight media failure callback with the exception

  Scenario: find no highlight media
    Given a list of highlight reel ids
    When find highlight media succeeds with no media
    Then calls the find highlight media success callback with an empty list

  Scenario: find with highlight media
    Given a list of highlight reel ids
    When find highlight media succeeds with media
    Then calls the find highlight media success callback with a list of media