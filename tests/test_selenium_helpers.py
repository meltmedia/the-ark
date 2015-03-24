__author__ = 'alow'

import os
import unittest

from mock import patch, Mock
from the_ark import selenium_helpers
from selenium.common import exceptions
from selenium.webdriver import PhantomJS

rhino_client_ojb = None
ROOT = os.path.abspath(os.path.dirname(__file__))
SELENIUM_TEST_HTML = '{0}/etc/test.html'.format(ROOT)
driver = None


class SeleniumHelpersTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = PhantomJS()

    def test_ensure_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.ensure_element_visible(valid_css_selector)

    def test_ensure_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.ensure_element_visible, ".invalid")

    def test_find_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.find_element(valid_css_selector)

    def test_find_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.find_element, ".invalid")

    def test_wait_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.wait_for_element(valid_css_selector)

    def test_wait_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.TimeoutException, sh.wait_for_element, ".invalid", 1)

    def test_click_element_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.click_an_element(valid_css_selector)

    def test_click_element_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.click_an_element, ".invalid a")

    def test_click_location_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.click_location(valid_css_selector, 30, 30)

    def test_click_location_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.click_location, ".invalid a")

    def test_double_click_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.double_click(valid_css_selector)

    def test_double_click_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.double_click, ".invalid a")

    def test_clear_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid input"
        sh.clear_an_element(valid_css_selector)

    def test_clear_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.clear_an_element, ".invalid input")

    def test_fill_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid input"
        sh.fill_an_element(valid_css_selector, "test text")

    def test_fill_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.fill_an_element, ".invalid input", "test text")

    def test_hover_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.hover_on_element(valid_css_selector)

    def test_hover_invali(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.hover_on_element, ".invalid a")

    def test_scroll_to_element_bottom_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.scroll_to_element(valid_css_selector, position_bottom=True)

    def test_scroll_to_element_middle_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.scroll_to_element(valid_css_selector, position_middle=True)

    def test_scroll_to_element_top_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid a"
        sh.scroll_to_element(valid_css_selector)

    def test_scroll_to_element_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.scroll_to_element, ".invalid a")

    def test_scroll_to_position_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        sh.scroll_to_position(x_position=0, y_position=10)

    def test_scroll_to_position_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.WebDriverException, sh.scroll_to_position, None, None)

    def test_scroll_element_top_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_top=True)

    def test_scroll_element_bottom_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_bottom=True)

    def test_scroll_element_position_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_position=50)

    def test_scroll_element_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_padding=5)

    def test_scroll_element_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.WebDriverException, sh.scroll_an_element, ".not-scrollable")

    def test_element_current_scroll_position_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        self.assertEqual(sh.element_current_scroll_position(valid_css_selector), 0)

    def test_element_current_scroll_position_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.WebDriverException, sh.element_current_scroll_position, ".not-scrollable")

    def test_element_scroll_position_at_top_true_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        self.assertEqual(sh.element_scroll_position_at_top(valid_css_selector), True)

    def test_element_scroll_position_at_top_false_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector)
        self.assertEqual(sh.element_scroll_position_at_top(valid_css_selector), False)

    def test_element_scroll_position_at_top_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.WebDriverException, sh.element_scroll_position_at_top, ".not-scrollable")

    def test_element_scroll_position_at_bottom_true_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        sh.scroll_an_element(valid_css_selector, scroll_bottom=True)
        self.assertEqual(sh.element_scroll_position_at_bottom(valid_css_selector), True)

    def test_element_scroll_position_at_bottom_false_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".scrollable"
        self.assertEqual(sh.element_scroll_position_at_bottom(valid_css_selector), False)

    def test_element_scroll_position_at_bottm_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.WebDriverException, sh.element_scroll_position_at_bottom, ".not-scrollable")

    def test_hide_element_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.hide_element(valid_css_selector)

    def test_hide_element_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.hide_element, ".invalid")

    def test_show_element_valid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        valid_css_selector = ".valid"
        sh.show_element(valid_css_selector)

    def test_show_element_invalid(self):
        self.driver.get(SELENIUM_TEST_HTML)
        sh = selenium_helpers.seleniumHelpers(self.driver)
        self.assertRaises(exceptions.NoSuchElementException, sh.show_element, ".invalid")