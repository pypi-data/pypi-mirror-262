"""This module contains the base model support.
"""

from typing import List, Optional, Union, Any
from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

from pydantic.dataclasses import dataclass
from pydantic.functional_validators import field_validator

from agptools.helpers import new_uid
from syncmodels.helpers.faker import fake


class SyncConfig:
    # anystr_lower = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True

    # min_anystr_length = 2
    # max_anystr_length = 10
    ## validate_all = True
    ## validate_assignment = True
    # error_msg_templates = {
    #'value_error.any_str.max_length': 'max_length:{limit_value}',
    # }
    # smart_union = True
    pass


# @dataclass(config=SyncConfig)
class BaseModel(PydanticBaseModel):
    @classmethod
    def _new_uid(cls):
        table = cls.__module__.replace(".", "_")
        return f"{table}:{new_uid()}"

    @classmethod
    def _random_data_(cls):
        return {
            "id": cls._new_uid(),
            "name": fake.item_name(),
            # "name": fake.name(),
            # "description": fake.sentence(),
            "description": fake.paragraph(nb_sentences=1),
        }

    @classmethod
    def random_item(cls):
        data = {
            **cls._random_data_(),
            "foo": 1,
        }
        return cls(**data)

    def __init__(self, /, **data: Any) -> None:  # type: ignore
        uid = data.pop("id", None) or new_uid()
        if ":" not in uid:
            table = self.__module__.replace(".", "_")
            uid = f"{table}:{uid}"
        super().__init__(id=uid, **data)
