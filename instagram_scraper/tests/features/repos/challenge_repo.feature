Feature: challenge repository

  Background: challenge repo setup
    Given a session and challenge repo

  Scenario: challenge mode selection succeeds
    Given a challenge url and selected mode
    When the challenge mode choice is successfully sent
    Then updates the Referer, X-CSRFToken, and X-Instagram-AJAX headers
    And calls the challenge mode success callback

  Scenario: challenge mode selection fails
    Given a challenge url and selected mode
    When the challenge mode choice request fails
    Then calls the challenge mode failure callback with the exception

  Scenario: challenge mode selection fails due to unsupported mode
    Given a challenge url and selected mode
    When the challenge mode choice request fails due to unsupported mode
    Then calls the challenge mode failure callback with a challenge exception


  Scenario: challenge code succeeds
    Given a challenge url and code
    When the challenge code is successful
    Then updates the X-CSRFToken header
    And calls the challenge code success callback

  Scenario: challenge code fails
    Given a challenge url and code
    When the challenge code fails
    Then calls the challenge code failure callback with the exception and response

  Scenario: challenge code fails due to invalid code
    Given a challenge url and code
    When the challenge code fails due to invalid code
    Then calls the challenge code failure callback with a challenge exception and response