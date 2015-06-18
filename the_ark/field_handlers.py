import logging

import selenium_helpers
import traceback

class FieldHandler():

    TEXT_FIELD_TYPES = ["string", "phone", "zip_code"]

    def __init__(self, driver):
        """
        Methods that contain logic of how to handle each of the field types.
        :param driver:  The current browser window that is being interacted with.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.sh = selenium_helpers.SeleniumHelpers(driver)

    def dispatch_field(self, field):
        try:
            if field["type"].lower() in self.TEXT_FIELD_TYPES:
                confirm_css_selector = None if "confirm_css_selector" not in field else field["confirm_css_selector"]
                self.handle_text_field(field["css_selector"], field["input"], confirm_css_selector)
            if field["type"] == "select":
                first_valid = False if "first_valid" not in field else field["first_valid"]
                self.handle_select(field["css_selector"], field["input"], first_valid)
            if field["type"].lower() == "check_box":
                self.handle_check_box(field["enum"], field["input"])
            if field["type"].lower() == "drop_down":
                self.handle_drop_down(field["css_selector"], field["enum"], field["input"])

        except FieldHandlerException as fhe:
            fhe.message = "Encountered an error while handling the '{0}' field | {1}".format(field["name"], fhe.msg)
            raise fhe

        except KeyError as key:
            #TODO: Flesh out the messaging here. Mention to check the code as there may be a typo in the code
            raise MissingKey

        except Exception as e_text:
            message = "Encountered an error while handling the '{0}' field | {1}".format(field["name"], e_text)
            raise FieldHandlerException(message, stacktrace=traceback.format_exc())

    def handle_text_field(self, css_selector="", input_text="", confirm_css_selector=None):
        """

        :param css_selector:
        :param input_text:
        :param confirm_css_selector:
        :return:
        """
        try:
            #--- Handle the field
            self.sh.fill_an_element(css_selector, input_text)
            #- Fill in the confirm field as well, if provided
            if confirm_css_selector:
                self.sh.fill_an_element(confirm_css_selector, input_text)

        except selenium_helpers.SeleniumHelperExceptions as selenium_error:
            message = "An issue arose while filling in the field."
            error = SeleniumError(message, selenium_error)
            raise error

    def handle_check_box(self, enum, input_indexes):
        """

        :param enum:
        :param input_indexes:
        :return:
        """
        try:
            current_test_index = "N/A"
            #--- Handle the field
            for index in input_indexes:
                current_test_index = index
                self.sh.click_an_element(enum[index]["css_selector"])

        except KeyError as key:
            #TODO:
            message = "Key '{0}' is missing from the dictionary at " \
                      "index {1} in the enum list: {2}".format(key, current_test_index, enum[current_test_index])
            raise MissingKey(message, key, stacktrace=traceback.format_exc())

        except selenium_helpers.SeleniumHelperExceptions as selenium_error:
            message = "An issue arose while attempting to click the given checkbox element."
            error = SeleniumError(message, selenium_error)
            raise error

        except Exception as e_text:
            message = "Error while filling a Check Box field: {0}".format(e_text)
            raise FieldHandlerException(message)

    def handle_select(self, css_selector, input_index, first_valid=False):
        """

        :param enum:
        :param input_index:
        :param field:
        """
        try:
            #- Create an index offset to manage the difference in Zero Base numbering between lists and :nth-child()
            index_offset = 2
            if first_valid:
                index_offset = 1

            self.sh.click_an_element("{0} option:nth-child({1})".format(
                css_selector, input_index + index_offset))

        except selenium_helpers.SeleniumHelperExceptions as selenium_error:
            message = "An issue arose while attempting to select the given select option element."
            error = SeleniumError(message, selenium_error)
            raise error

    def handle_drop_down(self, css_selector, enum, input_index):
        """

        :param enum:
        :param input_index:
        :param field:
        """
        try:
            #--- Handle the field
            #- Click the parent element to reveal the options
            self.sh.click_an_element(css_selector)
            #- Click the option that corresponds with the css_selector in the given index of the enum
            self.sh.click_an_element(enum[input_index]["css_selector"])

        except KeyError as key:
            # TODO:
            message = "Key '{0}' is missing from the dictionary at " \
                      "index {1} in the enum list: {2}".format(key, enum[input_index])
            raise MissingKey(message, key)

        except selenium_helpers.SeleniumHelperExceptions as selenium_error:
            # TODO: Raise field handler error
            raise selenium_error

        except Exception as e_text:
            message = "Error while filling a Check Box field: {0}".format(e_text)
            raise FieldHandlerException(message)

#TODO: See how this exception looks printed out
class FieldHandlerException(Exception):
    def __init__(self, msg, stacktrace=None, details=None):
        self.msg = msg
        self.details = {} if details is None else details
        self.stacktrace = stacktrace
        super(FieldHandlerException, self).__init__()

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.details:
            detail_string = "Exception Details:\n"
            for key, value in self.details.items():
                detail_string += "{0}: {1}\n".format(key, value)
            exception_msg += detail_string
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg

class MissingKey(FieldHandlerException):
    def __init__(self, message, key, stacktrace=None):
        super(MissingKey, self).__init__(msg=message, stacktrace=stacktrace)
        self.key = key
        self.details["missing_key"] = key

class SeleniumError(FieldHandlerException):
    def __init__(self, message, selenium_helper_exception):
        new_message = "{0} | {1}".format(message, selenium_helper_exception.msg)
        super(SeleniumError, self).__init__(msg=message,
                                            stacktrace=selenium_helper_exception.stacktrace,
                                            details=selenium_helper_exception.details)


if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Firefox()
    fh = FieldHandler(driver)
    driver.get("https://braf.cd.meltqa.com/patient/resources/register")
    fh.handle_select("#currently-taking", 1, True)
    print "Yay"
