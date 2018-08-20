Feature: query media generator

  Background: media repo
    Given a fake media repo

  Scenario: query returns no media
    Given a user and last scraped time
    When the initial call to query media returns no media
    Then returns an empty list

  Scenario: succeeds with no more items
    Given a user and last scraped time
    When query media succeeds with no more items
    Then returns the list of items

  Scenario: succeeds with more items
    Given a user and last scraped time
    When query media succeeds with more items
    Then returns a list of media items from all query media calls

  Scenario: succeeds with old items
    Given a user and last scraped time
    When query media succeeds with old items
    Then returns a list of the new media items