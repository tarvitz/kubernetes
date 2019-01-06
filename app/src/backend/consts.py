import abc


#: CONSTS
# noinspection PyPep8Naming
class HttpStatus(object, metaclass=abc.ABCMeta):
    """
    Includes only used statuses in test cases, so please extend it
    by your own will according to rfc
    """
    OK = 200
    DOWN = 521
