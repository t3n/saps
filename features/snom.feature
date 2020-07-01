Feature: Fixture loading
    Test if all snom site work.

    Scenario: Phone type is valid
        When I visit "/snom320.htm"
        Then I should see "snom320"

    Scenario: Phone is created
        When I visit "/snom320-0004132C0AD4.htm"
        Then Status code is 201
        When I visit "/snom320-0004132C0AD4.htm"
        Then Status code is 200

    Scenario: MAC address is correct
        When I visit "/snom320-0004132C0AD4.htm"
        Then I should see "0004132C0AD4"
