import unittest
from stream_tool import create_website, _website, _page, _button, exceptions


class TestCreateWebsite(unittest.TestCase):

    def tearDown(self):
        _website.Website.one_website_made = False

    def test_create_website(self):
        created_website = create_website()
        website_class = _website.Website
        self.assertIsInstance(created_website, website_class,
                              "create_website does not create instance of Website class")
        page_class = _page.Page

        self.assertIsInstance(created_website.index_page, page_class,
                              "create_website does not create index page that is instance of Page class")

        created_website._build()
        self.app = created_website._app.test_client()
        r = self.app.get('/')
        server_page_html = r.data
        with open("html_test_samples/blank_page.html", "r") as f:
            page_html = f.read()
        page_html = page_html.encode("utf-8")
        self.assertEqual(page_html, server_page_html,
                         "live html on server for index page does not match expected html for a blank page")


class TestAddPage(unittest.TestCase):

    def setUp(self):
        self.website = create_website()

    def tearDown(self):
        _website.Website.one_website_made = False

    def test_add_page(self):
        created_page = self.website.add_page("test-page")
        self.assertIsInstance(created_page, _page.Page,
                              "add_page does not create instance of Page class")

    def test_add_pages_with_bad_names(self):
        created_page = self.website.add_page("test page")
        self.assertEqual(created_page.name, "test-page", "format_page_name is not working")
        self.assertEqual(created_page.url, "/test-page", "url is not being created correctly")
        self.assertRaises(exceptions.DuplicatePageNameError, self.website.add_page, "test page")
        self.assertRaises(exceptions.DuplicatePageNameError, self.website.add_page, "standard_files")

    def test_build_and_run_page(self):
        created_page = self.website.add_page("test-page")
        self.website._build()
        self.app = self.website._app.test_client()
        r = self.app.get('/test-page')
        server_page_html = r.data
        with open("html_test_samples/blank_page.html", "r") as f:
            page_html = f.read()
        page_html = page_html.encode("utf-8")
        self.assertEqual(page_html, server_page_html,
                         "live html on server does not match expected html for a blank page")

# TODO: test buttons
class TestAddButton(unittest.TestCase):

    def setUp(self):
        self.website = create_website()
        self.page = self.website.add_page("button-page")

    def tearDown(self):
        _website.Website.one_website_made = False

    def test_button(self):
        button = self.page.add_button("button 1")
        self.assertIsInstance(button, _button.Button)

    def test_button_naming(self):
        button = self.page.add_button("test button")
        self.assertEqual("TestButton", button.name, "Button name is not formatted in PascalCase")
        self.assertEqual("TestButton", button.text, "Button name is not being set as button text")

        button.name = "another test  name"
        self.assertEqual("AnotherTestName", button.name, "Button name is not formatted in PascalCase")
        self.assertEqual("TestButton", button.text, "Button text is not staying the same after changing name")

        button.text = "this button says this"
        self.assertEqual("this button says this", button.text, "Changing button text attribute doesn't work")

        button2 = self.page.add_button("test button 2", text="The Button Text")
        self.assertEqual("TestButton2", button2.name, "Button name doesn't work when text is set as kwarg")
        self.assertEqual("The Button Text", button2.text, "Button text doesn't work when set as a kwarg")

        self.assertRaises(exceptions.DuplicateButtonNameError, self.page.add_button, "test button")
        self.assertRaises(exceptions.DuplicateButtonNameError, self.page.add_button, "testButton")
        self.assertRaises(exceptions.DuplicateButtonNameError, self.page.add_button, "TestButton")
        self.assertRaises(exceptions.DuplicateButtonNameError, self.page.add_button, "test-button")
        self.assertRaises(exceptions.DuplicateButtonNameError, self.page.add_button, "test_button")

        self.assertRaises(exceptions.ButtonNameSyntaxError, self.page.add_button, "test-button?")

    def test_button_function(self):

        def my_function(arg1, arg2, arg3, kwarg1=None, kwarg2=None, kwarg3=None):
            return arg1, arg2, arg3, kwarg1, kwarg2, kwarg3

        btn = self.page.add_button("test_button",
                                   button_function=my_function,
                                   button_function_args=[1, 2, 3],
                                   button_function_kwargs={
                                       "kwarg1": 4,
                                       "kwarg3": 6,
                                       "kwarg2": 5
                                   })

        args = btn.button_function_args
        kwargs = btn.button_function_kwargs
        r = btn.button_function(*args, **kwargs)
        e = 1, 2, 3, 4, 5, 6
        self.assertEqual(e, r, "button_function with args and kwargs as arguments is not performing as expected")

        btn = self.page.add_button("test_button2")
        btn.button_function = my_function
        btn.button_function_args = [1, 2, 3]
        btn.button_function_kwargs = {
            "kwarg1": 4,
            "kwarg3": 6,
            "kwarg2": 5
        }

        args = btn.button_function_args
        kwargs = btn.button_function_kwargs
        r = btn.button_function(*args, **kwargs)
        e = 1, 2, 3, 4, 5, 6
        self.assertEqual(e, r, "button_function with args and kwargs as attributes is not performing as expected")

        def my_function(arg, kwarg=None):
            return arg, kwarg

        btn = self.page.add_button("test_button3")
        btn.button_function = my_function
        btn.button_function_args = [1]
        btn.button_function_kwargs = {"kwarg": 2}

        args = btn.button_function_args
        kwargs = btn.button_function_kwargs
        r = btn.button_function(*args, **kwargs)
        e = (1, 2)
        self.assertEqual(e, r, "button_function with one arg and one kwarg as a list and dict failed")

        btn = self.page.add_button("test_button4")
        btn.button_function = my_function
        btn.button_function_args = 1
        btn.button_function_kwargs = ("kwarg", 2)

        args = btn.button_function_args
        kwargs = btn.button_function_kwargs
        r = btn.button_function(*args, **kwargs)
        e = (1, 2)
        self.assertEqual(e, r, "button_function with one arg as itself and kwarg as tuple failed")

        btn.button_function_kwargs = ["kwarg", 2]

        args = btn.button_function_args
        kwargs = btn.button_function_kwargs
        r = btn.button_function(*args, **kwargs)
        self.assertEqual(e, r, "button_function with one arg as itself and kwarg as list failed")

    def test_button_function_html_and_flask(self):

        function_result = []

        def my_function(result, arg1, arg2, arg3, kwarg1=None, kwarg2=None, kwarg3=None,):
            result.append((arg1, arg2, arg3, kwarg1, kwarg2, kwarg3))

        btn = self.page.add_button("test_button")
        btn.button_function = my_function
        btn.button_function_args = [function_result, 1, 2, 3]
        btn.button_function_kwargs = {
            "kwarg1": 4,
            "kwarg3": 6,
            "kwarg2": 5
        }

        self.website._build()
        self.app = self.website._app.test_client()
        r = self.app.get('/button-page')
        server_page_html = r.data
        with open("html_test_samples/button_function.html", "r") as f:
            page_html = f.read()
        page_html = page_html.encode("utf-8")
        self.assertEqual(page_html, server_page_html,
                         "live html on server for index page does not match expected html for a blank page")

        r = self.app.get('/TestButton')
        self.assertEqual(b'TestButton', r.data, "button press is not returning expected response through flask")
        e = 1, 2, 3, 4, 5, 6
        self.assertEqual(e, function_result[0],
                         "button_function with args and kwargs is not performing as expected in flask test")

    def test_button_link(self):

        btn = self.page.add_button("test button", button_link="google.com")
        self.assertEqual('http://google.com', btn.button_link, "button link not formatted correctly")
        btn.button_link = "youtube.com"
        self.assertEqual('http://youtube.com', btn.button_link, "button link not formatted correctly")

    def test_button_html(self):
        btn = self.page.add_button("test button", button_link="google.com")

        self.website._build()
        self.app = self.website._app.test_client()
        r = self.app.get('/button-page')
        server_page_html = r.data
        with open("html_test_samples/button_link.html", "r") as f:
            page_html = f.read()
        page_html = page_html.encode("utf-8")
        self.assertEqual(page_html, server_page_html,
                         "live html on server for button w/ link does not match expected html")

# TODO: test obs websocket

# TODO: test builtin obs actions maybe


if __name__ == '__main__':
    unittest.main()