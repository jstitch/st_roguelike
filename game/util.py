"""
util.py

RogueWarts utility definitios, functions and classes.

  variable debug            : flag for debug messages (default False)

  function _                : translates a message (yet a dummy, but the idea is to
                              use it everywhere in the code until full
                              implementation of the localization logic
                              gets done)

  class Message             : Messages the game gives to the user via the UI

  class RoguewartsException : Exceptions for the game should be
                              handled using this class
"""

"""
Debug game flag.
"""
debug = False

def _(message):
    """
    Translation function.

    Arguments:
      message : the message to be translated

    Returns:
      string with the translated message
    """
    return message

class Message:
    """
    Messages class.

    Methods:
      __init__

    Variables:
      message
      properties
    """
    def __init__(self, message, properties):
        """
        Initialize class

        Arguments:
          message : the message to be hold by this class
          properties : a map with extra attributes for the message
            - 'color'  : the color used to render the message
        """
        self.message = message
        self.properties = properties

    def __str__(self):
        return self.message

class RoguewartsException(Exception):
    """
    Generic game exception.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
