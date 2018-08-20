Feature: parse a delimited string of usernames

  Scenario Outline: parse delimited string
    Given we have a string "<string>"
    When we parse the string
    Then returns a list of tokens <tokens>

   Examples: words
     | string       |  tokens       |
     | a            |  a            |
     | hello        |  hello        |
     | hello world  |  hello,world  |
     | ,hello  ,   , world  ;; test,,  |  hello,world,test  |


  Scenario: parse delimited string
    Given we have an empty string
    When we parse the string
    Then returns an empty list