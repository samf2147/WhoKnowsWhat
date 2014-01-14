from config import BASE_URL

@when('I load the home page')
def step_impl(context):
    context.browser.get(BASE_URL + '/')

@then('I should see the home page')
def step_impl(context):
    assert context.browser.title == 'WhoOwesWhat - Home'
    
@when('I load the login page')
def step_impl(context):
    context.browser.get(BASE_URL + '/login')

@then('I should see the login page')
def step_impl(context):
    assert context.browser.title == 'WhoOwesWhat - Login'

@when('I load the events page')
def step_impl(context):
    context.browser.get(BASE_URL + '/events')

@when('I enter my login information')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('username').send_keys('test_user')
    br.find_element_by_name('password').send_keys('test_password')
    br.find_element_by_id('submit').click()

@then('I should be logged in')
def step_impl(context):
    br = context.browser
    assert br.find_element_by_id('login_status').text == \
                                          'Logged in as test_user'


#events
@then('I should see my events')
def step_impl(context):
    br = context.browser
    event_list = br.find_element_by_id('event-list').text
    assert 'test_event' in event_list

@when('I click on an event')
def step_impl(context):
    br = context.browser
    br.find_element_by_id('test_event').click()

@then('I can see payments for that event')
def step_impl(context):
    br = context.browser
    assert '120.00' in br.find_element_by_id('payments').text

#adding and deleting events and payments
@when('I add an event')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('name').send_keys('test_add_event')
    br.find_element_by_id('submit').click()

@then('I can see that event')
def step_impl(context):
    br = context.browser
    assert 'test_add_event' in br.find_element_by_id('event-list').text

@when('I delete an event')
def step_impl(context):
    br = context.browser
    br.find_element_by_id('delete-test_add_event').click()

@then('I cannot see that event')
def step_impl(context):
    br = context.browser
    assert 'test_add_event' not in br.find_element_by_id('event-list').text

@when('I add a payment')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('payer').send_keys('test_add_payer')
    br.find_element_by_name('amount').send_keys('137.53')
    br.find_element_by_id('submit').click()

@then('I can see that payment')
def step_impl(context):
    br = context.browser
    payments = br.find_element_by_id('payments').text
    assert 'test_add_payer' in payments and '137.53' in payments

@when('I delete a payment')
def step_impl(context):
    br = context.browser
    br.find_element_by_name('delete-payment-test_add_payer').click()

@then('I cannot see that payment')
def step_impl(context):
    br = context.browser
    assert 'test_add_payer' not in br.find_element_by_id('payments').text
