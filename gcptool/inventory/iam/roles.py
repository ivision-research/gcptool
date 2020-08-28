from dataclasses import dataclass
from typing import Any, List, Set, Optional

from ..cache import Cache, with_cache
from . import api


@dataclass
class Role:
    name: str
    title: Optional[str]
    description: Optional[str]
    included_permissions: Set[str]
    deleted: bool


@with_cache("iam", "grantable_roles")
def __grantable_roles(resource: str) -> List[Any]:
    data: List[Any] = []
    body = {"fullResourceName": resource, "view": "FULL"}
    while True:
        request = api.roles.queryGrantableRoles(body=body)
        response = request.execute()

        data.extend(response.get("roles", []))

        if "nextPageToken" not in response:
            return data

        body["pageToken"] = response["nextPageToken"]


def grantable_roles(resource: str, cache: Cache) -> List[Role]:
    roles = __grantable_roles(cache, resource)

    parsed_roles: List[Role] = []

    for role in roles:
        parsed_roles.append(
            Role(
                role["name"],
                role.get("title"),
                role.get("description"),
                set(role.get("includedPermissions", [])),
                role.get("deleted", False),
            )
        )

    return parsed_roles


@with_cache("iam", "role")
def __get(name: str):
    return api.roles.get(name=name).execute()


def get(name: str, cache: Cache) -> Any:
    role_data = __get(cache, name)
    return role_data
