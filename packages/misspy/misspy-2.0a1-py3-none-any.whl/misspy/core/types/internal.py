from pydantic import dataclasses

@dataclasses.dataclass(config=dict(extra="allow"))
class mspy:
    tlId: str