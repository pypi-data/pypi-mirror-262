import json
import os
import re
from collections import OrderedDict, defaultdict
from datetime import date
from typing import Callable, Dict, Iterable, List, Optional

import requests
from commitizen import defaults, git, config
from commitizen.cz.base import BaseCommitizen
from commitizen.config.base_config import BaseConfig
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.defaults import Questions

__all__ = ["ConventionalYouTrackCz"]


def parse_scope(text):
    if not text:
        return ""

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return "-".join(scope)


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


class ConventionalYouTrackCz(BaseCommitizen):
    changelog_pattern = r"^(mile|feat|fix|refactor|perf)"
    bump_pattern = r"^(mile|feat|fix|refactor|perf)(\(.+\))?(!)?"
    bump_map = OrderedDict(
        (
            (r"^.+!$", defaults.MAJOR),
            (r"^mile", defaults.MAJOR),
            (r"^feat", defaults.MINOR),
            (r"^fix", defaults.PATCH),
            (r"^refactor", defaults.PATCH),
            (r"^perf", defaults.PATCH),
        )
    )
    change_type_order = ["Milestone", "Feature", "Fix", "Refactor", "Perf"]
    commit_parser = r"^(?P<change_type>feat|fix|refactor|perf|mile)(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)\n\n(?P<detail>.*(?:\n?\n(?!\d).*)*)\((?P<tasks>.*)\) ?"
    change_type_map = {
        "mile": "Milestone",
        "feat": "Feature",
        "fix": "Fix",
        "docs": "Documentation",
        "style": "Styling",
        "refactor": "Refactor",
        "perf": "Performance",
        "test": "Test",
        "build": "Build",
        "ci": "CI",
        "task": "Task",
        "chore": "Chore",
        "wip": "WIP",
    }

    # Read the config file
    conf = config.read_cfg()

    git_base_url = conf.settings.get("git_base_url", "https://github.com")
    use_gitlab = conf.settings.get("use_gitlab", False)
    git_repo = conf.settings.get("git_repo", "")
    projectid = conf.settings.get("projectid", "")
    youtrack_base_url = conf.settings.get("youtrack_base_url", "")
    youtrack_api_url = youtrack_base_url + "/api"
    yt_key = os.environ.get("YT_KEY")
    issues_api_endpoint = "/issues?query=project:%20{projectId}%20for:%20me%20%23Unresolved%20&fields=idReadable,summary,description"
    scope_api_endpoint = "/admin/customFieldSettings/bundles/ownedField?fields=id,name,values(id,name)"
    issue_app_url = "/issue/{issueId}"

    def questions(self) -> Questions:
        if "git_repo" not in self.conf.settings:
            print("Please add the key git_repo to your .cz.yaml|json|toml config file.")
            quit()

        if "projectid" not in self.conf.settings:
            print("Please add the key projectid to your .cz.yaml|json|toml config file.")
            quit()

        if "youtrack_base_url" not in self.conf.settings:
            print("Please add the key youtrack_base_url to your .cz.yaml|json|toml config file.")
            quit()

        questions: Questions = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "mile",
                        "name": "🎯 milestone: A milestone release. Correlates with MAJOR in SemVer",
                        "key": "m",
                    },
                    {
                        "value": "fix",
                        "name": "🐛 fix: A bug fix. Correlates with PATCH in SemVer",
                        "key": "x",
                    },
                    {
                        "value": "feat",
                        "name": "🎉 feat: A new feature. Correlates with MINOR in SemVer",
                        "key": "f",
                    },
                    {
                        "value": "docs",
                        "name": "📜 docs: Documentation only changes",
                        "key": "d",
                    },
                    {
                        "value": "style",
                        "name": (
                            "😎 style: Changes that do not affect the "
                            "meaning of the code (white-space, formatting,"
                            " missing semi-colons, etc)"
                        ),
                        "key": "s",
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "🔧 refactor: A code change that neither fixes "
                            "a bug nor adds a feature"
                        ),
                        "key": "r",
                    },
                    {
                        "value": "perf",
                        "name": "🚀 perf: A code change that improves performance",
                        "key": "p",
                    },
                    {
                        "value": "test",
                        "name": (
                            "🚦 test: Adding missing or correcting " "existing tests"
                        ),
                        "key": "t",
                    },
                    {
                        "value": "build",
                        "name": (
                            "🚧 build: Changes that affect the build system or "
                            "external dependencies (example scopes: pip, docker, npm)"
                        ),
                        "key": "b",
                    },
                    {
                        "value": "ci",
                        "name": (
                            "🛸 ci: Changes to our CI configuration files and "
                            "scripts (example scopes: GitLabCI)"
                        ),
                        "key": "c",
                    },
                    {
                        "value": "chore",
                        "name": (
                            "🧹 chore: General housekeeping chores"
                        ),
                        "key": "h",
                    },
                    {
                        "value": "task",
                        "name": (
                            "📥 task: General project task"
                        ),
                        "key": "a",
                    },
                    {
                        "value": "wip",
                        "name": (
                            "🧰 wip: Work-in-progress"
                        ),
                        "key": "w",
                    },
                ],
            },
            {
                "type": "select",
                "name": "scope",
                "message": (
                    "What is the scope of this change?:\n"
                ),
                "choices": []
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: (lower case and no period)\n"
                ),
            },
            {
                "type": "checkbox",
                "name": "tasks",
                "message": "Tasks(optional):\n",
                "choices": []
            },
            {
                "type": "list",
                "name": "task_status",
                "message": "Task Status:\n",
                "choices": [
                    {
                        "value": "",
                        "name": "🚫 Not Applicable",
                        "key": "x",
                    },
                    {
                        "value": "Fixed",
                        "name": "✔️ Fixed",
                        "key": "f",
                    },
                    {
                        "value": "In Progress",
                        "name": "🧰 Work In Progress",
                        "key": "w",
                    },
                ],
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: (press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit closes: (press [enter] to skip)\n"
                ),
            },
        ]

        if self.projectid != 0 and self.projectid is not None:
            url = self.youtrack_api_url + self.issues_api_endpoint.format(projectId=self.projectid)

            headers = {"Authorization": "Bearer " + str(self.yt_key)}

            r = requests.get(url, headers=headers)
            response_data = json.loads(r.text)

            if "error" in response_data:
                print("YouTrack returned an error: " + response_data["error"])
                quit()

            for question in filter(lambda q: q["name"] == "tasks", questions):
                for task in response_data:
                    question["choices"].append(
                        {
                            "value": task["idReadable"],
                            "name": task["idReadable"] + ": " + task["summary"] + "\n" + task["description"]
                        }
                    )

            url = self.youtrack_api_url + self.scope_api_endpoint.format(projectId=self.projectid)

            headers = {"Authorization": "Bearer " + str(self.yt_key)}

            r = requests.get(url, headers=headers)
            response_data = json.loads(r.text)

            if "error" in response_data:
                print("YouTrack returned an error: " + response_data["error"])
                quit()

            for question in filter(lambda q: q["name"] == "scope", questions):
                question["choices"].append(
                    {
                        "value": "project",
                        "name": "project"
                    }
                )
                question["choices"].append(
                    {
                        "value": "repo",
                        "name": "repo"
                    }
                )
                for ownedField in response_data:
                    if ownedField["name"] == "Traveller Universe: Subsystem":
                        for value in ownedField["values"]:
                            question["choices"].append(
                                {
                                    "value": value["name"],
                                    "name": value["name"]
                                }
                            )
        else:
            for question in filter(lambda q: q["name"] == "tasks", questions):
                question["type"] = "input"
                question["message"] = "Tasks ID(s) separated by spaces (optional):\n"
                question["filter"] = lambda x: x.strip() if x else ""
                del(question["choices"])

        return questions

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        tasks = answers["tasks"]
        tasks_status = answers["task_status"]
        tasks_text = ""
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE 🚨: {footer}"
        if footer:
            footer = f"\n\n{footer}"
        if tasks:
            tasks_text = ', '.join([f'#{task_id}' for task_id in tasks])
            tasks_text = f"\n\n({tasks_text}) {tasks_status}"

        message = f"{prefix}{scope}: {subject}{body}{footer}{tasks_text}"

        return message

    def example(self) -> str:
        return (
            "fix(code): correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "(#12) Fixed"
        )

    def schema(self) -> str:
        return (
            "<change_type>(<scope>): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: )<footer>\n"
            "(<tasks>)"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(mile|feat|fix|docs|style|refactor|perf|test|build|ci|task|chore|wip|bump)"
            r"(\(\S+\))?!?:(\s.*)"
        )
        return PATTERN

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "cz_commitizen_youtrack_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()

    def workitem_url_builder(self, issueId: str) -> str:
        url = self.youtrack_base_url + self.issue_app_url.format(issueId=issueId)
        return url

    def changelog_message_builder_hook(
            self, parsed_message: dict, commit: git.GitCommit
    ) -> dict:

        """add git and youtrack links to the changelog"""
        rev = commit.rev
        m = parsed_message["message"]
        s = parsed_message["scope"]

        if "tasks" in parsed_message:
            t = parsed_message["tasks"]
            parsed_message["scope"] = parsed_message["tasks"]
            parsed_message["scope"] = ", ".join(
                [
                    f"[{task_id}]({self.workitem_url_builder(task_id)})"
                    for task_id in parsed_message["tasks"].replace("#", "").split(", ")
                ]
            )
            parsed_message["scope"] = f"({s}) - " + parsed_message["scope"]
        else:
            parsed_message["scope"] = f"({s})"

        m = m.rstrip()
        lines = m.splitlines()

        if len(lines) > 1:
            for index, item in enumerate(lines):
                if index > 0 and len(item) > 0:
                    lines[index] = f"  - {item}"
                else:
                    del lines[index]

            m = '\n'.join(lines)

        if self.use_gitlab:
            parsed_message[
                "message"
            ] = f"\[[{rev[:5]}]({self.git_base_url}/{self.git_repo}/-/commit/{commit.rev})\] {m}"
        else:
            parsed_message[
                "message"
            ] = f"\[[{rev[:5]}]({self.git_base_url}/{self.git_repo}/commit/{commit.rev})\] {m}"

        return parsed_message
