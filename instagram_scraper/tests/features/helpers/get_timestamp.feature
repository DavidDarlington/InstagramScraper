Feature: gets the timestamp from media item

  Scenario: item with no timestamp fields
    Given an item with no timestamp fields
    When we get the timestamp from the media item
    Then returns 0 for the timestamp


  Scenario: item with not a number timestamp fields
    Given an item with a not a number timestamp field value
    When we get the timestamp from the media item
    Then returns 0 for the timestamp

  Scenario: item with timestamp fields
    Given an item with timestamp fields
    When we get the timestamp from the media item
    Then returns the timestamp