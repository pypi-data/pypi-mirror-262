import json
import os
from pathlib import Path

import click

import grob
from grob.main import TagSpec


@click.command()
@click.argument("spec", type=click.STRING, default="{name}.*")
@click.argument("root_dir", type=click.Path(path_type=Path), default=None)
@click.option(
    "--relative/--absolute",
    default=False,
    is_flag=True,
    help="Whether to return absolute paths or paths relative to ROOT_DIR",
)
def cli(spec: str, root_dir: Path, relative: bool):
    spec = _parse_spec(spec)
    # print(*os.listdir(root_dir), file=sys.stderr)
    files = grob.find(spec, root_dir=root_dir or Path(os.getcwd()), relative=relative)
    click.echo(json.dumps(files, indent=2, default=str))


def _parse_spec(raw_spec: str) -> TagSpec | dict[str, TagSpec]:
    if "," not in raw_spec and "=" not in raw_spec:
        return raw_spec
    spec = {}
    for part in raw_spec.split(","):
        part = part.strip()
        if "=" not in part:
            raise ValueError(
                f"Invalid tag specification: expected format `<tag_name>=<pattern>`, got '{part}'. Maybe one of the "
                "provided pattern provides commas, which is not supported."
            )
        tag, pattern = part.split("=", maxsplit=1)
        spec[tag.strip()] = pattern.strip()
    return spec


if __name__ == "__main__":
    cli()
