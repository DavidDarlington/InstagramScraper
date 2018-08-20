Feature: user repository

  Background: user repo setup
    Given a user repo

  Scenario: get profile fails due to error
    Given a username and session
    When get profile fails
    Then calls the get profile failure callback with the exception

   Scenario: get profile fails due to missing content
    Given a username and session
    When get profile fails due to missing content
    Then calls the get profile failure callback with a profile exception

   Scenario: get profile fails due to parse content error
    Given a username and session
    When get profile fails due to parse content error
    Then calls the get profile failure callback with a profile exception

   Scenario: get profile succeeds
    Given a username and session
    When get profile succeeds
    Then calls the get profile success callback with the user


   Scenario: get user info fails
     Given a user id
     When get user info fails
     Then calls the get user info failure callback with the exception

   Scenario: get user info succeeds
     Given a user id
     When get user info succeeds
     Then calls the get user info success callback with the user