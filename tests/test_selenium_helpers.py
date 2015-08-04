import os
import unittest

from mock import patch
from selenium.webdriver import PhantomJS
from the_ark import selenium_helpers

ROOT = os.path.abspath(os.path.dirname(__file__))
SELENIUM_TEST_HTML = '{0}/etc/test.html'.format(ROOT)


class SeleniumHelpersTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sh = selenium_helpers.SeleniumHelpers()
        cls.driver = cls.sh.create_driver(browserName="phantomjs")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    def setUp(self):
        self.sh.get_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.__init__")
    def test_sauce_browser_valid(self, mock_browser):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(username="test", access_key="test", browserName="firefox")
        self.assertTrue(mock_browser.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.__init__")
    def test_mobile_browser_valid(self, mock_browser):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(mobile=True)
        self.assertTrue(mock_browser.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.__init__")
    def test_chrome_browser_valid(self, mock_browser):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(browserName="chrome")
        self.assertTrue(mock_browser.called)

    #TODO: Creates Firefox driver, needs to not do that crap
    @patch("selenium.webdriver.remote.webdriver.WebDriver.__init__")
    def test_firefox_browser_valid(self, mock_browser):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(browserName="firefox")
        self.assertTrue(mock_browser.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.__init__")
    def test_phantomjs_browser_valid(self, mock_browser):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(browserName="phantomjs")
        self.assertTrue(mock_browser.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.__init__")
    def test_safari_browser_valid(self, mock_browser):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(browserName="safari")
        self.assertTrue(mock_browser.called)

    def test_no_driver_invalid(self):
        self.assertRaises(selenium_helpers.DriverAttributeError, self.sh.create_driver, browserName="browser")

    def test_driver_creation_invalid(self):
        self.assertRaises(selenium_helpers.DriverAttributeError, self.sh.create_driver, browserName="")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.set_window_size")
    def test_resize_window_width_and_height_valid(self, mock_set_size):
        self.sh.resize_browser(width=50, height=50)
        self.assertTrue(mock_set_size.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.set_window_size")
    def test_resize_window_width_valid(self, mock_set_size):
        self.sh.resize_browser(width=50)
        self.assertTrue(mock_set_size.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.set_window_size")
    def test_resize_window_height_valid(self, mock_set_size):
        self.sh.resize_browser(height=50)
        self.assertTrue(mock_set_size.called)

    def test_resize_window_invalid(self):
        self.assertRaises(selenium_helpers.DriverSizeError, self.sh.resize_browser, width="text")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.get")
    def test_get_url_bypass_valid(self, mock_get):
        self.sh.get_url("www.google.com", bypass_status_code_check=True)
        self.assertTrue(mock_get.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.get")
    def test_get_url_valid(self, mock_get):
        self.sh.get_url("http://www.google.com")
        self.assertTrue(mock_get.called)

    def test_get_url_invalid(self):
        self.assertRaises(selenium_helpers.DriverURLError, self.sh.get_url, url="google.com")

    def test_get_current_handle_valid(self):
        self.assertTrue(self.sh.get_window_handles(get_current=True))

    def test_get_window_handles_valid(self):
        self.assertEqual(len(self.sh.get_window_handles()), 1)

    def test_get_window_handles_invalid(self):
        sh = selenium_helpers.SeleniumHelpers()
        self.assertRaises(selenium_helpers.DriverAttributeError, sh.get_window_handles)

    @patch("selenium.webdriver.remote.switch_to.SwitchTo.window")
    def test_switch_handle_specific_valid(self, mock_switch):
        current_handle = self.sh.get_window_handles(get_current=True)
        self.sh.switch_window_handle(specific_handle=current_handle)
        self.assertTrue(mock_switch.called)

    @patch("selenium.webdriver.remote.switch_to.SwitchTo.window")
    def test_switch_handle_current_valid(self, mock_switch):
        self.sh.switch_window_handle()
        self.assertTrue(mock_switch.called)

    def test_switch_handle_invalid(self):
        self.assertRaises(selenium_helpers.DriverAttributeError, self.sh.switch_window_handle, specific_handle="test")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.close")
    def test_close_window_valid(self, mock_close):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(browserName="phantomjs")
        sh.close_window()
        self.assertTrue(mock_close.called)

    def test_close_window_invalid(self):
        sh = selenium_helpers.SeleniumHelpers()
        self.assertRaises(selenium_helpers.DriverAttributeError, sh.close_window)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.quit")
    def test_quit_window_valid(self, mock_quit):
        sh = selenium_helpers.SeleniumHelpers()
        sh.create_driver(browserName="phantomjs")
        sh.quit_driver()
        self.assertTrue(mock_quit.called)

    def test_quit_window_invalid(self):
        sh = selenium_helpers.SeleniumHelpers()
        self.assertRaises(selenium_helpers.DriverAttributeError, sh.quit_driver())

    @patch("selenium.webdriver.remote.webdriver.WebDriver.find_element_by_css_selector")
    def test_exist_valid(self, mock_find):
        valid_css_selector = ".valid"
        self.sh.ensure_element_exists(valid_css_selector)
        mock_find.assert_called_with(valid_css_selector)

    def test_exist_invalid(self):
        self.assertRaises(selenium_helpers.ElementError, self.sh.ensure_element_exists, ".invalid")

    def test_visible_valid(self):
        valid_css_selector = ".valid"
        self.assertTrue(self.sh.ensure_element_visible(valid_css_selector))

    def test_visible_invalid(self):
        self.assertRaises(selenium_helpers.ElementNotVisibleError, self.sh.ensure_element_visible, ".hidden")

    def test_get_valid(self):
        valid_css_selector = ".valid"
        self.assertEqual(self.sh.get_element(valid_css_selector).location, {'y': 21, 'x': 48})

    def test_get_list_of_elements_valid(self):
        valid_css_selector = ".valid-list li"
        self.assertEqual(len(self.sh.get_list_of_elements(valid_css_selector)), 3)

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_wait_valid(self, mock_wait):
        valid_css_selector = ".valid"
        self.sh.wait_for_element(valid_css_selector)
        self.assertTrue(mock_wait.called)

    def test_wait_invalid(self):
        self.assertRaises(selenium_helpers.TimeoutError, self.sh.wait_for_element, ".invalid", 1)

    @patch("selenium.webdriver.remote.webelement.WebElement.click")
    def test_click_element_valid(self, mock_click):
        valid_css_selector = ".valid a"
        self.sh.click_an_element(valid_css_selector)
        self.assertTrue(mock_click.called)

    def test_click_element_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.click_an_element, ".invalid a")

    def test_click_element_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.click_an_element, "*valid a")

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_to_element_with_offset")
    def test_click_location_valid(self, mock_click_location):
        valid_css_selector = ".valid a"
        self.sh.click_location(valid_css_selector, 30, 30)
        self.assertTrue(mock_click_location.called)

    def test_click_location_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.click_location, ".invalid a")

    def test_click_location_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.click_location, "*valid a")

    @patch("selenium.webdriver.common.action_chains.ActionChains.double_click")
    def test_double_click_valid(self, mock_double_click):
        valid_css_selector = ".valid a"
        self.sh.double_click(valid_css_selector)
        self.assertTrue(mock_double_click.called)

    def test_double_click_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.double_click, ".invalid a")

    def test_double_click_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.double_click, "@hidden a")

    @patch("selenium.webdriver.remote.webelement.WebElement.clear")
    def test_clear_valid(self, mock_clear):
        valid_css_selector = ".valid input"
        self.sh.clear_an_element(valid_css_selector)
        self.assertTrue(mock_clear.called)

    def test_clear_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.clear_an_element, ".invalid input")

    def test_clear_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.clear_an_element, "*invalid input")

    @patch("selenium.webdriver.remote.webelement.WebElement.send_keys")
    def test_fill_valid(self, mock_fill):
        valid_css_selector = ".valid input"
        self.sh.fill_an_element(valid_css_selector, "test text")
        self.assertTrue(mock_fill.called)

    def test_fill_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.fill_an_element, ".invalid input", "test text")

    def test_fill_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.fill_an_element, ".invalid &input", "test text")

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_to_element")
    def test_hover_valid(self, mock_hover):
        valid_css_selector = ".valid a"
        self.sh.hover_on_element(valid_css_selector)
        self.assertTrue(mock_hover.called)

    def test_hover_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.hover_on_element, ".invalid a")

    def test_hover_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.hover_on_element, "+invalid a")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_element_bottom_valid(self, mock_scroll_bottom):
        valid_css_selector = ".valid a"
        self.sh.scroll_to_element(valid_css_selector, position_bottom=True)
        self.assertTrue(mock_scroll_bottom.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_element_middle_valid(self,  mock_scroll_middle):
        valid_css_selector = ".valid a"
        self.sh.scroll_to_element(valid_css_selector, position_middle=True)
        self.assertTrue(mock_scroll_middle.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_element_top_valid(self, mock_scroll_top):
        valid_css_selector = ".valid a"
        self.sh.scroll_to_element(valid_css_selector)
        self.assertTrue(mock_scroll_top.called)

    def test_scroll_to_element_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.scroll_to_element, ".invalid a")

    def test_scroll_to_element_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.scroll_to_element, "*invalid a")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_position_valid(self, mock_scroll_position):
        self.sh.scroll_to_position(y_position=0, x_position=10)
        self.assertTrue(mock_scroll_position.called)

    def test_scroll_to_position_invalid(self):
        self.assertRaises(selenium_helpers.ScrollPositionError, self.sh.scroll_to_position, None, None)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_top_valid(self, mock_scroll_element_top):
        valid_css_selector = ".scrollable"
        self.sh.scroll_an_element(valid_css_selector, scroll_top=True)
        self.assertTrue(mock_scroll_element_top.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_bottom_valid(self, mock_scroll_element_bottom):
        valid_css_selector = ".scrollable"
        self.sh.scroll_an_element(valid_css_selector, scroll_bottom=True)
        self.assertTrue(mock_scroll_element_bottom.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_position_valid(self, mock_scroll_element_position):
        valid_css_selector = ".scrollable"
        self.sh.scroll_an_element(valid_css_selector, scroll_position=50)
        self.assertTrue(mock_scroll_element_position.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_valid(self, mock_scroll_element_padding):
        valid_css_selector = ".scrollable"
        self.sh.scroll_an_element(valid_css_selector, scroll_padding=5)
        self.assertTrue(mock_scroll_element_padding.called)

    def test_scroll_element_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.scroll_an_element, ".not-scrollable")

    def test_scroll_element_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.scroll_an_element, "!not-scrollable")

    def test_element_current_scroll_position_valid(self):
        valid_css_selector = ".scrollable"
        self.assertEqual(self.sh.element_current_scroll_position(valid_css_selector), 0)

    def test_element_current_scroll_position_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.element_current_scroll_position,
                          ".not-scrollable")

    def test_element_current_scroll_position_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.element_current_scroll_position, "*not-scrollable")

    def test_element_scroll_position_at_top_true_valid(self):
        valid_css_selector = ".scrollable"
        self.assertTrue(self.sh.element_scroll_position_at_top(valid_css_selector))

    def test_element_scroll_position_at_top_false_valid(self):
        valid_css_selector = ".scrollable"
        self.sh.scroll_an_element(valid_css_selector)
        self.assertFalse(self.sh.element_scroll_position_at_top(valid_css_selector))

    def test_element_scroll_position_at_top_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.element_scroll_position_at_top,
                          ".not-scrollable")

    def test_element_scroll_position_at_top_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.element_scroll_position_at_top, "*not-scrollable")

    def test_element_scroll_position_at_bottom_true_valid(self):
        valid_css_selector = ".scrollable"
        self.sh.scroll_an_element(valid_css_selector, scroll_bottom=True)
        self.assertTrue(self.sh.element_scroll_position_at_bottom(valid_css_selector))

    def test_element_scroll_position_at_bottom_false_valid(self):
        valid_css_selector = ".scrollable"
        self.assertFalse(self.sh.element_scroll_position_at_bottom(valid_css_selector))

    def test_element_scroll_position_at_bottom_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.element_scroll_position_at_bottom,
                          ".not-scrollable")

    def test_element_scroll_position_at_bottom_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.element_scroll_position_at_bottom, "*not-scrollable")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_hide_element_valid(self, mock_hide):
        valid_css_selector = ".valid"
        self.sh.hide_element(valid_css_selector)
        self.assertTrue(mock_hide.called)

    def test_hide_element_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.hide_element, ".invalid")

    def test_hide_element_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.hide_element, "*invalid")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_show_element_valid(self, mock_show):
        valid_css_selector = ".valid"
        self.sh.show_element(valid_css_selector)
        self.assertTrue(mock_show.called)

    def test_show_element_invalid(self):
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, self.sh.show_element, ".invalid")

    def test_show_element_unexpected_invalid(self):
        self.assertRaises(Exception, self.sh.show_element, "*invalid")

    def test_driver_exception_to_string_without_details(self):
        field_handler = selenium_helpers.DriverExceptions("Message text")
        error_string = field_handler.__str__()
        self.assertNotIn("stacktrace", error_string)

    def test_driver_exception_to_string_with_details(self):
        field_handler = selenium_helpers.DriverExceptions("message",
                                              "stacktrace:\nLine 1\nLine 2",
                                              {"css_selector": "selector.1"})
        error_string = field_handler.__str__()
        self.assertIn("css_selector", error_string)
        self.assertIn("stacktrace", error_string)
