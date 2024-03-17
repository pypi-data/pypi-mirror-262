from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import polars as pl
import pytest

import narwhals as nw
from tests.utils import compare_dicts

df_pandas = pd.DataFrame({"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]})
df_polars = pl.DataFrame({"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]})
df_lazy = pl.LazyFrame({"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9]})


@pytest.mark.parametrize(
    "df_raw",
    [df_pandas, df_polars, df_lazy],
)
def test_sort(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.sort("a", "b")
    result_native = nw.to_native(result)
    expected = {
        "a": [1, 2, 3],
        "b": [4, 6, 4],
        "z": [7.0, 9.0, 8.0],
    }
    compare_dicts(result_native, expected)


@pytest.mark.parametrize(
    "df_raw",
    [df_pandas, df_polars, df_lazy],
)
def test_filter(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.filter(nw.col("a") > 1)
    result_native = nw.to_native(result)
    expected = {"a": [3, 2], "b": [4, 6], "z": [8.0, 9.0]}
    compare_dicts(result_native, expected)


@pytest.mark.parametrize(
    "df_raw",
    [df_pandas, df_polars, df_lazy],
)
def test_add(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.with_columns(
        c=nw.col("a") + nw.col("b"),
        d=nw.col("a") - nw.col("a").mean(),
    )
    result_native = nw.to_native(result)
    expected = {
        "a": [1, 3, 2],
        "b": [4, 4, 6],
        "z": [7.0, 8.0, 9.0],
        "c": [5, 7, 8],
        "d": [-1.0, 1.0, 0.0],
    }
    compare_dicts(result_native, expected)


@pytest.mark.parametrize(
    "df_raw",
    [df_pandas, df_polars, df_lazy],
)
def test_double(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.with_columns(nw.all() * 2)
    result_native = nw.to_native(result)
    expected = {"a": [2, 6, 4], "b": [8, 8, 12], "z": [14.0, 16.0, 18.0]}
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_sumh(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.with_columns(horizonal_sum=nw.sum_horizontal(nw.col("a"), nw.col("b")))
    result_native = nw.to_native(result)
    expected = {
        "a": [1, 3, 2],
        "b": [4, 4, 6],
        "z": [7.0, 8.0, 9.0],
        "horizonal_sum": [5, 7, 8],
    }
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_sumh_literal(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.with_columns(horizonal_sum=nw.sum_horizontal("a", nw.col("b")))
    result_native = nw.to_native(result)
    expected = {
        "a": [1, 3, 2],
        "b": [4, 4, 6],
        "z": [7.0, 8.0, 9.0],
        "horizonal_sum": [5, 7, 8],
    }
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_sum_all(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.select(nw.all().sum())
    result_native = nw.to_native(result)
    expected = {"a": [6], "b": [14], "z": [24.0]}
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_double_selected(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.select(nw.col("a", "b") * 2)
    result_native = nw.to_native(result)
    expected = {"a": [2, 6, 4], "b": [8, 8, 12]}
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_rename(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.rename({"a": "x", "b": "y"})
    result_native = nw.to_native(result)
    expected = {"x": [1, 3, 2], "y": [4, 4, 6], "z": [7.0, 8, 9]}
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_join(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    df_right = df.rename({"z": "z_right"})
    result = df.join(df_right, left_on=["a", "b"], right_on=["a", "b"], how="inner")
    result_native = nw.to_native(result)
    expected = {"a": [1, 3, 2], "b": [4, 4, 6], "z": [7.0, 8, 9], "z_right": [7.0, 8, 9]}
    compare_dicts(result_native, expected)


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_schema(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.schema
    expected = {"a": nw.dtypes.Int64, "b": nw.dtypes.Int64, "z": nw.dtypes.Float64}
    assert result == expected


@pytest.mark.parametrize("df_raw", [df_pandas, df_polars, df_lazy])
def test_columns(df_raw: Any) -> None:
    df = nw.LazyFrame(df_raw)
    result = df.columns
    expected = ["a", "b", "z"]
    assert len(result) == len(expected)
    assert all(x == y for x, y in zip(result, expected))


def test_accepted_dataframes() -> None:
    array = np.array([[0, 4.0], [2, 5]])
    with pytest.raises(
        TypeError,
        match="Expected pandas-like dataframe, Polars dataframe, or Polars lazyframe, got: <class 'numpy.ndarray'>",
    ):
        nw.LazyFrame(array)
