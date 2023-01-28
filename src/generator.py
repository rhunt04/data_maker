"""
    generator.py

        Generate data in the requested schema using `faker`. Return as a list of
        data frames of the requested number of rows.

        TODO: Replace hard-coded write to csv with a middle-man: write to a
        pd.DataFrame and piggyback the write methods in exporting.        
"""

import csv
from faker import Faker
from pathlib import Path
from src.parser import get_config, Config, TableEntry


class DataGenerator(object):
    def __init__(self, config: Config):
        self.config: Config = config
        self.faker: Faker = Faker()

    def generate_table(self, table: TableEntry):
        config = dict(self.config.config)
        if table.table_config:
            # Overlay table-specific config.
            config.update(dict(table.table_config))

        print(
            "Generating {nrow} rows of {ncol} columns for `{table}`.".format(
                nrow=config["num_rows"], ncol=len(table.columns), table=table.name
            )
        )

        names = [col.name for col in table.columns]
        providers = [self.faker.__getattr__(col.col_type) for col in table.columns]

        # Ensure we have a place to save the data.
        Path(config["base_dir"]).mkdir(parents=True, exist_ok=True)

        filename = "{base}/{table}.{fmt}".format(
            base=config["base_dir"], table=table.name, fmt=config["out_format"]
        )
        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile, lineterminator="\n")
            writer.writerow(names)
            for n in range(config["num_rows"]):
                writer.writerow([p() for p in providers])

    def run(self):
        [self.generate_table(t) for t in self.config.tables]
