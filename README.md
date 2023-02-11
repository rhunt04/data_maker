# `data_maker`

An interface for generating fake data in a schema using [`mimesis`](https://mimesis.name/en/master/).

You supply:

-   A `.yaml` configuration outlining dataset schemas, and some more general
    settings (e.g. an output format, number of rows to generate).

`data_maker`:

-   Reads the schema, validates it, uses `mimesis` to generate the requisite
    data sets it specifies, and outputs to the required spec.

## What `data_maker` doesn't do

-   Implement any of it's own data-faking steps.

## Examples

# Generate a single `.csv` table

The following `data_maker` configuration generates a table named
`names_list.csv` containing a number of rows of `mimesis`-generated data, via
the generic `full_name` provider with default arguments. The column name is
`name`.

```YAML
tables:
    - name: names_list
      columns:
          - name: name
            col_type: full_name
```

We build heavily on `mimesis`-supported syntax in general, and if one wants to
try to supply additional arguments to the `mimesis` `Field()` provider object,
one can, with an optional `args` dict.

```YAML
tables:
    - name: sampled_years_after_1990
      columns:
          - name: year
            col_type: year
            args:
              minimum: 9
```
