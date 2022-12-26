from os import environ as env

import ampalibe
from ampalibe import Messenger, Model, Payload, translate
from ampalibe.ui import QuickReply, Button, Type
from ampalibe.messenger import Action


query = Model()
chat = Messenger()

chat.get_started("/GET_STARTED")

from src.main import *


@ampalibe.before_receive()
def before_process(sender_id, **ext):
    chat.send_action(sender_id, Action.mark_seen)
    return True


@ampalibe.after_receive()
def after_process(sender_id, lang, res, **ext):
    query.set_action(sender_id, "/ATTENTE_QUERY")
    if res is None:
        return
    if lang is None:
        lang = "fr"
    if res.get("VALUE") is not None:
        lang = res.get("VALUE")
    if res.get("SEND_CHANGE_LANGUAGE") is True:
        quick_rep = [
            QuickReply(
                title="MG",
                image_url=env.get("AMP_URL") + "/asset/mg.png",
                payload=Payload("/SET_LANGUAGE", value="mg"),
            ),
            QuickReply(
                title="FR",
                image_url=env.get("AMP_URL") + "/asset/fr.png",
                payload=Payload("/SET_LANGUAGE", value="fr"),
            ),
            QuickReply(
                title="EN",
                image_url=env.get("AMP_URL") + "/asset/en.jpg",
                payload=Payload("/SET_LANGUAGE", value="en"),
            ),
        ]
        chat.send_quick_reply(
            sender_id, quick_rep, translate("choose_language", lang)
        )
    if res.get("SEND_PERSISTANT_MENU") is True:
        persistent_menu = [
            Button(
                type=Type.postback,
                title=translate("search", lang),
                payload=Payload("/SEARCH"),
            ),
            Button(
                type=Type.postback,
                title=translate("choose", lang),
                payload=Payload("/CHOOSE_LANGUAGE"),
            ),
        ]
        chat.persistent_menu(sender_id, persistent_menu)


@ampalibe.command("/")
def main(sender_id, cmd, lang, **ext):
    chat.send_text(sender_id, translate("greeting", lang))
