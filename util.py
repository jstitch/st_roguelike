'''
util.py
'''

"""Debug game flag"""
debug = False

def _(message):
    """Translation dummy"""
    return message

class Message:
    """Messages"""
    # def __init__(self, message, type):
    #     self.message = message
    #     self.type = type

    def __init__(self, message, properties):
        self.message = message
        self.properties = properties

class RoguewartsException(Exception):
    """Generic game exception"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
