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

# @when('I create an account')
# def step_impl(context):
#     br = context.browser
#     br.get(BASE_URL + '/login')
#     br.find_element_by_name('new_username').send_keys('test_user')
#     br.find_element_by_name('new_password').send_keys('test_password')
#     br.find_element_by_id('submit').click()
# 
# @then('My account should be added to the database')
# def step_impl(context):
#     br = context.browser
#     assert br.find_element_by_id('login_status').text == 'Logged in as test_user'