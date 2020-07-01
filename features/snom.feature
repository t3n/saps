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

    Scenario: General is valid
        When I visit "/snom320/general.xml"
        Then I should see "<phone-settings>"
        Then Content type is "application/xml"

    Scenario: Firmware is valid
        When I visit "/snom320/firmware.xml"
        Then I should see "<firmware-settings>"
        Then Content type is "application/xml"

    Scenario: Language is valid
        When I visit "/snom320/general.xml"
        Then I should see "<setting_server perm"
        Then Content type is "application/xml"
