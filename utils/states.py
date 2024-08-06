from aiogram.fsm.state import StatesGroup, State


class UserInsertDeviceStates(StatesGroup):
    """ДОБАВЛЕНИЕ ОБОРУДОВАНИЯ"""
    ADD_SERIAL_NUMBER = State()
    ADD_TYPE = State()
    ADD_DURANCE = State()
    ADD_DATE = State()
    ADD_ADDRESS = State()

class UserInsertInnStates(StatesGroup):
    """ДОБАВЛЕНИЕ ИНН"""
    ADD_NEW_INN = State()
    ADD_ORG_NAME = State()
    ADD_ADDRESS = State()

class Registration(StatesGroup):
    """РЕГИСТРАЦИЯ"""
    REGISTRATION_NUMBER = State()
    REGISTRATION = State()
    PHONE = State()








# class UserViewStates(StatesGroup):
#     CHOOSE_VIEW = State()
#     VIEW_INN = State()
#     VIEW_SERIAL_NUMBER = State()