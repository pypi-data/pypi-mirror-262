"""
Callbacks for click commands.
"""

from pathlib import Path

import click

from .params_utils import FilePrefixProtocol, ModelProtocol, RegionProtocol

__all__ = [
    "make_file_prefix",
    "split_commas",
]


def make_file_prefix(_ctx, param, param_val: Path) -> FilePrefixProtocol:
    from perigene.perigene_types import FilePrefix

    if param_val.is_dir():
        # If arg receieved is a directory, add default file prefix
        dir_out = param_val
        prefix_out = Path(param.default).name
    else:
        dir_out, prefix_out = param_val.parent, param_val.name
        if not dir_out.is_dir():
            raise click.BadParameter(f"Folder does not exist: {dir_out}")
    return FilePrefix(parent=dir_out, file_prefix=prefix_out)


def get_nullable_str(_ctx, param, param_val: str) -> str | None:

    if param_val.lower() == "none":
        return None
    return param_val.lower()


def get_model_cls(_ctx, param, param_val: str) -> ModelProtocol:
    from perigene.models import MODELS_STR_MAP

    return MODELS_STR_MAP.get(param_val)


def get_region_list(_ctx, param, param_val: list[str]) -> list[RegionProtocol]:
    from perigene.perigene_types import Region

    return [Region.from_str(v) for v in param_val]


def split_commas(_ctx, param, param_val: str) -> tuple:
    try:
        if not param_val:
            return ()
        return tuple(v.strip() for v in param_val.split(","))
    except ValueError:
        raise click.BadParameter(
            f"Values of {param} are expected to be comma separated."
        )


def read_lines(_ctx, param, param_val: str) -> list[str]:
    try:
        if not param_val:
            return []
        with open(param_val) as f:
            return [
                v.strip() for v in f.readlines() if v.strip() and not v.startswith("#")
            ]
    except ValueError:
        raise click.BadParameter(
            f"{param} is expected to be a file containing one value per line."
        )
