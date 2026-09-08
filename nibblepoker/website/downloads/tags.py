from dataclasses import dataclass, field


@dataclass
class ReleaseSortingTagGroup:
    table_header_lang_key: str
    table_header_lang_domain: str
    tags: list[ReleaseSortingTag]

    def __post_init__(self):
        for tag in self.tags:
            tag.parent = self


@dataclass
class ReleaseSortingTag:
    parent: ReleaseSortingTagGroup
    lang_key: str
    lang_domain: str
    keywords: list[str]

    # Smaller = 1st in the list, Bigger - later in the list
    importance: int = field(default=0)

    def matches(self, text: str) -> bool:
        for keyword in self.keywords:
            for segment_divider in ['.', '-', "_"]:
                if f"{segment_divider}{keyword}" in text:
                    return True
                if f"{keyword}{segment_divider}" in text:
                    return True
        return False


# NOTE: The sorting tags should be ordered in order of desired matching.
#       The importance/display order sorting is done later in the utility functions.
TAG_GROUPS: dict[str, ReleaseSortingTagGroup] = {
    "arch": ReleaseSortingTagGroup(
        "cpu.responsive",
        "commons",
        [
            ReleaseSortingTag(None, "cpu.x64", "commons", ["x64", "amd64"]),
            ReleaseSortingTag(None, "cpu.x86", "commons", ["x86", "i386"]),
            ReleaseSortingTag(None, "cpu.arm64", "commons", ["arm64"]),
        ]
    ),
    "win32crt": ReleaseSortingTagGroup(
        "win32crt.heading.simple",
        "commons",
        [
            ReleaseSortingTag(None, "win32crt.msvcrt", "commons", ["msvcrt"]),
            ReleaseSortingTag(None, "win32crt.ucrt", "commons", ["ucrt"]),
        ]
    ),
    "minified-python": ReleaseSortingTagGroup(
        "minified.heading.simple",
        "commons",
        [
            ReleaseSortingTag(None, "minified.true", "commons", ["min.py", "min-py", "py.min", "py-min"], 9),
            ReleaseSortingTag(None, "minified.false", "commons", ["py"], 1),
        ]
    ),
}

#"lang": {
#    "en":           ["english"],
#    "fr":           ["french"],
#    "multilingual": [],# empty = matches anything not matched above
#},
