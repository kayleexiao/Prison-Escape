class game_map:

    def __init__(self, map_file, guard_file):
        try:
            temp_map = open(map_file).readlines()                   # add lines to a list
            temp_map = [line.rstrip("\n") for line in temp_map]     # remove \n from each line
            self.map = []
            # loop that makes a sublist for each line in the map
            for i in range(12):
                self.map.append([])
                for x in temp_map[i]:
                    self.map[i].append(x)
            print(self.map)
        except (IOError, OSError):
            print("File does not exist.")
            exit()

        try:
            temp_guards = open(guard_file).readlines()                  # add lines to a list
            temp_guards = [line.rstrip("\n") for line in temp_guards]   # remove \n from each line
            self.guard_info = []

            # loop that creates a sublist for the info list of each guard
            for i in range(len(temp_guards)):
                self.guard_info.append(temp_guards[i].split(" "))
            print(self.guard_info)
        except (IOError, OSError):
            print("File does not exist.")
            exit()

        self.guard_movements = []       # list for the movement list of each guard
        self.get_movements()
        self.guard_list = self.get_guards()     # list of guard objects
        self.player_location = [10, 1]      # starting player location

        # puts guards in initial starting position
        for guards in self.guard_list:
            self.map[int(guards.get_location()[0])][int(guards.get_location()[1])] = "G"

    def get_grid(self):
        return self.map     # return current map

    # method that makes a list of just the movements of guards
    def get_movements(self):

        for i in range(len(self.guard_info)):       # for each guard object
            self.guard_movements.append([])         # create sublist
            for x in range(3, len(self.guard_info[i])):
                self.guard_movements[i].append(self.guard_info[i][x])       # add movements of each guard to individual sublists

    def get_guards(self):
        guards = []
        for i in range(len(self.guard_info)):       # for each guard in guard info list, create a guard object
            guards.append(guard(self.guard_info[i][0], self.guard_info[i][1], self.guard_info[i][2], self.guard_movements[i]))

        return guards

    def update_player(self, direction):
        # replace old location of player with a space
        r = 0
        c = 0
        for row in self.map:
            for col in row:
                if self.map[r][c] == "P":
                    self.map[r][c] = " "
                c = c + 1
            c = 0
            r = r + 1

        # move player my updating player location
        if direction == "L":
            self.player_location[1] = self.player_location[1] - 1
            # if position that player tried to move to is a wall
            if self.map[self.player_location[0]][self.player_location[1]] == "#":
                self.player_location[1] = self.player_location[1] + 1       # under player movement
        elif direction == "R":
            self.player_location[1] = self.player_location[1] + 1
            if self.map[self.player_location[0]][self.player_location[1]] == "#":
                self.player_location[1] = self.player_location[1] - 1
        elif direction == "U":
            self.player_location[0] = self.player_location[0] - 1
            if self.map[self.player_location[0]][self.player_location[1]] == "#":
                self.player_location[0] = self.player_location[0] + 1
        elif direction == "D":
            self.player_location[0] = self.player_location[0] + 1
            if self.map[self.player_location[0]][self.player_location[1]] == "#":
                self.player_location[0] = self.player_location[0] - 1

        # place player at the updated player location
        self.map[self.player_location[0]][self.player_location[1]] = "P"

    def update_guards(self):
        # replace old location of guards with a space
        r = 0
        c = 0
        for row in self.map:
            for col in row:
                if self.map[r][c] == "G":
                    self.map[r][c] = " "
                c = c + 1
            c = 0
            r = r + 1

        # loop that updates the location of each guard
        for guards in self.guard_list:
            new_location = guards.move(self.map)
            self.map[new_location[0]][new_location[1]] = "G"

    def player_wins(self):
        if self.player_location == [1, 14]:     # if player location is equal to the exit location
            player_win = True
        else:
            player_win = False

        return player_win

    def player_loses(self):
        lose = False

        for guards in self.guard_list:      # for each guard
            if guards.enemy_in_range(self.player_location[0], self.player_location[1]):     # if player is within attack range
                lose = True

        return lose


class guard:

    def __init__(self, row, col, attack_range, movements):
        self.row = int(row)
        self.col = int(col)
        self.attack_range = int(attack_range)
        self.movements = movements

    def get_location(self):
        return self.row, self.col       # current location

    def move(self, current_grid):

        # updates guard location based on the next move in the list
        if self.movements[0] == "L":
            self.col -= 1
            if current_grid[self.row][self.col] == "#":     # if updated location is the same location as a wall
                self.col += 1                               # undo guard movement
        elif self.movements[0] == "R":
            self.col += 1
            if current_grid[self.row][self.col] == "#":
                self.col -= 1
        elif self.movements[0] == "U":
            self.row -= 1
            if current_grid[self.row][self.col] == "#":
                self.row += 1
        elif self.movements[0] == "D":
            self.row += 1
            if current_grid[self.row][self.col] == "#":
                self.row -= 1

        # updates movement list so that next move is moved to the front and previous move is moved to the back
        self.movements.append(self.movements[0])
        self.movements.remove(self.movements[0])

        return self.row, self.col

    def enemy_in_range(self, enemy_row, enemy_col):
        in_range = False
        row = 0
        col = 0
        temp_point = []

        for i in range(self.attack_range, 0, -1):
            # up
            row = self.get_location()[0] - i
            col = self.get_location()[1]
            temp_point = [row, col]
            if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                in_range = True

            # attack range on left side of top attack ranges
            for x in range(self.attack_range - i):
                col = temp_point[1] - 1
                temp_point = [row, col]
                if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                    in_range = True

            # right
            row = self.get_location()[0]
            col = self.get_location()[1] + i
            temp_point = [row, col]
            if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                in_range = True

            for x in range(self.attack_range - i):
                row = temp_point[0] - 1
                temp_point = [row, col]
                if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                    in_range = True

            # down
            row = self.get_location()[0] + i
            col = self.get_location()[1]
            temp_point = [row, col]
            if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                in_range = True

            for x in range(self.attack_range - i):
                col = temp_point[1] + 1
                temp_point = [row, col]
                if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                    in_range = True

            # left
            row = self.get_location()[0]
            col = self.get_location()[1] - i
            temp_point = [row, col]
            if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                in_range = True

            for x in range(self.attack_range - i):
                row = temp_point[0] + 1
                temp_point = [row, col]
                if enemy_row == temp_point[0] and enemy_col == temp_point[1]:
                    in_range = True

        return in_range




