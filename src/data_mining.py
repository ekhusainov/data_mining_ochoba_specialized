from argparse import (
    ArgumentParser,
    ArgumentDefaultsHelpFormatter,
)
import logging
import logging.config
import os.path
from typing import DefaultDict

import yaml

from src.download_function.download import (
    download,
)

DEFAULT_LOGGING_PATH = "configs/logging.conf.yml"

APPLICATION_NAME = "core"

logger = logging.getLogger(APPLICATION_NAME)


def setup_logging():
    "Logger from yaml config."
    with open(DEFAULT_LOGGING_PATH) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin))


def callback_download(arguments):
    setup_logging()
    if arguments.site_name is None or arguments.content is None:
        logger.error("Enter site name and type content.")
    else:
        download(arguments.site_name, arguments.content,
                 arguments.first_number, arguments.number_pages)


def setup_parser(parser):
    "Argparser."
    subparsers = parser.add_subparsers(
        help="choose command",
    )

    download = subparsers.add_parser(
        "download",
        help="site name",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    download.add_argument(
        "-s", "--site",
        dest="site_name",
        help="help defalt TODO",
    )
    download.add_argument(
        "-c", "--content",
        dest="content",
        help="help defalt TODO",
    )
    download.add_argument(
        "-f", "--first_number",
        dest="first_number",
        help="TODO",
        default=1,
        type=int,
    )
    download.add_argument(
        "-n", "--number_pages",
        dest="number_pages",
        help="TODO",
        default=500,
        type=int,
    )
    download.add_argument(
        "-d", "--directory",
        dest="directory",
        help="TODO",
        default="output",
        type=str,
    )
    download.set_defaults(callback=callback_download)


def main():
    "Our int main."
    parser = ArgumentParser(
        prog=APPLICATION_NAME,
        description="Download ochoba sites",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
