# Credit to https://stackoverflow.com/a/57069782
# This allows C#-ish event handlers.

class Event:
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        """Shortcut for using += to add a listener."""
        self.listeners.append(listener)
        return self

    def __isub__(self, listener):
        """Shortcut for using -= to remove a listener."""
        self.listeners.remove(listener)
        return self

    def invoke(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)