from typing import List

from . import api
from gcptool.inventory.cache import with_cache, Cache

@with_cache("compute", "target_ssl_proxies")
def __all(project_id: str):
    return api.target_ssl_proxies.list(project=project_id).execute().get("items", [])

def all(project_id: str, cache: Cache) -> List[str]:
    return [proxy for proxy in __all(cache, project_id)]