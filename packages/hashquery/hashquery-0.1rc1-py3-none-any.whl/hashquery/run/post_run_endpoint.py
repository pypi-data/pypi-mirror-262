from typing import *
from datetime import datetime

from ..hashboard_api.api import HashboardAPI
from .run_results import RunResults

if TYPE_CHECKING:
    from ..model.model import Model  # avoid circular dep


def post_run_endpoint(
    model: "Model",
    *,
    sql_only: bool = False,
    freshness: Optional[Union[datetime, Literal["latest"]]] = None,
    print_warnings: bool = True,
    print_exec_stats: bool = False,
) -> RunResults:
    freshness_datetime = datetime.now() if freshness == "latest" else freshness
    results_json = HashboardAPI.post(
        "db/v2/execute-model",
        {
            "model": model.to_wire_format(),
            "projectId": HashboardAPI.project_id,
            "options": {
                "sqlOnly": sql_only,
                "freshness": (
                    freshness_datetime.isoformat() if freshness_datetime else None
                ),
            },
        },
    )
    return RunResults(
        results_json,
        print_warnings=print_warnings,
        print_exec_stats=print_exec_stats,
    )
