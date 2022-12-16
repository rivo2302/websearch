import ampalibe
from ampalibe import Messenger, Model, Payload, translate
from ampalibe.ui import QuickReply, Button, Type
from utils.websearch import Botsearch
from ampalibe.messenger import Action
from os import environ as env

query = Model()
chat = Messenger()

chat.get_started("/GET_STARTED")


def send_language(sender_id, lang):
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


def send_persistant_menu(sender_id, lang):
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


@ampalibe.before_receive()
def before_process(sender_id, **ext):
    chat.send_action(sender_id, Action.mark_seen)
    return True


@ampalibe.after_receive()
def after_process(sender_id, **ext):
    query.set_action(sender_id, "/ATTENTE_QUERY")


@ampalibe.command("/CHOOSE_LANGUAGE")
def choose_langue(sender_id, lang, **ext):
    send_language(sender_id, lang)


@ampalibe.command("/GET_STARTED")
def get_started(sender_id, lang, cmd, **ext):

    chat.send_message(sender_id, translate("greeting", "fr"))
    send_persistant_menu(sender_id, "fr")
    buttons = [
        Button(
            type=Type.web_url,
            title=translate("go_github", "fr"),
            url="https://github.com/rivo2302/websearch",
        )
    ]

    chat.send_button(sender_id, buttons, "Voir le code source")
    send_language(sender_id, "fr")


@ampalibe.command("/SET_LANGUAGE")
def change_langue(sender_id, cmd, value, **ext):
    query.set_lang(sender_id, value)
    send_persistant_menu(sender_id, value)
    chat.send_message(sender_id, translate("language_changed", value))


@ampalibe.command("/SEARCH")
def search(sender_id, lang, cmd, **ext):
    chat.send_message(sender_id, translate("type_word", lang))


@ampalibe.action("/ATTENTE_QUERY")
def send_option(sender_id, cmd, **ext):
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
            title="Image",
            image_url=env.get("AMP_URL") + "/asset/image.png",
            payload=Payload(
                "/IMAGE",
                value=cmd,
            ),
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
    ]
    chat.send_quick_reply(
        sender_id,
        quick_rep,
        "Quel type de format vous voulez voir.",
    )
    query.set_temp(sender_id, "keyword", cmd)


@ampalibe.command("/DOCX")
def search_docs(sender_id, lang, cmd, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).docx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_message(
        sender_id, translate("not_result", lang)
    )


@ampalibe.command("/XLSX")
def search_xlsx(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).xlsx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_message(
        sender_id, translate("not_result", lang)
    )


@ampalibe.command("/PDF")
def search_pdf(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).pdf
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_message(
        sender_id, translate("not_result", lang)
    )


@ampalibe.command("/IMAGE")
def search_image(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).image
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_message(
        sender_id, translate("not_result", lang)
    )


@ampalibe.command("/PPTX")
def search_pptx(sender_id, cmd, lang, value, **ext):
    keyword = query.get_temp(sender_id, "keyword")
    results = Botsearch(keyword, lang).pptx
    chat.send_template(
        sender_id, results, next=True
    ) if results else chat.send_message(
        sender_id, translate("not_result", lang)
    )


@ampalibe.command("/DOWNLOAD")
def download(sender_id, cmd, lang, link, **ext):
    chat.send_message(sender_id, translate("download_loading", lang))
    try:
        if ext.get("typefile") == "image":
            chat.send_file_url(sender_id, link, filetype="image")
        else:
            chat.send_file_url(sender_id, link)

    except Exception as e:
        print(e)
        chat.send_message(
            sender_id,
            translate("file_not_sent", lang),
        )


@ampalibe.command("/")
def main(sender_id, cmd, lang, **ext):
    chat.send_text(sender_id, translate("greeting", lang))
