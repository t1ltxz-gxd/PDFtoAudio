import asyncio
from dataclasses import dataclass, asdict
import time
import langdetect
import pdfplumber
from pathlib import Path
from loguru import logger
from os import walk
from gtts import gTTS


logger.add(
    "logs/debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="5 MB",
    retention="10 days",
    compression="zip",
    serialize=True,
)


@dataclass
class Document:
    title: str
    language: str
    text: str

    def get_text(self):
        return self.text

    def get_name(self):
        return self.title

    def get_language(self):
        return self.language


class DocumentHandler:
    def __int__(self, name, text, language):
        self.Document = Document(title=name, text=text, language=language)

    def get_dataclass(self):
        return asdict(self.Document)

    def edit(self, key, value):
        self.Document.__dict__[key] = value


async def get_documents(file_path):
    logger.info("Checking for PDF Files in Directory...")
    filenames = next(walk(file_path), (logger.info(next(walk(file_path))), None, []))[
        2
    ]  # [] if no file
    for file in filenames:
        if Path(file).suffix == ".pdf":
            logger.debug("Page content analysis...")
            with pdfplumber.open(f"{file_path}/{file}") as pdf:
                pages = [page.extract_text() for page in pdf.pages]
            text = "\n".join(pages)
            text = text.replace("\n", "")
            title = file[:-4]
            # logger.info('Writing data to txt document...')
            # with open(f'data/{title}.txt', "w", encoding="utf-8") as file:
            #     file.write(text)
            logger.debug("Language detection...")
            language = langdetect.detect(text)
            document = Document(title=title, text=text, language=language)
            logger.info(document.get_name() + ": " + document.get_language())
            await save_mp3(language=language, document=document)


async def save_mp3(document, language, slow=False):
    logger.info("Saving an mp3 file...")
    my_audio = gTTS(text=document.get_text(), lang=language, slow=slow)
    file_name = document.get_name()
    my_audio.save(f"data/mp3/{file_name}.mp3")


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(get_documents(file_path="data/pdf"))
    logger.info(
        f"The program has ended. Timeout was: {time.perf_counter() - start:.02f} second(s)"
    )
