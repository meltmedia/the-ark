from mock import patch
import os
from the_ark.selenium_helpers import SeleniumHelpers, ElementNotVisibleError, ElementError
from the_ark.screen_capture import Screenshot, ScreenshotException
import unittest

from PIL import Image
from StringIO import StringIO

ROOT = os.path.abspath(os.path.dirname(__file__))
SCREENSHOT_TEST_PNG = '{0}/etc/test.png'.format(ROOT)
All_WHITE_TEST_PNG = '{0}/etc/all_white.png'.format(ROOT)
SELENIUM_TEST_HTML = '{0}/etc/test.html'.format(ROOT)

class ScreenCaptureTestCase(unittest.TestCase):
    def setUp(self):
        self.instantiate_screenshot_class()

    @patch("the_ark.selenium_helpers.SeleniumHelpers")
    def instantiate_screenshot_class(self, selenium_helper):
        self.sc = Screenshot(selenium_helper)

    #===================================================================
    #--- Screenshot Types
    #===================================================================
    #--- Viewport Only
    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_single_viewport(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        returned_image = self.sc.screenshot_page(True)
        self.assertIsInstance(returned_image, StringIO)

    #--- Paginated
    @patch("the_ark.screen_capture.Screenshot._capture_single_viewport")
    def test_paginated_capture(self, capture_single_viewport):
        capture_single_viewport.return_value = True
        self.sc.sh.driver.excecute_script.return_value = "1200"
        # capture.return_value = True
        self.sc.paginated = True
        self.assertEqual(self.sc.screenshot_page(), [True, True])
        #TODO: Determine how best to check variables within the method (like that the scroll and padding are working)

    #--- Full Page
    @patch("the_ark.screen_capture.Screenshot._crop_and_stitch_image")
    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    @patch("the_ark.screen_capture.Screenshot._show_elements")
    @patch("the_ark.screen_capture.Screenshot._hide_elements")
    def test_capture_full_page_with_headers_and_footers(self, hide, show, image_data, crop):
        hide.return_value = True
        show.return_value = True
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        crop.return_value = Image.open(SCREENSHOT_TEST_PNG)
        self.sc.footers = ["footers"]
        self.sc.headers = ["headers"]
        returned_image = self.sc.screenshot_page()
        self.assertIsInstance(returned_image, StringIO)

    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_full_page_with_headers_only(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        self.sc.headers = ["headers"]
        returned_image = self.sc.screenshot_page()
        self.assertIsInstance(returned_image, StringIO)

    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_full_page_with_footers_only(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        self.sc.footers = ["footers"]
        returned_image = self.sc.screenshot_page()
        self.assertIsInstance(returned_image, StringIO)

    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_full_page_with_no_stickies(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        returned_image = self.sc.screenshot_page()
        self.assertIsInstance(returned_image, StringIO)

    #--- Scrolling Element
    def test_scrolling_element_with_viewport_only(self):
        sh = SeleniumHelpers()
        sc = Screenshot(sh, scroll_padding=100)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        self.assertIsInstance(sc.capture_scrolling_element(".scrollable"), list)

    def test_scrolling_element_with_full_page_capture(self):
        sh = SeleniumHelpers()
        sc = Screenshot(sh, scroll_padding=100)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        self.assertIsInstance(sc.capture_scrolling_element(".scrollable", False), list)

    #===================================================================
    #--- Helper Functions
    #===================================================================
    #--- Hide Elements
    def test_hide_elements(self):
        sh = SeleniumHelpers()
        sc = Screenshot(sh)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        link = "li.valid"
        sc._hide_elements([link])
        with self.assertRaises(ElementNotVisibleError):
            sh.click_an_element(link)

    def test_hide_elements_visibility_error(self):
        sh = SeleniumHelpers()
        sc = Screenshot(sh)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        link = "li.hidden"
        sc._hide_elements([link])

    @patch("the_ark.selenium_helpers.SeleniumHelpers.hide_element")
    def test_hide_elements_general_error(self, hide_element):
        sh = SeleniumHelpers()
        sc = Screenshot(sh)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        hide_element.side_effect = ElementError("Boo!", "stacktrace", "google", ".class")

        sc._hide_elements(["li.badClass"])

    #--- Show Elements
    def test_show_elements(self):
        sh = SeleniumHelpers()
        sc = Screenshot(sh)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        link = "li.hidden"
        sc._show_elements([link])
        sh.click_an_element(link)

    @patch("the_ark.selenium_helpers.SeleniumHelpers.show_element")
    def test_show_elements_error(self, show_element):
        sh = SeleniumHelpers()
        sc = Screenshot(sh)
        sh.create_driver(browserName="phantomjs")
        sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        show_element.side_effect = ElementError("Boo!", "stacktrace", "google", ".class")

        sc._show_elements(["li.badClass"])

    #--- Crop and Stitch
    def test_crop_and_stitch(self):
        header = Image.open(SCREENSHOT_TEST_PNG)
        footer = Image.open(SCREENSHOT_TEST_PNG)
        returned_image = self.sc._crop_and_stitch_image(header, footer)
        self.assertIsInstance(returned_image, Image.Image)

    def test_crop_and_stitch_crop_zero(self):
        header = Image.open(All_WHITE_TEST_PNG)
        footer = Image.open(All_WHITE_TEST_PNG)
        returned_image = self.sc._crop_and_stitch_image(header, footer)
        self.assertIsInstance(returned_image, Image.Image)











