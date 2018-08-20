Feature: send challenge code

  Background: use case setup
    Given a challenge url, code, observer, and challenge repo

  Scenario: send challenge code succeeds
    When a challenge code is successfully sent
    Then calls the send challenge code success callback

  Scenario: send challenge code fails due to error
    When sending the challenge code fails
    Then the send challenge code error callback is called with the exception and response