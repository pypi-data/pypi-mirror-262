from typing import *

from ..model.model import Model
from ..utils.resource import LinkedResource
from .api import HashboardAPI


def fetch_all_models() -> List[Model]:
    """
    Fetches all the models in the project.
    """
    wire_models = HashboardAPI.graphql(
        """
        query HashqueryModels($projectId: String!) {
            hashqueryModels(projectId: $projectId)
        }
        """,
        {"projectId": HashboardAPI.project_id},
    )["data"]["hashqueryModels"]
    return [Model.from_wire_format(wire) for wire in wire_models]


def fetch_all_connections() -> List[LinkedResource]:
    """
    Fetches all the data connections in the project.
    """
    raw_data_connections = HashboardAPI.graphql(
        """
        query HashqueryDataConnections($projectId: String!) {
            dataConnections(projectId: $projectId) { id, name }
        }
        """,
        {"projectId": HashboardAPI.project_id},
    )["data"]["dataConnections"]
    return [
        LinkedResource(
            id=wire["id"],
            # currently, DataConnections do not have aliases, so just use
            # the lowercased name and snake-spaced
            alias=cast(str, wire["name"]).replace(" ", "_").lower(),
        )
        for wire in raw_data_connections
    ]
