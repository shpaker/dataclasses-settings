from typing import Any, Dict, Optional


def field_params(
    alias: Optional[str] = None,
) -> Dict[str, Any]:
    return dict(
        alias=alias,
    )
