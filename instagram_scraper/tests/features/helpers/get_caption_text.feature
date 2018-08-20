Feature: get caption text

  Scenario: no caption
    Given an item without a caption
    When we get caption text
    Then returns None for the caption text

  Scenario: string caption
    Given an item with a string caption
    When we get caption text
    Then returns the caption text

  Scenario: dict caption
    Given an item with a dict caption
    When we get caption text
    Then returns the caption text


   Scenario: nested caption
    Given an item with a nested caption
    When we get caption text
    Then returns the caption text