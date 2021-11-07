import logging
import logging.config
import requests
from time import sleep

import yaml

DEFAULT_LOGGING_PATH = "configs/logging.conf.yml"

APPLICATION_NAME = "download"

logger = logging.getLogger(APPLICATION_NAME)

BEGIN_URL = "https://api."
MIDDLE_URL = ".ru/v1.9/entry/"
END_URL = "/comments"
WRONG_TEXT = "<head><title>429 Too Many Requests</title></head>"
NO_ACCESS = '{"message":"У вас нет доступа к комментариям","error":{"code":403,"info":[]}}'
NO_URL = '{"message":"К сожалению, запрашиваемая страница не найдена, но есть другие, тоже хорошие","error":{"code":404,"info":[]}}'
EMPTY = '{"message":"","result":[]}'

MAX_PAGES_WITHOUT_SLEEP = 150


def setup_logging():
    with open(DEFAULT_LOGGING_PATH) as config_file:
        logging.config.dictConfig(yaml.safe_load(config_file))


def add_nulls(number, numcount=10):
    len_number = len(str(number))
    if len_number > 10:
        raise ValueError
    return "0" * (numcount - len_number) + str(number)


def requests_content(begin_url, end_url, first_number, number_pages):

    if begin_url == "https://api.vc.ru/v1.9/entry/" and end_url == "":
        output_dir = "vc_ru_posts"
    elif begin_url == "https://api.vc.ru/v1.9/entry/" and end_url == "/comments":
        output_dir = "vc_ru_comments"
    elif begin_url == "https://api.tjournal.ru/v1.9/entry/" and end_url == "":
        output_dir = "tj_posts"
    elif begin_url == "https://api.tjournal.ru/v1.9/entry/" and end_url == "/comments":
        output_dir = "tj_comments"
    elif begin_url == "https://api.dtf.ru/v1.9/entry/" and end_url == "":
        output_dir = "dtf_posts"
    elif begin_url == "https://api.dtf.ru/v1.9/entry/" and end_url == "/comments":
        output_dir = "dtf_comments"
    else:
        return

    for i in range(first_number, first_number + number_pages):
        if i % MAX_PAGES_WITHOUT_SLEEP == 0:
            sleep(5)
        current_url = begin_url + str(i) + end_url
        while True:
            try:
                request_html = requests.get(current_url).text
                break
            except (requests.exceptions.Timeout,
                    requests.exceptions.RequestException,
                    requests.exceptions.ConnectionError,
                    ConnectionError):
                sleep(60)
        number_with_nulls = add_nulls(i)
        while WRONG_TEXT in request_html:
            percent_done = round((i - first_number) / number_pages * 100, 2)
            logger.warning("%s: soft_ban, %s%% done", repr(number_with_nulls), repr(percent_done))
            sleep(60)
            request_html = requests.get(current_url).text
        output_file = output_dir + "/" + number_with_nulls
        if NO_ACCESS in repr(request_html) or NO_URL in repr(request_html) or EMPTY in repr(request_html):
            continue
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(request_html)

    logger.info("Finish download from %s to %s", repr(
        first_number), repr(first_number + number_pages))


def download(site_name, content, first_number, number_pages):
    setup_logging()
    logger.info("Start download.")

    error_flag = 0
    current_begin_url = BEGIN_URL
    current_end_url = ""

    if site_name == "vc":
        logger.info("Start download vc.ru")
        current_begin_url += "vc"
    elif site_name == "tj":
        logger.info("Start download tjournal")
        current_begin_url += "tjournal"
    elif site_name == "dtf":
        logger.info("Start download dtf")
        current_begin_url += "dtf"
    else:
        logger.error("Unknown site.")
        error_flag = 1
    current_begin_url += ".ru/v1.9/entry/"

    if content == "posts":
        logger.info("Start download posts.")
    elif content == "comments":
        logger.info("Start download comments.")
        current_end_url += "/comments"
    else:
        logger.error("It is unclear what to download")
        error_flag = 1

    if not error_flag:
        logger.info("Start download from %s to %s", repr(
            first_number), repr(first_number + number_pages))
        requests_content(current_begin_url, current_end_url,
                         first_number, number_pages)
