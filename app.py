import os
from time import time
from typing import Union
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from redis import Redis
from rq import Queue

# project
from panel_extractor import PanelExtractor
from utils import download_lmages

app = FastAPI()

load_dotenv()

redis_conn = Redis(
  host= os.environ.get('REDIS_HOST'),
  port= '31538',
  password= os.environ.get('REDIS_PASS'),
)
q = Queue(os.environ.get('QUEUE_NAME'), connection=redis_conn)


# logging_example.py

import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

panel_extractor = PanelExtractor(just_contours=True, keep_text=True, min_pct_panel=2, max_pct_panel=90)


class Data(BaseModel):
    chapter_url: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/queueSize')
def queueSize():
    """Test endpoint"""
    return {'Queue Size': len(q)}


def wrapper(chapter_url):
    _path = f"./images/{uuid4()}"
    download_lmages(chapter_url, _path)
    panel_extractor.extract(_path)

@app.post("/chapter")
def post_chapter(data: Data):
    logger.info("post_chapter")
    chapter_url = data.chapter_url

    # TODO: this needs!!!! to be fixed
    # we do not need to dowload all the images for the same chapter several times
    # and to be honest we don't need to calc the panels each time
    # a lot of caching needs to be done :)
    # _path = f"./images/{uuid4()}"

    # download_lmages(chapter_url, _path)

    # potentially we want the shell script to generate a uuid each time, save the result in a folder named as the uuid
    # and return the uuid as output, and use the autput uuid as input for the method extract
    final = q.enqueue(wrapper, chapter_url)

    size = len(q)

    return {'size': size}

# @app.get("/result/{job}")
# def result(job):
#     while not job.is_finished:
#         yield('Job not finished yet, wait for 1s')
#         time.sleep(1)

#     return(job.result)