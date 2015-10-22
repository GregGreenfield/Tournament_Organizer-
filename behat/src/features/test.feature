# test feature

Feature: ls
  In order to see the directory structure
  As a UNIX user
  I need to be able to list the current directory's contents

  Scenario: Searching for a page that does NOT exist
    Given I am on "http://en.wikipedia.org/wiki/Main_Page"
    When I fill in "search" with "Glory Driven Development"
    And I press "searchButton"
    Then I should see "Search results"

    @javascript
    Scenario: Searching for a page with autocompletion
      Given I am on "http://en.wikipedia.org/wiki/Main_Page"
      When I fill in "search" with "Behavior Driv"
      And I wait for the suggestion box to appear
      Then I should see "Behavior-driven development"
