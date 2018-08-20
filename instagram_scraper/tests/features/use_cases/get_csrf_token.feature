Feature: get csrf token

  Background: observer and auth_repo
    Given an observer and auth_repo setup

  Scenario: get csrf token is successful
    When get csrf token is successful
    Then calls the get csrf token success callback

  Scenario: get csrf token fails
    When get csrf token fails
    Then calls the get csrf token failure callback with the exception
