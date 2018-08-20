Feature: get story urls

  Scenario: item with video and image urls
    Given item with video and image urls
    When we get the story urls
    Then returns a list of story image and video urls

  Scenario: item with no video and image urls
    Given item with no video and image urls
    When we get the story urls
    Then returns an empty list with no urls