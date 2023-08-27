class StageLimitExceeded(Exception):
    """
    Raised when the maximum number of characters on stage (which is 2) is exceeded.
    """
    pass

class InvalidNumberError(Exception):
    """
    Raised when a number supplied in operations (:py:meth:`Play.sum`, 
    :py:meth:`Play.difference`, and so on) is invalid.

    The cause is usually because of the number not being a power of 2.
    """
    pass

class CharacterNotOnstage(Exception):
    """
    Raised when an operation is trying to be done on a character who is not onstage.
    """
    pass

class NotEnoughCharacters(Exception):
    """
    Raised when there is only one character onstage.

    That does not work because you need a character to set or print another character's value.
    """
    pass
