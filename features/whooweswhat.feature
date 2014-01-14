Feature: confirming that the calculator works
    Scenario: check that the home page displays
        When I load the home page
        Then I should see the home page

    Scenario: check that the login page displays
        When I load the login page
        Then I should see the login page
    
    Scenario: check that I can log in
        When I load the login page
        And I enter my login information
        Then I should be logged in
    
    Scenario: check that I can view my events
        When I load the events page
        Then I should see my events
    
    Scenario: check that I can view payments for an event
        When I click on an event
        Then I can see payments for that event
    
    Scenario: check that I can add payments for an event
        When I load the events page
        And I add an event
        Then I can see that event
    
    Scenario: check that I can delete events
        When I delete an event
        Then I cannot see that event
    
#     Scenario: check that I can add payments
#         When I click on an event
#         And I add a payment
#         Then I can see that payment
#     
#     Scenario: check that I can delete payments
#         When I delete a payment
#         Then I cannot see that payment