Feature: select challenge mode

  Background: a challenge url, mode and observer
    Given a challenge url, mode, observer, and challenge repo

  Scenario: select challenge mode succeeds
    When a challenge mode is successfully selected
    Then calls the select challenge mode success callback with the challenge url

  Scenario: select challenge mode fails
    When challenge mode selection fails
    Then calls the select challenge mode failure callback with the exception