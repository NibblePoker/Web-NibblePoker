from dataclasses import dataclass, field
import os

import yaml

from nibblepoker.objects.content.applet import ContentApplet
from nibblepoker.objects.content.project import ContentProject
from nibblepoker.objects.content.tool import ContentTool


@dataclass
class ContentRepository:
    applets: dict[str, ContentApplet] = field(default_factory=dict)
    # articles: list[Con] = field(default_factory=list)
    projects: dict[str, ContentProject] = field(default_factory=dict)
    tools: dict[str, ContentTool] = field(default_factory=dict)
    #projects_languages: list[str] = field(default_factory=list)

    #    # Loading articles definition files
    #    """for article_folder in os.listdir(os.path.join(os.getcwd(), "data/articles")):
    #        article_folder_path = os.path.join(os.getcwd(), "data/articles", article_folder)
    #        if not os.path.isdir(article_folder_path):
    #            continue
    #        pass"""

    #    # Preparing some more stuff
    #    for project in __CONTENT.projects.values():
    #        __CONTENT.projects_languages.extend(project.metadata.general.languages)
    #    __CONTENT.projects_languages = list(set(__CONTENT.projects_languages))
    #    __CONTENT.projects_languages.sort()
    #    #print(__CONTENT.projects_languages)

    def load_applets_folder(self, folder_path: str) -> None:
        for applets_file in os.listdir(folder_path):
            applets_file_path = os.path.join(folder_path, applets_file)

            if not os.path.isfile(applets_file_path) or applets_file.startswith("."):
                continue

            applets_data = yaml.safe_load(open(applets_file_path))
            if "applets" not in applets_data:
                print(f"Unable to load '{applets_file_path}' due to missing 'applets' field !")
                continue

            for applet_data in applets_data["applets"]:
                _applet = ContentApplet(**applet_data)
                self.applets[_applet.id] = _applet
                print(_applet)

    def load_projects_folder(self, folder_path: str) -> None:
        for project_file in os.listdir(folder_path):
            project_file_path = os.path.join(folder_path, project_file)
            if not os.path.isfile(project_file_path) or project_file.startswith("."):
                continue

            projects_data = yaml.safe_load(open(project_file_path))
            if "projects" not in projects_data:
                print(f"Unable to load '{project_file_path}' due to missing 'projects' field !")
                continue

            for project_data in projects_data["projects"]:
                _project = ContentProject(**project_data)
                self.projects[_project.id] = _project
                print(_project)

    def load_tools_folder(self, folder_path: str) -> None:
        for tools_file in os.listdir(folder_path):
            tools_file_path = os.path.join(folder_path, tools_file)
            if not os.path.isfile(tools_file_path) or tools_file.startswith("."):
                continue

            tools_data = yaml.safe_load(open(tools_file_path))
            if "tools" not in tools_data:
                print(f"Unable to load '{tools_file_path}' due to missing 'tools' field !")
                continue

            for tool_data in tools_data["tools"]:
                _tool = ContentTool(**tool_data)
                self.tools[_tool.id] = _tool
                print(_tool)

    def projects_to_ini(self) -> str:
        ini_data = ""
        for x in self.projects.values():
            ini_data += f"[{x.id}]\n"
            ini_data += f"Id={x.id}\n"
            ini_data += f"Priority={x.metadata.index.priority}\n"
            ini_data += f"Tags={"|".join(x.metadata.general.tags)}\n"
            ini_data += "\n"
        return ini_data

    def tools_to_ini(self) -> str:
        ini_data = ""
        for x in self.tools.values():
            ini_data += f"[{x.id}]\n"
            ini_data += f"Id={x.id}\n"
            ini_data += f"Priority={x.metadata.index.priority}\n"
            ini_data += f"Tags={"|".join(x.metadata.general.tags)}\n"
            ini_data += "\n"
        return ini_data
