Feature: login user

  Background: observer and auth repo
    Given an observer and auth repo

  Scenario: login succeeds
    Given a username and password
    When the login is successful
    Then tells the observer the login was successful

  Scenario: login fails due to invalid credentials
    Given a username and password
    When the login request is successful but the user is not authenticated
    Then tells the observer the login failed with the exception and response content

  Scenario: login fails due to a required challenge
    Given a username and password
    When the login request fails due to a required challenge
    Then tells the observer a challenge is prompted with the challenge url
