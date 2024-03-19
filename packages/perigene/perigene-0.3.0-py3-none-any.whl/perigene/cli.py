#!/usr/bin/env python

import sys

import click

from . import __version__
from .commands.cmd_preprocessing import preprocessing
from .commands.cmd_run import run

# from .commands.cmd_step import step


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx: click.Context) -> list[str]:
        return list(self.commands.keys())


def init_logger(verbosity: int) -> None:
    import logging

    format = "[%(levelname)s - %(asctime)s] %(message)s"
    if verbosity < 1:
        lvl = logging.WARN
    elif verbosity == 1:
        lvl = logging.INFO
    else:
        lvl = logging.DEBUG
        format = (
            "[%(levelname)s - %(asctime)s] "
            "%(name)s.%(funcName)s:%(lineno)d: "
            "%(message)s"
        )

    logging.basicConfig(
        level=lvl,
        format=format,
        datefmt="%d %b %Y %H:%M:%S",
        stream=sys.stdout,
    )


@click.group(cls=NaturalOrderGroup)
@click.option(
    "-v",
    "--verbosity",
    count=True,
    help="Increases verbosity level. By default, only warning and errors are shown.",
)
@click.version_option(version=__version__)
def main(verbosity: int) -> None:
    """Polygenic Enrichments for Risk Gene prioritization (PERiGene)"""
    init_logger(verbosity)


main.add_command(preprocessing)
# main.add_command(step)
main.add_command(run)
