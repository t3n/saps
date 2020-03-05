Feature: Fixture loading
    Test if all snom site work.

    Scenario: Phone type is valid
        When I visit "/snom320.htm"
        Then I should see "snom320"
