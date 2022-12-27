from os import environ as env


import ampalibe
from ampalibe import Messenger, Model, Payload, translate, Logger
from ampalibe.ui import QuickReply, Button, Type

from tools import Botsearch

query = Model()
chat = Messenger()


@ampalibe.command("/GET_STARTED")
def get_started(sender_id, lang, cmd, **ext):

    chat.send_text(sender_id, translate("greeting", "fr"))
    buttons = [
        Button(
            type=Type.web_url,
            title=translate("go_github", "fr"),
            url="https://github.com/rivo2302/websearch",
        )
    ]
    chat.send_button(sender_id, buttons, "Voir le code source")
    return {"SEND_PERSISTANT_MENU": True, "SEND_CHANGE_LANGUAGE": True}


@ampalibe.command("/CHOOSE_LANGUAGE")
def choose_langue(sender_id, lang, **ext):
    return {"SEND_CHANGE_LANGUAGE": True}


@ampalibe.command("/SET_LANGUAGE")
def change_langue(sender_id, cmd, value, **ext):
    query.set_lang(sender_id, value)
    chat.send_text(sender_id, translate("language_changed", value))
    return {"SEND_PERSISTANT_MENU": True, "VALUE": value}


@ampalibe.command("/SEARCH")
def search(sender_id, lang, cmd, **ext):
    chat.send_text(sender_id, translate("type_word", lang))


@ampalibe.action("/ATTENTE_QUERY")
def send_option(sender_id, lang, cmd, **ext):
    quick_rep = [
        QuickReply(
            title="Docx",
            image_url=env.get("AMP_URL") + "/asset/docx.png",
            payload=Payload("/DOCX", value=cmd),
        ),
        QuickReply(
            title="Pdf",
            image_url=env.get("AMP_URL") + "/asset/pdf.jpg",
            payload=Payload("/PDF", value=cmd),
        ),
        QuickReply(
            title="Powerpoint",
            image_url=env.get("AMP_URL") + "/asset/ppt.png",
            payload=Payload("/PPTX", value=cmd),
        ),
        QuickReply(
            title="Excel",
            image_url=env.get("AMP_URL") + "/asset/excel.jpg",
            payload=Payload("/XLSX", value=cmd),
        ),
        #! TODO: Add image search
        # QuickReply(
        #     title="Image",
        #     image_url=env.get("AMP_URL") + "/asset/image.png",
        #     payload=Payload(
        #         "/IMAGE",
        #         value=cmd,
        #     ),
        # ),
    ]
    chat.send_quick_reply(
        sender_id,
        quick_rep,
        translate("format_type", lang),
    )
    query.set_temp(sender_id, "keyword", cmd)


@ampalibe.command("/DOCX")
def search_docs(sender_id, lang, cmd, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).docx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/XLSX")
def search_xlsx(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).xlsx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/PDF")
def search_pdf(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).pdf
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/PPTX")
def search_pptx(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).pptx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_text(sender_id, translate("not_result", lang))


@ampalibe.command("/IMAGE")
def search_image(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
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
