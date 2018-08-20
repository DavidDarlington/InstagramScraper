Feature: logout user

  Background: observer and auth repo
    Given an observer and auth repo

  Scenario: logout fails due to an error
    Given a csrf token
    When the logout fails due to an error
    Then tells the observer logout failed with an error

  Scenario: logout succeeds
    Given a csrf token
    When logout succeeds
    Then tells the observer logout is successful