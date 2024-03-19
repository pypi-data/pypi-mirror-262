from functools import partial
from typing import cast

from promplate import ChainContext
from promptools.extractors.json import extract_json


class Context(ChainContext):
    def __init__(self, context: ChainContext):
        if not isinstance(context.get("snapshots"), list):
            context["snapshots"] = []
        super().__init__(context)

    @property
    def snapshots(self) -> list[dict]:
        return self["snapshots"]

    def __setitem__(self, key, value):
        self.snapshots[0][key] = value
        super().__setitem__(key, value)

    def __getitem__(self, key: str):
        if key != "snapshots":
            for snapshot in self.snapshots:
                if key in snapshot:
                    return snapshot[key]
        return super().__getitem__(key)

    @property
    def extract_json(self):
        try:
            return partial(extract_json, self.result, self.result)
        except NameError:  # pydantic v1
            # NameError: Field name "schema" shadows a BaseModel attribute; use a different field name with "alias='schema'".
            return partial(cast, val=extract_json(self.result))


def new_checkpoint(context: ChainContext):
    Context(context).snapshots.insert(0, {})
