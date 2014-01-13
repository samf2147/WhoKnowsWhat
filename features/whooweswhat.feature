Feature: confirming that the calculator works
    Scenario: check that the home page displays
        When I load the home page
        Then I should see the home page

    Scenario: check that the login page displays
        When I load the home page
        Then I should see the home page
    
    Scenario: check that I can create an account
        When I create an account
        Then my account should be added to the database