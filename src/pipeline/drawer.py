from pipeline.world import Stage


def draw(stage: Stage):
    for x in range(stage.size_x):
        for y in range(stage.size_y):
            if stage.places[x][y] is not None:
                character = stage.places[x][y].characters
                type = character[0].type
                typeAbbr = type[0]
                print(typeAbbr, end="")
            else:
                print(".", end="")
        print()
