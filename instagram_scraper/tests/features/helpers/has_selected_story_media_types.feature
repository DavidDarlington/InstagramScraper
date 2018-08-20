Feature: has selected story media types

  Scenario: item is image type
    Given an item with media type image and selected media types includes images
    When we call has selected story media types
    Then returns true for has selected story media types

  Scenario: item is video type
    Given an item with media type video and selected media types includes videos
    When we call has selected story media types
    Then returns true for has selected story media types

  Scenario: item is story image type
    Given an item with story type image and selected media types includes images
    When we call has selected story media types
    Then returns true for has selected story media types

  Scenario: item is story video type
    Given an item with story type video and selected media types includes videos
    When we call has selected story media types
    Then returns true for has selected story media types

  Scenario: item without media type
    Given an item without media type
    When we call has selected story media types
    Then returns false for has selected story media types