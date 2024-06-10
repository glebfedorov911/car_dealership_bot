import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')