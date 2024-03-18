# -*- coding: utf-8 -*-
"""Documentation about the Geometry-to-Grid generator module."""

import logging
from itertools import product
from typing import Tuple

import geopandas as gpd
import numpy as np
import shapely.geometry

logger = logging.getLogger(__name__)


def simple_gridify(
    area: gpd.GeoDataFrame, grid_size: Tuple[float, float] = (288, 288)
) -> gpd.GeoDataFrame:
    """Construct grid that covers an area.

    Gridify covers the area with grid_size sized box shaped
    polygons.

    Parameters
    ----------
    area : geopandas.GeoDataFrame
        Area to cover with grid sized box shaped polygons.
    grid_size : tuple[float, float]
        The size (width, height) of the sized box shaped polygons in [meter]

    Returns
    -------
    geopandas.GeoDataFrame
        Geopandas dataframe containing grid covering the area.
    """
    # set coordinate system to the RD (EPSG:28992) to work with meters
    area_rd = _transform_to_rd_crs(area)
    minx, miny, maxx, maxy = area_rd.total_bounds
    width, height = grid_size
    grid = _make_grid(minx, miny, maxx, maxy, width, height)
    if area_rd.crs and area.crs:
        grid = grid.set_crs(area_rd.crs, allow_override=True).to_crs(area.crs)

    grid = grid.sjoin(area, how="inner", predicate="intersects").drop_duplicates(
        subset="geometry"
    )
    grid["col"] = range(grid.shape[0])  # For debugging / vis

    return grid


def gridify(
    include_area: gpd.GeoDataFrame,
    exclude_area: gpd.GeoDataFrame = None,
    grid_size: Tuple[float, float] = (288, 288),
    include_partial: bool = True,
) -> gpd.GeoDataFrame:
    """Construct grid that covers an area.

    Gridify covers the area given by include_area with grid_size sized box shaped
    polygons. The area indicated by exclude_area is subtracted. If include_partial
    is True (default), then boxes that partially overlap the resulting area are
    included, and if include_partial is False then they are excluded.

    Parameters
    ----------
    include_area : geopandas.GeoDataFrame
        Geopandas dataframe that indicates the area to be included
    exclude_area : geopandas.GeoDataFrame
    grid_size : tuple[float, float]
        The size (width, height) of the sized box shaped polygons.
    include_partial : bool

    Returns
    -------
    geopandas.GeoDataFrame
        Geopandas dataframe containing grid covering include_area excluding exclude_area.

    """
    grid = simple_gridify(include_area, grid_size)

    if exclude_area is not None:
        exclude_poly = exclude_area.dissolve().geometry[0]
        if include_partial:
            grid = grid[~grid.within(exclude_poly)]
        else:
            grid = grid[~grid.intersects(exclude_poly)]

    return grid


def overlay_gridify(
    primary_area: gpd.GeoDataFrame,
    secondary_area: gpd.GeoDataFrame,
    how: str = "difference",
    grid_size: Tuple[float, float] = (288, 288),
):
    """Construct grid over a performed spatial overlay between two areas.

    Gridify covers the area of the performed spatial overlay between two
    areas with grid_size sized box shaped polygons.

    Parameters
    ----------
    primary_area : geopandas.GeoDataFrame
        Primary area for the spatial overlay operation
    secondary_area : geopandas.GeoDataFrame
        Secondary area for the spatial overlay operation
    how : str
        Method of spatial overlay: `intersection`, `union`, `identity`,
        `symmetric_difference` or `difference`. The default is `intersection`.
    grid_size : tuple[float, float]
        The size (width, height) of the sized box shaped polygons.

    Returns
    -------
    geopandas.GeoDataFrame
        Geopandas dataframe containing grid covering the performed spatial
        overlay operation.
    """
    return simple_gridify(gpd.overlay(primary_area, secondary_area, how=how), grid_size)


def _make_grid(
    min_x: float, min_y: float, max_x: float, max_y: float, width: float, height: float
) -> gpd.GeoDataFrame:
    """Make a grid of polygons in a geopandas GeoSeries.

    Parameters
    ----------
        min_x: minimum x value of resulting grid
        min_y: minimum y value of resulting grid
        max_x: maximum x value of resulting grid
        max_y: maximum y value of resulting grid
        width: width of grid cells
        height: height of grid cells

    Returns
    -------
    gpd.GeoDataFrame containing a grid with bounding points (min_x, min_y, max_x, max_y)
    built out of width x height cells
    """
    return gpd.GeoDataFrame(
        geometry=gpd.GeoSeries(
            [
                shapely.geometry.box(x, y, x + width, y + height)
                for x, y in product(
                    np.arange(min_x, max_x, width), np.arange(min_y, max_y, height)
                )
            ]
        )
    )


def _transform_to_rd_crs(area: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Transform the GeoDataframe to a new GeoDataframe in the RD-coordinate system.

    Transform the geometry to EPSG:28992. If no CRS is set on the geometry, the
    GeoDataframe will not be transformed to the RD-coordinate system.
    """
    rd_crs = "EPSG:28992"

    if area.crs is not None:
        if area.crs != rd_crs:
            logger.warning(
                "Geometry is not in in %s, but %s CRS. "
                "Transformed geometry might have inaccuracies.",
                rd_crs,
                area.crs,
            )
        return area.to_crs(rd_crs)
    logger.warning(
        "No CRS is set on the GeoDataFrame, cannot transform GeoDataFrame to %s", rd_crs
    )
    return area
