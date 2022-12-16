from websearch import WebSearch
from ampalibe.ui import Button, Type, Element
from ampalibe import Payload, translate
from os import environ as env


class Botsearch:
    def __init__(self, query, lang):
        self.query = query
        self.lang = lang
        self.websearch = WebSearch(self.query)

    @property
    def docx(self):
        docs = self.websearch.docx
        items = (
            [
                Element(
                    title=doc.split("/")[-1],
                    image_url=env.get("AMP_URL") + "/asset/docx.png",
                    buttons=[
                        Button(
                            title=translate("download", self.lang),
                            type=Type.postback,
                            payload=Payload("/DOWNLOAD", link=doc),
                        )
                    ],
                )
                for doc in docs
            ]
            if self.websearch.docx
            else []
        )
        return items

    @property
    def pdf(self):
        pdfs = self.websearch.pdf
        items = (
            [
                Element(
                    title=pdf.split("/")[-1],
                    image_url=env.get("AMP_URL") + "/asset/pdf.jpg",
                    buttons=[
                        Button(
                            title=translate("download", self.lang),
                            type=Type.postback,
                            payload=Payload("/DOWNLOAD", link=pdf),
                        )
                    ],
                )
                for pdf in pdfs
            ]
            if self.websearch.pdf
            else []
        )
        return items

    @property
    def image(self):
        images = self.websearch.images
        items = (
            [
                Element(
                    title=image.split("/")[-1],
                    image_url=image,
                    buttons=[
                        Button(
                            title=translate("download", self.lang),
                            type=Type.postback,
                            payload=Payload(
                                "/DOWNLOAD", link=image, typefile="image"
                            ),
                        )
                    ],
                )
                for image in images
            ]
            if self.websearch.images
            else []
        )
        return items

    @property
    def xlsx(self):
        xlsxs = self.websearch.xlsx
        items = (
            [
                Element(
                    title=xlsx.split("/")[-1],
                    image_url=env.get("AMP_URL") + "/asset/excel.jpg",
                    buttons=[
                        Button(
                            title=translate("download", self.lang),
                            type=Type.postback,
                            payload=Payload("/DOWNLOAD", link=xlsx),
                        )
                    ],
                )
                for xlsx in xlsxs
            ]
            if self.websearch.xlsx
            else []
        )
        return items

    @property
    def pptx(self):
        pptxs = self.websearch.pptx
        items = [
            Element(
                title=pptx.split("/")[-1],
                image_url=env.get("AMP_URL") + "/asset/ppt.png",
                buttons=[
                    Button(
                        title=translate("download", self.lang),
                        type=Type.postback,
                        payload=Payload("/DOWNLOAD", link=pptx),
                    )
                ],
            )
            for pptx in pptxs
        ]
        return items
