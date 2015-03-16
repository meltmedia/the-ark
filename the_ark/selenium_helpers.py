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
        except common.exceptions.NoSuchElementException:
            message = "Element '{0}' not found on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.NoSuchElementException(message)

    def click_an_element(self, css_selector):
        """
        This will click an element on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.driver.find_element_by_css_selector(css_selector).click()
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to click the element '{0}' on page '{1}'.".format(css_selector, self.driver.current_url)
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
            self.driver.find_element_by_css_selector(css_selector).clear()
        except common.exceptions.ElementNotVisibleException:
            message = "Unable to clear the element '{0}' on page '{1}'.".format(css_selector, self.driver.current_url)
            raise common.exceptions.ElementNotVisibleException(message)

    def fill_an_element(self, css_selector, fill_text):
        """
        This will field a field on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
            -   fill_text:        string - The text that will be sent through to a field on page.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.click_an_element(css_selector)
            self.clear_an_element(css_selector)
            self.driver.find_element_by_css_selector(css_selector).send_keys(fill_text)
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
            hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector(css_selector))
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
            element = self.driver.find_element_by_css_selector(css_selector)

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

    def scroll_an_element(self, css_selector):
        """
        This will scroll through an element on a page.
        :param
            -   css_selector:     string - The specific element that will be interacted with.
        """