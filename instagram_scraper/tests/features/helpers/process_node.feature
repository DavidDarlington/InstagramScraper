Feature: processes media nodes

  Background: media repo
    Given a fake media repo

  Scenario: node is an image
    Given a node with media type image
    And include location is false
    When we process the node
    Then returns a node with tags and urls

  Scenario: node is a video
    Given a node with media type video
    And include location is false
    When we process the node
    Then returns a node with tags and urls

  Scenario: node is a video with no video url
    Given a node with media type video with no video url
    And include location is false
    When we process the node
    Then returns a node with tags and urls

  Scenario: node is a carousel with sidecar items
    Given a node with media type sidecar with items
    And include location is false
    When we process the node
    Then returns a node with tags and urls

  Scenario: node is a carousel with no sidecar items
    Given a node with media type sidecar with no items
    And include location is false
    When we process the node
    Then returns a node with tags and urls

  Scenario: node is a carousel with no sidecar items and include location is true
    Given a node with media type sidecar with no items
    And include location is true
    When we process the node
    Then returns a node with tags and urls