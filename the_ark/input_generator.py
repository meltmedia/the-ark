__author__ = 'vbraun'

from datetime import datetime, timedelta
import inspect
import logging
import random
import string
import time

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s at line %(lineno)d - %(message)s (%(threadName)s)',
                    datefmt='%Y-%m-%d %I:%M:%S %p',
                    level='INFO')
log = logging.getLogger("InputGenerator")

#TODO: Add a "Random" option to the SELECT Field type, for things like State and year, etc.
#TODO: Add a parameter to the SELECT Field that lets the code know whether the first option is selectable (if even possible/needed)
#TODO: Add an underscore to the ZIP_CODE field type
#TODO: Add "padding" option to the INTEGER Field type, for doing month as 04, etc.

def _set_required_blank(test_number, field):
    """Sets a generation method's values for whether the field is currently required and if it is not, whether
        to leave it blank.
    :param
        -   test_number:    Dict containing a site config
        -   field:          The field object. Should include a key:value for all pertinent information to its field type
    :returns
        bool, bool:         Both the required and leave_blank values generated
    """
    #- Instantiate the variables to their defaults
    required = None
    leave_blank = False

    #- Set "required" to the value of the corresponding key in the field object
    if field:
        required = field["required"]

    #- If the field is not required, do logic to determine whether to leave it blank upon fill
    if required is False:
        #- Always fill in the field on the first test...
        if test_number != 1:
            # ... but give 25% chance to leave blank otherwise
            leave_blank = True if random.random() < .25 == 1 else False

    return required, leave_blank


def _check_min_vs_max(min_length, max_length, field):
    if min_length > max_length:
        message = "The minimum cannot be greater than the maximum value"
        if field:
            message += ". Please review the 'min' and 'max' values for the field"
        raise InputGeneratorException(message)


def generate_string(min_length=1, max_length=10, test_number=None, field=None):
    """ Creates a str object with a length greater than min_length and less than max_length, made up of randomly
        selected upper and lowercase letters.
    :param
        -   min_length:     The minimum length, in characters, that the generated string can be. Defaults to 1
        -   max_length:     The maximum length, in characters, that the generated string can be. Defaults to 10
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether the field has been populated previously and whether to leave it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. If the object has "min" and "max" keys, those values will override the "min_length"
                            and "max_length" parameters.
    :returns
        -   string:         The randomly generated or blank string
    """
    try:
        #- Reset min and max lengths with the field object values
        min_length = min_length if not field else field["min"]
        max_length = max_length if not field else field["max"]
        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        #- Ensure the minmium and maximum values create a valid range
        _check_min_vs_max(min_length, max_length, field)

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create a string
        if leave_blank:
            random_string = ""
        else:
            random_string = "".join(random.choice(string.ascii_letters) for f in range(random.randint(min_length,
                                                                                                      max_length)))

        return random_string

    except Exception as e_text:
        message = "Error while generating a String"
        if field and "name" in field.keys():
            message += " for the {0} field".format(field["name"].upper())
        message += ": {0}".format(e_text)
        raise InputGeneratorException(message)


def generate_integer(min_int=1, max_int=9, padding=1, test_number=None, field=None):
    """ Generates an str object with an int character that is greater that min_int and less than max_int.
    :param
        -   min_int:        The minimum value that the generated integer can be. Defaults to 1
        -   max_int:        The maximum value that the generated integer can be. Defaults to 9
        -   padding:        The number of characters the string will be. if the int created is 2 characters, but a
                            padding of 3 is given, then two leading zeroes are be added to make the int three characters
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether the field has been populated previously and whether to leave it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. If the object has "min" and "max" keys, those values will override the "min_int" and
                            "max_int" parameters.
    :returns
        -   integer:        The randomly generated, or blank integer
    """
    try:
        #- Reset min, max and padding variables with the field object values
        min_int = min_int if not field else field["min"]
        max_int = max_int if not field else field["max"]
        padding = padding if not field else field["padding"]
        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        # - Ensure the minimum and maximum values create a valid range
        _check_min_vs_max(min_int, max_int, field)

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create an integer
        if leave_blank:
            integer = ""
        else:
            #- Create the integer value between the min and max and with the padding provided
            integer = "{0:0{1}d}".format(random.randint(min_int, max_int), padding)

        return integer

    except KeyError as key:
        message = "Error while generating an Integer"
        if "name" in field.keys():
            message += " for the {0} field".format(field["name"])
        message += ". The {0} key is required when passing a field object into the generate_integer method".format(key)
        raise InputGeneratorException(message)

    except Exception as e_text:
        message = "Error while generating an Integer"
        if field and "name" in field.keys():
            message += " for the {0} field".format(field["name"].upper())
        message += ": {0}".format(e_text)
        raise InputGeneratorException(message)


def generate_email(domain="meltmedia.com", test_number=None, field=None):
    """ Generates a random email address in the firstname.lastname@domain format
    :param
        -   domain:         The domain address the email will be from ie. @domain. This defaults to "meltmedia.com"
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether the field has been populated previously and whether to leave it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. Only the "required" key is used while generating an email field input.
    :returns
        -   string:         The randomly generated, or blank email string
    """
    try:
        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create an email
        if leave_blank:
            email = ""
        else:
            #--- Create an email in the firstname.lastname@domain format.
            #-   The first and last names are generated using the generate_string method
            first_name = generate_string(6, 10)
            last_name = generate_string(6, 10)
            email = "{0}.{1}@{2}".format(first_name, last_name, domain)

        return email

    except KeyError as key:
        message = "Error while generating an Email"
        if "name" in field.keys():
            message += " for the {0} field".format(field["name"])
        message += ". The {0} key is required when passing a field object into the generate_email method".format(key)
        raise InputGeneratorException(message)

    except Exception as e_text:
        message = "Error while generating an Email"
        if field and "name" in field.keys():
            message += " for the {0} field".format(field["name"].upper())
        message += ": {0}".format(e_text)
        raise InputGeneratorException(message)


def generate_phone(decimals=False, parenthesis=False, dash=False, space=False, test_number=None, field=None):
    """ Generates a random phone number
    :param
        -   decimals:       Bool used to determine whether to put a decimals between each of the portions of the phone
                            number. When True this parameter supersedes the others as you cannot have both decimals and
                            parenthesis, or decimals and space or dash, etc.
        -   parenthesis:    Bool used to determine whether to put a parenthesis around the Area Code of the generated
                            number. The default value is False
        -   dash:           Bool used to determine whether to put a dash between the first three and last 4 digits of
                            the phone number. The default value is False
        -   space:          Bool used to determine whether to put a space between the area code and number portions
                             of the phone number. The default value is False
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether the field has been populated previously and whether to leave it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. Only the "required" key is used while generating an phone field input.
    :returns
        -   integer:        The randomly generated, or blank phone number
    """

    #TODO: Other formats to add: ###-###-#### all dashes, (###)### #### no space after parenth
    try:
        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create a phone number
        if leave_blank:
            phone_number = ""
        else:
            #--- Generate the Area Code portion of the phone number
            #- Area Code should not start with 0's or 1's
            area_code = "".join(str(random.randint(2, 9)) for x in range(0, 3))

            #--- Generate the number portion of the phone number
            #- The first three digits of the number should not start with 0's or 1's
            start = "".join(str(random.randint(2, 9)) for x in range(0, 3))
            finish = "".join(str(random.randint(0, 9)) for y in range(0, 4))

            #--- Format the number
            #- Use only the decimal formatting if the user specified they wanted decimals
            if decimals:
                phone_number = "{0}.{1}.{2}".format(area_code, start, finish)
            else:
                #- Surround the area code in parenthesis if parenthesis parameter is True
                area_code = "({0})".format(area_code) if parenthesis else area_code

                #- Format the "number" portion of the phone number
                #  Dash takes precedence over space
                if dash:
                    #- Add the dash between the start and finish of the number if dash parameter is True
                    number = "{0}-{1}".format(start, finish)
                elif space:
                    #- Add a space if space parameter is True, but dash is False
                    number = "{0} {1}".format(start, finish)
                else:
                    number = "{0}{1}".format(start, finish)

                #- Plug the area code and number together
                if space:
                    phone_number = "{0} {1}".format(area_code, number)
                else:
                    phone_number = area_code + number

        return phone_number

    except KeyError as key:
        message = "Error while generating a Phone Number"
        if "name" in field.keys():
            message += " for the {0} field".format(field["name"])
        message += ". The {0} key is required when passing a field object into the generate_phone method".format(key)
        raise InputGeneratorException(message)

    except Exception as e_text:
        message = "Error while generating a Phone Number"
        if field and "name" in field.keys():
            message += " for the {0} field".format(field["name"].upper())
        message += ": {0}".format(e_text)
        raise InputGeneratorException(message)


def generate_zip_code(test_number=None, field=None):
    """ Generates a random 5 digit string to act as a ZIP code
    :param
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether the field has been populated previously and whether to leave it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. Only the "required" key is used while generating an ZIP Code field input.
    :returns
        -   sting:          The randomly generated, or blank ZIP Code string
    """
    try:
        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create a zip code
        if leave_blank:
            zip_code = ""
        else:
            #--- Generate the ZIP Code
            #- Prevent the first number from being 0 so that it is not truncated when the output is viewed in Excel
            first = str(random.randint(1, 9))
            #- The last four digits are between 0 and 9
            zip_code = first + "".join(str(random.randint(0, 9)) for z in range(0, 4))

        return zip_code

    except KeyError as key:
        message = "Error while generating a Zip Code"
        if "name" in field.keys():
            message += " for the {0} field".format(field["name"])
        message += ". The {0} key is required when passing a field object into the generate_zip_code method".format(key)
        raise InputGeneratorException(message)

    except Exception as e_text:
        raise InputGeneratorException("Zip Code generation error: {0}".format(e_text))


def _generate_index(num_of_options=2, test_number=None, field=None):
    """ Calculates which option should be selected from the given field based on test number. The index is randomly
        selected after all options have been used at least once.
    :param
        -   num_of_options: The number oof options available in the list. If a field object is passed in then this
                            value is overwritten by the "enum" key for that field. Defaults to a value of 2
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether all options for the field have been used or not and whether to leave
                            it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. The "required", "enum" and "random" keys are used to calculate the input index.
    :returns
        -   integer:        The randomly generated, or blank index to select from the field's options
    """
    #TODO: Consider using this code block when filling out this field type:
    # selected_option = driver.find_elements_by_css_selector("{0} options:nth-child({1})".format(field_config["css_selector"], (test_number % len(field_config["enums"])) + 1))
    try:
        #--- Reset min and max lengths with the field object values
        num_of_options = num_of_options if not field else len(field["enum"])
        required = None if not field else field["required"]
        #- Set whether the form should always select a random value or not.
        #  The field must have a "random" key set to override this value (Radio and Drop Down field also pass in here)
        always_random = None if not field or "random" not in field.keys() else field["random"]

        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        leave_blank = False
        random_choice = None
        all_options_used = True if test_number > num_of_options else False

        #--- Always choose a random index if all options have already been sent once
        if all_options_used:
            random_choice = True
            #- But give a 25% chance of leaving the field blank too
            if not required and random.random() < .25:
                leave_blank = True

        #--- Generate the input index to use when filling out this field
        if leave_blank:
            #- Set the return to a blank string if leave_blank is true.
            #TODO: Decide how best to handle the blank selection, can't interact with it as an integer if it's ""
            input_index = ""
        elif random_choice or always_random:
            #- Select a random index if the field is "random" or if all options have already been selected previously
            input_index = random.randint(0, num_of_options - 1)
        else:
            #- Select the modulo unless the test_number and number of options is the same, then select the last index
            if test_number == num_of_options:
                input_index = num_of_options - 1
            else:
                input_index = test_number % num_of_options - 1

        return input_index

    except InputGeneratorException:
        print "yeah"
    except Exception as e_text:
        raise InputGeneratorException(e_text)


def generate_select(num_of_options=2, test_number=None, field=None):
    """ Calculates which option should be selected from the select list based on test number. The index is randomly
        selected after all options have been used at least once.
    :param
        -   num_of_options: The number oof options available in the list. If a field object is passed in then this
                            value is overwritten by the "enum" key for that field. Defaults to a value of 2
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether all options for the field have been used or not and whether to leave
                            it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. The "required", "enum" and "random" keys are used to calculate the input index.
    :returns
        -   integer:        The randomly generated, or blank index to select from the field's options
    """
    try:
        return _generate_index(num_of_options, test_number, field)
    except InputGeneratorException as e_text:
        raise InputGeneratorException("Select Field input index generator error: {0}".format(e_text))


def generate_drop_down(num_of_options=2, test_number=None, field=None):
    """ Calculates which option should be selected from the drop down list based on test number. The index is randomly
        selected after all options have been used at least once.
    :param
        -   num_of_options: The number oof options available in the list. If a field object is passed in then this
                            value is overwritten by the "enum" key for that field. Defaults to a value of 2
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether all options for the field have been used or not and whether to leave
                            it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. The "required" and "enum" keys are used to calculate the input index
    :returns
        -   integer:        The randomly generated, or blank index to select from the field's options
    """
    try:
        return _generate_index(num_of_options, test_number, field)

    except InputGeneratorException as e_text:
        raise InputGeneratorException("Drop Down Field input index generator error: {0}".format(e_text))


def generate_radio(num_of_options=2, test_number=None, field=None):
    """ Calculates which radio button from the list of buttons should be selected based on test number. The index is
        randomly selected after all options have been used at least once.
    :param
        -   num_of_options: The number oof options available in the list. If a field object is passed in then this
                            value is overwritten by the "enum" key for that field. Defaults to a value of 2
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether all options for the field have been used or not and whether to leave
                            it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. The "required" and "enum" keys are used to calculate the input index
    :returns
        -   integer:        The randomly generated, or blank index to select from the field's options
    """
    try:
        return _generate_index(num_of_options, test_number, field)

    except Exception as e_text:
        raise InputGeneratorException("Radio Field input index generator error: {0}".format(e_text))


def generate_check_box(num_of_options=1, test_number=None, field=None):
    """ Calculates which check box from the list of boxes should be selected based on test number. The index is
        randomly selected after all options have been used at least once. When randomly selecting there is a chance
        that more than one of the checkboxes will be selected.
    :param
        -   num_of_options: The number oof options available in the list. If a field object is passed in then this
                            value is overwritten by the "enum" key for that field. Defaults to a value of 1
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether all options for the field have been used or not and whether to leave
                            it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. The "required" and "enum" keys are used to calculate the input index
    :returns
        -   list:           A list of indexes (integers) to select from the check box list when filling out this form
    """
    try:
        #- Reset min and max lengths with the field object values
        num_of_options = num_of_options if not field else len(field["enum"])
        required = None if not field else field["required"]

        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        leave_blank = False
        random_choice = None
        all_options_used = True if test_number > num_of_options else False

        #- 25% chance of leaving the field blank if it is not required and all options have already been used
        if required is False and all_options_used:
            if random.random() < .25:
                leave_blank = True

        #- Always select a random index if all options have already been used
        if all_options_used:
            random_choice = True

        input_indexes = []

        if leave_blank:
            pass
        elif random_choice:
            #--- Add at least one item to the input list
            index = random.randint(0, num_of_options - 1)
            input_indexes.append(index)
            #--- 50/50 chance of adding another input index to the list
            while random.randint(0, 1) == 1 and len(input_indexes) <= num_of_options:
                #- Cycle through indexes until finding one that is not already being used
                while index in input_indexes:
                    index = random.randint(0, num_of_options - 1)
                #- Add the index to the list
                input_indexes.append(index)
        else:
            #- Select the modulo unless the test_number and number of options is the same, then select the last index
            if test_number == num_of_options:
                input_indexes.append(num_of_options - 1)
            else:
                input_indexes.append(test_number % num_of_options - 1)

        return input_indexes

    except Exception as e_text:
        raise InputGeneratorException("Check Box Field input index generator error: {0}".format(e_text))


def generate_date(start_date=None, end_date=None, date_format="%m/%d/%Y", test_number=None, field=None):
    """ Generates a date in the given date format. By default this date will be -18 to -100 years ago in order to keep
        the user over the age of 18 when filling out birthdays. However these dates can be passed through if need be.
    :param
        -   start_date:     Date in "%Y-%m-%d" format or an integer specifying days. This is the default format for
                            datetime.now().date(). This date is used as the furthest back in history the generated date
                            will be. If the user sends through an integer rather than a date the integer will be used
                            to specify how many days in the past to start generating from. If the integer value is
                            negative, then the start date will be in the future. If no start date is given the date
                            100 years, or 52*100 weeks, ago will be used.
        -   end_date:       Date in "%Y-%m-%d" format or an integer specifying days. This is the default format for
                            datetime.now().date(). This date is used as the most recent day in history the generated
                            date will be. If the user sends through an integer rather than a date the integer will be
                            used to specify how many days in the past to stop generating from. If the integer value is
                            negative, then the end date will be in the future. If no end date is given an end date of
                            18 years, or 52*18 weeks, ago will be used.
        -   date_format:    The format you'd like the date to be when it is returned. This defaults to %m/%d/%Y which
                            would make a MM/DD/YYYY format. Other format examples are %y-%m-%d to get YY-MM-DD or
                            %d%m%Y to get DDMMYYYY, etc.
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether all options for the field have been used or not and whether to leave
                            it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. The "required" and "enum" keys are used to calculate the input index
    :returns
        -   string:         A string formatted to look like a date
    """
    try:
        start_date = start_date if not field or "start_date" not in field.keys() else field["start_date"]
        end_date = end_date if not field or "end_date" not in field.keys() else field["end_date"]

        if start_date and isinstance(start_date, int):
            start_date = str((datetime.now() - timedelta(days=start_date)).date())
        if end_date and isinstance(end_date, int):
            end_date = str((datetime.now() - timedelta(days=end_date)).date())

        if not start_date:
            start_date = start_date if start_date else str((datetime.now() - timedelta(weeks=52 * 18)).date())
        if not end_date:
            end_date = end_date if end_date else str((datetime.now() - timedelta(weeks=52 * 100)).date())

        start_time = time.mktime(time.strptime(start_date, "%Y-%m-%d"))
        end_time = time.mktime(time.strptime(end_date, "%Y-%m-%d"))

        random_time = start_time + random.random() * (end_time - start_time)

        return time.strftime(date_format, time.localtime(random_time))

    except Exception as e_text:
        raise InputGeneratorException("Date generation error: {0}".format(e_text))


class InputGeneratorException(Exception):
    pass

if __name__ == '__main__':
    log.info("Starting!")
    form_data = {"name": "First Name",
                 "min": 4,
                 "max": 10,
                 "required": False}
    try:
        field = {"name": "Birth Month", "min": 3, "max": 2}
        print generate_integer(2, 1, field=field)
        #===================================================================
        #--- Generate a whole bunch of junk
        #===================================================================
        for i in range(100):
            log.info(generate_string(test_number=i, field=form_data))

        #===================================================================
        #--- Generate a "form"
        #===================================================================
        # drop_index = generate_drop_down()
        # form_data = {
        #     "first_name": generate_string(11, 11),
        #     "last_name": generate_string(4, 6),
        #     "date": generate_date(date_format="%m-%d-%y"),
        #     "phone": generate_phone(),
        #     "zipcode": generate_zip_code(),
        #     "birth_month": generate_integer(10, 10, padding=2)
        # }
    except InputGeneratorException as e:
        log.error(e)

    log.info(form_data)