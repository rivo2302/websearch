from os import environ as env


import ampalibe
from ampalibe import Messenger, Payload, translate, Logger
from ampalibe.ui import QuickReply, Button, Type

from tools import Botsearch
from .views import View
from src.models import CustomModel

model = CustomModel()
chat = Messenger()
view = View()


@ampalibe.command("/GET_STARTED")
def get_started(sender_id, lang, cmd, **ext):

    chat.send_text(sender_id, translate("greeting", "fr"))
    return {"SEND_PERSISTANT_MENU": True, "SEND_CHANGE_LANGUAGE": True}


@ampalibe.command("/ABOUT")
def about_me(sender_id, lang, cmd, **ext):
    chat.send_text(sender_id, translate("description", lang))
    chat.send_text(sender_id, translate("features", lang))
    chat.send_button(
        sender_id, view.github_button("fr"), "Voir le code source"
    )
    return {"SEND_KEY": True}


@ampalibe.command("/CHOOSE_LANGUAGE")
def choose_langue(sender_id, lang, **ext):
    return {"SEND_CHANGE_LANGUAGE": True}


@ampalibe.command("/SET_LANGUAGE")
def change_langue(sender_id, cmd, value, **ext):
    model.set_lang(sender_id, value)
    chat.send_text(sender_id, translate("language_changed", value))
    return {"SEND_PERSISTANT_MENU": True, "VALUE": value, "SEND_KEY": True}


@ampalibe.command("/SEARCH")
def search(sender_id, lang, cmd, **ext):
    chat.send_text(sender_id, translate("type_word", lang))


@ampalibe.action("/ATTENTE_QUERY")
def send_option(sender_id, lang, cmd, **ext):
    chat.send_quick_reply(
        sender_id,
        view.choice_menu(lang, cmd),
        translate("format_type", lang),
    )
    model.set_temp(sender_id, "keyword", cmd)


@ampalibe.command("/DOCX")
def search_docs(sender_id, lang, cmd, value, **ext):
    keyword = model.get_temp(sender_id, "keyword")
    model.add_query(sender_id, keyword, "DOCX")
    results = Botsearch(keyword, lang).docx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/XLSX")
def search_xlsx(sender_id, cmd, lang, value, **ext):
    keyword = model.get_temp(sender_id, "keyword")
    model.add_query(sender_id, keyword, "XLSX")
    results = Botsearch(keyword, lang).xlsx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/PDF")
def search_pdf(sender_id, cmd, lang, value, **ext):
    keyword = model.get_temp(sender_id, "keyword")
    model.add_query(sender_id, keyword, "PDF")
    results = Botsearch(keyword, lang).pdf
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/PPTX")
def search_pptx(sender_id, cmd, lang, value, **ext):
    keyword = model.get_temp(sender_id, "keyword")
    model.add_query(sender_id, keyword, "PPTX")
    results = Botsearch(keyword, lang).pptx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/IMAGE")
def search_image(sender_id, cmd, lang, value, **ext):
    keyword = model.get_temp(sender_id, "keyword")
    model.add_query(sender_id, keyword, "IMAGE")
    results = Botsearch(keyword, lang).image
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/DOWNLOAD")
def download(sender_id, cmd, lang, link, **ext):
    chat.send_text(sender_id, translate("download_loading", lang))
    try:
        if ext.get("typefile") == "image":
            chat.send_file_url(sender_id, link, filetype="image")
        else:
            chat.send_file_url(sender_id, link)

    except Exception as e:
        Logger.error(e)
        chat.send_text(
            sender_id,
            translate("file_not_sent", lang),
        )
