from nibblepoker.l10n.localizer import Localizer
from nibblepoker.website.downloads.structures import ReleaseVersion
from nibblepoker.website.downloads.utils import ReleaseVersionGroup


# Renders the row, or sub-segments of it.
def _render_release_version_group(release_data: ReleaseVersion, release_grouping: ReleaseVersionGroup,
                                  localizer: Localizer, lang: str) -> str:
    html = ""

    if release_grouping.sub_groups is None and release_grouping.artifact_values is None:
        raise Exception("Both subgroups and values are None !")

    if release_grouping.sub_groups is not None:
        html += f"<td rowspan='{len(release_grouping.sub_groups)}' class='bb-0'>"
        html += localizer.localize( lang, release_grouping.tag.lang_domain, release_grouping.tag.lang_key)
        html += f"</td>"
        for release_subgroup in release_grouping.sub_groups:
            html += _render_release_version_group(release_data, release_subgroup, localizer, lang)

    if release_grouping.artifact_values is not None:
        html += f"<td>"
        html += localizer.localize( lang, release_grouping.tag.lang_domain, release_grouping.tag.lang_key)
        html += f"</td>"

        html += f"<td>"
        for release_value in release_grouping.artifact_values:
            html += f"{release_value} - "
        html += f"</td>"
        html += f"</tr><tr>"

    return html


def render_release_version(release_data: ReleaseVersion, release_root_groups: list[ReleaseVersionGroup],
                           localizer: Localizer, lang: str) -> str:
    html = ""

    # TODO: Add headers
    html += "<table>"

    for release_subgroup in release_root_groups:
        if release_subgroup.sub_groups is not None:
            # Grouped release
            html += "<tr>"
            html += _render_release_version_group(release_data, release_subgroup, localizer, lang)
            html += "</tr>"
            html = html.replace("<tr></tr>", "")

        elif release_subgroup.artifact_values is not None:
            # Simple release (Not implemented/designed yet)
            pass

        else:
            raise Exception("Both subgroups and values are None !")

    html += "</table>"

    return html
