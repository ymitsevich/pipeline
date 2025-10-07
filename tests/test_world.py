"""
Sample tests for pipeline.world module demonstrating pytest basics.
"""

import pytest
from pipeline.world import Character, Place, Stage, generate_random_world


# Test 1: Simple test - pytest discovers this automatically
def test_character_creation():
    """Test basic character creation."""
    character = Character(type="mage")
    assert character.type == "mage"


# Test 2: Using a fixture - reusable setup code

def test_place_starts_empty(empty_place):
    """Test that a new place has no characters."""
    assert len(empty_place.characters) == 0
    assert empty_place.x == 2
    assert empty_place.y == 3


def test_character_can_move_to_place(empty_place):
    """Test moving a character to a place."""
    character = Character(type="warior")
    character.move(empty_place)

    assert len(empty_place.characters) == 1
    assert empty_place.characters[0].type == "warior"


# Test 3: Parametrize - run same test with different inputs
@pytest.mark.parametrize(
    "char_type,expected_type",
    [
        ("mage", "mage"),
        ("warior", "warior"),
    ],
)
def test_character_types(char_type, expected_type):
    """Test character creation with different types."""
    character = Character(type=char_type)
    assert character.type == expected_type


@pytest.mark.parametrize(
    "size_x,size_y",
    [
        (5, 5),
        (10, 10),
        (3, 7),
    ],
)
def test_stage_creation_with_different_sizes(size_x, size_y):
    """Test that stages are created with correct dimensions."""
    stage = Stage.with_size(size_x=size_x, size_y=size_y)

    assert stage.size_x == size_x
    assert stage.size_y == size_y
    assert len(stage.places) == size_x
    assert len(stage.places[0]) == size_y


# Bonus: Testing the full world generation
def test_generate_random_world_creates_valid_stage():
    """Test that generate_random_world returns a properly configured stage."""
    stage = generate_random_world()

    assert stage.size_x == 10
    assert stage.size_y == 10
    # Check that places were added
    assert stage.places[5][8] is not None
    assert stage.places[4][9] is not None
