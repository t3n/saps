import requests

from behave import when, then


@when(u'I visit "{url}"')
def visit(context, url):
    context.response = requests.get(context.base_url + url)


@then(u'I should see "{text}"')
def i_should_see(context, text):
    assert text in context.response.text


@then("Status code is {status}")
def status_code(context, status):
    code = context.response.status_code
    assert code == int(status), "{0} != {1}".format(code, status)


@then(u'Content type is "{content_type}"')
def content_type(context, content_type):
    assert content_type in context.response.headers["Content-Type"]
