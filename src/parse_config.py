"""
    parser.py

        Parse user-supplied configuration files.

        Offer the option to generate an example configuration file.

"""

from mimesis.schema import Field
from yaml import safe_load
from typing import List, Optional, Dict
from pydantic import BaseModel, validator, Extra


class ColumnEntry(BaseModel, extra=Extra.forbid):
    # TODO: make name or col_type optional: perhaps "name" is the default,
    # and "col_type" is set to that, assuming one is happy for column names to
    # coincide with mimesis provider names (seems reasonable).
    name: str
    col_type: str
    args: Optional[Dict] = {}

    @validator("col_type")
    def col_types_are_recognised_providers(cls, col_type) -> str:
        """Ensure the column type variables correspond are mimesis Field providers.

        Args:
            col_type (str): the provider we're aiming to use to generate this
            column.

        Raises:
            ValueError: if the column type is _not_ a default Field provider.

        Returns:
            str: the _valid_ column type.
        """

        try:
            _ = Field()(col_type)
        except Exception as e:
            raise ValueError(
                f"`{col_type}` is not a valid `mimesis` Field provider!\n\n{e}"
            )
        return col_type

    @validator("args")
    def args_are_recognised_provider_args(cls, args, values) -> dict:
        """Ensure user-supplied args are actually valid arguments for this
        provider.

        Args:
            fargs (dict): user-supplied dict of argument/value pairs.
            values (dict): pydantic-supplied dict of key/value pairs for class model.

        Raises:
            ValueError: if we identify that a supplied item in args is not a
            valid provider argument.

        Returns:
            dict: the set of valid arguments (not type checked!).
        """
        col_type = values.get("col_type")
        try:
            _ = Field()(col_type, *args)
        except Exception as e:
            raise ValueError(
                f"arguments error for the `{col_type}` provider!\n\n{e}"
            )
        return args


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
