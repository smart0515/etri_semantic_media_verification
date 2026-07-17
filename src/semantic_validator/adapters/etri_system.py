from __future__ import annotations

from typing import Any


class EtriSystemAdapter:
    """Interface boundary for the year-end ETRI target-system integration.

    The report-stage deliverable keeps this adapter unimplemented on purpose.
    A concrete adapter may later call an HTTP API, consume a JSONL exchange
    directory, or translate a transport-protocol payload.
    """

    def request_analysis(self, video_id: str, query: str) -> dict[str, Any]:
        raise NotImplementedError(
            "ETRI target-system protocol is not fixed in report-stage v0.1.0"
        )

