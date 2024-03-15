import os
import re
from collections import UserDict
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import NewType, TypeAlias, cast

InputKey = NewType("InputKey", str)
KeyPart = NewType("KeyPart", str)

FileTag = NewType("FileTag", str)
InputGroup: TypeAlias = dict[FileTag, Path | list[Path]]
TagSpec: TypeAlias = str | re.Pattern | Callable[[Path], str | None] | Callable[[Path], dict[str, str] | None]
Filter: TypeAlias = Callable[[Path], dict[KeyPart, str] | None]


DEFAULT_TAG_NAME = FileTag("default")
DEFAULT_KEY_PART = KeyPart("name")


def normalize_filter(pattern: TagSpec) -> Filter:
    if callable(pattern):
        filter_func = partial(parse_name_from_callable, func=pattern)
    else:
        filter_func = PathParser(pattern)
    return cast(Filter, filter_func)


def normalize_spec(spec: TagSpec | dict[str, TagSpec]) -> dict[FileTag, Filter]:
    if isinstance(spec, str) or callable(spec):
        return {DEFAULT_TAG_NAME: normalize_filter(spec)}
    return {FileTag(tag): normalize_filter(tag_spec) for tag, tag_spec in spec.items()}


def parse_name_from_pattern(name: str | Path, pattern: str) -> dict[KeyPart, str] | None:
    pass


def parse_name_from_callable(
    name: str | Path, func: Callable[[Path], str | None] | Callable[[Path], dict[str, str] | None]
) -> dict[KeyPart, str] | None:
    result = func(str(name))
    if result is None:
        return None
    # if not isinstance(result, dict):
    #     return {DEFAULT_KEY_PART: result}
    return cast(dict[KeyPart, str], result)


def parse_name(name: str | Path, spec: dict[FileTag, Filter]) -> tuple[FileTag, dict[KeyPart, str]] | None:
    for tag, tag_filter in spec.items():
        parsed = tag_filter(name)
        if parsed is not None:
            return tag, parsed
    return None


def get_key(parts: dict[KeyPart, str] | str, key_pattern: str) -> InputKey:
    # TODO: support optional parts
    # TODO: support arbitrary pattern
    if isinstance(parts, str):
        return InputKey(parts)
    return InputKey(key_pattern.format(**parts))


def get_key_pattern(parts: list[KeyPart], sep: str = "_") -> str:
    return sep.join("{" + part + "}" for part in parts)


class InputGroup(UserDict):
    def __init__(self, spec: dict[FileTag, Filter], allow_multiple: set[str]) -> None:
        super().__init__()
        self.allow_multiple = allow_multiple
        self.spec = spec


class KeyMaker:
    def __init__(
        self, key_pattern: str | None = None, use_full_path: bool = False, root_dir: Path | None = None, sep: str = "_"
    ) -> None:
        self._key_pattern = key_pattern
        self._key_parts: dict[KeyPart, int] = {}
        self._sep: str = sep
        self._root_dir = root_dir or Path(os.getcwd())
        self._use_full_path = use_full_path

    def get_key(self, path: Path, parts: dict[KeyPart, str] | str) -> InputKey:
        if isinstance(parts, str):
            return InputKey(parts)
        if self._key_pattern is not None:
            # TODO: display meaningful error message on error
            return InputKey(self._key_pattern.format(**parts))
        if self._use_full_path:
            if path.is_relative_to(self._root_dir):
                path = path.relative_to(self._root_dir)
            return InputKey(path.as_posix())
        unknown_key_parts = parts.keys() - self._key_parts.keys()
        for key_part in sorted(unknown_key_parts):
            self._key_parts[key_part] = len(self._key_parts)
        # TODO: display meaningful error message on KeyError. These can happen if the user provides:
        # - a regex with optional capturing groups
        # - a callable that don't always return the same set of keys
        # TODO: we could imagine providing a default value (`?` or `none` or an empty string) for optional keys
        return InputKey(self._sep.join(parts[part] for part in self._key_parts))


def find(
    spec: TagSpec | dict[str, TagSpec] = "**/*",
    root_dir: Path = Path("."),
    allow_multiple: bool | list[str] = False,
    optional: bool | list[str] = False,
    key: str | None = None,
    squeeze: bool = False,
    relative: bool = False,
) -> list[Path] | dict[InputKey, InputGroup]:
    must_squeeze = not isinstance(spec, dict) or (squeeze and len(spec) == 1)
    listable = isinstance(spec, str) and "{" not in spec
    spec = normalize_spec(spec)
    key_maker = KeyMaker(key_pattern=key, use_full_path=listable, root_dir=root_dir)
    accept_multiple_files = (
        set() if allow_multiple is False else set(spec.keys()) if allow_multiple is True else set(allow_multiple)
    )
    mandatory_tags = (
        set() if optional is True else set(spec.keys()) if optional is False else spec.keys() - set(optional)
    )
    files: dict[InputKey, dict[FileTag, Path | list[Path]]] = dict()
    # TODO: optimize by identifying fixed prefix and suffix
    # TODO: treat separately tags that don't expose some key parts
    for path in root_dir.rglob("*"):
        if path.is_dir():
            continue
        parsed = parse_name(path, spec)
        if parsed is None:
            continue
        if relative:
            path = path.relative_to(root_dir)
        tag, parts = parsed
        input_key = key_maker.get_key(path, parts)
        if input_key in files and tag in files[input_key] and files[input_key][tag] != path:
            if tag not in accept_multiple_files:
                # TODO: have custom exceptions
                raise ValueError(
                    f"Found two different files with the same key '{input_key}' and same tag '{tag}': "
                    f"{files[input_key][tag]} and {path}. You should either:\n- mark `{tag}` as allowing multiple files "
                    f"with `allow_multiple=['{tag}']`\n- mark all tags as allowing multiple files with "
                    f"`allow_multiple=True`\n- use a more specific filter for `{tag}` to ensure each key matches a unique"
                    " file."
                )
            else:
                files[input_key][tag].append(path)
        else:
            files.setdefault(input_key, {})[tag] = [path] if tag in accept_multiple_files else path
    invalid_input_groups = {}
    for input_key, input_group in files.items():
        missing_tags = [tag for tag in mandatory_tags if tag not in input_group]
        if missing_tags:
            invalid_input_groups[input_key] = missing_tags
    if invalid_input_groups:
        error_message = _format_missing_tag_error(invalid_input_groups)
        missing_tag = next(iter(invalid_input_groups.values()))[0]
        raise ValueError(
            f"{error_message}\nEither update the filters for these tags to ensure all files are matched or mark these "
            f"tags as optional with `optional=['{missing_tag}', ...]`"
        )
    if must_squeeze:
        squeezed = {key: next(iter(group.values())) for key, group in files.items()}
        if listable:
            return sorted(squeezed.values())
        return squeezed
    return files


def _format_missing_tag_error(invalid_input_groups):
    if len(invalid_input_groups) < 5:
        formatted_groups = "\n".join(
            f"- input '{input_key}': missing '" + "', '".join(missing_tags) + "'"
            for input_key, missing_tags in invalid_input_groups.items()
        )
        error_message = f"The following input groups are missing mandatory tags:\n{formatted_groups}"
    else:
        input_key, missing_tags = next(iter(invalid_input_groups.items()))
        formatted_tags = "', '".join(missing_tags)
        error_message = (
            f"Input group '{input_key}' is missing mandatory tag(s): '{formatted_tags}', as well as "
            f"{len(invalid_input_groups)} other input groups."
        )
    return error_message


def _create_named_capturing_group(match_obj):
    name = match_obj["placeholder"]
    modifier = "" if match_obj["greedy"] else "?"
    optional = match_obj["optional"]
    return f"(?P<{name}>[^/]+{modifier}){optional}"


def _convert_pattern_to_regex(pattern: str) -> re.Pattern:
    option_groups = []
    for group in re.findall(r"\([^/()]+(?:|[^/()]+)+\)", pattern):
        before = re.escape(group)
        after = "(?:" + "|".join(re.escape(option) for option in group[1:-1].split("|")) + ")"
        option_groups.append((before, after))
    # Unescape escaped parenthesis
    pattern = pattern.replace(r"\(", "(").replace(r"\)", ")")
    pattern = re.escape(pattern)
    for before, after in option_groups:
        pattern = pattern.replace(before, after)
    pattern = re.sub(r"(/)?\\\*\\\*(?(1)/?|/)", r"\1([^/]+/)*", pattern)
    pattern = pattern.replace(r"\*", "[^/]+")
    # Replace placeholders {name} by named capturing group (P<name>...)
    pattern = re.sub(
        r"\\{(?P<placeholder>[a-zA-Z_]\w*)(?P<greedy>!g)?\\}(?P<optional>\??)", _create_named_capturing_group, pattern
    )
    pattern += "$"
    regex = pattern
    return re.compile(regex)


def unformat(path: str | Path, pattern: str) -> dict[KeyPart, str] | None:
    regex = pattern if isinstance(pattern, re.Pattern) else _convert_pattern_to_regex(pattern)
    matches = regex.search(str(path))
    if not matches:
        return None
    return {KeyPart(key): value for key, value in matches.groupdict().items() if value is not None}


class PathParser:
    def __init__(self, pattern: str | re.Pattern) -> None:
        if isinstance(pattern, re.Pattern):
            self.pattern = None
            self.regex = pattern
        else:
            self.pattern = pattern
            self.regex = _convert_pattern_to_regex(pattern)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.pattern or self.regex}')"

    def __call__(self, path: Path) -> dict[KeyPart, str] | None:
        matches = self.regex.search(str(path))
        if not matches:
            return None
        return {KeyPart(key): value for key, value in matches.groupdict().items() if value is not None}
