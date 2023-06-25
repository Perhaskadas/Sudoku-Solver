class Board:
    # A class representing sudoku board
    def __init__(self, board: list[list]):
        """
        Initializes the Sudoku Board by having a list of its rows from left to right, a list of its columns
        from top to bottom
        :param board: A list containing each row of a sudoku board, 0s represent empty spaces
        """
        self.rows = board
        self.columns = list(map(list, zip(*board)))

    def print_board(self):
        """
        Prints a sudoku board in the console with more readable formatting
        :return: A text representation of the sudoku board
        """
        counter = 1
        print('- - - - - - - - - - - - - - -')
        for row in self.rows:
            print('| ', *row[0:3],' | ', *row[3:6], ' | ', *row[6:], '|')
            if counter % 3 == 0:
                print('- - - - - - - - - - - - - - -')
            counter += 1


    def find_empty(self) -> tuple[int, int]:
        """
        Finds the first empty square of a sudoku board starting from left to right, top to bottom
        :return: A tuple containing the row and column of the empty square
        """
        for row in range(9):
            for column in range(9):
                if self.rows[row][column] == 0:
                    return row, column

    def valid_entry(self, number: int, position: tuple[int, int]) -> bool:
        """
        Checks to see if it is possible to insert a specific number at a given position
        :param number: The number to be inserted
        :param position: The position the number is supposed to be inserted at
        :return: A True if valid, False if invalid
        """
        box = (position[0]//3, position[1]//3)
        for rows in range(box[0]*3, box[0]*3 + 3):
            for columns in range(box[1]*3, box[1]*3 + 3):
                if self.rows[rows][columns] == number and (rows, columns) != position:
                    return False
        if number in self.rows[position[0]]:
            return False
        if number in self.columns[position[1]]:
            return False
        return True

    def solve_sudoku(self) -> bool:
        """
        Solves the sudoku board in place, returns a bool depending on success
        :return: Returns a bool upon success or failure
        """
        if not self.find_empty():
            return True
        else:
            row, column = self.find_empty()

        for i in range(1,10):
            if self.valid_entry(i, (row, column)):
                self.rows[row][column] = i
                self.columns[column][row] = i

                if self.solve_sudoku():
                    return True

                self.rows[row][column] = 0
                self.columns[column][row] = 0

        return False