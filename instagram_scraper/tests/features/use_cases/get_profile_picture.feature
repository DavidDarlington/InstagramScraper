Feature: get profile picture

  Background: user repo setup
    Given a session and user repo

  Scenario: get profile picture succeeds with the highest quality picture
    Given a user and an observer
    When get profile picture succeeds with the highest quality picture
    Then tells the observer get profile picture was successful with the profile picture url

  Scenario: get profile picture succeeds with the lowest quality picture
    Given a user and an observer
    When get profile picture succeeds with the lowest quality picture
    Then tells the observer get profile picture was successful with the profile picture url

  Scenario: get profile picture succeeds with no profile pictures
    Given a user and an observer
    When get profile picture succeeds with no profile pictures
    Then tells the observer get profile picture was successful with the profile picture url from the user

  Scenario: anonymous profile picture
    Given a user and an observer
    When get profile picture is anonymous
    Then tells the observer get profile picture is default

  Scenario: get profile picture fails
    Given a user and an observer
    When get profile picture fails
    Then tells the observer get profile picture failed with the exception