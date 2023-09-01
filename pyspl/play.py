from dataclasses import dataclass
import os
from typing import Callable, Union

from .character import Character
from .errors import StageLimitExceeded, CharacterNotOnstage, NotEnoughCharacters
from .operations import Value, value_as_str

@dataclass
class _Act:
    """
    A dataclass for adding acts to plays.
    """
    obj: 'Act'
    number: str
    description: str

class Play:
    """A play script in the Shakespeare Programming Language (SPL). All programs made using **PySPL** must use this object."""
    def __init__(self, description: str) -> None:
        self.description = description
        self._characters: list[Character] = []
        self._characters_on_stage: list[Character] = []
        self.acts: list[_Act] = []
        self.lines = []

    @property
    def characters(self) -> list[Character]:
        """
        Returns a list of the characters in this play.

        :rtype: list[:py:class:`Character`]
        """
        return self._characters
    
    def add_character(self, character: Character):
        """
        Adds a character to the play.

        .. note::

            This function does **NOT** add the character onto the stage. Use :py:func:`Act.enter` for that purpose.
        
        """
        self._characters.append(character)
    
    def character(self, name: str, description: str) -> Character:
        """
        Creates a character and adds it to the play.

        This is equivalent to:

        .. code-block:: python
        
            character = pyspl.Character(name, description)
            play.add_character(character)

        :return: The character created.
        :rtype: Character
        """
        character = Character(name, description)
        self.add_character(character)
        return character
    
    def add_act(self, act: 'Act', number: str, description: str):
        """
        Adds an act to the play.

        :param Act act: An Act object. Note that it should be an instance of a class, not the class itself.
        :param str number: A roman numeral representing the order. PySPL does not actually consider this, it is here just for the SPL syntax.
        :param str description: The description of the act. Must end with a period.
        """
        self.acts.append(_Act(act, number, description))

    def code(self) -> str:
        """
        Generates SPL code for this play.

        :returns: A piece of SPL code generated for this play.
        :rtype: str
        """
        self.lines = [self.description, '']
        for character in self._characters:
            self.lines.append(f'{character.name}, {character.description}')
        self.lines.append('')
        for act in self.acts:
            lines = act.obj._gencode(act.number, act.description)
            self.lines.extend(lines)
            self.lines.append('')

        return '\n'.join(self.lines)

    def save(self, fn: Union[str, bytes, os.PathLike], mode='w') -> None:
        """
        Saves SPL code for this play into _fn_ using the mode specified.

        :param str fn: The file to write to.
        :param str mode: The mode to use for writing. Defaults to 'w'.
        """
        self.code()
        with open(fn, mode) as f:
            for line in self.lines:
                f.write(line + '\n')


@dataclass
class Scene:
    """
    Represents a scene in a SPL play.

    This is a data class.
     
    .. warning::

        This should not be constructed manually by the user. 
        Instead, use :py:meth:`Act.add_scene`.

    """
    name: str
    number: str
    description: str

class Act:
    """
    Represents an act in a SPL play.

    The recommended way is to subclass this object and create methods inside it, then add them by using :py:meth:`Act.add_scene`.

    Example
    ^^^^^^^
    .. code-block:: python
        
        class Act1(pyspl.Act):
            def __init__(self):
                super().__init__(self, 'I', 'The First Act.')
                self.add_scene(sceneI)

            def scene1(self):
                # do whatever you need to do here
                pass    

    """
    def __init__(self, play: Play):
        self._play = play
        self._scene_names: list[Scene] = []
        self._lines: list[str] = []
    
    def add_scene(self, func: Callable, number: str, description: str) -> None:
        """
        Adds a scene to the act.

        :param typing.Callable func: The function of the scene to add.
        :param str number: A roman numeral representing the number of the scene. 
        :param str description: The description of the scene. Must end with a period (AKA a full stop) (``.``).
        """
        self._scene_names.append(Scene(func.__name__, number=number, description=description))

    def enter(self, *characters: Character):
        """
        Calls for the characters provided to enter the stage.

        :param \*characters: The characters to enter the stage.
        :type \*characters: Character, ...

        :raises StageLimitExceeded: There are too many characters on stage.
        """
        if len(characters) + len(self._play._characters_on_stage) > 2:
            raise StageLimitExceeded('character limit onstage exceeded')
        
        self._play._characters_on_stage.extend(characters)
        self._lines.append(f'[Enter {" and ".join(map(lambda c: str(c), characters))}]')
    
    def exit(self, *characters: Character):
        """
        Calls for the characters provided to exit the stage.

        :param \*characters: The characters to exit the stage. If not provided, all characters onstage will exit the stage.
        :type \*characters: Character, ...

        :raises CharacterNotOnstage: The character who is trying to exit is not onstage.
        """
        for character in characters:
            if character not in self._play._characters_on_stage:
                raise CharacterNotOnstage(f'character not on stage: {character}')
        
        if len(characters) == 0:
            self._play._characters_on_stage = []
            self._lines.append('[Exeunt]')
        elif len(characters) == 1:
            self._play._characters_on_stage.remove(characters[0])
            self._lines.append(f'[Exit {characters[0]}]')
        else:
            for character in characters:
                self._play._characters_on_stage.remove(character)
            
            self._lines.append(f'[Exeunt {" and ".join(map(lambda c: str(c), characters))}]')
        
    def set(self, target: Character, value: Value):
        """
        Sets a character to a value.

        :param Character target: The character being set.
        :param value: The value to set.
        :type value: int | Character | Operation

        :raises CharacterNotOnstage: The target is not onstage.
        :raises NotEnoughCharacters: There is only one character onstage. 
        """
        characters_onstage = self._play._characters_on_stage
        if target not in characters_onstage:
            raise CharacterNotOnstage('tried to set value of a character not on stage')
        if len(characters_onstage) < 2:
            raise NotEnoughCharacters('unable to set character value: only one character on stage')
        
        setter = self._get_opposite_character(target)

        self._lines.append(f'{setter}: You are {value_as_str(value)}!')

    def print(self, target: Character, type: type[str|int]=str):
        """
        Prints the value of a character.

        :param Character target: The character being printed.
        :param type: The type to print. Defaults to ``str``.
        """
        characters_onstage = self._play._characters_on_stage
        if target not in characters_onstage:
            raise CharacterNotOnstage('tried to print value of a character not on stage')
        if len(characters_onstage) < 2:
            raise NotEnoughCharacters('unable to print character value: only one character on stage')
        
        printer = self._get_opposite_character(target)
        
        if type == str:
            line = 'Speak your mind'
        elif type == int:
            line = 'Open your heart'
        else:
            raise TypeError('invalid type to print')

        self._lines.append(f'{printer}: {line}!')

    def input(self, target: Character, type: type[str|int]=str):
        """
        Receives input and sets the target to that value.

        :param Character target: The character being set.
        :param type: The type to receive. Defaults to ``str``.
        """
        characters_onstage = self._play._characters_on_stage
        if target not in characters_onstage:
            raise CharacterNotOnstage('tried to set value of a character not on stage')
        if len(characters_onstage) < 2:
            raise NotEnoughCharacters('unable to set character value: only one character on stage')
        
        setter = self._get_opposite_character(target)

        if type == str:
            line = 'Open your mind'
        elif type == int:
            line = 'Listen to your heart'
        else:
            raise TypeError('invalid type to print')
        
        self._lines.append(f'{setter}: {line}!')

    def remember(self, target: Character, value: Value):
        """
        Pushes the value onto the target's stack.

        :param Character target: The character to be modified.
        :param value: The value to push.
        :type value: int | Character | Operation
        """
        characters_onstage = self._play._characters_on_stage
        if target not in characters_onstage:
            raise CharacterNotOnstage('tried to push to the stack of a character not on stage')
        if len(characters_onstage) < 2:
            raise NotEnoughCharacters('unable to push to the stack of character: only one character on stage')
        
        setter = self._get_opposite_character(target)

        self._lines.append(f'{setter}: Remember {value_as_str(value)}!')

    def pop(self, target: Character):
        """
        Pops an item from the target's stack and set him/her to it.

        :param Character target: The character to be modified.
        """
        characters_onstage = self._play._characters_on_stage
        if target not in characters_onstage:
            raise CharacterNotOnstage('tried to pop from the stack of a character not on stage')
        if len(characters_onstage) < 2:
            raise NotEnoughCharacters('unable to pop from the stack of character: only one character on stage')
        
        setter = self._get_opposite_character(target)

        self._lines.append(f'{setter}: Recall yourself!')

    def _get_opposite_character(self, character: Character):
        characters_onstage = self._play._characters_on_stage
        first_item = characters_onstage[0]
        if first_item == character:
            c = characters_onstage[1] # The second item (index=1) is now the first item (index=0).
        else:
            c = first_item

        return c

    def _gencode(self, number: str, description: str):
        self._lines = [f'Act {number}: {description}']
        for scene in self._scene_names:
            self._lines.append(f'Scene {scene.number}: {scene.description}')
            scene_func = getattr(self, scene.name)
            scene_func()

        return self._lines

        

