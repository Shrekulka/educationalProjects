# ai_checklist_guardian/states.py

from aiogram.dispatcher.filters.state import StatesGroup, State


class UserSteps(StatesGroup):
    """
        The UserSteps class represents a group of states used in aiogram to manage various stages
        of user interaction with the Telegram bot. Each state in this class corresponds to a specific
        user input stage.

        Attributes:
        - LOCATION: State for choosing the location.
        - CHECKLIST: State for the checklist.
        - COMMENT: State for user input of comments.
        - PHOTO: State for uploading a photo.
        - REPORT: State for completion and report generation.
    """

    LOCATION = State()         # Тип данных: aiogram.dispatcher.storage.memory.states.State
    CHECKLIST = State()        # Тип данных: aiogram.dispatcher.storage.memory.states.State
    COMMENT = State()          # Тип данных: aiogram.dispatcher.storage.memory.states.State
    PHOTO = State()            # Тип данных: aiogram.dispatcher.storage.memory.states.State
    REPORT = State()           # Тип данных: aiogram.dispatcher.storage.memory.states.State
