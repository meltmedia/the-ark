import logging

import requests
from selenium import common
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected_condition
import traceback


class SeleniumHelpers:

    def __init__(self):
        """
        Methods to do various and repeatable selenium tasks.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.driver = None

    def create_driver(self, **desired_capabilities):
        """
        Creating a driver with the desired settings.
        :param
            -   desired_capabilities:   dictionary - Settings used to set up the desired browser.
        """
        if desired_capabilities.get("username") and desired_capabilities.get("access_key"):
            sauce_url = "http://{0}:{1}@ondemand.saucelabs.com:80/wd/hub".format(desired_capabilities["username"],
                                                                                 desired_capabilities["access_key"])
            self.driver = webdriver.Remote(desired_capabilities=desired_capabilities, command_executor=sauce_url)
        elif desired_capabilities.get("browserName").lower() == "chrome":
            self.driver = webdriver.Chrome()
        elif desired_capabilities.get("browserName").lower() == "firefox":
            self.driver = webdriver.Firefox()
        elif desired_capabilities.get("browserName").lower() == "phantomjs":
            self.driver = webdriver.PhantomJS()
        # elif desired_capabilities.get("browserName").lower() == "safari":
        #     self.driver = webdriver.Safari()
        elif desired_capabilities.get("mobile"):
            self.driver = webdriver.Remote(desired_capabilities=desired_capabilities)

    def resize_browser(self, width=None, height=None):
        """
        This will resize the browser with the given width and/or height.
        :param
            -   width:  integer - The number the width of the browser will be re-sized to.
            -   height: integer - The number the height of the browser will be re-sized to.
        """
        if width and height:
            self.driver.set_window_size(width, height)
        elif width:
            self.driver.set_window_size(width, self.driver.get_window_size()["height"])
        elif height:
            self.driver.set_window_size(self.driver.get_window_size()["width"], height)

    def get_url(self, url, bypass_status_code_check=False):
        """
        This will check to see if the status code of the URL is not 4XX or 5XX and navigate to the URL. If the
        bypass_status_code_check is set to True it will just navigate to the given URL.
        :param
            -   url:    string - A valid URL (e.g. "http://www.google.com")
            -   bypass_status_code_check:   boolean - Navigate to the given URL without checking the status code or not.
        """
        if bypass_status_code_check:
            self.driver.get(url)
        else:
            url_request = requests.get(url)
            if url_request.status_code == requests.codes.ok:
                self.driver.get(url)

    def get_window_handles(self, get_current=None):
        """
        This will get and return a list of windows or tabs currently open.
        :return
            -   current_handle:  unicode - The current window handle of the driver.
            -   window_handles:    list - A list of the current windows or tabs open in the driver.
        """
        if get_current:
            current_handle = self.driver.current_window_handle
            return current_handle
        else:
            window_handles = self.driver.window_handles
            return window_handles

    def switch_window_handle(self, specific_handle=None):
        """
        This will either switch to a specified window handle or the latest window handle.
        :param
            -   specific_handle:    unicode - The specific window handle to switch to in the driver.
        """
        if specific_handle:
            self.driver.switch_to.window(specific_handle)
        else:
            window_handles = self.get_window_handles()
            self.driver.switch_to.window(window_handles[-1])

    def close_window(self):
        """
        This will close the active window of the driver.
        """
        try:
            self.driver.close()
        except AttributeError as close_error:
            raise close_error

    def quit_driver(self):
        """
        This will quit the driver.
        """
        try:
            self.driver.quit()
        except AttributeError as quit_error:
            raise quit_error

    def ensure_element_exists(self, css_selector):
        """
        This will ensure that an element exists on the page under test, if not an exception will be raised.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.driver.find_element_by_css_selector(css_selector)
        except common.exceptions.NoSuchElementException as no_such:
            message = "Element '{0}' does not exist on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, no_such)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def ensure_element_visible(self, css_selector):
        """
        This will ensure that an element is visible, if not an exception will be raised.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        self.ensure_element_exists(css_selector)
        element_visible = self.driver.find_element_by_css_selector(css_selector).is_displayed()
        if not element_visible:
            message = "Element '{0}' is not visible on page '{1}'.".format(css_selector, self.driver.current_url)
            raise ElementNotVisibleError(msg=message, stacktrace=traceback.format_exc(),
                                         current_url=self.driver.current_url, css_selector=css_selector)
        else:
            return element_visible

    def get_element(self, css_selector):
        """
        Find a specific element on the page using a css_selector.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        :return
            -   web_element:    object - The WebElement object that has been found.
        """
        self.ensure_element_visible(css_selector)
        web_element = self.driver.find_element_by_css_selector(css_selector)
        return web_element

    def get_list_of_elements(self, css_selector):
        """
        Return a full list of elements from a drop down menu, checkboxes, radio buttons, etc.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        :return
            -   list_of_elements:   list - The full list of web elements from a parent selector (e.g. drop down menus)
        """
        self.ensure_element_visible(css_selector)
        list_of_elements = self.driver.find_elements_by_css_selector(css_selector)
        return list_of_elements

    def wait_for_element(self, css_selector, wait_time=15):
        """
        This will wait for a specific element to be present on the page within a specified amount of time, in seconds.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   wait_time:  integer - The amount of time, in seconds, given to wait for an element to be present.
        """
        try:
            WebDriverWait(self.driver, wait_time).until(expected_condition.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                        css_selector)))
        except common.exceptions.TimeoutException as timeout:
            message = "Element '{0}' does not exist on page '{1}' after waiting {2} seconds.\n" \
                      "<{3}>".format(css_selector, self.driver.current_url, wait_time, timeout)
            raise TimeoutError(msg=message, stacktrace=traceback.format_exc(), current_url=self.driver.current_url,
                               css_selector=css_selector, wait_time=wait_time)

    def click_an_element(self, css_selector):
        """
        This will click an element on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.get_element(css_selector).click()
        except SeleniumHelperExceptions as click_error:
            click_error.msg = "Unable to click element. | " + click_error.msg
            raise click_error
        except Exception as unexpected_error:
            message = "Unexpected error occurred attempting to click the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def click_location(self, css_selector="body", x_position=0, y_position=0):
        """
        Click on a specific location on the page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   y_position: integer - The position at which the mouse will be placed vertically.
            -   x_position: integer - The position at which the mouse will be placed horizontally.
        """
        try:
            self.ensure_element_visible(css_selector)
            ActionChains(self.driver).move_to_element_with_offset(self.get_element(css_selector), x_position,
                                                                  y_position)
        except SeleniumHelperExceptions as click_location_error:
            click_location_error.msg = "Unable to click the position ({0}, {1}). | ".format(x_position, y_position) + \
                                       click_location_error.msg
            raise click_location_error
        except Exception as unexpected_error:
            message = "Unable to click at the position ({0}, {1}) of the element '{2}' on page '{3}'.\n" \
                      "<{4}>".format(x_position, y_position, css_selector, self.driver.current_url, unexpected_error)
            raise ClickPositionError(msg=message, stacktrace=traceback.format_exc(),
                                     current_url=self.driver.current_url, css_selector=css_selector,
                                     y_position=y_position, x_position=x_position)

    def double_click(self, css_selector):
        """
        Double click an element on the page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            ActionChains(self.driver).double_click(self.get_element(css_selector))
        except SeleniumHelperExceptions as double_click_error:
            double_click_error.msg = "Unable to double click element. | " + double_click_error.msg
            raise double_click_error
        except Exception as unexpected_error:
            message = "Unable to double-click the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def clear_an_element(self, css_selector):
        """
        This will clear a field on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.click_an_element(css_selector)
            self.get_element(css_selector).clear()
        except SeleniumHelperExceptions as clear_error:
            clear_error.msg = "Unable to clear element. | " + clear_error.msg
            raise clear_error
        except Exception as unexpected_error:
            message = "Unable to clear the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def fill_an_element(self, css_selector, fill_text):
        """
        This will fill a field on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   fill_text:  string - The text that will be sent through to a field on page.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.click_an_element(css_selector)
            self.clear_an_element(css_selector)
            self.get_element(css_selector).send_keys(fill_text)
        except SeleniumHelperExceptions as fill_error:
            fill_error.msg = "Unable to fill element. | " + fill_error.msg
            raise fill_error
        except Exception as unexpected_error:
            message = "Unable to fill the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def hover_on_element(self, css_selector):
        """
        This will hover over an element on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            hover = ActionChains(self.driver).move_to_element(self.get_element(css_selector))
            hover.perform()
        except SeleniumHelperExceptions as hover_error:
            hover_error.msg = "Unable to hover over element. | " + hover_error.msg
            raise hover_error
        except Exception as unexpected_error:
            message = "Unable to hover over the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def scroll_to_element(self, css_selector, position_bottom=False, position_middle=False):
        """
        This will scroll to an element on a page. This element can be put at the top, the bottom, or the middle
        (or close to) of the page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   position_top:   boolean - Whether or not the element will be at the top of the page.
            -   position_bottom:    boolean - Whether or not the element will be at the bottom of the page.
            -   position_middle:    boolean - Whether or not the element will be in the middle of the page.
        """
        try:
            self.ensure_element_visible(css_selector)
            element = self.get_element(css_selector)

            if position_bottom or position_middle:
                # Scroll the window so the bottom of the element will be at the bottom of the window.
                self.driver.execute_script("var element = arguments[0]; element.scrollIntoView(false);", element)
                if position_middle:
                    # Scroll the window so the element is in the middle of the window.
                    scroll_position = (self.driver.get_window_size()["height"] / 2)
                    self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_position)
            else:
                # Scroll the window so the top of the element will be at the top of the window.
                self.driver.execute_script("var element = arguments[0]; element.scrollIntoView(true);", element)

        except SeleniumHelperExceptions as scroll_to_element_error:
            scroll_to_element_error.msg = "Unable to scroll to element. | " + scroll_to_element_error.msg
            raise scroll_to_element_error
        except Exception as unexpected_error:
            message = "Unable to scroll to the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def scroll_to_position(self, y_position=0, x_position=0):
        """
        This will scroll to a specific position on the current page.
        :param
            -   y_position: integer - The position the browser will scroll to vertically.
            -   x_position: integer - The position the browser will scroll to horizontally.
        """
        if type(y_position) == int or type(x_position) == int:
            self.driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", x_position, y_position)
        else:
            message = "Unable to scroll to position ('{0}', '{1}') on page '{2}'.".format(x_position, y_position,
                                                                                          self.driver.current_url)
            raise ScrollPositionError(msg=message, stacktrace=traceback.format_exc(),
                                      current_url=self.driver.current_url, y_position=y_position, x_position=x_position)

    def scroll_an_element(self, css_selector, scroll_position=None, scroll_padding=0, scroll_top=False,
                          scroll_bottom=False):
        """
        This will scroll an element on a page (i.e. An ISI modal).  The user can have it scroll to the top of the
        element, the bottom of the element, a specific position in the element, or by the height of the scrollable area
        of the element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   scroll_position:    integer - The position that the element will be scrolled to.
            -   scroll_padding: integer - The amount of padding that will be used when scroll by the element's height.
            -   scroll_top: boolean - Whether or not the element will be scrolled to the top.
            -   scroll_bottom:  boolean - Whether or not the element will be scrolled to the bottom.
        """
        try:
            self.ensure_element_visible(css_selector)
            if scroll_top:
                self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                           "element.scrollTop = 0;", css_selector)
            elif scroll_bottom:
                element_max_height = self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                                                "var scrollHeight = element.scrollHeight; "
                                                                "var clientHeight = element.clientHeight; "
                                                                "var maxHeight = scrollHeight - clientHeight; "
                                                                "return maxHeight;", css_selector)
                self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                           "element.scrollTop = arguments[1];", css_selector, element_max_height)
            elif scroll_position:
                self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                           "element.scrollTop = arguments[1];", css_selector, scroll_position)
            else:
                element_height = self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                                            "var elementHeight = element.offsetHeight; "
                                                            "return elementHeight;", css_selector)
                self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                           "element.scrollTop += (arguments[1] - arguments[2]);", css_selector,
                                           element_height, scroll_padding)
        except SeleniumHelperExceptions as scroll_element_error:
            scroll_element_error.msg = "Unable to scroll element. | " + scroll_element_error.msg
            raise scroll_element_error
        except Exception as unexpected_error:
            message = "Unable to scroll the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def element_current_scroll_position(self, css_selector):
        """
        Check to see what position the scrollable element is at.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        :return
            -   scroll_position:    integer - The amount that the element has been scrolled.
        """
        try:
            self.ensure_element_visible(css_selector)
            scroll_position = self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                                         "scrollPosition = element.scrollTop; "
                                                         "return scrollPosition;", css_selector)
            return scroll_position
        except SeleniumHelperExceptions as current_scroll_error:
            current_scroll_error.msg = "Unable to determine the element's scroll position. | " + \
                                       current_scroll_error.msg
            raise current_scroll_error
        except Exception as unexpected_error:
            message = "Unable to determine the scroll position of the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def element_scroll_position_at_top(self, css_selector):
        """
        Check to see if the scroll position is at the top of the scrollable element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        :return
            -   at_top: boolean - Whether or not the scrollable element is at the top.
        """
        try:
            self.ensure_element_visible(css_selector)
            scroll_position = self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                                         "scrollPosition = element.scrollTop; "
                                                         "return scrollPosition;", css_selector)
            if scroll_position != 0:
                return False
            else:
                return True
        except SeleniumHelperExceptions as scroll_at_top_error:
            scroll_at_top_error.msg = "Unable to determine if element is scrolled to the top. | " + \
                                      scroll_at_top_error.msg
            raise scroll_at_top_error
        except Exception as unexpected_error:
            message = "Unable to determine if the scroll position of the element '{0}' on page '{1}' is at the top.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def element_scroll_position_at_bottom(self, css_selector):
        """
        Check to see if the scroll position is at the bottom of the scrollable element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        :return
            -   at_bottom:  boolean - Whether or not the scrollable element is at the bottom.
        """
        try:
            self.ensure_element_visible(css_selector)
            element_max_height = self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                                            "var scrollHeight = element.scrollHeight; "
                                                            "var clientHeight = element.clientHeight; "
                                                            "var maxHeight = scrollHeight - clientHeight;"
                                                            "return maxHeight;", css_selector)
            scroll_position = self.driver.execute_script("var element = document.querySelector(arguments[0]); "
                                                         "var scrollPosition = element.scrollTop; "
                                                         "return scrollPosition;", css_selector)
            if scroll_position != element_max_height:
                return False
            else:
                return True
        except SeleniumHelperExceptions as scroll_at_bottom_error:
            scroll_at_bottom_error.msg = "Unable to determine if element is scrolled to the bottom. | " + \
                                         scroll_at_bottom_error.msg
            raise scroll_at_bottom_error
        except Exception as unexpected_error:
            message = "Unable to determine if the scroll position of the element '{0}' on page '{1}' is at the bottom."\
                      "\n<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def hide_element(self, css_selector):
        """
        This will hide a specified element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.driver.execute_script("document.querySelector(arguments[0]).style.display = 'none';", css_selector)
        except SeleniumHelperExceptions as hide_error:
            hide_error.msg = "Unable to hide element. | " + hide_error.msg
            raise hide_error
        except Exception as unexpected_error:
            message = "Unable to hide element '{0}' on page '{1}', it may already hidden.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def show_element(self, css_selector):
        """
        This will show a specified element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
        """
        try:
            self.ensure_element_visible(css_selector)
            self.driver.execute_script("document.querySelector(arguments[0]).style.display = 'block';", css_selector)
        except SeleniumHelperExceptions as show_error:
            show_error.msg = "Unable to show element. | " + show_error.msg
            raise show_error
        except Exception as unexpected_error:
            message = "Unable to show element '{0}' on page '{1}', that element may not exist.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)


class SeleniumHelperExceptions(common.exceptions.WebDriverException):
    def __init__(self, msg, stacktrace, current_url):
        self.current_url = current_url
        self.details = {"current_url": self.current_url}
        super(SeleniumHelperExceptions, self).__init__(msg=msg, stacktrace=stacktrace)


class ElementError(SeleniumHelperExceptions):
    def __init__(self, msg, stacktrace, current_url, css_selector):
        super(ElementError, self).__init__(msg=msg, stacktrace=stacktrace, current_url=current_url)
        self.css_selector = css_selector
        self.details["css_selector"] = self.css_selector


class ElementNotVisibleError(SeleniumHelperExceptions):
    def __init__(self, msg, stacktrace, current_url, css_selector):
        super(ElementNotVisibleError, self).__init__(msg=msg, stacktrace=stacktrace, current_url=current_url)
        self.css_selector = css_selector
        self.details["css_selector"] = self.css_selector


class TimeoutError(SeleniumHelperExceptions):
    def __init__(self, msg, stacktrace, current_url, css_selector, wait_time):
        super(TimeoutError, self).__init__(msg=msg, stacktrace=stacktrace, current_url=current_url)
        self.css_selector = css_selector
        self.wait_time = wait_time
        self.details["css_selector"] = self.css_selector
        self.details["wait time"] = self.wait_time


class ClickPositionError(SeleniumHelperExceptions):
    def __init__(self, msg, stacktrace, current_url, css_selector, y_position, x_position):
        super(ClickPositionError, self).__init__(msg=msg, stacktrace=stacktrace, current_url=current_url)
        self.css_selector = css_selector
        self.y_position = y_position
        self.x_position = x_position
        self.details["css_selector"] = self.css_selector
        self.details["y_position"] = self.y_position
        self.details["x_position"] = self.x_position


class ScrollPositionError(SeleniumHelperExceptions):
    def __init__(self, msg, stacktrace, current_url, y_position, x_position):
        super(ScrollPositionError, self).__init__(msg=msg, stacktrace=stacktrace, current_url=current_url)
        self.y_position = y_position
        self.x_position = x_position
        self.details["y_position"] = self.y_position
        self.details["x_position"] = self.x_position
