import os
import re
import shutil
from html import escape
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader

from nibblepoker.website.adam.custom_html import resolve_custom_tags
from nibblepoker.website.adam.l10n import DEFAULT_LANG, ALLOWED_LANGS, load_strings
from nibblepoker.website.adam.url_fondler import url_set_lang as _url_set_lang
from nibblepoker.website.applets import consolidate_applet_config
from nibblepoker.website.content.repository import ContentRepository
from nibblepoker.website.downloads.structures import ReleaseVersionRepository
from nibblepoker.website.downloads.tags import TAG_GROUPS
from nibblepoker.website.downloads.utils import group_single_release
from nibblepoker.website.sidebar import SidebarEntryRepository
from nibblepoker.website.static_page import StaticPageDefRepository
from nibblepoker.website.web_brand import WebBrandRepository


#DOMAINS = [("nibblepoker.lu", "lu",), ("nibblepoker.com", "com",)]
DOMAINS = [("nibblepoker.lu", "lu",)]
RENDERS_OUT_DIR = "./static/renders/"
RENDERS_PROJECT_CARDS_OUT_DIR = "./static/renders/project-cards/"
RENDERS_TOOLS_CARDS_OUT_DIR = "./static/renders/tool-cards/"
CODE_SNIPPETS_DIR = "./data/code/"
ERROR_CODES = [403, 404, 500]


if os.environ.get('NP_HTML_POST_PROCESS', "NONE") == "MINIFY":
    print("Using 'Flask-Minify' as HTML minifying post-processor")

    #from flask_minify import Minify
    #Minify(app=app, html=True, js=True, cssless=True)

    def post_process_html(html_content: str) -> str:
        html_content = resolve_custom_tags(html_content)
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        html_content = html_content.replace('\n', '')
        html_content = html_content.replace('\t', '')
        html_content = re.sub(r'\s+', ' ', html_content)
        html_content = html_content.replace("> <", "><")
        return re.sub(r'\s+', ' ', html_content)

    # This fucking library breaks so much shit it's unbelievable.
    # And it takes FOREVER to compile because "MuH rUsT iS sUpErIoR"...
    # Eat shit and die.

    # print("Using 'minify' as HTML post-processor")
    # from minify_html import minify
    # def post_process_html(html_content: str) -> str:
    #     return minify(html_content).replace("> <", "><")
elif os.environ.get('NP_HTML_POST_PROCESS', "NONE") == "BS4":
    print("Using 'BeautifulSoup4' as HTML non-minifying post-processor")

    from bs4 import BeautifulSoup

    def post_process_html(html_content: str) -> str:
        html_content = resolve_custom_tags(html_content)
        return BeautifulSoup(html_content, features="html.parser").prettify()
else:
    print("Using no HTML post-processor")

    def post_process_html(html_content: str) -> str:
        html_content = resolve_custom_tags(html_content)
        return html_content


def url_set_lang(url: str, new_lang: Optional[str] = None):
    return _url_set_lang(url, new_lang, ALLOWED_LANGS)


def get_code_lines(file_name: str) -> list[str]:
    file_path = os.path.join(CODE_SNIPPETS_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as code_file:
            return code_file.readlines()
    else:
        return [f"ERROR: Missing file `{file_name}`"]


if __name__ == "__main__":
    # Clearing the output directory
    print(f"Clearing '{RENDERS_OUT_DIR}'...")
    shutil.rmtree(RENDERS_OUT_DIR, ignore_errors=True)
    os.makedirs(RENDERS_OUT_DIR, exist_ok=True)
    os.makedirs(RENDERS_PROJECT_CARDS_OUT_DIR, exist_ok=True)
    os.makedirs(RENDERS_TOOLS_CARDS_OUT_DIR, exist_ok=True)

    # Loading and processing brands
    web_brand_repo = WebBrandRepository()
    web_brand_repo.load_folder("./data/brands")
    with open("./data/brands.ini", "w") as f:
        f.write(web_brand_repo.to_ini())

    # Loading and processing page definitions
    static_page_defs = StaticPageDefRepository()
    static_page_defs.load_folder("./data/pages")
    static_page_defs.expand_served_paths(langs=ALLOWED_LANGS)
    with open("./data/pages.ini", "w") as f:
        f.write(static_page_defs.to_ini())

    # loading sidebar data
    sidebar_defs = SidebarEntryRepository()
    sidebar_defs.load_file("./data/sidebar.yml")

    # Loading content definitions
    content_repo = ContentRepository()
    content_repo.load_applets_folder("./data/applets/")
    content_repo.load_projects_folder("./data/projects/")
    content_repo.load_tools_folder("./data/tools/")
    with open("./data/projects.ini", "w") as f:
        f.write(content_repo.projects_to_ini())
    with open("./data/tools.ini", "w") as f:
        f.write(content_repo.tools_to_ini())

    # Loading L10N stuff
    localizer = load_strings("./data/strings")

    # Release data
    release_repo = ReleaseVersionRepository()
    release_repo.load_folder("./data/downloads")
    for releases_key in release_repo.get_all_releases().keys():
        print(f"> {releases_key}")
        for release_data in release_repo.get_releases_for(releases_key):
            print(release_data)
            print(group_single_release(release_data))


    def _localize(strings_key: str, strings_domain: Optional[str], language: str, args: list[str] = None) -> str:
        global localizer

        # Special condition for selects and their inherent inability to be localized easily.
        if strings_domain is None:
            string_key_parts = strings_key.split(".", 1)
            if len(string_key_parts) == 1:
                return strings_key
            return _localize(string_key_parts[0], string_key_parts[1], language, args)

        return localizer.localize(language, strings_domain, strings_key, args)


    def _raise(msg):
        raise Exception(msg)


    # Loading other non-exported data

    # Setting up Jinja2
    jinja_env = Environment(loader=FileSystemLoader("templates/"))
    jinja_env.trim_blocks = True
    jinja_env.lstrip_blocks = True
    jinja_env.strip_trailing_newlines = True

    # Preparing common context
    context: dict[str, Any] = {
        # L10N
        "page_lang": DEFAULT_LANG,
        "url_lang": None,
        "is_lang_explicit": False,
        "l10n": _localize,

        # URL shit & L10N in URLs
        "domain_part": "nibblepoker.lu",
        "domain_id": "lu",
        "domain_tld": "lu",  # Legacy, somewhat
        "canonical_url": "https://nibblepoker.lu/unset-canonical-url/",
        "absolute_url": "/unset-absolute-url/",
        "url_set_lang": url_set_lang,

        "is_standalone": False,
        "current_brand": None,

        # Content-related nightmares
        # Note: Do not directly give the IDs, let the page template resolve it !
        "applets_index": content_repo.applets,
        "projects_index": content_repo.projects,
        "tools_index": content_repo.tools,

        "consolidate_applet_config": consolidate_applet_config,

        # Release table stuff
        "get_all_releases": release_repo.get_all_releases,
        "get_releases_for": release_repo.get_releases_for,
        "get_latest_releases_for": release_repo.get_latest_releases_for,

        "group_single_release": group_single_release,

        "release_tag_groups": TAG_GROUPS,

        # Other data
        "sidebar_entries": sidebar_defs.get_all_sidebar_defs(),
        "get_code_lines": get_code_lines,

        # Commons
        "html_escape": escape,
        "raise": _raise,
    }


    # Rendering static pages
    print("Rendering static pages...")
    for domain in DOMAINS:
        domain_part = domain[0]
        domain_id = domain[1]

        print(f"> {domain_part}")

        context["domain_part"] = domain_part
        context["domain_id"] = domain_id
        context["domain_tld"] = domain_id

        for is_lang_explicit in [False, True]:
            for lang in ALLOWED_LANGS:
                print(f"-> {lang} - {"Explicit" if is_lang_explicit else "Implicit"}")

                context["page_lang"] = lang
                context["url_lang"] = lang if is_lang_explicit else None
                context["is_lang_explicit"] = is_lang_explicit


                for project_key in content_repo.projects.keys():
                    print(f"--> {project_key}")

                    context["card_project_id"] = project_key

                    t = jinja_env.get_template("components/content-card.jinja", globals=context)
                    with open(
                            os.path.join(
                                RENDERS_OUT_DIR,
                                "project-cards",
                                f"{domain_id}.{project_key}.{"expl" if is_lang_explicit else "impl"}.{lang}.html"),
                            "w", encoding="utf-8") as f:
                        f.write(post_process_html(t.render()))

                    context["card_project_id"] = None


                for tool_key in content_repo.tools.keys():
                    print(f"--> {tool_key}")

                    context["card_tool_id"] = tool_key

                    t = jinja_env.get_template("components/tool-card.jinja", globals=context)
                    with open(
                            os.path.join(
                                RENDERS_OUT_DIR,
                                "tool-cards",
                                f"{domain_id}.{tool_key}.{"expl" if is_lang_explicit else "impl"}.{lang}.html"),
                            "w", encoding="utf-8") as f:
                        f.write(post_process_html(t.render()))

                    context["card_tool_id"] = None


                for static_page_def in static_page_defs.get_all_page_defs().values():
                    print(f"--> {static_page_def.id}")

                    context["canonical_url"] = f"https://{domain_part}{static_page_def.canonical_path}"
                    context["absolute_url"] = f"/{static_page_def.canonical_path}/".replace("//", "/")

                    # Rendering non-standalone base
                    context["is_standalone"] = False
                    context["current_brand"] = None

                    t = jinja_env.get_template(static_page_def.template_path, globals=context)
                    with open(
                            os.path.join(
                                RENDERS_OUT_DIR,
                                f"{domain_id}.{static_page_def.output_base_name}.base.{"expl" if is_lang_explicit else "impl"}.{lang}.html"),
                            "w", encoding="utf-8") as f:
                        f.write(post_process_html(t.render()))

                    if not static_page_def.standalone:
                        continue

                    # Rendering the standalone version
                    context["is_standalone"] = True

                    if static_page_def.brandable:
                        brands_to_render = web_brand_repo.get_all_brands()
                    else:
                        brands_to_render = dict()
                        brands_to_render["nibblepoker"] = web_brand_repo.get_all_brands()["nibblepoker"]

                    for brand in brands_to_render.values():
                        print(f"---> {brand.id}")
                        context["current_brand"] = brand

                        t = jinja_env.get_template(static_page_def.template_path, globals=context)
                        with open(
                                os.path.join(
                                    RENDERS_OUT_DIR,
                                    f"{domain_id}.{static_page_def.output_base_name}.{brand.id}.{"expl" if is_lang_explicit else "impl"}.{lang}.html"),
                                "w", encoding="utf-8") as f:
                            f.write(post_process_html(t.render()))

                for error_code in ERROR_CODES:
                    print(f"--> error-{error_code}")

                    context["error_code"] = error_code
                    context["error_key"] = str(error_code)
                    context["canonical_url"] = f"https://{domain_part}/"
                    context["absolute_url"] = "/"
                    context["is_standalone"] = False
                    context["current_brand"] = None

                    t = jinja_env.get_template("pages/error.jinja", globals=context)
                    with open(
                            os.path.join(
                                RENDERS_OUT_DIR,
                                f"{domain_id}.error.{error_code}.{"expl" if is_lang_explicit else "impl"}.{lang}.html"),
                            "w", encoding="utf-8") as f:
                        f.write(post_process_html(t.render()))

    # Done rendering static pages
    pass
