from __future__ import annotations

import logging
from functools import update_wrapper
from typing import Protocol

import click

logger = logging.getLogger(__name__)

__all__ = [
    "NaturalOrderGroup",
    "get_full_command",
    "log_arguments",
]


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()


def get_full_command(ctx: click.Context | None) -> str:
    if ctx is None:
        return ""

    name = str(ctx.command.name)
    if parent := get_full_command(ctx.parent):
        return parent + " " + name
    return name


def log_arguments(f):
    @click.pass_context
    def wrapped(ctx: click.Context, *args, **kwargs):
        if logger.isEnabledFor(logging.INFO):
            import perigene

            logger.info("*" * 40)
            logger.info("PERiGene version %s", perigene.__version__)
            logger.info(
                "Running command '%s' with arguments:",
                get_full_command(ctx),
            )
            for key, val in kwargs.items():
                logger.info("%s: %s", key, val)
            logger.info("*" * 40)

        return ctx.invoke(f, *args, **kwargs)

    return update_wrapper(wrapped, f)


######################################################################
# Type hints
# Use typing.Protocol to avoid importing perigene just for type hinting.
######################################################################


class FilePrefixProtocol(Protocol):
    """Protocol for the FilePrefix class.
    Use this protocol to type hint the FilePrefix class without importing it.
    """

    ...


class RegionProtocol(Protocol):
    """Protocol for the Region class.
    Use this protocol to type hint the Region class without importing it.
    """

    ...


class ModelProtocol(Protocol):
    """Protocol for the Model class.
    Use this protocol to type hint the Model class without importing it.
    """

    ...
