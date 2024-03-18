#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the gridify module.
"""
import pytest

from gridify.gridify import gridify, _transform_to_rd_crs


@pytest.mark.parametrize("include_partial", (True, False))
def test_gridify(include_area, exclude_area, include_partial):

    grid_size = ((1 / 3), (1 / 3))

    grid = gridify(
        include_area=include_area,
        exclude_area=exclude_area,
        grid_size=grid_size,
        include_partial=include_partial,
    )

    grid_no_exclude = gridify(
        include_area=include_area,
        grid_size=grid_size,
        include_partial=include_partial,
    )

    if include_partial:
        assert len(grid) == 7
    else:
        assert len(grid) == 4

    assert len(grid_no_exclude) == 8

    # ax = include_area.plot(alpha=0.5)
    # exclude_area.plot(ax=ax, alpha=0.5, color="red")
    # grid.plot(ax=ax, alpha=0.5, column="col")


def test_transform_to_rd_crs(include_area):
    area = include_area.set_crs("EPSG:4326")
    transformed_area = _transform_to_rd_crs(area)
    assert transformed_area.crs == "EPSG:28992"
