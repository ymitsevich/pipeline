"""Tests for the storage module."""

import os
import json
import pytest
from pathlib import Path

from pipeline.storage import JsonStorage
from pipeline.world import Stage, Place, Character


@pytest.mark.parametrize(
    "size_x,size_y",
    [
        (5, 5),
        (10, 10),
        (3, 7),
    ],
)
def test_json_storage_save_and_load(empty_place, tmp_path, size_x, size_y):
    """Test saving and loading a stage to/from JSON file."""
    # Create a test stage with some data
    stage = Stage.with_size(size_x=size_x, size_y=size_y)
    character = Character(type="mage")
    character.move(empty_place)
    stage.add_place(empty_place)

    # Create storage that writes to temp directory
    storage = JsonStorage()
    test_file = tmp_path / "stage.json"

    # Save the stage (temporarily change to test file)
    original_dir = os.getcwd()
    try:
        os.chdir(tmp_path)
        storage.save(stage)

        # Verify file was created and contains valid JSON
        assert test_file.exists()
        _assert_stage_size_in_file(test_file, size_x, size_y)

        # Load the stage back
        loaded_stage = storage.load()

        # Verify loaded stage matches original
        assert loaded_stage.size_x == stage.size_x
        assert loaded_stage.size_y == stage.size_y
        assert loaded_stage.places[2][3] is not None
        assert len(loaded_stage.places[2][3].characters) == 1
        assert loaded_stage.places[2][3].characters[0].type == "mage"
    finally:
        os.chdir(original_dir)


def test_json_storage_load_missing_file(tmp_path):
    """Test that loading a non-existent file raises an error."""
    storage = JsonStorage()

    # Change to empty temp directory where stage.json doesn't exist
    original_dir = os.getcwd()
    try:
        os.chdir(tmp_path)
        with pytest.raises(FileNotFoundError):
            storage.load()
    finally:
        os.chdir(original_dir)

def _assert_stage_size_in_file(file:str, size_x: int, size_y: int):
    """Assert that the stage has the correct size in the file."""
    with open(file, "r") as f:
        data = json.load(f)
        assert data["size_x"] == size_x
        assert data["size_y"] == size_y
