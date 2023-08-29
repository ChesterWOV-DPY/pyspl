from .names import names

class Character:
    """
    Represents a character in an SPL play.

    :raises ValueError: The character name supplied is invalid.

    .. note::

        In the current version (``0.1b``), all names are valid, because I'm too la]zy to add all the
        character names.

    """
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        # if name not in names:
        #     raise ValueError(f'invalid character name: {name!r}')
        
    def __str__(self):
        """
        Returns the name of the character.
        """
        return self.name

