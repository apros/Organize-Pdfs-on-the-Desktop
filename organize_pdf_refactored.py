import os
import shutil
import time
import re
import logging
import asyncio
from pathlib import Path
from typing import Tuple, Optional
from functools import lru_cache
import contextlib

import win32com.client
from openai import AsyncOpenAI

# Configuration
DESKTOP_PATH = Path.home() / "OneDrive" / "Desktop"
ORGANIZED_FOLDER_NAME = "Organized PDFs"
OPENAI_MODEL = "gpt-3.5-turbo"
CHATGPT_KEYWORDS = ["chatgpt", "ai", "open ai"]
API_DELAY = 1  # seconds

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFOrganizer:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.organized_folder = DESKTOP_PATH / ORGANIZED_FOLDER_NAME

    async def organize(self):
        self.organized_folder.mkdir(exist_ok=True)

        tasks = [self._process_file(filename) for filename in os.listdir(DESKTOP_PATH)]
        await asyncio.gather(*tasks)

        logger.info("PDF and PDF shortcut organization completed!")

    async def _process_file(self, filename: str):
        file_path = DESKTOP_PATH / filename
        is_pdf, pdf_path = self._is_pdf_or_pdf_shortcut(file_path)
        
        if is_pdf:
            cleaned_filename = self._clean_filename(pdf_path.name)
            category = await self._get_category(cleaned_filename)
            self._move_to_category(file_path, filename, category, pdf_path)
            await asyncio.sleep(API_DELAY)

    def _is_pdf_or_pdf_shortcut(self, file_path: Path) -> Tuple[bool, Optional[Path]]:
        if file_path.suffix.lower() == '.pdf':
            return True, file_path
        elif file_path.suffix.lower() == '.lnk':
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(str(file_path))
                target = Path(shortcut.Targetpath)
                if target.suffix.lower() == '.pdf':
                    return True, target
            except Exception as e:
                logger.error(f"Error resolving shortcut {file_path}: {e}")
        return False, None

    @staticmethod
    def _clean_filename(filename: str) -> str:
        name_without_ext = Path(filename).stem
        cleaned_name = re.sub(r'[^\w\s-]', '', name_without_ext)
        return re.sub(r'\s+', ' ', cleaned_name).strip()

    async def _get_category(self, filename: str) -> str:
        if any(keyword in filename.lower() for keyword in CHATGPT_KEYWORDS):
            return "ChatGPT"
        return await self._get_category_from_openai(filename)

    @lru_cache(maxsize=100)
    async def _get_category_from_openai(self, filename: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that categorizes PDF files based on their names."},
                    {"role": "user", "content": f"Suggest a single-word category for a PDF file named '{filename}'. Respond with just the category name, nothing else."}
                ],
                max_tokens=10,
                n=1,
                stop=None,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error getting category from OpenAI for {filename}: {e}")
            return "Uncategorized"

    def _move_to_category(self, file_path: Path, filename: str, category: str, pdf_path: Optional[Path]):
        category_folder = self.organized_folder / category
        category_folder.mkdir(exist_ok=True)
        
        try:
            if file_path.suffix.lower() == '.pdf':
                shutil.move(str(file_path), str(category_folder / filename))
                logger.info(f"Moved '{filename}' to '{category}' folder")
            else:  # It's a shortcut
                new_shortcut_path = category_folder / filename
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(str(new_shortcut_path))
                shortcut.Targetpath = str(pdf_path)
                shortcut.save()
                file_path.unlink()  # Remove the original shortcut
                logger.info(f"Created new shortcut for '{filename}' in '{category}' folder")
        except Exception as e:
            logger.error(f"Error moving file {filename}: {e}")

async def main():
    api_key = 'Actual API key here'  # Replace with your actual API key
    organizer = PDFOrganizer(api_key)
    await organizer.organize()

if __name__ == "__main__":
    asyncio.run(main())