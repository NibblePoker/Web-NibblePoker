
__CUSTOM_TAGS = {
    "default" : {
        "<np-content-spacer>": "<div class='content-spacer'>",
        "</np-content-spacer>": "</div>",

        "<np-section>": "<section class='mt-l mt-0-if-first'>",
        "</np-section>": "</section>",

        "<np-details>": "<details class='border bkgd-dark r-m mt-s'>",
        "</np-details>": "</details>",

        "<np-details-summary>": "<summary class='p-xs t-no-select'>",
        "</np-details-summary>": "</summary>",

        "<np-details-content>": "<div class='bt ox-auto'>",
        "</np-details-content>": "</div>",

        "<np-paragraph>": "<p class='mt-xs'>",
        "</np-paragraph>": "</p>",

        "<np-ul>": "<ul class='ml-s l-bullets l-bullet-inside'>",
        "</np-ul>": "</ul>",
    }
}


def resolve_custom_tags(html: str, theme="default"):
    if theme not in __CUSTOM_TAGS:
        return html

    for k, v in __CUSTOM_TAGS[theme].items():
        html = html.replace(k, v)

    return html
