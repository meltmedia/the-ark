__author__ = 'alow'

import logging
import selenium

from selenium import common
from selenium.webdriver.common.action_chains import ActionChains


class seleniumHelpers():

    def __init__(self, driver):
        """
        Methods to do various and repeatable selenium tasks.
        :param
            -   driver:     The current browser window that is being interacted with.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.driver = driver

    def ensure_element_visible(self, css_selector):
        """
        This will ensure that an element is visible, if not an exception will be raised.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """
        try:
            self.driver.find_element_by_css_selector(css_selector)
        except common.exceptions.ElementNotVisibleException:
            message = "Element '{0}' is not visible on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def find_element(self, css_selector):
        """
        Find a specific element on the page using a css_selector.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        :return
            -   web_element:      object - The WebElement object that has been found.
        """
        try:
            self.ensure_element_visible(css_selector)
            web_element = self.driver.find_element_by_css_selector(css_selector)
            return web_element
        except common.exceptions.NoSuchElementException:
            message = "Element '{0}' does not exist on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.NoSuchElementException(message)

    def click_an_element(self, css_selector):
        """
        This will click an element on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.find_element(css_selector).click()
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to click the element '{0}' on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def click_location(self, css_selector="body", x_position=0, y_position=0):
        """
        Click on a specific location on the page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
            -   y_position:     integer - The position at which the mouse will be placed vertically.
            -   x_position:     integer - The position at which the mouse will be placed horizontally.
        """
        try:
            self.ensure_element_visible(css_selector)
            ActionChains(self.driver).move_to_element_with_offset(self.find_element(css_selector), x_position,
                                                                  y_position)
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to click at the position ({0}, {1}) of the element '{2}' on page '{3}'."\
                .format(x_position, y_position, css_selector, self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def double_click(self, css_selector):
        """
        Double click an element on the page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            ActionChains(self.driver).double_click(self.find_element(css_selector))
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to double-click the element '{0}' on page '{1}'.".format(css_selector,
                                                                                       self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def clear_an_element(self, css_selector):
        """
        This will clear a field on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.click_an_element(css_selector)
            self.find_element(css_selector).clear()
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to clear the element '{0}' on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def fill_an_element(self, css_selector, fill_text):
        """
        This will fill a field on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
            -   fill_text:        string - The text that will be sent through to a field on page.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.click_an_element(css_selector)
            self.clear_an_element(css_selector)
            self.find_element(css_selector).send_keys(fill_text)
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to fill the element '{0}' on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def hover_on_element(self, css_selector):
        """
        This will hover over an element on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            hover = ActionChains(self.driver).move_to_element(self.find_element(css_selector))
            hover.perform()
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to hover over the element '{0}' on page '{1}'.".format(css_selector,
                                                                                     self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def scroll_to_element(self, css_selector, position_top=True, position_bottom=False, position_middle=False):
        """
        This will scroll to an element on a page. This element can be put at the top, the bottom, or the middle
        (or close to) of the page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
            -   position_top:     boolean - Whether or not the element will be at the top of the page.
            -   position_bottom:  boolean - Whether or not the element will be at the bottom of the page.
            -   position_middle:  boolean - Whether or not the element will be in the middle of the page.
        """
        try:
            self.ensure_element_visible(css_selector)
            element = self.find_element(css_selector)

            if position_bottom or position_middle:
                #--- Scroll the window so the bottom of the element will be at the bottom of the window.
                self.driver.execute_script("var element = arguments[0]; element.scrollIntoView(false);", element)
                if position_middle:
                    #--- Scroll the window so the element is in the middle of the window.
                    scroll_position = (self.driver.get_window_size()["height"] / 2)
                    self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_position)
            else:
                #--- Scroll the window so the top of the element will be at the top of the window.
                self.driver.execute_script("var element = arguments[0]; element.scrollIntoView(true);", element)

        except common.exceptions.ElementNotVisibleException:
            message = "Unable to scroll to the element '{0}' on page '{1}'.".format(css_selector,
                                                                                    self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def scroll_to_position(self, y_position=0, x_position=0):
        """
        This will scroll to a specific position on the current page.
        :param
            -   y_position:     integer - The position the browser will scroll to vertically.
            -   x_position:     integer - The position the browser will scroll to horizontally.
        """
        try:
            self.driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", x_position, y_position)
        except common.exceptions.WebDriverException:
            message = "Unable to scroll to position ('{0}', '{1}') on page '{2}'.".format(x_position, y_position,
                                                                                          self.driver.current_url)
            raise common.exceptions.WebDriverException(message)

    def scroll_an_element(self, css_selector, scroll_position=None, scroll_padding=0, scroll_top=False,
                          scroll_bottom=False):
        """
        This will scroll an element on a page (i.e. An ISI modal).  The user can have it scroll to the top of the
        element, the bottom of the element, a specific position in the element, or by the height of the scrollable area
        of the element.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
            -   scroll_position:  integer - The position that the element will be scrolled to.
            -   scroll_padding:   integer - The amount of padding that will be used when scroll by the element's height.
            -   scroll_top:       boolean - Whether or not the element will be scrolled to the top.
            -   scroll_bottom:    boolean - Whether or not the element will be scrolled to the bottom.
        """
        try:
            self.ensure_element_visible(css_selector)
            if scroll_top:
                self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                           "element[0].scrollTop = 0;").format(css_selector)
            elif scroll_bottom:
                element_max_height = self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                                                "var maxHeight = element[0].scrollTopMax; "
                                                                "return maxHeight;").format(css_selector)
                self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                           "element[0].scrollTop = {1};").format(css_selector, element_max_height)
            elif scroll_position:
                self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                           "element[0].scrollTop = {1};").format(css_selector, scroll_position)
            else:
                element_height = self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                                            "var elementHeight = element[0].offsetHeight; "
                                                            "return elementHeight;").format(css_selector)
                self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                           "element[0].scrollTop += ({1} + {2});").format(css_selector, element_height,
                                                                                          scroll_padding)
        except common.exceptions.WebDriverException:
            message = "Unable to scroll the element '{0}' on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.WebDriverException(message)

    def element_current_scroll_position(self, css_selector):
        """
        Check to see what position the scrollable element is at.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        :return
            -   scroll_position:  integer - The amount that the element has been scrolled.
        """
        try:
            self.ensure_element_visible(css_selector)
            scroll_position = self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                                         "scrollPosition = element[0].scrollTop; "
                                                         "return scrollPosition;").format(css_selector)
            return scroll_position
        except common.exceptions.WebDriverException:
            message = "Unable to determine the scroll position of the element '{0}' on page '{1}'."\
                .format(css_selector, self.driver.current_url)
            raise common.exceptions.WebDriverException(message)

    def element_scroll_position_at_top(self, css_selector):
        """
        Check to see if the scroll position is at the top of the scrollable element.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        :return
            -   at_top:           boolean - Whether or not the scrollable element is at the top.
        """
        try:
            self.ensure_element_visible(css_selector)
            scroll_position = self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                                         "scrollPosition = element[0].scrollTop; "
                                                         "return scrollPosition;").format(css_selector)
            if scroll_position != 0:
                at_top = False
            else:
                at_top = True
            return at_top
        except common.exceptions.WebDriverException:
            message = "Unable to determine if the scroll position of the element '{0}' on page '{1}' is at the top."\
                .format(css_selector, self.driver.current_url)
            raise common.exceptions.WebDriverException(message)

    def element_scroll_position_at_bottom(self, css_selector):
        """
        Check to see if the scroll position is at the bottom of the scrollable element.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        :return
            -   at_bottom:        boolean - Whether or not the scrollable element is at the bottom.
        """
        try:
            self.ensure_element_visible(css_selector)
            element_max_height = self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                                            "var maxHeight = element[0].scrollTopMax; "
                                                            "return maxHeight;").format(css_selector)
            scroll_position = self.driver.execute_script("var element = document.querySelectorAll('{0}'); "
                                                         "scrollPosition = element[0].scrollTop; "
                                                         "return scrollPosition;").format(css_selector)
            if scroll_position != element_max_height:
                at_bottom = False
            else:
                at_bottom = True
            return at_bottom
        except common.exceptions.WebDriverException:
            message = "Unable to determine if the scroll position of the element '{0}' on page '{1}' is at the bottom."\
                .format(css_selector, self.driver.current_url)
            raise common.exceptions.WebDriverException(message)