from dataclasses import dataclass
from typing import Optional

from nibblepoker.website.downloads.structures import ReleaseVersion
from nibblepoker.website.downloads.tags import TAG_GROUPS, ReleaseSortingTag


@dataclass
class ReleaseVersionGroup:
    tag: ReleaseSortingTag
    sub_groups: Optional[list[ReleaseVersionGroup]]
    artifact_values: Optional[list[str]]

    def count_subgroups(self) -> int:
        if self.sub_groups is not None:
            return len(self.sub_groups)
        if self.artifact_values is not None:
            return 0
        raise Exception("Both subgroups and values are None !")


def _prepare_groups_from_tags(remaining_tags: list[str]) -> list[ReleaseVersionGroup]:
    returned_groups = list()

    if remaining_tags[0] not in TAG_GROUPS:
        raise Exception(f"The {remaining_tags[0]} isn't known !")

    # Creating the groups for this tag
    for tag in TAG_GROUPS[remaining_tags[0]].tags:
        returned_groups.append(ReleaseVersionGroup(tag, None, None))

    # Populating the subs and values
    for returned_group in returned_groups:
        if len(remaining_tags) > 1:
            returned_group.sub_groups = _prepare_groups_from_tags(remaining_tags[1:])
        else:
            returned_group.artifact_values = list()

    return returned_groups


def _add_download_tags_entries(artifacts: list[str], download_groups: list[ReleaseVersionGroup],
                               parent_tags: Optional[list[ReleaseSortingTag]] = None) -> None:
    if parent_tags is None:
        parent_tags = list()

    for download_group in download_groups:
        current_tags = parent_tags + [download_group.tag]

        if download_group.sub_groups is not None:
            # Adding sub-tags
            _add_download_tags_entries(artifacts, download_group.sub_groups, current_tags)

        elif download_group.artifact_values is not None:
            # Adding every entry that matches all tags along the chain, then
            # removing it from the shared pool so a broader/catch-all tag
            # processed later (e.g. "py" matching both minified and regular
            # builds) doesn't also claim it.
            for artifact in list(artifacts):
                had_all_tags = True

                for tag in current_tags:
                    if not tag.matches(artifact):
                        had_all_tags = False
                        break

                if had_all_tags:
                    download_group.artifact_values.append(artifact)
                    artifacts.remove(artifact)
        else:
            raise Exception("Both subgroups and values are None !")


# FIXME: BROKEN !!!
def _sort_groups_by_importance(groups: list[ReleaseVersionGroup]) -> None:
    groups.sort(key=lambda g: g.tag.importance, reverse=True)
    for group in groups:
        if group.sub_groups:
            _sort_groups_by_importance(group.sub_groups)


def group_single_release(release_data: ReleaseVersion) -> list[ReleaseVersionGroup]:
    # Preparing the structure
    groups: list[ReleaseVersionGroup] = _prepare_groups_from_tags(release_data.columns)

    # Adding the entries (working on a copy so the release's own artifact
    # list isn't consumed/mutated in the process)
    _add_download_tags_entries(list(release_data.artifacts), groups)

    # Sorting based on importance and not desired matching order
    _sort_groups_by_importance(groups)

    return groups
