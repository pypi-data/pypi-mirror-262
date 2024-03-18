"""Class to process raw data into Gridify grids."""

import logging
import os
from pathlib import Path
from typing import Optional, Tuple, Union

import geopandas as gpd

import gridify.gridify as gridify

logger = logging.getLogger(__name__)

# Dictionary with the supported GIS file formats.
gis_file_format_extensions = {
    "GeoJSON": ".geojson",
    "Shapefile": ".shp.zip",
    "GPKG": ".gpkg",
}


class GridifyProcessor:
    """Class to process raw data into Gridify grids."""

    def __init__(
        self,
        path_to_primary_geometry: Union[os.PathLike, str],
        path_to_secondary_geometry: Optional[Union[os.PathLike, str]] = None,
        path_to_output_dir: Optional[Union[os.PathLike, str]] = None,
        file_format: str = "GeoJSON",
        crs: str = "EPSG:4326",
        as_centroids: bool = False,
    ):
        """Class to process raw data into Gridify grids.

        The GridifyProcessor is initialized by a path to the primary geometry
        and possible secondary geometry. An output directory path may be set. The
        processor is able to generate a grid for different geofiles types and crs.
        When as_centroids is set to `True`, the grid is transformed into a grid of
        centroids (centre points of the grid boxlike polygons).

        Parameters
        ----------
        path_to_primary_geometry: os.PathLike
            Path to the primary geometry file.
        path_to_secondary_geometry: Optional[os.PathLike]
            Optional path to the secondary geometry file. If not provided, spatial overlay
            grid generation is not possible.
        path_to_output_dir: Optional[os.PathLike]
            Optional path to the output directory. If not provided the output directory
            is set to the directory of the primary geometry file.
        file_format: str
            The file format to save the grid as. Possible values are {"GeoJSON", "Shapefile",
            "GPKG"}
        crs: str
            The CRS of the grid.
        as_centroids: bool
            Whether the grid is saved as a grid of centroids.
        """
        self.path_to_primary_geometry = Path(path_to_primary_geometry)
        self.file_format = file_format
        self.crs = crs
        self.as_centroids = as_centroids
        if path_to_secondary_geometry:
            self.path_to_secondary_geometry = Path(path_to_secondary_geometry)
        else:
            self.__path_to_secondary_geometry = Path()
            self.__secondary_gdf = None
        if path_to_output_dir:
            self.path_to_output_dir = Path(path_to_output_dir)
        else:
            self.path_to_output_dir = self.path_to_primary_geometry.parent

    @property
    def primary_gdf(self) -> gpd.GeoDataFrame:
        """Get the primary GeoDataframe."""
        return self.__primary_gdf

    @property
    def secondary_gdf(self) -> Optional[gpd.GeoDataFrame]:
        """Get the secondary GeoDataframe if the path to the secondary geometry is set."""
        return self.__secondary_gdf

    @property
    def path_to_primary_geometry(self) -> Path:
        """Get the path to the primary geometry file."""
        return self.__path_to_primary_geometry

    @path_to_primary_geometry.setter
    def path_to_primary_geometry(self, path: Path):
        """Set the path to the primary geometry file.

        Raises
        ------
        FileNotFoundError
            When the specified path does not refer to an existing file.
        """
        if not path.is_file():
            raise FileNotFoundError(f"Path {path} is not a file.")
        self.__path_to_primary_geometry = path
        self.__primary_gdf = gpd.read_file(self.path_to_primary_geometry)

    @property
    def path_to_secondary_geometry(self) -> Path:
        """Get the path to the secondary geometry file.

        Raises
        ------
        FileNotFoundError
            When the path to the secondary geometry file is not set.
        """
        if self.__path_to_secondary_geometry.is_file():
            return self.__path_to_secondary_geometry
        raise FileNotFoundError("Path to secondary geometry is not set!")

    @path_to_secondary_geometry.setter
    def path_to_secondary_geometry(self, path: Path):
        """Set the path to the secondary geometry file.

        Raises
        ------
        FileNotFoundError
            When the specified path does not refer to an existing file.
        """
        if not path.is_file():
            raise FileNotFoundError(f"Path {path} is not a file.")
        self.__path_to_secondary_geometry = path
        self.__secondary_gdf = gpd.read_file(self.path_to_secondary_geometry)

    @property
    def path_to_output_dir(self) -> Path:
        """Get the path to the output directory."""
        return self.__path_to_output_dir

    @path_to_output_dir.setter
    def path_to_output_dir(self, path: Path):
        """Set the path to the output directory."""
        if not path.is_dir():
            raise FileNotFoundError(f"Path {path} is not a directory.")
        self.__path_to_output_dir = path

    @property
    def file_format(self) -> str:
        """Get the file format to save the grid as."""
        return self.__file_format

    @file_format.setter
    def file_format(self, file_format: str):
        """Set the file format to save the grid as."""
        if file_format not in gis_file_format_extensions:
            raise ValueError(f"File format {file_format} is not supported!")
        self.__file_format = file_format

    def gridify_primary_geometry(
        self, grid_size: Tuple[float, float] = (288, 288)
    ) -> Path:
        """Generate a grid over the primary geometry.

        Gridify covers the primary geometry with grid_size sized box shaped
        polygons. The grid is saved to the output directory.

        Parameters
        ----------
        grid_size : tuple[float, float]
            The size (width, height) of the sized box shaped polygons in [meters].

        Returns
        -------
        str
            Path to the generated grid.
        """
        grid = gridify.simple_gridify(self.primary_gdf, grid_size)
        return self.__save(
            geodata=grid,
            filename=self.path_to_primary_geometry.stem,
            grid_size=grid_size,
        )

    def gridify_secondary_geometry(
        self, grid_size: Tuple[float, float] = (288, 288)
    ) -> Path:
        """Generate a grid over the secondary geometry.

        Gridify covers the secondary geometry with grid_size sized box shaped
        polygons. The grid is saved to the output directory.

        Parameters
        ----------
        grid_size : tuple[float, float]
            The size (width, height) of the sized box shaped polygons in [meters].

        Returns
        -------
        str
            Path to the generated grid.
        """
        self.__verify_secondary_gdf()
        grid = gridify.simple_gridify(self.secondary_gdf, grid_size)
        return self.__save(
            geodata=grid,
            filename=self.path_to_secondary_geometry.stem,
            grid_size=grid_size,
        )

    def gridify_overlay(
        self, how: str = "difference", grid_size: Tuple[float, float] = (288, 288)
    ) -> Path:
        """Generate a grid over a performed spatial overlay between two areas.

        Gridify covers the area of the performed spatial overlay between primary
        geometry and secondary geometry with grid_size sized box shaped polygons.
        The grid is saved to the output directory.

        Parameters
        ----------
        how : str
            Method of spatial overlay: `intersection`, `union`, `identity`,
            `symmetric_difference` or `difference`. The default is `intersection`.
        grid_size : tuple[float, float]
            The size (width, height) of the sized box shaped polygons in [meters].

        Returns
        -------
        str
            Path to the generated grid.
        """
        self.__verify_secondary_gdf()
        grid = gridify.overlay_gridify(
            primary_area=self.primary_gdf,
            secondary_area=self.secondary_gdf,
            how=how,
            grid_size=grid_size,
        )
        return self.__save(
            geodata=grid,
            filename=f"{self.path_to_primary_geometry.stem}+{self.path_to_secondary_geometry.stem}_{how}",
            grid_size=grid_size,
        )

    def __verify_secondary_gdf(self):
        """Verify whether the secondary geometry is set.

        Raises
        ------
        ValueError
            When the secondary geometry is not set.
        """
        if self.secondary_gdf is None:
            logger.error("No secondary gdf file is set.")
            raise ValueError(
                "Secondary geometry is not set. Set path to secondary geometry first."
            )

    def __save(
        self, geodata: gpd.GeoDataFrame, filename: str, grid_size: Tuple[float, float]
    ) -> Path:
        """Save the geometry to a GeoData-file.

        Parameters
        ----------
        geodata : gpd.GeoDataFrame
            The GeoDataframe object to save.
        filename : str
            The filename to use without extension. The grid size and possible use of
            centroids are appended to this filename;
            (e.g. "<filename>_<with>x<height>_centroids>").
        grid_size : tuple[float, float]
            The size (width, height) of the sized box shaped polygons in [meters].

        Returns
        -------
        Path
            Path to the saved GeoDataFrame.
        """
        filename += f"_{grid_size[0]}x{grid_size[1]}"
        if self.as_centroids:
            geo = geodata.centroid
            filename += "_centroids"
        else:
            geo = geodata.geometry
        filename += gis_file_format_extensions[self.file_format]
        path = self.path_to_output_dir / filename
        geo.to_crs(self.crs).to_file(path, driver=self.file_format)
        logger.info(f"Saved grid GeoDataFrame to {path}")
        return path
