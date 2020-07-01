from urllib.request import urlopen

from behave import when, then


@when(u'I visit "{url}"')
def visit(context, url):
    page = urlopen(context.base_url + url)
    context.response = str(page.read())
    context.status = page.status


@then(u'I should see "{text}"')
def i_should_see(context, text):
    assert text in context.response


@then("Status code is {status}")
def status_code(context, status):
    code = context.status
    assert code == int(status), "{0} != {1}".format(code, status)
