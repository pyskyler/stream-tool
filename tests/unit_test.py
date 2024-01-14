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

    def test_button_link_html(self):
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

    def test_button_color(self):
        blue_btn = self.page.add_button("test button", color="blue")
        red_btn = self.page.add_button("test2", color="rED")
        gold_btn = self.page.add_button("test3", color="FFD700")
        orange_btn = self.page.add_button("test4", color="#fFa500")
        yellow_btn = self.page.add_button("test5", color="yellow")
        yellow_btn.color = "ffFF00"

        self.website._build()

        self.assertEqual(blue_btn.color, "blue", "color formatting during build did not work correctly")
        self.assertEqual(red_btn.color, "red", "color formatting during build did not work correctly")
        self.assertEqual(gold_btn.color, "#FFD700", "color formatting during build did not work correctly")
        self.assertEqual(orange_btn.color, "#FFA500", "color formatting during build did not work correctly")
        self.assertEqual(yellow_btn.color, "#FFFF00", "color formatting during build did not work correctly")

    def test_button_color_flask(self):
        blue_btn = self.page.add_button("test button", color="blue")
        red_btn = self.page.add_button("test2", color="rED")
        gold_btn = self.page.add_button("test3", color="FFD700")
        orange_btn = self.page.add_button("test4", color="#fFa500")
        yellow_btn = self.page.add_button("test5", color="yellow")
        yellow_btn.color = "ffFF00"
        blue_btn2 = self.page.add_button("test6", color="blue")
        blue_btn3 = self.page.add_button("test7", color="blue")
        gold_btn2 = self.page.add_button("test8", color="#FfD700")

        self.website._build()

        self.app = self.website._app.test_client()
        r = self.app.get('/button-page')
        server_page_html = r.data
        with open("html_test_samples/color1.html", "r") as f:
            page_html_colors = f.read()
        with open("html_test_samples/color2.html", "r") as f:
            page_html_buttons = f.read()
        page_html_colors = page_html_colors.encode("utf-8")
        page_html_buttons = page_html_buttons.encode("utf-8")
        self.assertIn(page_html_colors, server_page_html,
                      "live html on server for button class colors does not match expected html")
        self.assertIn(page_html_buttons, server_page_html,
                      "live html on server for button w/ colors does not match expected html")

    def test_button_default_color(self):
        self.page.button_color = "aqua"
        page_2 = self.website.add_page("page2", button_color="FFFF00")

        self.website._build()

        self.app = self.website._app.test_client()
        r1 = self.app.get('/button-page')
        r2 = self.app.get('/page2')
        r3 = self.app.get('/')

        server_page1_html = r1.data
        server_page2_html = r2.data
        server_page3_html = r3.data

        button1 = "button {\n\
            width: 100%;\n\
            height: 100%;\n\
            border: none;\n\
            background-color: aqua;\n\
            color: white;\n\
            font-size: 50px;\n\
            border-radius: 25px;\n\
        }"

        button2 = "button {\n\
            width: 100%;\n\
            height: 100%;\n\
            border: none;\n\
            background-color: #FFFF00;\n\
            color: white;\n\
            font-size: 50px;\n\
            border-radius: 25px;\n\
        }"

        button3 = "button {\n\
            width: 100%;\n\
            height: 100%;\n\
            border: none;\n\
            background-color: #3498DB;\n\
            color: white;\n\
            font-size: 50px;\n\
            border-radius: 25px;\n\
        }"

        button1 = button1.encode("utf-8")
        button2 = button2.encode("utf-8")
        button3 = button3.encode("utf-8")
        self.assertIn(button1, server_page1_html,
                      "live html on server for page button default color does not match expected html")
        self.assertIn(button2, server_page2_html,
                      "live html on server for page button default color does not match expected html")
        self.assertIn(button3, server_page3_html,
                      "live html on server for page button default color does not match expected html")


class TestPageColor(unittest.TestCase):

    def tearDown(self):
        _website.Website.one_website_made = False

    def setUp(self):
        colors = ".button0 {background-color: aqua;} \n\t\t" \
                 ".button1 {background-color: green;} \n\t\t" \
                 ".button2 {background-color: red;} \n\t\t" \
                 ".button3 {background-color: #3498DB;}"

        buttons = "<div class='button-container'><button class=button0" \
                  " onclick='performActionPage1()'>Page1</button></div>\n\t" \
                  "<div class='button-container'><button class=button1" \
                  " onclick='performActionPage2()'>Page2</button></div>\n\t" \
                  "<div class='button-container'><button class=button2" \
                  " onclick='performActionPage3()'>Page3</button></div>\n\t" \
                  "<div class='button-container'><button class=button3" \
                  " onclick='performActionIndex()'>Index</button></div>"

        link1 = "function performActionPage1() {\n\t\t\t" \
                "window.location.href = \"/page-1\";		}"
        link2 = "function performActionPage2() {\n\t\t\t" \
                "window.location.href = \"/Page-2\";		}"
        link3 = "function performActionPage3() {\n\t\t\t" \
                "window.location.href = \"/Page-3\";		}"
        link4 = "function performActionIndex() {\n\t\t\t" \
                "window.location.href = \"/\";		}"
        self.needed_html = [colors, buttons, link1, link2, link3, link4]

    def test_use_linked_page_color(self):
        site = create_website()
        site.use_linked_page_color = True

        page1 = site.add_page("page 1", button_color="aqua")
        page2 = site.add_page("Page 2", button_color="green")
        page3 = site.add_page("Page 3", button_color="red")
        btn_page = site.add_page("Button Page", button_color="yellow")

        btn_page.add_button("page1", button_link=page1.url)
        btn_page.add_button("page2", button_link=page2.url)
        btn_page.add_button("page3", button_link=page3.url)
        btn_page.add_button("index", button_link=site.index_page.url)

        site._build()
        app = site._app.test_client()
        r = app.get('/Button-Page')
        server_page_html = r.data

        for html in self.needed_html:
            html = html.encode("utf-8")
            self.assertIn(html, server_page_html,
                          f"live html on server for use_linked_page_color does not match expected line: {html}")

if __name__ == '__main__':
    unittest.main()
