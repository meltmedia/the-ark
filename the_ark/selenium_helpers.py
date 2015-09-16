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
        try:
            if desired_capabilities.get("username") and desired_capabilities.get("access_key"):
                sauce_url = "http://{0}:{1}@ondemand.saucelabs.com:80/wd/hub".format(desired_capabilities["username"],
                                                                                     desired_capabilities["access_key"])
                self.driver = webdriver.Remote(desired_capabilities=desired_capabilities, command_executor=sauce_url)
            elif desired_capabilities.get("mobile"):
                self.driver = webdriver.Remote(desired_capabilities=desired_capabilities)
            elif desired_capabilities.get("browserName").lower() == "chrome":
                self.driver = webdriver.Chrome()
            elif desired_capabilities.get("browserName").lower() == "firefox":
                self.driver = webdriver.Firefox()
            elif desired_capabilities.get("browserName").lower() == "phantomjs":
                self.driver = webdriver.PhantomJS()
            elif desired_capabilities.get("browserName").lower() == "safari":
                self.driver = webdriver.Safari()
            else:
                message = "No driver has been created. Pass through the needed desired capabilities in order to " \
                          "create a driver. | Desired Capabilities: {0}".format(desired_capabilities)
                raise DriverAttributeError(msg=message)
            return self.driver
        except Exception as driver_creation_error:
            message = "There was an issue creating a driver with the specified desired capabilities: {0}\n" \
                      "<{1}>".format(desired_capabilities, driver_creation_error)
            raise DriverAttributeError(msg=message, stacktrace=traceback.format_exc())

    def resize_browser(self, width=None, height=None):
        """
        This will resize the browser with the given width and/or height.
        :param
            -   width:  integer - The number the width of the browser will be re-sized to.
            -   height: integer - The number the height of the browser will be re-sized to.
        """
        try:
            if not width and not height:
                pass
            elif width and height:
                self.driver.set_window_size(width, height)
            elif width:
                self.driver.set_window_size(width, self.driver.get_window_size()["height"])
            else:
                self.driver.set_window_size(self.driver.get_window_size()["width"], height)
        except Exception as resize_error:
            message = "Unable to resize the browser with the give width ({0}) and/or height ({1}) value(s)\n" \
                      "<{2}>".format(width, height, resize_error)
            raise DriverSizeError(msg=message, stacktrace=traceback.format_exc(), width=width, height=height)

    def load_url(self, url, bypass_status_code_check=False):
        """
        This will check to see if the status code of the URL is not 4XX or 5XX and navigate to the URL. If the
        bypass_status_code_check is set to True it will just navigate to the given URL.
        :param
            -   url:    string - A valid URL (e.g. "http://www.google.com")
            -   bypass_status_code_check:   boolean - Navigate to the given URL without checking the status code or not.
        """
        try:
            if bypass_status_code_check:
                self.driver.get(url)
            else:
                url_request = requests.get(url)
                if url_request.status_code == requests.codes.ok:
                    self.driver.get(url)
                else:
                    message = "The URL: {0} has the status code of: {1}. You may bypass the status code check if you " \
                              "need to navigate to this URL.".format(url, url_request.status_code)
                    raise DriverURLError(msg=message, desired_url=url)
        except Exception as get_url_error:
            message = "Unable to navigate to the desired URL: {0}\n" \
                      "<{1}>".format(url, get_url_error)
            raise DriverURLError(msg=message, stacktrace=traceback.format_exc(), desired_url=url)

    def get_current_url(self):
        """
        This will get and return the URL the driver is currently on.
        :return
            -   current_url:  string - The current URL the driver is on.
        """
        try:
            current_url = self.driver.current_url
            return current_url
        except Exception as get_current_url_error:
            message = "Unable to get the URL the driver is currently on.\n" \
                      "<{0}>".format(get_current_url_error)
            raise DriverURLError(msg=message, stacktrace=traceback.format_exc())

    def refresh_driver(self):
        """
        This will refresh the page the driver is currently on.
        """
        try:
            self.driver.refresh()
        except Exception as refresh_driver_error:
            message = "Unable to refresh the driver.\n" \
                      "<{0}>".format(refresh_driver_error)
            raise DriverURLError(msg=message, stacktrace=traceback.format_exc())

    def get_viewport_size(self, get_only_width=False, get_only_height=False):
        """
        This will get the width and/or height of the viewport. The reason for not using driver.get_window_size here
        instead is because it's not just getting the height of the viewport but the whole window (address bar,
        favorites bar, etc.). In order to be accurate this uses the driver.execute_script with scripts to get the
        clientWidth and/or clientHeight.
        :param
            -   get_only_width: boolean - Whether or not to just return the width of the viewport.
            -   get_only_height:    boolean - Whether or not to just return the height of the viewport.
        :return
            -   viewport_width: integer - The number the width of the viewport is at.
            -   viewport_height:    integer - The number the height of the viewport is at.
        """
        try:
            if get_only_width and not get_only_height:
                viewport_width = self.driver.execute_script("return document.documentElement.clientWidth")
                return viewport_width
            elif get_only_height and not get_only_width:
                viewport_height = self.driver.execute_script("return document.documentElement.clientHeight")
                return viewport_height
            else:
                viewport_width = self.driver.execute_script("return document.documentElement.clientWidth")
                viewport_height = self.driver.execute_script("return document.documentElement.clientHeight")
                return viewport_width, viewport_height
        except Exception as get_viewport_size_error:
            message = "Unable to get the width and/or the height of the viewport.\n" \
                      "<{0}>".format(get_viewport_size_error)
            raise DriverAttributeError(msg=message, stacktrace=traceback.format_exc())

    def get_window_handles(self, get_current=None):
        """
        This will get and return a list of windows or tabs currently open.
        :return
            -   current_handle:  unicode - The current window handle of the driver.
            -   window_handles:    list - A list of the current windows or tabs open in the driver.
        """
        try:
            if get_current:
                current_handle = self.driver.current_window_handle
                return current_handle
            else:
                window_handles = self.driver.window_handles
                return window_handles
        except Exception as get_handle_error:
            message = "Unable to get window handle(s).\n<{0}>".format(get_handle_error)
            raise DriverAttributeError(msg=message, stacktrace=traceback.format_exc())

    def switch_window_handle(self, specific_handle=None):
        """
        This will either switch to a specified window handle or the latest window handle.
        :param
            -   specific_handle:    unicode - The specific window handle to switch to in the driver.
        """
        try:
            if specific_handle:
                self.driver.switch_to.window(specific_handle)
            else:
                window_handles = self.get_window_handles()
                self.driver.switch_to.window(window_handles[-1])
        except Exception as window_handle_error:
            message = "Unable to switch window handles.\n<{0}>".format(window_handle_error)
            raise DriverAttributeError(msg=message, stacktrace=traceback.format_exc())

    def close_window(self):
        """
        This will close the active window of the driver.
        """
        try:
            self.driver.close()
        except Exception as close_error:
            message = "Unable to close the current window. Is it possible you already closed the window?\n" \
                      "<{0}>".format(close_error)
            raise DriverAttributeError(msg=message, stacktrace=traceback.format_exc())

    def quit_driver(self):
        """
        This will quit the driver.
        """
        try:
            self.driver.quit()
        except Exception as quit_error:
            message = "Unable to quit the driver. Is it possible you already quit the driver?\n" \
                      "<{0}>".format(quit_error)
            raise DriverAttributeError(msg=message, stacktrace=traceback.format_exc())

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

    def ensure_element_visible(self, css_selector=None, web_element=None):
        """
        This will ensure that an element is visible, if not an exception will be raised.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        if web_element:
            element_visible = web_element.is_displayed()
        else:
            self.ensure_element_exists(css_selector)
            element_visible = self.driver.find_element_by_css_selector(css_selector).is_displayed()
        if not element_visible:
            message = "The element is not visible on page '{0}'.".format(self.driver.current_url)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
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
        try:
            self.ensure_element_exists(css_selector)
            web_element = self.driver.find_element_by_css_selector(css_selector)
            return web_element
        except Exception as unexpected_error:
            message = "Unable to find and return the element '{0}' on page '{1}'.\n" \
                      "<{2}>".format(css_selector, self.driver.current_url, unexpected_error)
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

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

    def click_an_element(self, css_selector=None, web_element=None):
        """
        This will click an element on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                web_element.click()
            else:
                self.ensure_element_visible(css_selector=css_selector)
                self.get_element(css_selector).click()
        except SeleniumHelperExceptions as click_error:
            click_error.msg = "Unable to click element. | " + click_error.msg
            raise click_error
        except Exception as unexpected_error:
            message = "An nexpected error occurred attempting to click the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def click_location(self, css_selector="body", web_element=None, x_position=0, y_position=0):
        """
        Click on a specific location on the page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
            -   y_position: integer - The position at which the mouse will be placed vertically.
            -   x_position: integer - The position at which the mouse will be placed horizontally.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                ActionChains(self.driver).move_to_element_with_offset(web_element, x_position, y_position)
            else:
                self.ensure_element_visible(css_selector=css_selector)
                ActionChains(self.driver).move_to_element_with_offset(self.get_element(css_selector), x_position,
                                                                      y_position)
        except SeleniumHelperExceptions as click_location_error:
            click_location_error.msg = "Unable to click the position ({0}, {1}). | ".format(x_position, y_position) + \
                                       click_location_error.msg
            raise click_location_error
        except Exception as unexpected_error:
            message = "Unable to click at the position ({0}, {1}) of the element on page '{2}'.\n" \
                      "<{3}>".format(x_position, y_position, self.driver.current_url, unexpected_error)
            if web_element:
                message += " | Based off the WebElement passed through."
            else:
                message += " | CSS Selector: {0}".format(css_selector)
            raise ClickPositionError(msg=message, stacktrace=traceback.format_exc(),
                                     current_url=self.driver.current_url, css_selector=css_selector,
                                     y_position=y_position, x_position=x_position)

    def double_click(self, css_selector=None, web_element=None):
        """
        Double click an element on the page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                ActionChains(self.driver).double_click(web_element)
            else:
                self.ensure_element_visible(css_selector)
                ActionChains(self.driver).double_click(self.get_element(css_selector))
        except SeleniumHelperExceptions as double_click_error:
            double_click_error.msg = "Unable to double click element. | " + double_click_error.msg
            raise double_click_error
        except Exception as unexpected_error:
            message = "Unable to double-click the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def clear_an_element(self, css_selector=None, web_element=None):
        """
        This will clear a field on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                self.click_an_element(web_element=web_element)
                web_element.clear()
            else:
                self.click_an_element(css_selector=css_selector)
                self.get_element(css_selector).clear()
        except SeleniumHelperExceptions as clear_error:
            clear_error.msg = "Unable to clear element. | " + clear_error.msg
            raise clear_error
        except Exception as unexpected_error:
            message = "Unable to clear the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def fill_an_element(self, fill_text, css_selector=None, web_element=None):
        """
        This will fill a field on a page.
        :param
            -   fill_text:  string - The text that will be sent through to a field on page.
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                self.clear_an_element(web_element=web_element)
                web_element.send_keys(fill_text)
            else:
                self.clear_an_element(css_selector=css_selector)
                self.get_element(css_selector).send_keys(fill_text)
        except SeleniumHelperExceptions as fill_error:
            fill_error.msg = "Unable to fill element. | " + fill_error.msg
            raise fill_error
        except Exception as unexpected_error:
            message = "Unable to fill the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def hover_on_element(self, css_selector=None, web_element=None):
        """
        This will hover over an element on a page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                hover = ActionChains(self.driver).move_to_element(web_element)
                hover.perform()
            else:
                self.ensure_element_visible(css_selector=css_selector)
                hover = ActionChains(self.driver).move_to_element(self.get_element(css_selector))
                hover.perform()
        except SeleniumHelperExceptions as hover_error:
            hover_error.msg = "Unable to hover over element. | " + hover_error.msg
            raise hover_error
        except Exception as unexpected_error:
            message = "Unable to hover over the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def scroll_to_element(self, css_selector=None, web_element=None, position_bottom=False, position_middle=False):
        """
        This will scroll to an element on a page. This element can be put at the top, the bottom, or the middle
        (or close to) of the page.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
            -   position_top:   boolean - Whether or not the element will be at the top of the page.
            -   position_bottom:    boolean - Whether or not the element will be at the bottom of the page.
            -   position_middle:    boolean - Whether or not the element will be in the middle of the page.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                element = web_element
            else:
                self.ensure_element_visible(css_selector=css_selector)
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
            message = "Unable to scroll to the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
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

    def scroll_an_element(self, css_selector=None, web_element=None, scroll_position=None, scroll_padding=0,
                          scroll_top=False, scroll_bottom=False):
        """
        This will scroll an element on a page (i.e. An ISI modal).  The user can have it scroll to the top of the
        element, the bottom of the element, a specific position in the element, or by the height of the scrollable area
        of the element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
            -   scroll_position:    integer - The position that the element will be scrolled to.
            -   scroll_padding: integer - The amount of padding that will be used when scroll by the element's height.
            -   scroll_top: boolean - Whether or not the element will be scrolled to the top.
            -   scroll_bottom:  boolean - Whether or not the element will be scrolled to the bottom.
        """
        try:
            if web_element:
                element = web_element
                self.ensure_element_visible(web_element=web_element)
            else:
                self.ensure_element_visible(css_selector=css_selector)
                element = self.get_element(css_selector)
            if scroll_top:
                self.driver.execute_script("arguments[0].scrollTop = 0;", element)
            elif scroll_bottom:
                element_max_height = self.driver.execute_script("var element = arguments[0]; "
                                                                "var scrollHeight = element.scrollHeight; "
                                                                "var clientHeight = element.clientHeight; "
                                                                "var maxHeight = scrollHeight - clientHeight; "
                                                                "return maxHeight;", element)
                self.driver.execute_script("arguments[0].scrollTop = arguments[1];", element, element_max_height)
            elif scroll_position:
                self.driver.execute_script("arguments[0].scrollTop = arguments[1];", element, scroll_position)
            else:
                element_height = self.driver.execute_script("var element = arguments[0]; "
                                                            "var elementHeight = element.offsetHeight; "
                                                            "return elementHeight;", element)
                self.driver.execute_script("arguments[0].scrollTop += (arguments[1] - arguments[2]);", element,
                                           element_height, scroll_padding)
        except SeleniumHelperExceptions as scroll_element_error:
            scroll_element_error.msg = "Unable to scroll element. | " + scroll_element_error.msg
            raise scroll_element_error
        except Exception as unexpected_error:
            message = "Unable to scroll the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def get_element_current_scroll_position(self, css_selector=None, web_element=None):
        """
        Check to see what position the scrollable element is at.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        :return
            -   scroll_position:    integer - The amount that the element has been scrolled.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                element = web_element
            else:
                self.ensure_element_visible(css_selector=css_selector)
                element = self.get_element(css_selector)
            scroll_position = self.driver.execute_script("var element = arguments[0]; "
                                                         "scrollPosition = element.scrollTop; "
                                                         "return scrollPosition;", element)
            return scroll_position
        except SeleniumHelperExceptions as current_scroll_error:
            current_scroll_error.msg = "Unable to determine the element's scroll position. | " + \
                                       current_scroll_error.msg
            raise current_scroll_error
        except Exception as unexpected_error:
            message = "Unable to determine the scroll position of the element on page '{0}'.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def is_element_scroll_position_at_top(self, css_selector=None, web_element=None):
        """
        Check to see if the scroll position is at the top of the scrollable element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        :return
            -   at_top: boolean - Whether or not the scrollable element is at the top.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                element = web_element
            else:
                self.ensure_element_visible(css_selector=css_selector)
                element = self.get_element(css_selector)
            scroll_position = self.driver.execute_script("var element = arguments[0]; "
                                                         "scrollPosition = element.scrollTop; "
                                                         "return scrollPosition;", element)
            if scroll_position != 0:
                return False
            else:
                return True
        except SeleniumHelperExceptions as scroll_at_top_error:
            scroll_at_top_error.msg = "Unable to determine if element is scrolled to the top. | " + \
                                      scroll_at_top_error.msg
            raise scroll_at_top_error
        except Exception as unexpected_error:
            message = "Unable to determine if the scroll position of the element on page '{0}' is at the top.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def is_element_scroll_position_at_bottom(self, css_selector=None, web_element=None):
        """
        Check to see if the scroll position is at the bottom of the scrollable element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        :return
            -   at_bottom:  boolean - Whether or not the scrollable element is at the bottom.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                element = web_element
            else:
                self.ensure_element_visible(css_selector=css_selector)
                element = self.get_element(css_selector)
            element_max_height = self.driver.execute_script("var element = arguments[0]; "
                                                            "var scrollHeight = element.scrollHeight; "
                                                            "var clientHeight = element.clientHeight; "
                                                            "var maxHeight = scrollHeight - clientHeight;"
                                                            "return maxHeight;", element)
            scroll_position = self.driver.execute_script("var element = arguments[0]; "
                                                         "var scrollPosition = element.scrollTop; "
                                                         "return scrollPosition;", element)
            if scroll_position != element_max_height:
                return False
            else:
                return True
        except SeleniumHelperExceptions as scroll_at_bottom_error:
            scroll_at_bottom_error.msg = "Unable to determine if element is scrolled to the bottom. | " + \
                                         scroll_at_bottom_error.msg
            raise scroll_at_bottom_error
        except Exception as unexpected_error:
            message = "Unable to determine if the scroll position of the element on page '{0}' is at the bottom."\
                      "\n<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def hide_element(self, css_selector=None, web_element=None):
        """
        This will hide a specified element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                self.ensure_element_visible(web_element=web_element)
                element = web_element
            else:
                self.ensure_element_visible(css_selector=css_selector)
                element = self.get_element(css_selector)
            self.driver.execute_script("arguments[0].style.display = 'none';", element)
        except SeleniumHelperExceptions as hide_error:
            hide_error.msg = "Unable to hide element. | " + hide_error.msg
            raise hide_error
        except Exception as unexpected_error:
            message = "Unable to hide element on page '{0}', it may already hidden.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)

    def show_element(self, css_selector=None, web_element=None):
        """
        This will show a specified element.
        :param
            -   css_selector:   string - The specific element that will be interacted with.
            -   web_element:    object - The WebElement that will be interacted with.
        """
        try:
            if web_element:
                element = web_element
            else:
                element = self.get_element(css_selector)
            self.driver.execute_script("arguments[0].style.display = 'block';", element)
        except SeleniumHelperExceptions as show_error:
            show_error.msg = "Unable to show element. | " + show_error.msg
            raise show_error
        except Exception as unexpected_error:
            message = "Unable to show element on page '{0}', that element may not exist.\n" \
                      "<{1}>".format(self.driver.current_url, unexpected_error)
            if css_selector:
                message += " | CSS Selector: {0}".format(css_selector)
            else:
                message += " | Based off the WebElement passed through."
            raise ElementError(msg=message, stacktrace=traceback.format_exc(),
                               current_url=self.driver.current_url, css_selector=css_selector)


class SeleniumHelperExceptions(common.exceptions.WebDriverException):
    def __init__(self, msg, stacktrace, current_url):
        self.current_url = current_url
        self.details = {"current_url": self.current_url, "stacktrace": stacktrace}
        super(SeleniumHelperExceptions, self).__init__(msg=msg, stacktrace=stacktrace)

    def __str__(self):
        exception_msg = "Selenium Exception: \n"
        detail_string = "Exception Details:\n"
        for key, value in self.details.items():
            detail_string += "{0}: {1}\n".format(key, value)
        exception_msg += detail_string
        exception_msg += "Message: {0}".format(self.msg)

        return exception_msg


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
        self.details["wait_time"] = self.wait_time


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


class DriverExceptions(Exception):
    def __init__(self, msg, stacktrace=None, details=None):
        self.msg = msg
        self.details = {} if details is None else details
        self.stacktrace = stacktrace
        super(DriverExceptions, self).__init__()

    def __str__(self):
        exception_msg = "Driver Creation Exception: \n"
        if self.stacktrace is not None:
            exception_msg += "\nStacktrace: {0}\n".format(self.stacktrace)
        if self.details:
            detail_string = "\nException Details:\n"
            for key, value in self.details.items():
                detail_string += "{0}: {1}\n".format(key, value)
            exception_msg += detail_string
        exception_msg += "Message: {0}".format(self.msg)

        return exception_msg


class DriverAttributeError(DriverExceptions):
    def __init__(self, msg, stacktrace=None):
        super(DriverAttributeError, self).__init__(msg=msg, stacktrace=stacktrace)


class DriverSizeError(DriverExceptions):
    def __init__(self, msg, stacktrace=None, width=None, height=None):
        super(DriverSizeError, self).__init__(msg=msg, stacktrace=stacktrace)
        self.width = width
        self.height = height
        self.details["width"] = self.width
        self.details["height"] = self.height


class DriverURLError(DriverExceptions):
    def __init__(self, msg, stacktrace=None, desired_url=None):
        super(DriverURLError, self).__init__(msg=msg, stacktrace=stacktrace)
        self.desired_url = desired_url
        self.details["desired_url"] = self.desired_url
