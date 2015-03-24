import unittest
from the_ark import input_generator as ig
from mock import patch, Mock

#TODO: Determine how to test the random generation chances

class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        #TODO: Might need his later, i dont know
        pass

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
        field_data = {"type": "String"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string(field=field_data)
        #- field name
        field_data = {"name": "Vincent"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string(field=field_data)

        #--- General Exception
        #- With field
        field_data = {"name": "Vincent", "min": "Apples", "max": "Oranges"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string(field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_string("apples", "oranges")

    @patch("the_ark.input_generator.set_required_blank")
    def test_generate_integer(self, required_blank):
        #TODO: Test Padding
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

        #--- Test string length ranges
        required_blank.return_value = False, False
        returned_integer = ig.generate_integer(15, 15)
        self.assertEqual(returned_integer, "15")

        #--- Key Errors
        #- no name
        field_data = {"type": "String"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer(field=field_data)
        #- name in field object
        field_data = {"name": "Vincent"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer(field=field_data)

        #--- General Exception
        #- With field
        field_data = {"name": "Vincent", "min": "Apples", "max": "Oranges"}
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer(field=field_data)
        #- Without field
        with self.assertRaises(ig.InputGeneratorException):
            ig.generate_integer("apples", "oranges")
