Feature: get user profile

  Background: user repo setup
    Given a session and user repo

  Scenario: get user profile returns a private user and you are not an approved follower
    Given a username and an observer
    When get user profile returns a private user and you are not an approved follower
    Then tells the observer get user profile is private with the user

  Scenario: get user profile returns a private user and you are an approved follower
    Given a username and an observer
    When get user profile returns a private user and you are an approved follower
    Then tells the observer get user profile was successful with the user

  Scenario: get user profile returns a public user
    Given a username and an observer
    When get user profile returns a public user
    Then tells the observer get user profile was successful with the user

  Scenario: get user profile fails
    Given a username and an observer
    When get user profile fails
    Then tells the observer get profile failed with the exception