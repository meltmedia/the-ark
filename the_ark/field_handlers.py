import logging

from selenium import common
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected_condition
import selenium_helpers

#TODO: Remove These after debugging
from selenium import webdriver, common
import time


class FieldHandler():

    def __init__(self, driver):
        """
        Methods that contain logic of how to handle each of the field types.
        :param
            -   driver:     The current browser window that is being interacted with.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.sh = selenium_helpers.SeleniumHelpers(driver)

    def handle_text_field(self, css_selector="", input_text="", field=None):
        """

        :param css_selector:
        :param input_text:
        :param field:
        :return:
        """
        try:
            #--- Set up variables, overwriting them if a field was passed in
            css_selector = css_selector if not field else field["css_selector"]
            input_text = input_text if not field else field["input"]

            #--- Handle the field
            self.sh.fill_an_element(css_selector, input_text)

        except KeyError as key:
            message = ". The '{0}' key is required when filling a text entry type field.".format(key)
            raise FieldHandlerException(message)

        except selenium_helpers as e_text:
            raise FieldHandlerException(e_text)

    def handle_integer(self, css_selector="", input_integer="", field=None):
        """

        :param css_selector:
        :param input_integer:
        :param field:
        :return:
        """

        try:
            self.handle_text_field(css_selector, input_integer, field)

        except KeyError as key:
            message = "Error while filling an Integer field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ". The {0} key is required when passing a field object into the handle_integer method".format(
                key)
            raise FieldHandlerException(message)

        except Exception as e_text:
            message = "Error while filling an Integer field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ": {0}".format(e_text)
            raise FieldHandlerException(message)

    def handle_email(self, css_selector="", email="", field=None):
        """

        :param css_selector:
        :param email:
        :param field:
        :return:
        """
        try:
            #--- Set up variables, overwriting them if a field was passed in
            css_selector = css_selector if not field else field["css_selector"]
            email = email if not field else field["input"]

            #--- Handle the field
            self.sh.clear_an_element(css_selector)
            self.sh.click_an_element(css_selector)
            self.sh.fill_an_element(css_selector, email)

        except KeyError as key:
            message = "Error while filling an Email field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ". The {0} key is required when passing a field object into the handle_email method".format(
                key)
            raise FieldHandlerException(message)

        except Exception as e_text:
            message = "Error while filling an Email field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ": {0}".format(e_text)
            raise FieldHandlerException(message)

    def handle_phone(self, css_selector="", phone="", field=None):
        """

        :param css_selector:
        :param phone:
        :param field:
        :return:
        """
        try:
            #--- Set up variables, overwriting them if a field was passed in
            css_selector = css_selector if not field else field["css_selector"]
            phone = phone if not field else field["input"]

            #--- Handle the field
            self.sh.clear_an_element(css_selector)
            self.sh.click_an_element(css_selector)
            self.sh.fill_an_element(css_selector, phone)

        except KeyError as key:
            message = "Error while filling a Phone field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ". The {0} key is required when passing a field object into the handle_phone method".format(
                key)
            raise FieldHandlerException(message)

        except Exception as e_text:
            message = "Error while filling a Phone field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ": {0}".format(e_text)
            raise FieldHandlerException(message)

    def handle_check_box(self, enum="", input_indexes="", field=None):
        """

        :param enum:
        :param input_indexes:
        :param field:
        :return:
        """
        try:
            #--- Set up variables, overwriting them if a field was passed in
            enum = enum if not field else field["enum"]
            input_indexes = input_indexes if not field else field["input"]

            if enum == "":
                enum = [{}]
            if input_indexes == "":
                input_indexes = [1]

            #--- Handle the field
            for index in input_indexes:
                self.sh.click_an_element(enum[index]["css_selector"])

        except KeyError as key:
            message = "Error while filling a Check Box field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ". The {0} key is required when passing a field object into the handle_check_box method".format(
                key)
            raise FieldHandlerException(message)

        except Exception as e_text:
            message = "Error while filling a Check Box field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ": {0}".format(e_text)
            raise FieldHandlerException(message)

    def handle_drop_down(self, enum="", input_index="", field=None):
        """

        :param enum:
        :param input_index:
        :param field:
        :return:
        """
        try:
            # --- Set up variables, overwriting them if a field was passed in
            enum = enum if not field else field["enum"]
            input_index = input_index if not field else field["input"]

            if enum == "":
                enum = [{}]
            if input_index == "":
                input_index = 1

            #--- Handle the field
            #TODO: Verify drop down schema for clicking the parent
            self.sh.click_an_element(field["css_selector"])
            self.sh.click_an_element(enum[input_index]["css_selector"])

        except KeyError as key:
            message = "Error while filling a Drop Down field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ". The {0} key is required when passing a field object into the handle_drop_down method".format(
                key)
            raise FieldHandlerException(message)

        except Exception as e_text:
            message = "Error while filling a Drop Down field"
            if "name" in field.keys():
                message += " named '{0}'".format(field["name"])
            message += ": {0}".format(e_text)
            raise FieldHandlerException(message)


class FieldHandlerException(Exception):
    pass