__author__ = 'vbraun'

from datetime import datetime, timedelta
import random
import string
import time


#TODO: Add Custom Exception classes

#TODO: Add a "Random" option to the SELECT Field type, for things like State and year, etc.
#TODO: Add a parameter to the SELECT Field that lets the code know whether the first option is selectable (if even possible)
#TODO: Add an underscore to the ZIP_CODE field type
#TODO: Add "Padding" option to the INTEGER Field type, for doing month as 04
#TODO: Add Date Field Type with a format parameter like "%m/%d/%Y"
#TODO: Add "domain" option to the email field.

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
        #- Always fill in the field with something on the first test
        if test_number != 1:
            leave_blank = True if random.randint(0, 2) == 1 else False

    return required, leave_blank


def generate_string(min_length=4, max_length=10, test_number=None, field=None):
    """ Creates a str object with a length greater than min_length and less than max_length, made up of randomly
        selected upper and lowercase letters.
    :param
        -   min_length:     The minimum length, in characters, that the generated string can be
        -   max_length:     The maximum length, in characters, that the generated string can be
        -   test_number:    An int that specifies which submission number this generation is being used for. This will
                            help determine whether the field has been populated previously and whether to leave it blank
        -   field:          The field object. Should include a key:value for all pertinent information to its field
                            type. If the object has "min" and "max" keys, those values will override the "min_length"
                            and "max_length" parameters.
    :returns
        -   string:         The randomly generated, or blank string
    """
    try:
        #- Reset min and max lengths with the field object values
        min_length = min_length if not field else field["min"]
        max_length = max_length if not field else field["max"]
        #- Set test_number to a default of 1 unless a value was passed in.
        test_number = 1 if not test_number else test_number

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create a string
        if leave_blank:
            random_string = ""
        else:
            random_string = "".join(random.choice(string.ascii_letters) for i in range(random.randint(min_length,
                                                                                                      max_length)))

        return random_string
    except Exception as e:
        raise e


def generate_integer(min_int=0, max_int=9, padding=1, test_number=None, field=None):
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

        #- Instantiate the required and leave_blank variables based on the field object and test number
        required, leave_blank = _set_required_blank(test_number, field)

        #- Set the return to a blank string if leave_blank is true. Otherwise create an integer
        if leave_blank:
            #TODO: Determine best way to specify a blank value for an int here. Make it negative? Set to None?
            integer = ""
        else:
            #- Create the integer value between the min and max and with the padding provided
            #TODO: Consider adding padding at time of input so that the return can be an int object rather than string
            integer = "{0:0{1}d}".format(random.randint(min_int, max_int), padding)

        return integer

    except Exception as e:
        raise e


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

    except Exception as e:
        raise e


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

    #TODO: Other formats to add: ### ### #### all spaces, ###-###-#### all dashes, (###)### #### no space after parenth
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

            if decimals:
                phone_number = "{0}.{1}.{2}".format(area_code, start, finish)
            else:
                #- Surround the area code in parenthesis if parenthesis parameter is True
                area_code = "({0})".format(area_code) if parenthesis else area_code
                #- Add the dash between the start and finish of the number if dash parameter is True
                number = start + finish if not dash else "{0}-{1}".format(start, finish)
                if space:
                    phone_number = "{0} {1}".format(area_code, number)
                else:
                    phone_number = area_code + number

        return phone_number

    except Exception as e:
        raise e


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

    except Exception as e:
        raise e


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
            if not required and random.randint(0, 4) == 2:
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

    except Exception as e:
        raise e


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
        #TODO: make sure the errors show that it occurred while filling a Drop Down field
        return generate_select(num_of_options, test_number, field)

    except Exception as e:
        raise e


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
        #TODO: make sure the errors show that it occurred while filling a Radio field
        return generate_select(num_of_options, test_number, field)

    except Exception as e:
        raise e


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
            if random.randint(0, 4) == 2:
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

    except Exception as e:
        raise e


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

    except Exception as e:
        raise e