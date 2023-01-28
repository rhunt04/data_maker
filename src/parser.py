"""
    parser.py

        Parse user-supplied configuration files.

        Offer the option to generate an example configuration file.

"""

import inspect
from faker import Faker
from yaml import safe_load
from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Extra


class ColumnEntry(BaseModel, extra=Extra.forbid):
    name: str
    col_type: str
    fargs: Optional[Dict]

    @validator("col_type")
    def col_types_are_recognised_faker_methods(cls, col_type) -> str:
        """Ensure the column type variables correspond to faker providers.

        Args:
            col_type (str): the provider we're aiming to use to generate this
            column.

        Raises:
            ValueError: if the column type is _not_ a faker provider.

        Returns:
            str: the _valid_ column type.
        """
        providers = [m for m in dir(Faker()) if not m.startswith("_")]
        if col_type not in providers:
            raise ValueError(f"`{col_type}` is not a valid `faker` provider!")
        return col_type

    @validator("fargs")
    def fargs_are_recognised_provider_args(cls, fargs, values) -> dict:
        """Ensure user-supplied fargs are actually valid arguments for this
        provider.

        Args:
            fargs (dict): user-supplied dict of argument/value pairs.
            values (dict): pydantic-supplied dict of key/value pairs for class model.

        Raises:
            ValueError: if we identify that a supplied item in fargs is not a
            valid provider argument.

        Returns:
            dict: the set of valid arguments (not type checked!).
        """
        col_type = values.get("col_type")
        provider = Faker().__getattr__(col_type)
        provider_args = inspect.getfullargspec(provider).args
        valid_args = all([arg in provider_args for arg in fargs])
        if not valid_args:
            raise ValueError(
                f"{fargs} are not all arguments of the `{col_type}` provider!"
            )
        return valid_args


class MainConfigBlock(BaseModel, extra=Extra.forbid):
    info: Optional[str] = "Global configuration block"
    num_rows: Optional[int] = 100
    out_format: Optional[str] = "csv"
    base_dir: Optional[str] = "data"


class TableEntry(BaseModel, extra=Extra.forbid):
    name: str
    columns: List[ColumnEntry]
    table_config: Optional[MainConfigBlock]


class Config(BaseModel, extra=Extra.forbid):
    tables: List[TableEntry]
    config: Optional[MainConfigBlock] = MainConfigBlock()


def get_config(filename) -> Config:
    try:
        with open(filename) as conf_file:
            raw_conf = safe_load(conf_file)
            return Config.parse_obj(raw_conf)
    except Exception as e:
        raise SystemError(e)
