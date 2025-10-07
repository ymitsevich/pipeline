from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional


def generate_random_world():
    place1 = Place(x=5, y=8)
    place2 = Place(x=4, y=9)

    stage = Stage.with_size(size_x=10, size_y=10)
    stage.add_place(place1)
    stage.add_place(place2)

    character1 = Character(type="mage")
    character1.move(place=place1)

    character2 = Character(type="warior")
    character2.move(place=place2)

    return stage


class Character(BaseModel):
    type: Literal["mage", "warior"]

    def move(self, place: Place):
        place.add_character(self)


class Place(BaseModel):
    x: int
    y: int
    characters: list[Character] = Field(default_factory=list)

    def add_character(self, character: Character):
        self.characters.append(character)


class Stage(BaseModel):
    size_x: int
    size_y: int
    places: list[list[Optional[Place]]] = Field(default_factory=list)

    @classmethod
    def with_size(cls, size_x: int, size_y: int) -> "Stage":
        grid = [[None for _ in range(size_y)] for _ in range(size_x)]
        return cls(size_x=size_x, size_y=size_y, places=grid)

    def add_place(self, place: Place) -> None:
        try:
            self.places[place.x][place.y] = place
        except IndexError:
            raise ValueError(f"Place ({place.x}, {place.y}) is out of bounds")
