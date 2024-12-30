class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: tuple[int],
            end: tuple[int],
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.decks = self.create_ship(start, end)

    @staticmethod
    def create_ship(start: tuple[int], end: tuple[int]) -> list:
        if start[0] == end[0] and start[1] < end[1]:
            return [
                Deck(start[0], column)
                for column in range(start[1], end[1] + 1)
            ]
        elif start[0] < end[0] and start[1] == end[1]:
            return [
                Deck(row, start[1])
                for row in range(start[0], end[0] + 1)
            ]
        elif start[0] == end[0] and start[1] == end[1]:
            return [Deck(start[0], start[1])]

    def get_deck(self, row: int, column: int) -> Deck:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck

    def fire(self, row: int, column: int) -> None:
        self.get_deck(row, column).is_alive = False
        if not any(deck.is_alive for deck in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        self.field = self.create_field(ships)

        try:
            self._validate_field()
        except ValueError as ve:
            print(ve)
            exit()

    @staticmethod
    def create_field(ships: list[tuple]) -> dict:
        ships_list = []
        field_dict = {}

        for ship in ships:
            ships_list.append(Ship(ship[0], ship[1]))

        for ship in ships_list:
            for deck in ship.decks:
                field_dict[(deck.row, deck.column)] = ship

        return field_dict

    def fire(self, location: tuple) -> str:
        if location in self.field.keys():
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def print_field(self) -> None:
        field_string = ""

        for row in range(10):
            for column in range(10):
                if (row, column) in self.field.keys():
                    ship = self.field[(row, column)]
                    if ship.get_deck(row, column).is_alive:
                        field_string += u"\u25A1" + "\t"
                    else:
                        if ship.is_drowned:
                            field_string += "x" + "\t"
                        else:
                            field_string += "*" + "\t"
                else:
                    field_string += "~" + "\t"
            field_string += "\n"

        print(field_string)

    def _validate_field(self) -> None:
        ships_list = []

        for (row, column) in self.field.keys():
            ship = self.field[(row, column)]
            ships_list.append(ship)

        ships_list = list(set(ships_list))

        if len(ships_list) != 10:
            raise ValueError("The total number of the ships should be 10")
        if len([ship for ship in ships_list if len(ship.decks) == 1]) != 4:
            raise ValueError("There should be 4 single-deck ships")
        if len([ship for ship in ships_list if len(ship.decks) == 2]) != 3:
            raise ValueError("There should be 3 double-deck ships")
        if len([ship for ship in ships_list if len(ship.decks) == 3]) != 2:
            raise ValueError("There should be 2 three-deck ships")
        if len([ship for ship in ships_list if len(ship.decks) == 4]) != 1:
            raise ValueError("There should be 1 four-deck ship")

        not_allowed_cells = set()

        for ship in ships_list:
            for deck in ship.decks:
                not_allowed_cells.update(
                    {
                        (deck.row + 1, deck.column + 1),
                        (deck.row - 1, deck.column - 1),
                        (deck.row + 1, deck.column - 1),
                        (deck.row - 1, deck.column + 1)
                    }
                )
            if len(ship.decks) == 1:
                deck = ship.decks[0]
                not_allowed_cells.update(
                    {
                        (deck.row + 1, deck.column),
                        (deck.row - 1, deck.column),
                        (deck.row, deck.column + 1),
                        (deck.row, deck.column - 1)
                    }
                )
            else:
                start_row, start_column = ship.start
                end_row, end_column = ship.end
                if start_row == end_row:
                    not_allowed_cells.update(
                        {
                            (start_row, start_column - 1),
                            (end_row, end_column + 1)
                        }
                    )
                if start_column == end_column:
                    not_allowed_cells.update(
                        {
                            (start_row - 1, start_column),
                            (end_row + 1, end_column)
                        }
                    )

        for ship in ships_list:
            if (
                    ship.start in not_allowed_cells
                    or ship.end in not_allowed_cells
            ):
                raise ValueError(
                    "ships shouldn't be located in the neighboring cells "
                    "(even if cells are neighbors by diagonal)"
                )
