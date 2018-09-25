from mock import patch
import os
from PIL import Image
from the_ark import selenium_helpers
from the_ark.screen_capture import Screenshot, ScreenshotException, SeleniumError, DEFAULT_PIXEL_MATCH_OFFSET
from StringIO import StringIO
import unittest

ROOT = os.path.abspath(os.path.dirname(__file__))
SCREENSHOT_TEST_PNG = '{0}/etc/test.png'.format(ROOT)
All_WHITE_TEST_PNG = '{0}/etc/all_white.png'.format(ROOT)
All_BLACK_TEST_PNG = '{0}/etc/all_black.png'.format(ROOT)
WHITE_STRIPES_TEST_PNG = '{0}/etc/white_stripes.png'.format(ROOT)
SMALL_TEST_PNG = '{0}/etc/small.png'.format(ROOT)
SELENIUM_TEST_HTML = '{0}/etc/test.html'.format(ROOT)


class ScreenCaptureTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sh = selenium_helpers.SeleniumHelpers()
        cls.driver = cls.sh.create_driver(browserName="phantomjs")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    def setUp(self):
        self.instantiate_screenshot_class(self.sh)
        self.sh.load_url("file://{}".format(SELENIUM_TEST_HTML), bypass_status_code_check=True)

    # @patch("the_ark.selenium_helpers.SeleniumHelpers")
    def instantiate_screenshot_class(self, selenium_helper):
        self.sc = Screenshot(selenium_helper)

    # ===================================================================
    # --- Screenshot Types
    # ===================================================================
    # - Viewport Only
    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_single_viewport(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        returned_image = self.sc.capture_page(True)
        self.assertIsInstance(returned_image, StringIO)

    # - Paginated
    @patch("the_ark.screen_capture.Screenshot._capture_single_viewport")
    def test_paginated_capture(self, capture_single_viewport):
        capture_single_viewport.return_value = True
        # self.sc.sh.driver.execute_script.return_value = "1200"
        # capture.return_value = True
        self.sc.paginated = True
        self.assertEqual(self.sc.capture_page(), [True, True, True, True])

    @patch("the_ark.screen_capture.Screenshot._capture_single_viewport")
    @patch("the_ark.screen_capture.Screenshot._capture_paginated_page")
    def test_paginated_capture_with_padding(self, capture_paginated_page, capture_single_viewport):
        capture_single_viewport.return_value = True
        # self.sc.sh.driver.execute_script.return_value = "1200"
        self.sc.paginated = True
        self.sc.capture_page(False, 300)
        capture_paginated_page.assert_called_with(300)

    # - Full Page
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
        returned_image = self.sc.capture_page()
        self.assertIsInstance(returned_image, StringIO)

    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_full_page_with_headers_only(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        self.sc.headers = ["headers"]
        returned_image = self.sc.capture_page()
        self.assertIsInstance(returned_image, StringIO)

    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_full_page_with_footers_only(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        self.sc.footers = ["footers"]
        returned_image = self.sc.capture_page()
        self.assertIsInstance(returned_image, StringIO)

    @patch("the_ark.screen_capture.Screenshot._get_image_data")
    def test_capture_full_page_with_no_stickies(self, image_data):
        image_data.return_value = Image.open(SCREENSHOT_TEST_PNG)
        returned_image = self.sc.capture_page()
        self.assertIsInstance(returned_image, StringIO)

    # - Scrolling Element
    def test_scrolling_element_with_viewport_only(self):
        sc = Screenshot(self.sh, scroll_padding=100, file_extenson="bmp")
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        self.assertIsInstance(sc.capture_scrolling_element(".scrollable"), list)

    def test_scrolling_element_with_full_page_capture(self):
        sc = Screenshot(self.sh, scroll_padding=100)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        self.assertIsInstance(sc.capture_scrolling_element(".scrollable", False), list)

    # --- Horizontal Scrolling Element
    def test_horizontal_scrolling_element_with_viewport_only(self):
        sc = Screenshot(self.sh, scroll_padding=10, file_extenson="bmp")
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        self.assertIsInstance(sc.capture_horizontal_scrolling_element(".image-scroll"), list)

    def test_horizontal_scrolling_element_with_full_page_capture(self):
        sc = Screenshot(self.sh, scroll_padding=10)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        self.assertIsInstance(sc.capture_horizontal_scrolling_element(".image-scroll", False), list)

    @patch("PIL.Image")
    def test_mobile_device_capture(self, image_class):
        sc = Screenshot(self.sh, scroll_padding=100)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.desired_capabilities["mobile"] = True
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)
        image = sc._get_image_data()
        self.assertFalse(image_class.crop.called)

    # ===================================================================
    # --- Helper Functions
    # ===================================================================
    # - Hide Elements
    def test_hide_elements(self):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        link = "li.valid"
        sc._hide_elements([link])
        with self.assertRaises(selenium_helpers.ElementNotVisibleError):
            self.sh.click_an_element(link)

    def test_hide_elements_visibility_error(self):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        link = "li.hidden"
        sc._hide_elements([link])

    @patch("the_ark.selenium_helpers.SeleniumHelpers.hide_element")
    def test_hide_elements_general_error(self, hide_element):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        hide_element.side_effect = selenium_helpers.ElementError("Boo!", "stacktrace", "google", ".class")

        sc._hide_elements(["li.badClass"])

    # - Show Elements
    def test_show_elements(self):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        link = "li.hidden"
        sc._show_elements([link])
        self.sh.click_an_element(link)

    @patch("the_ark.selenium_helpers.SeleniumHelpers.show_element")
    def test_show_elements_error(self, show_element):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        show_element.side_effect = selenium_helpers.ElementError("Boo!", "stacktrace", "google", ".class")

        sc._show_elements(["li.badClass"])

    # - Crop and Stitch
    def test_crop_and_stitch(self):
        header = Image.open(SCREENSHOT_TEST_PNG)
        footer = Image.open(SCREENSHOT_TEST_PNG)
        returned_image = self.sc._crop_and_stitch_image(header, footer)
        self.assertIsInstance(returned_image, Image.Image)

    def test_crop_and_stitch_crop_zero(self):
        header = Image.open(All_BLACK_TEST_PNG)
        footer = Image.open(All_WHITE_TEST_PNG)
        returned_image = self.sc._crop_and_stitch_image(header, footer)
        self.assertIsInstance(returned_image, Image.Image)

    def test_crop_and_stitch_small_image(self):
        header = Image.open(SMALL_TEST_PNG)
        footer = Image.open(All_WHITE_TEST_PNG)
        returned_image = self.sc._crop_and_stitch_image(header, footer)
        self.assertIsInstance(returned_image, Image.Image)

    def test_crop_and_stitch_pixel_offset(self):
        header = Image.open(SMALL_TEST_PNG)
        footer = Image.open(All_WHITE_TEST_PNG)

        sc1 = Screenshot(self.sh)
        self.sc._crop_and_stitch_image(header, footer)
        self.assertEqual(sc1.pixel_match_offset, DEFAULT_PIXEL_MATCH_OFFSET)

        test_pixel_value = 20
        sc2 = Screenshot(self.sh, pixel_match_offset=test_pixel_value)
        self.sc._crop_and_stitch_image(header, footer)
        self.assertEqual(sc2.pixel_match_offset, test_pixel_value)

    @patch("numpy.array_equal")
    def test_crop_and_stitch_error(self, numpy):
        numpy.side_effect = Exception("Boo!")

        header = Image.open(SMALL_TEST_PNG)
        footer = Image.open(All_WHITE_TEST_PNG)
        with self.assertRaises(ScreenshotException):
            self.sc._crop_and_stitch_image(header, footer)

    def test_crop_and_stitch_not_100_matching_rows(self):
        header = Image.open(All_WHITE_TEST_PNG)
        footer = Image.open(WHITE_STRIPES_TEST_PNG)
        returned_image = self.sc._crop_and_stitch_image(header, footer)
        self.assertIsInstance(returned_image, Image.Image)

    # ===================================================================
    # --- Exceptions
    # ===================================================================
    @patch("the_ark.screen_capture.Screenshot._capture_full_page")
    def test_screenshot_page_selenium_error(self, capture_full_page):
        capture_full_page.side_effect = selenium_helpers.ElementError("Boo!", "stacktrace", "google", ".class")
        with self.assertRaises(SeleniumError) as selenium_error:
            self.sc.capture_page()
        self.assertIn("selenium issue", selenium_error.exception.msg)

    @patch("the_ark.screen_capture.Screenshot._capture_full_page")
    def test_screenshot_page_screenshot_error(self, capture_full_page):
        capture_full_page.side_effect = Exception("Boo!")
        with self.assertRaises(ScreenshotException) as selenium_error:
            self.sc.capture_page()
        self.assertIn("Unhandled", selenium_error.exception.msg)

    def test_screenshot_exception_to_string_with_details(self):
        error = ScreenshotException("Message text", "stacktrace\ntext\nhere", {"url": "google"})
        error_string = error.__str__()
        self.assertIn("stacktrace", error_string)
        self.assertIn("google", error_string)

    def test_scrolling_screenshot_element_selenium_error(self):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        with self.assertRaises(SeleniumError) as selenium_error:
            sc.capture_scrolling_element(".class")
        self.assertIn("selenium issue", selenium_error.exception.msg)

    @patch("the_ark.selenium_helpers.SeleniumHelpers.scroll_an_element")
    def test_scrolling_screenshot_element_screenshot_error(self, scroll_an_element):
        scroll_an_element.side_effect = Exception("Boo!")
        css_selector = ".class"
        with self.assertRaises(ScreenshotException) as selenium_error:
            self.sc.capture_scrolling_element(css_selector)
        self.assertIn("Unhandled", selenium_error.exception.msg)
        self.assertIn(css_selector, selenium_error.exception.msg)

    def test_horizontal_scrolling_screenshot_element_selenium_error(self):
        sc = Screenshot(self.sh)
        self.sh.create_driver(browserName="phantomjs")
        self.sh.load_url(SELENIUM_TEST_HTML, bypass_status_code_check=True)

        with self.assertRaises(SeleniumError) as selenium_error:
            sc.capture_horizontal_scrolling_element(".class")
        self.assertIn("selenium issue", selenium_error.exception.msg)

    @patch("the_ark.selenium_helpers.SeleniumHelpers.scroll_an_element")
    def test_horizontal_scrolling_screenshot_element_screenshot_error(self, scroll_an_element):
        scroll_an_element.side_effect = Exception("Boo!")
        css_selector = ".class"
        with self.assertRaises(ScreenshotException) as selenium_error:
            self.sc.capture_horizontal_scrolling_element(css_selector)
        self.assertIn("Unhandled", selenium_error.exception.msg)
        self.assertIn(css_selector, selenium_error.exception.msg)
