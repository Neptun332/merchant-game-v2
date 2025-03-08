from enum import Enum

class EventName(str, Enum):
    SOME_EVENT = "SOME_EVENT"

class Event:
    def __init__(self, name: EventName, data=None):
        self.name = name
        self.data = data

class EventManager:
    def __init__(self):
        self.listeners = {}

    def register_listener(self, event_name: EventName, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def dispatch(self, event):
        if event.name in self.listeners:
            for listener in self.listeners[event.name]:
                listener(event) 