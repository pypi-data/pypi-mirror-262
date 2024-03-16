# ruff: noqa
from typing import Any, TYPE_CHECKING, TypeVar
import pandas as pd
import polars as pl

import narwhals as nw

T = TypeVar("T")


def my_agnostic_function(
    suppliers_native: T,
    parts_native: T,
) -> T:
    suppliers = nw.DataFrame(suppliers_native)
    parts = nw.DataFrame(parts_native)

    result = (
        suppliers.join(parts, left_on="city", right_on="city")
        .filter(
            nw.col("color").is_in(["Red", "Green"]),
            nw.col("weight") > 14,
        )
        .group_by("s", "p")
        .agg(
            weight_mean=nw.col("weight").mean(),
            weight_max=nw.col("weight").max(),
        )
    ).with_columns(nw.col("weight_max").cast(nw.Int64))
    return nw.to_native(result)


suppliers = {
    "s": ["S1", "S2", "S3", "S4", "S5"],
    "sname": ["Smith", "Jones", "Blake", "Clark", "Adams"],
    "status": [20, 10, 30, 20, 30],
    "city": ["London", "Paris", "Paris", "London", "Athens"],
}
parts = {
    "p": ["P1", "P2", "P3", "P4", "P5", "P6"],
    "pname": ["Nut", "Bolt", "Screw", "Screw", "Cam", "Cog"],
    "color": ["Red", "Green", "Blue", "Red", "Blue", "Red"],
    "weight": [12.0, 17.0, 17.0, 14.0, 12.0, 19.0],
    "city": ["London", "Paris", "Oslo", "London", "Paris", "London"],
}

reveal_type(parts)

print("pandas output:")
print(
    my_agnostic_function(
        pd.DataFrame(suppliers),
        pd.DataFrame(parts),
    )
)
print("\nPolars output:")
print(
    my_agnostic_function(
        pl.DataFrame(suppliers),
        pl.DataFrame(parts),
    )
)
reveal_type(
    my_agnostic_function(
        pl.DataFrame(suppliers),
        pl.DataFrame(parts),
    )
)
print("\nPolars lazy output:")
print(
    my_agnostic_function(
        pl.LazyFrame(suppliers),
        pl.LazyFrame(parts),
    ).collect()
)
