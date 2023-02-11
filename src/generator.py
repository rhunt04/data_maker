"""
generator.py.

    Generate data in the requested schema using `mimesis`. Return as a list
    of data frames of the requested number of rows.

"""

from pathlib import Path

from mimesis import Field, Schema

from src.parse_config import Config, TableEntry


class DataGenerator(object):
    """Handle data generation from schema(s)."""

    def __init__(self, config: Config):
        """Just get config object."""
        self.config: Config = config

    def generate_table(self, table: TableEntry):
        """Given a table schema entry, generate data."""
        config = dict(self.config.config)
        if table.table_config:
            # Overlay table-specific config.
            config.update(dict(table.table_config))

        # print(
        #     "Generating {nrow} rows of {ncol} columns for `{table}`.".format(
        #         nrow=config["num_rows"],
        #         ncol=len(table.columns),
        #         table=table.name,
        #     )
        # )

        _ = Field()
        schema = Schema(
            lambda: dict(
                [c.col_type, _(c.col_type, *c.args)] for c in table.columns
            )
        )

        # Ensure we have a place to save the data.
        Path(config["base_dir"]).mkdir(parents=True, exist_ok=True)

        filename = "{base}/{table}.{fmt}".format(
            base=config["base_dir"], table=table.name, fmt=config["out_format"]
        )

        # Process in chunks:
        schema.to_csv(file_path=filename, iterations=config["num_rows"])

    def run(self):
        """For tables in schema, run generator."""
        [self.generate_table(t) for t in self.config.tables]
