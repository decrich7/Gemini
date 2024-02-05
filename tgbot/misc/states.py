from aiogram.dispatcher.filters.state import StatesGroup, State


class ChatMode(StatesGroup):
    chat = State()



class Mode(StatesGroup):
    mode = State()
    change_mode = State()




class AdminState(StatesGroup):
    token_add = State()
    token_del = State()
    proxy_add = State()
    proxy_del = State()
    prompt_add = State()
    prompt_del = State()
    count_referal = State()
    mass_post = State()
    mass_post_button = State()
    mass_post_button2 = State()


