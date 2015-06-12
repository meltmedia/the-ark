__author__ = 'alow'

import os
import unittest

from mock import create_autospec
from mock import patch
from selenium.webdriver import PhantomJS
from the_ark import selenium_helpers

ROOT = os.path.abspath(os.path.dirname(__file__))
SELENIUM_TEST_HTML = '{0}/etc/test.html'.format(ROOT)


class SeleniumHelpersTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    def setUp(self):
        self.driver.get(SELENIUM_TEST_HTML)

    def test_exist_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        ensure_function = create_autospec(sh.ensure_element_exists)
        ensure_function(valid_css_selector)
        ensure_function.assert_called_once_with(valid_css_selector)

    def test_exist_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.ElementError, sh.ensure_element_exists, ".invalid")

    def test_visible_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        self.assertEqual(sh.ensure_element_visible(valid_css_selector), True)

    def test_visible_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.ElementNotVisibleError, sh.ensure_element_visible, ".hidden")

    def test_get_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        self.assertEqual(sh.get_element(valid_css_selector).location, {'y': 21, 'x': 48})

    @patch("selenium.webdriver.support.ui.WebDriverWait.until")
    def test_wait_valid(self, mock_wait):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.wait_for_element(valid_css_selector)
        self.assertTrue(mock_wait.called)

    def test_wait_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.TimeoutError, sh.wait_for_element, ".invalid", 1)

    @patch("selenium.webdriver.remote.webelement.WebElement.click")
    def test_click_element_valid(self, mock_click):
        valid_css_selector = ".valid a"
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        sh.click_an_element(valid_css_selector)
        self.assertTrue(mock_click.called)

    def test_click_element_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.click_an_element, ".invalid a")

    def test_click_element_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.click_an_element, "*valid a")

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_to_element_with_offset")
    def test_click_location_valid(self, mock_click_location):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.click_location(valid_css_selector, 30, 30)
        self.assertTrue(mock_click_location.called)

    def test_click_location_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.click_location, ".invalid a")

    def test_click_location_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.click_location, "*valid a")

    @patch("selenium.webdriver.common.action_chains.ActionChains.double_click")
    def test_double_click_valid(self, mock_double_click):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.double_click(valid_css_selector)
        self.assertTrue(mock_double_click.called)

    def test_double_click_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.double_click, ".invalid a")

    def test_double_click_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.double_click, "@hidden a")

    @patch("selenium.webdriver.remote.webelement.WebElement.clear")
    def test_clear_valid(self, mock_clear):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid input"
        sh.clear_an_element(valid_css_selector)
        self.assertTrue(mock_clear.called)

    def test_clear_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.clear_an_element, ".invalid input")

    def test_clear_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.clear_an_element, "*invalid input")

    @patch("selenium.webdriver.remote.webelement.WebElement.send_keys")
    def test_fill_valid(self, mock_fill):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid input"
        sh.fill_an_element(valid_css_selector, "test text")
        self.assertTrue(mock_fill.called)

    def test_fill_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.fill_an_element, ".invalid input", "test text")

    def test_fill_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.fill_an_element, ".invalid &input", "test text")

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_to_element")
    def test_hover_valid(self, mock_hover):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.hover_on_element(valid_css_selector)
        self.assertTrue(mock_hover.called)

    def test_hover_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.hover_on_element, ".invalid a")

    def test_hover_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.hover_on_element, "+invalid a")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_element_bottom_valid(self, mock_scroll_bottom):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.scroll_to_element(valid_css_selector, position_bottom=True)
        self.assertTrue(mock_scroll_bottom.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_element_middle_valid(self,  mock_scroll_middle):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.scroll_to_element(valid_css_selector, position_middle=True)
        self.assertTrue(mock_scroll_middle.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_element_top_valid(self, mock_scroll_top):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.scroll_to_element(valid_css_selector)
        self.assertTrue(mock_scroll_top.called)

    def test_scroll_to_element_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.scroll_to_element, ".invalid a")

    def test_scroll_to_element_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.scroll_to_element, "*invalid a")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_to_position_valid(self, mock_scroll_position):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        sh.scroll_to_position(y_position=0, x_position=10)
        self.assertTrue(mock_scroll_position.called)

    def test_scroll_to_position_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.ScrollPositionError, sh.scroll_to_position, None, None)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_top_valid(self, mock_scroll_element_top):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_top=True)
        self.assertTrue(mock_scroll_element_top.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_bottom_valid(self, mock_scroll_element_bottom):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_bottom=True)
        self.assertTrue(mock_scroll_element_bottom.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_position_valid(self, mock_scroll_element_position):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_position=50)
        self.assertTrue(mock_scroll_element_position.called)

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_scroll_element_valid(self, mock_scroll_element_padding):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_padding=5)
        self.assertTrue(mock_scroll_element_padding.called)

    def test_scroll_element_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.scroll_an_element, ".not-scrollable")

    def test_scroll_element_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.scroll_an_element, "!not-scrollable")

    def test_element_current_scroll_position_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        self.assertEqual(sh.element_current_scroll_position(valid_css_selector), 0)

    def test_element_current_scroll_position_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.element_current_scroll_position,
                          ".not-scrollable")

    def test_element_current_scroll_position_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.element_current_scroll_position, "*not-scrollable")

    def test_element_scroll_position_at_top_true_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        self.assertEqual(sh.element_scroll_position_at_top(valid_css_selector), True)

    def test_element_scroll_position_at_top_false_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector)
        self.assertEqual(sh.element_scroll_position_at_top(valid_css_selector), False)

    def test_element_scroll_position_at_top_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.element_scroll_position_at_top,
                          ".not-scrollable")

    def test_element_scroll_position_at_top_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.element_scroll_position_at_top, "*not-scrollable")

    def test_element_scroll_position_at_bottom_true_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_bottom=True)
        self.assertEqual(sh.element_scroll_position_at_bottom(valid_css_selector), True)

    def test_element_scroll_position_at_bottom_false_valid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        self.assertEqual(sh.element_scroll_position_at_bottom(valid_css_selector), False)

    def test_element_scroll_position_at_bottom_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.element_scroll_position_at_bottom,
                          ".not-scrollable")

    def test_element_scroll_position_at_bottom_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.element_scroll_position_at_bottom, "*not-scrollable")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_hide_element_valid(self, mock_hide):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.hide_element(valid_css_selector)
        self.assertTrue(mock_hide.called)

    def test_hide_element_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.hide_element, ".invalid")

    def test_hide_element_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.hide_element, "*invalid")

    @patch("selenium.webdriver.remote.webdriver.WebDriver.execute_script")
    def test_show_element_valid(self, mock_show):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.show_element(valid_css_selector)
        self.assertTrue(mock_show.called)

    def test_show_element_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(selenium_helpers.SeleniumHelperExceptions, sh.show_element, ".invalid")

    def test_show_element_unexpected_invalid(self):
        sh = selenium_helpers.SeleniumHelpers(self.driver)
        self.assertRaises(Exception, sh.show_element, "*invalid")
