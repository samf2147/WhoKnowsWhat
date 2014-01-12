from config import BASE_URL

@when('I load the home page')
def step_impl(context):
    context.browser.get(BASE_URL + '/')

@then('I should see the home page')
def step_impl(context):
    assert context.browser.title == 'WhoOwesWhat - Home'