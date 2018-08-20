Feature: get hashtags from media item

  Scenario: no caption text
    Given an item with no caption text
    When we get the hashtags
    Then returns an empty list for the hashtags

  Scenario: no hashtags
    Given caption without hashtags
    When we get the hashtags
    Then returns an empty list for the hashtags

  Scenario: hashtag emojis
    Given caption with hashtag emojis
    When we get the hashtags
    Then returns a list of hashtags emojis