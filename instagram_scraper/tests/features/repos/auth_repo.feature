Feature: authentication repository

  Background: auth repo setup
    Given an auth repo

  Scenario: find the csrf token fails
    Given a session
    When find csrf token fails
    Then updates the referer and user-agent headers
    And calls the failure callback with the exception

  Scenario: find the csrf token fails
    Given a session
    When find csrf token fails with no shared data
    Then updates the referer and user-agent headers
    And calls the failure callback with the missing shared data exception

  Scenario: find the csrf token fails
    Given a session
    When find csrf token fails with no rhx gis value
    Then updates the referer and user-agent headers
    And calls the failure callback with an exception

  Scenario: find the csrf token is successful
    Given a session
    When find csrf token is successful
    Then updates the referer and user-agent headers
    And updates the X-CSRFToken header
    And calls the find the csrf token success callback


  Scenario: login fails
    Given a username and password
    When login fails
    Then calls the failure callback with the exception and response

  Scenario: login fails due to authentication failure
    Given a username and password
    When login fails due to authentication failure
    Then calls the failure callback with an invalid credentials exception and response

  Scenario: login is successful
    Given a username and password
    When login succeeds
    Then updates the X-CSRFToken header
    And calls the login success callback


  Scenario: logout is successful
    Given a session and a csrf token
    When logout is successful
    Then calls the success callback

  Scenario: logout is fails
    Given a session and a csrf token
    When logout fails
    Then calls the failure callback with the exception

