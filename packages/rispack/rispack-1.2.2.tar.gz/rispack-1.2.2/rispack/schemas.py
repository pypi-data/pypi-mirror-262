from __future__ import annotations

from copy import deepcopy
from typing import Dict, Union

from marshmallow.utils import EXCLUDE
from marshmallow_dataclass import dataclass

DEFAULT_MASKS = {
    "document": {"only": 3},
    "password": True,
    "password_digest": True,
    "secret": True,
    "token": True,
}


def mask_data(data, mask=None):
    try:
        data = deepcopy(data)
        mask = mask or DEFAULT_MASKS

        if isinstance(data, dict):
            for key, value in data.items():
                if key in mask:
                    data[key] = _mask_value(value, mask[key])
                else:
                    data[key] = mask_data(value, mask)
        return data
    except Exception as e:
        logger.error(f"Error in mask_date: {e}")
        return ""


def _mask_value(value, config):
    only = None

    if isinstance(config, dict):
        only = config.get("only")

    if only and value and len(value) > only:
        return "*" * (len(value) - only) + value[-only:]

    return "*" * len(value)


class BaseSchema:
    @classmethod
    def load(cls, data: Union[dict, BaseSchema], unknown=EXCLUDE, **kwargs):
        if isinstance(data, BaseSchema):
            data = data.dump()

        return cls.Schema().load(data, unknown=unknown, **kwargs)

    def dump(self, skip_none=False, mask=None, **kwargs):
        data = self.Schema(**kwargs).dump(self)
        if skip_none:
            data = {key: val for key, val in data.items() if val is not None}

        if mask:
            if isinstance(mask, dict):
                data = mask_data(data, mask)
            else:
                data = mask_data(data)

        return data
