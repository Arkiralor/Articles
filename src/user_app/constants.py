import re


class UserRegex:
    """
    Class to hold regexes for User models in userapp.
    """

    # 'john.doe@email.com'
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    ## prithoo: Full ISO Spec 10 to 12 digit phone number (+(ISD)(STD)(AREA)(SUBSCRIBER)):
    ##  8811098879, 881-109-8879, +918811098879, +91-881-109-8879, +91-361-222-0324, +913612220324
    ## confirmed on 'https://regex101.com/'
    PHONE_REGEX_ISD = re.compile(r"^(\+[0-9]{0,2})?([\s.-])?(\+\d{1,2}\s)?\(?\d{3}\)?([\s.-])?\d{3}([\s.-])?\d{4}$")
    ## Normal 10-digit phone number ((STD)(AREA)(SUBSCRIBER))
    PHONE_REGEX = re.compile(r"^([\s.-])?(\+\d{1,2}\s)?\(?\d{3}\)?([\s.-])?\d{3}([\s.-])?\d{4}$")

    # >=1 UC char, >=1 LC char, >=1 NUM char >=[@, $ ,!, %, *, ?, &]; between 8 to 15 chars; confirmed on 'https://regex101.com/'
    PASSWORD_REGEX = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$')