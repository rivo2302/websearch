from os import environ as env

from ampalibe.ui import QuickReply, Button, Type
from ampalibe import Payload, translate


class View:
    @staticmethod
    def github_button(lang):
        return [
            Button(
                type=Type.web_url,
                title=translate("go_github", lang),
                url="https://github.com/rivo2302/websearch",
            )
        ]

    @staticmethod
    def choice_menu(lang, cmd):
        return [
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

    @staticmethod
    def persistant_menu(lang):
        return [
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
            Button(
                type=Type.postback,
                title=translate("about_me", lang),
                payload=Payload("/ABOUT"),
            ),
        ]

    @property
    def language_menu(self):
        return [
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
