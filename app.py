import logging
import os
from logging.handlers import TimedRotatingFileHandler
from time import time
from typing import Union
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from rq import Queue

# project
from panel_extractor import PanelExtractor
from utils import download_lmages

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://one-panel-next.vercel.app",
    "https://one-panel-next.vercel.app/",
    "https://one-panel-next.vercel.app/canvas",
    "https://one-panel-next.vercel.app/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

redis_conn = Redis(
  host= os.environ.get('REDIS_HOST'),
  port= '31538',
  password= os.environ.get('REDIS_PASS'),
)

q = Queue(os.environ.get('QUEUE_NAME'), connection=redis_conn)

panel_extractor = PanelExtractor(just_contours=True, keep_text=True, min_pct_panel=2, max_pct_panel=90)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler which logs even debug messages

fh = TimedRotatingFileHandler('OnePanelLogs',  when='midnight')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


class Data(BaseModel):
    chapter_url: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/queueSize')
def queueSize():
    """queueSize"""
    logger.info("queueSize")
    return {'Queue Size': len(q)}


def wrapper(chapter_url):
    request_id = uuid4()
    logger.info(f"request_id: {request_id}")

    _path = f"./images/{request_id}"
    download_lmages(chapter_url, _path)
    logger.info("images downloaded")

    panels_extracted = panel_extractor.extract(_path)
    logger.info("panels extracted")
    
    return panels_extracted

@app.post("/chapter")
async def post_chapter(data: Data):
    logger.info("New Request")
    chapter_url = data.chapter_url

    # TODO: this needs!!!! to be fixed
    # we do not need to dowload all the images for the same chapter several times
    # and to be honest we don't need to calc the panels each time
    # a lot of caching needs to be done :)
    # _path = f"./images/{uuid4()}"

    # download_lmages(chapter_url, _path)

    # potentially we want the shell script to generate a uuid each time, save the result in a folder named as the uuid
    # and return the uuid as output, and use the autput uuid as input for the method extract
    # final = q.enqueue(wrapper, chapter_url)

    # size = len(q)

    # return {'size': size}
    result = wrapper(chapter_url)
    return result

# @app.get("/result/{job_id}")
# def result(job_id):
#     job = q.fetch_job(job_id)

#     if job.is_failed:
#         return 'Job has failed!', 400

#     while not job.is_finished:
#         yield('Job not finished yet, wait for 1s')
#         time.sleep(1)

#     return(job.result)