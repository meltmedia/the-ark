import re
import unittest
from datetime import datetime, timedelta
from the_ark import input_generator as ig
from mock import patch


class UtilsTestCase(unittest.TestCase):
    @patch("random.random")
    def test_set_required_blank(self, random_value):
        #--- Tests without field date
        fake_required, fake_blank = ig.set_required_blank(1)
        self.assertEqual(fake_required, None)
        self.assertEqual(fake_blank, False)

        #--- Tests with field data
        #-- Not Required
        #- Blank
        random_value.return_value = 0.20
        field_data = {"required": False}
        fake_required, fake_blank = ig.set_required_blank(5, field_data)
        self.assertEqual(fake_required, False)
        self.assertEqual(fake_blank, True)
        #- Not Blank
        random_value.return_value = 0.20
        field_data = {"required": False}
        fake_required, fake_blank = ig.set_required_blank(1, field_data)
        self.assertEqual(fake_required, False)
        self.assertEqual(fake_blank, False)
        #-- Required
        field_data = {"required": True}
        fake_required, fake_blank = ig.set_required_blank(5, field_data)
        self.assertEqual(fake_required, True)
        self.assertEqual(fake_blank, False)

    def test_check_min_vs_max(self):
        #- Test without a field
        with self.assertRaises(ig.InputGeneratorException):
            ig.check_min_vs_max(13, 12)

        #- Test with field
        field_data = {"name": "Check Min Field"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.check_min_vs_max(13, 12, field_data)

    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_string(self, required_blank):
        #--- Test default values
        required_blank.return_value = True, False
        returned_string = ig.generate_string()
        if not ig.DEFAULT_STRING_MIN <= len(returned_string) <= ig.DEFAULT_STRING_MAX:
            self.fail("The string length returned using the method defaults was incorrect. "
                      "It should be between {0} and {1} but was {2}".format(ig.DEFAULT_STRING_MIN,
                                                                            ig.DEFAULT_STRING_MAX,
                                                                            len(returned_string)))

        #--- Test blank field return
        required_blank.return_value = False, True
        self.assertEqual("", ig.generate_string())

        required_blank.return_value = False, False
        #--- Test string length ranges
        returned_string = ig.generate_string(15, 15)
        self.assertEqual(len(returned_string), 15)

        #--- Key Errors
        #- no name
        field_data = {"type": "STRING"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string(field=field_data)
        #- field name
        field_data = {"name": "String Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string(field=field_data)

        #--- General Exception
        #- With field
        field_data = {"name": "String Generator", "min": "Apples", "max": "Oranges"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string(field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string("apples", "oranges")

    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_integer(self, required_blank):
        #--- Test default values
        required_blank.return_value = True, False
        returned_integer = ig.generate_integer()
        if not ig.DEFAULT_INTEGER_MIN <= len(returned_integer) <= ig.DEFAULT_INTEGER_MAX:
            self.fail("The integer length returned using the method defaults was incorrect. "
                      "It should be between {0} and {1} but was {2}".format(ig.DEFAULT_INTEGER_MIN,
                                                                            ig.DEFAULT_INTEGER_MAX,
                                                                            len(returned_integer)))

        #--- Test blank field return
        required_blank.return_value = False, True
        self.assertEqual("", ig.generate_integer())

        #--- Test integer ranges
        required_blank.return_value = False, False
        returned_integer = ig.generate_integer(15, 15)
        self.assertEqual(returned_integer, "15")

        #--- Key Errors
        #- no name
        field_data = {"type": "INTEGER"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer(field=field_data)
        #- name in field object
        field_data = {"name": "Vincent"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer(field=field_data)

        #--- General Exception
        #- With field
        field_data = {"name": "Vincent", "min": "Apples", "max": "Oranges", "padding": 1}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer(field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer("apples", "oranges")

        #--- Test padding
        required_blank.return_value = False, False
        returned_integer = ig.generate_integer(3, 8, 4)
        self.assertEqual(len(returned_integer), 4)

    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_email(self, required_blank):
        #--- Test default values
        required_blank.return_value = True, False
        returned_email = ig.generate_email()
        if ig.DEFAULT_DOMAIN not in returned_email:
            self.assertIn(ig.DEFAULT_DOMAIN, returned_email,
                          "The generated email did not include the default domain when the default parameters were "
                          "used. It should contain '{0}' but the returned email was: '{1}'".format(ig.DEFAULT_DOMAIN,
                                                                                                   returned_email))
        #--- Test custom domain
        required_blank.return_value = True, False
        test_domain = "vincentrocks.com"
        returned_email = ig.generate_email(test_domain)
        if ig.DEFAULT_DOMAIN not in returned_email:
            self.assertIn(test_domain, returned_email,
                          "The generated email did not include the custom domain when a domain was passed in."
                          "It should contain '{0}' but the returned email was: '{1}'".format(test_domain,
                                                                                             returned_email))

        #--- Blank email
        required_blank.return_value = False, True
        returned_email = ig.generate_email(test_domain)
        self.assertEqual("", returned_email)

        #--- Passing in a field object
        required_blank.return_value = True, False
        field_data = {"domain": test_domain}
        returned_email = ig.generate_email(field=field_data)
        if ig.DEFAULT_DOMAIN not in returned_email:
            self.assertIn(test_domain, returned_email,
                          "The generated email did not include the custom domain when a field object containing "
                          "a domain was passed in. It should contain '{0}' but the returned email was: '{1}'"
                          .format(test_domain, returned_email))

        #--- Test the General Exception catch
        #- Without field data
        required_blank.side_effect = Exception('Boom!')
        self.assertRaises(ig.InputGeneratorException, ig.generate_email)
        #- With field data
        field_data = {"name": "Email Field"}
        self.assertRaises(ig.InputGeneratorException, ig.generate_email, field=field_data)

    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_phone(self, required_blank):
        #--- Test default values ########## ^\d{10}
        required_blank.return_value = True, False
        returned_phone = ig.generate_phone()
        self.assertRegexpMatches(returned_phone, "^\d{10}")

        #--- Test Blank
        required_blank.return_value = False, True
        returned_phone = ig.generate_phone()
        self.assertEqual(returned_phone, "")

        #--- Check for ###-###-#### ^[2-9]\d{2}-\d{3}-\d{4}
        #- Parameters passed in
        required_blank.return_value = True, False
        returned_phone = ig.generate_phone(dash=True)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}-\d{3}-\d{4}")
        #- Parameters from field
        field_data = {"name": "phone field", "dash": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}-\d{3}-\d{4}")

        #--- Check for ### ### #### ^[2-9]\d{2}\s\d{3}\s\d{4}
        #- Parameters passed in
        required_blank.return_value = True, False
        returned_phone = ig.generate_phone(space=True)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}\s\d{3}\s\d{4}")
        #- Parameters from field
        field_data = {"name": "phone field", "space": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}\s\d{3}\s\d{4}")

        #--- Check for (###)###-#### ^\(\d{3}\)\d{3}-\d{4}
        #- Parameters passed in
        required_blank.return_value = True, False
        returned_phone = ig.generate_phone(parenthesis=True, dash=True)
        self.assertRegexpMatches(returned_phone, "^\(\d{3}\)\d{3}-\d{4}")
        #- Parameters from field
        field_data = {"name": "phone field", "parenthesis": True, "dash": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "^\(\d{3}\)\d{3}-\d{4}")

        #--- Check for (###)####### ^\(\d{3}\)\d{7}
        #- Parameters passed in
        required_blank.return_value = True, False
        returned_phone = ig.generate_phone(parenthesis=True)
        self.assertRegexpMatches(returned_phone, "^\(\d{3}\)\d{7}")
        #- Parameters from field
        field_data = {"name": "phone field", "parenthesis": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "^\(\d{3}\)\d{7}")

        #--- Check for (###) ###-#### ^\(\d{3}\)\s\d{3}-\d{4}
        #- Parameters passed in
        returned_phone = ig.generate_phone(parenthesis=True, dash=True, space=True)
        self.assertRegexpMatches(returned_phone, "\(\d{3}\)\s\d{3}-\d{4}")
        #- Parameters from field
        field_data = {"name": "phone field", "parenthesis": True, "dash": True, "space": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "\(\d{3}\)\s\d{3}-\d{4}")

        #--- Check for ###.###.#### ^[2-9]\d{2}\.\d{3}\.\d{4}
        #-- Just Decimals
        #- Parameters passed in
        returned_phone = ig.generate_phone(decimals=True)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}\.\d{3}\.\d{4}")
        #- Parameters from field
        field_data = {"name": "phone field", "decimals": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}\.\d{3}\.\d{4}")

        #--- Decimals override everything
        #- Parameters passed in
        returned_phone = ig.generate_phone(decimals=True, parenthesis=True, dash=True, space=True)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}\.\d{3}\.\d{4}")
        #- Parameters from field
        field_data = {"name": "phone field", "decimals": True, "parenthesis": True, "dash": True, "space": True}
        returned_phone = ig.generate_phone(field=field_data)
        self.assertRegexpMatches(returned_phone, "^[2-9]\d{2}\.\d{3}\.\d{4}")

        #--- Test the General Exception catch
        #- Without field
        required_blank.return_value = "Duck", "Duck", "Goose!"
        self.assertRaises(ig.InputGeneratorException, ig.generate_phone)
        #- With field data
        field_data = {"name": "Phone Field"}
        self.assertRaises(ig.InputGeneratorException, ig.generate_phone, field=field_data)


    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_zip(self, required_blank):
        #--- Test default values
        required_blank.return_value = True, False
        returned_zip = ig.generate_zip_code()
        self.assertEqual(len(returned_zip), 5)

        #--- Blank Zip
        required_blank.return_value = False, True
        returned_zip = ig.generate_zip_code()
        self.assertEqual("", returned_zip)

        #--- Test the General Exception catch
        required_blank.side_effect = Exception('Boom!')
        #- Without field
        self.assertRaises(ig.InputGeneratorException, ig.generate_zip_code)
        #- With field
        field_data = {"name": "Email Field"}
        self.assertRaises(ig.InputGeneratorException, ig.generate_zip_code, field=field_data)

    @patch("random.random")
    def test_generate_index(self, random_result):
        #--- Test default values
        returned_index = ig.generate_index()
        if returned_index not in range(0, 2):
            self.fail("The index generated using the method defaults was incorrect. "
                      "It should be between 0 and {0} but was {1}".format(ig.DEFAULT_INDEX_OPTIONS, returned_index))

        #--- Test Required
        field_data = {"required": True, "enum": {"stuff": "more_stuff"}}
        self.assertEqual(0, ig.generate_index(field=field_data))

        #--- Always Random
        enums = {}
        for i in range(0, 100):
            enums["key{0}".format(i)] = "value{0}".format(i)
        field_data = {"required": True, "enum": enums, "random": True}
        generated_indexes = []
        for i in range(0, 10):
            generated_indexes.append(ig.generate_index(test_number=1, field=field_data))
        if all(x == generated_indexes[0] for x in generated_indexes):
            self.fail("The indexes generated in the Always Random check were not different!")

        #--- All options already used, not blank
        enums = {}
        random_result.return_value = 0.5
        for i in range(0, 100):
            enums["key{0}".format(i)] = "value{0}".format(i)
        field_data = {"required": True, "enum": enums}
        generated_indexes = []
        for i in range(0, 10):
            generated_indexes.append(ig.generate_index(test_number=1000, field=field_data))
        if all(x == generated_indexes[0] for x in generated_indexes):
            self.fail("The indexes generated in the Always Random check were not different!")

        #--- All options already used, blank
        random_result.return_value = 0.2
        field_data = {"required": False, "enum": {"stuff": "more_stuff",
                                                  "stuff2": "more_stuff2",
                                                  "stuff3": "more_stuff3",
                                                  "stuff4": "more_stuff4",
                                                  "stuff5": "more_stuff5"}}

        self.assertEqual("", ig.generate_index(test_number=10, field=field_data))

        #--- Key Errors
        #- With name
        field_data = {"name": "Index Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_index(field=field_data)
        #- Without name
        field_data = {"fake": "data"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_index(field=field_data)

        #--- General Exception
        #- With field
        field_data = {"name": "Index Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_index("apples", field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_index("apples")

    def test_generate_select(self):
        #--- General Exception
        field_data = {"name": "Select Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_select("apples", field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_select("apples")

    def test_generate_drop_down(self):
        #--- General Exception
        field_data = {"name": "Select Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_drop_down("apples", field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_drop_down("apples")

    def test_generate_radio(self):
        #--- General Exception
        field_data = {"name": "Select Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_radio("apples", field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_radio("apples")

    @patch("random.random")
    def test_generate_check_box(self, random_result):
        #--- Test default values
        returned_index = ig.generate_check_box()
        if not isinstance(returned_index, list):
            self.fail("The index array generated by the default parameters was not... an array. "
                      "It should be a list, but this was returned: {0}".format(returned_index))

        #--- Test Required
        field_data = {"required": True, "enum": {"stuff": "more_stuff"}}
        self.assertEqual([0], ig.generate_check_box(field=field_data))

        #--- Blank
        random_result.return_value = .20
        field_data = {"required": False, "enum": {"stuff": "more_stuff", "things": "more_things"}}
        self.assertEqual([], ig.generate_check_box(test_number=10, field=field_data))

        #--- Not Required, but not blank
        random_result.return_value = .50
        self.assertIsInstance(ig.generate_check_box(test_number=10, field=field_data), list)

        #--- Random Choice
        random_result.return_value = .50
        enums = {}
        number_of_indexes = 5
        for i in range(0, number_of_indexes):
            enums["key{0}".format(i)] = "value{0}".format(i)
        field_data = {"required": True, "enum": enums}
        generated_indexes = ig.generate_check_box(test_number=10, field=field_data)
        self.assertEqual(len(generated_indexes), number_of_indexes)

        #--- Test Number == Number of Options
        random_result.return_value = .50
        field_data = {"required": True, "enum": {"stuff": "more_stuff", "things": "more_things"}}
        self.assertEqual([1], ig.generate_check_box(test_number=2, field=field_data))

        #--- Key Errors
        #- With name
        field_data = {"name": "Check Box Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_check_box(field=field_data)
        #- Without name
        field_data = {"fake": "data"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_check_box(field=field_data)

        #--- General Exception
        #- With field
        field_data = {"name": "Check Box Generator", "required": True, "enum": 6}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_check_box("apples", field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_check_box("apples")

    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_date(self, required_blank):
        #--- Test Defaults
        required_blank.return_value = True, False
        returned_date = ig.generate_date()
        #- Format Check
        try:
            datetime.strptime(returned_date, ig.DEFAULT_DATE_FORMAT)
        except Exception as e:
            self.fail("The default settings for generate_date() did not return a date in the default format "
                      "of {0}. The date returned was '{1}': {2}".format(ig.DEFAULT_DATE_FORMAT, returned_date, e))

        #--- Blank Date
        required_blank.return_value = False, True
        returned_date = ig.generate_date()
        self.assertEqual("", returned_date, "The check for blank dates did not return a blank string")

        #--- Date Range Checks (in the past)
        required_blank.return_value = True, False
        #-- Past in days (int)
        start_date = 4
        end_date = 2
        expected_date_format = ig.DEFAULT_DATE_FORMAT
        returned_date = ig.generate_date(start_date, end_date)
        try:
            formatted_date = datetime.strptime(returned_date, ig.DEFAULT_DATE_FORMAT).date()
        except Exception as e:
            self.fail("When checking the date range, could not convert the returned date into '{0}' format in "
                      "order to compare the dates. The returned date was {1}: {2}".format(expected_date_format,
                                                                                          returned_date, e))
        #- Returned Date older than current date
        self.assertGreater(datetime.now().date(), formatted_date,
                           "When using days, in the past, the returned date was not older than the current date")
        #- Returned Date older than end date
        self.assertGreater((datetime.now() - timedelta(days=end_date)).date(),
                           formatted_date,
                           "When using days, in the past, the returned date was not older than the end date")
        #-- Past in dates (%Y-%m-%d) with "%Y/%d/%m" format
        expected_format = "%Y/%d/%m"
        start_date = datetime.strptime("19800404", "%Y%m%d").date()
        end_date = datetime.strptime("20150325", "%Y%m%d").date()
        returned_date = ig.generate_date(str(start_date), str(end_date), expected_format)
        #- Check returned date format
        try:
            formatted_date = datetime.strptime(returned_date, expected_format).date()
        except Exception as e:
            self.fail("When checking the date range with custom format, could not convert the returned date into '{0}'"
                      " format in order to compare the dates. The returned date was {1}: {2}"
                      .format(expected_format, returned_date, e))
        #- Returned Date older than current date
        self.assertGreater(formatted_date, start_date,
                           "When using dates, in the past, the returned date was not older than the start date")
        #- Returned Date older than end date
        self.assertGreater(end_date, formatted_date,
                           "When using dates, in the past, the returned date was not older than the end date")

        #--- Date Range Checks (in the FUTURE!!! *cue sci-fi sound effects)
        required_blank.return_value = True, False
        #-- Future in days (int)
        start_date = -4
        end_date = -20
        expected_date_format = ig.DEFAULT_DATE_FORMAT
        returned_date = ig.generate_date(start_date, end_date)
        try:
            formatted_date = datetime.strptime(returned_date, ig.DEFAULT_DATE_FORMAT).date()
        except Exception as e:
            self.fail("When checking the date range in the future, could not convert the returned date into '{0}' "
                      "format in order to compare the dates. The returned date was {1}: {2}"
                      .format(expected_date_format, returned_date, e))
        #- Returned Date later than current date
        self.assertGreater(formatted_date, datetime.now().date(),
                           "When using days, in the future, the returned date was not later than the current date")
        #- Returned Date older than end date
        self.assertGreater((datetime.now() - timedelta(days=end_date)).date(), formatted_date,
                           "When using days, in the past, the returned date was not older than the end date")
        #-- Future in dates (%Y-%m-%d) with "%m-%d-%y" format, using a field
        expected_future_format = "%m-%d-%y"
        start_date = datetime.strptime("20250404", "%Y%m%d").date()
        end_date = datetime.strptime("20300325", "%Y%m%d").date()
        field_data = {"start_date": str(start_date), "end_date": str(end_date), "date_format": expected_future_format}
        returned_date = ig.generate_date(field=field_data)
        #- Check returned date format
        try:
            formatted_date = datetime.strptime(returned_date, expected_future_format).date()
        except Exception as e:
            self.fail("When checking the future date range with custom format, could not convert the returned date "
                      "into '{0}' format in order to compare the dates. The returned date was {1}: {2}"
                      .format(expected_future_format, returned_date, e))
        #- Returned Date later than current date
        self.assertGreater(formatted_date, datetime.now().date(),
                           "When using dates, in the future, the returned date was not later than the start date")
        #- Returned Date older than end date
        self.assertGreater(end_date, formatted_date,
                           "When using dates, in the future, the returned date was not older than the end date")

        #--- General Exception
        #- With field
        field_data = {"name": "Date Generator"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_date("apples", field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_date("apples")