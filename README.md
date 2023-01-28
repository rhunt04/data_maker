# `data_maker`

An interface for generating fake data in a schema using [`faker`](https://github.com/joke2k/faker).

You supply:

-   A `.yaml` configuration outlining dataset schemas, and some more general
    settings (e.g. an output format, number of rows to generate).

`data_maker`:

-   Reads the schema, validates it, uses `faker` to generate the requisite
    data sets it specifies, and outputs to the required spec.

## What `data_maker` doesn't do

-   Implement any of it's own data-faking steps.

## Examples

# Generate a single `.csv` table

The following `data_maker` config generates a `.csv` tabled named
`integer_list` containing a number of rows of `faker`-generated data, via the
`pyint` provider with default arguments.

```YAML
tables:
    - name: integer_list
      columns:
          - name: super_integer
            col_type: pyint
```

We build heavily on `faker`-supported syntax in general, and if one wants to try
to supply additional arguments to the `faker.Faker()` provider object, one can,
with an optional `fargs` dict.

```YAML
tables:
    - name: integer_list
      columns:
          - name: super_integer
            col_type: pyint
            fargs:
              max_value: 9
```
