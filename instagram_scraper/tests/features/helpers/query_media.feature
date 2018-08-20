Feature: query media

  Background: media repo
    Given a fake media repo

  Scenario: query media returns no media
    Given a user id and end cursor
    When query media returns no media
    Then returns no nodes and no end cursor

  Scenario: query media returns media with no end cursor
    Given a user id and end cursor
    When query media returns media with no end cursor
    Then returns media and no end cursor

  Scenario: query media returns media with an end cursor
    Given a user id and end cursor
    When query media returns media with an end cursor
    Then returns media and end cursor