"""Tests for the gridify processor class."""

import os
from pathlib import Path

import geopandas as gpd
import pytest
from shapely import Point

from gridify.processor import GridifyProcessor, gis_file_format_extensions


class TestProcessor:

    @pytest.fixture()
    def path_primary(self, test_data_dir) -> Path:
        return Path(test_data_dir) / "square_1000.geojson"

    @pytest.fixture()
    def path_secondary(self, test_data_dir) -> Path:
        return Path(test_data_dir) / "square_150.geojson"

    @pytest.fixture()
    def path_output_dir(self, test_data_dir) -> Path:
        output_dir = Path(test_data_dir) / "output"
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    @pytest.fixture()
    def processor(
        self, path_primary, path_secondary, path_output_dir
    ) -> GridifyProcessor:
        return GridifyProcessor(
            path_to_primary_geometry=path_primary,
            path_to_secondary_geometry=path_secondary,
            path_to_output_dir=path_output_dir,
            crs="EPSG:28992",
        )

    def test_init_primary(self, test_data_dir, path_primary):
        """Test initializing the gridify processor."""

        processor = GridifyProcessor(path_primary)

        assert processor.path_to_primary_geometry == path_primary
        assert processor.primary_gdf is not None
        assert processor.path_to_output_dir == Path(test_data_dir)

        with pytest.raises(FileNotFoundError):
            print(processor.path_to_secondary_geometry)
        assert processor.secondary_gdf is None

    def test_set_secondary(self, path_primary, path_secondary):
        """Test set the secondary geometry after initialization."""

        processor = GridifyProcessor(path_primary)

        processor.path_to_secondary_geometry = path_secondary
        assert processor.path_to_secondary_geometry == path_secondary
        assert processor.secondary_gdf is not None

    def test_set_output_directory(self, path_primary, path_output_dir):
        """Test set a path to the output directory."""

        processor = GridifyProcessor(path_primary)

        processor.path_to_output_dir = path_output_dir
        assert processor.path_to_output_dir == path_output_dir

    def test_init_primary_secondary(self, path_primary, path_secondary):
        """Test initializing the gridify processor with primary and secondary geometries."""

        processor = GridifyProcessor(
            path_to_primary_geometry=path_primary,
            path_to_secondary_geometry=path_secondary,
        )

        assert processor.path_to_secondary_geometry == path_secondary
        assert processor.secondary_gdf is not None

    def test_init_primary_output_dir(self, path_primary, path_output_dir):
        """Test initializing the gridify processor with primary geometry and an output directory."""

        processor = GridifyProcessor(
            path_to_primary_geometry=path_primary, path_to_output_dir=path_output_dir
        )

        assert processor.path_to_output_dir == path_output_dir

    def test_gridify_primary_geometry(self, processor):
        """Test generating a grid over the primary geometry."""

        path_to_grid = processor.gridify_primary_geometry(grid_size=(100, 100))
        grid = gpd.read_file(path_to_grid)

        assert len(grid) == 100

    def test_gridify_secondary_geometry(self, processor):
        """Test generating a grid over the secondary geometry."""

        path_to_grid = processor.gridify_secondary_geometry(grid_size=(100, 100))
        grid = gpd.read_file(path_to_grid)

        assert len(grid) == 4

    def test_gridify_primary_secondary_geometry_difference(self, processor):
        """Test generating a grid over the spatial overlay of the primary and secondary geometries."""

        path_to_grid = processor.gridify_overlay(how="difference", grid_size=(100, 100))
        grid = gpd.read_file(path_to_grid)

        assert len(grid) == 99

    def test_centroid_grid(self, processor):
        """Test generating a grid off centroids."""

        processor.as_centroids = True
        path_to_grid = processor.gridify_primary_geometry(grid_size=(1000, 1000))

        grid = gpd.read_file(path_to_grid)

        assert grid.geometry[0] == Point(500, 500)

    def test_set_invalid_path(self, processor):
        """Test setting an invalid path raises an error."""

        invalid_path = Path("invalid_path")
        assert invalid_path.exists() == False

        with pytest.raises(FileNotFoundError):
            processor.path_to_primary_geometry = invalid_path
        with pytest.raises(FileNotFoundError):
            processor.path_to_secondary_geometry = invalid_path
        with pytest.raises(FileNotFoundError):
            processor.path_to_output_dir = invalid_path

    def test_gridify_without_secondary_geometry_set(self, path_primary):
        """Test generating a grid without the secondary geometry raises an error."""

        processor = GridifyProcessor(path_primary)

        with pytest.raises(ValueError):
            processor.gridify_secondary_geometry()
        with pytest.raises(ValueError):
            processor.gridify_overlay(how="difference")

    def test_set_invalid_file_format(self, processor):
        """Test setting an invalid file format raises an error."""

        with pytest.raises(ValueError):
            processor.file_format = "THIS_IS_NOT_A_VALID_FILE_FORMAT"

    @pytest.mark.parametrize("file_format", gis_file_format_extensions.keys())
    def test_save_to_other_formats(self, processor, file_format):
        """Test saving to other GIS file formats."""
        processor.file_format = file_format

        path_to_grid = processor.gridify_primary_geometry(grid_size=(1000, 1000))
        assert Path(path_to_grid).exists()
