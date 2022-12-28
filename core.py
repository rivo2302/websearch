from os import environ as env

import ampalibe
from ampalibe import Messenger, Payload, translate, Logger
from ampalibe.messenger import Action


from src.routes import *
from src.views import View
from src.models import CustomModel

model = CustomModel()
chat = Messenger()
view = View()

chat.get_started("/GET_STARTED")


@ampalibe.before_receive()
def before_process(sender_id, **ext):
    chat.send_action(sender_id, Action.mark_seen)
    chat.send_action(sender_id, Action.typing_on)

    # Check if user has name if true we get and set it if possible
    if model.get_name(sender_id) is None:
        user_info = chat.get_user_profile(sender_id)
        name = user_info.get("first_name") + " " + user_info.get("last_name")
        if name is not None:
            res = model.set_name(sender_id, name)
    return True


@ampalibe.after_receive()
def after_process(sender_id, lang, res, **ext):
    model.set_action(sender_id, "/ATTENTE_QUERY")
    if res is None:
        return
    if lang is None:
        lang = "fr"
    if res.get("VALUE") is not None:
        lang = res.get("VALUE")
    if res.get("SEND_CHANGE_LANGUAGE") is True:
        chat.send_quick_reply(
            sender_id, view.language_menu, translate("choose_language", lang)
        )
    if res.get("SEND_PERSISTANT_MENU") is True:
        chat.persistent_menu(sender_id, view.persistant_menu(lang))

    if res.get("SEND_KEY") is True:
        chat.send_text(sender_id, translate("type_word", lang))


@ampalibe.command("/")
def main(sender_id, cmd, lang, **ext):
    chat.send_text(sender_id, translate("greeting", lang))
