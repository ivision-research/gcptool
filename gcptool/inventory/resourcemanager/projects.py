import enum
from dataclasses import dataclass
from typing import Any, List, NewType, Optional

from . import api

# These classes are used to assist with deserialization of GCP project resources.


class LifecycleState(enum.Enum):
    """
    Used by the GCP API to represent the
    """

    ACTIVE = "ACTIVE"
    DELETE_REQUESTED = "DELETE_REQUESTED"


class ParentType(enum.Enum):
    ORGANIZATION = "organization"
    FOLDER = "folder"


# TODO - this could probably be a union of organization/folder ID types.
ParentId = NewType("ParentId", int)


@dataclass
class Parent:
    """
    Represents a GCP project's parent in the organiation hierarchy.
    """

    type: ParentType
    id: ParentId


ProjectNumber = NewType("ProjectNumber", int)
ProjectId = NewType("ProjectId", str)


@dataclass
class Project:
    """
    Represents a GCP project.
    """

    number: ProjectNumber
    id: ProjectId
    name: str
    state: LifecycleState
    parent: Optional[Parent] = None


def all() -> List[Project]:
    """
    Retrieve a list of all GCP projects this account has access to.
    """
    response = api.projects.list().execute()

    return [_parse(project) for project in response.get("projects", [])]


def get(id: str) -> Project:
    response = api.projects.get(projectId=id).execute()
    return _parse(response)


def _parse(raw: dict) -> Project:
    raw_parent = raw.get("parent")

    if raw_parent:
        parent: Optional[Parent] = Parent(raw_parent["type"], ParentId(raw_parent["id"]))
    else:
        parent = None

    return Project(
        ProjectNumber(raw["projectNumber"]),
        raw["projectId"],
        raw["name"],
        raw["lifecycleState"],
        parent,
    )
