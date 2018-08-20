Feature: get a session with retry capability

  Scenario: get session
    Given a session does not exist
    When we get the session with retry
    Then returns a new session with retry capability
