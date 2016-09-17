
import random
import sys

#class V2:
#    def __init__(self, x, y):
#        self.x = x
#        self.y = y
#
#    def __repr__(self):
#        return str(self.x) + "," + str(self.y)
#        
#    def __add__(self, other):
#        return V2(self.x + other.x, self.y + other.y)

verbose = False
def printv(msg):
    if verbose:
        print(msg)

    
class Room:

    def __init__(self, top, left, w, h):
        self.top = top
        self.left = left
        self.w = w
        self.h = h

    def __repr__(self):
        return "Room:\t" + str(self.top) + "," + str(self.left) + "\t " + str(self.w) + "," + str(self.h)

class Level:

    W = 80
    H = 30

    def tile(self,x,y):
        if x < 0 or x >= self.W-1:
            return ""
        if y < 0 or y >= self.H-1:
            return ""
        return self._level[y][x]
    
    def initial_level_gen(self):
        self._level = []
        for y in range(self.H):
            self._level.append([])
            for x in range(self.W):
                tile = "*"
                if x == 0 or x == self.W-1 or y == 0 or y == self.H-1:
                    tile = "*"
                
                self._level[y].append(tile)
                
    def is_room_solid(self, room, border = 0):
        solid = True
        for y in range(room.top - border, room.top + room.h + border):
            for x in range(room.left - border, room.left + room.w + border):
                if (self.tile(x,y) != "*"):
                    solid = False
        return solid
                
    def carve_room(self, room, msg = "carve_room"):
        printv(msg + "\t" + str(room))
        for y in range(room.top, room.top + room.h):
            for x in range(room.left, room.left + room.w):
                self._level[y][x] = "."

    def carve_passage(self, x0, y0, x1, y1):
        #x
        passage0 = Room(y0, min(x0,x1), abs(x1 - x0), 1)
        self.carve_room(passage0, "carve_passage")
        #y
        passage1 = Room(min(y0,y1), x1, 1, abs(y1 - y0))
        self.carve_room(passage1, "carve_passage")
            
    def connect_rooms(self, room0, room1):
        self.carve_passage(room0.left + room0.w/2, room0.top + room0.h/2, room1.left + room1.w/2, room1.top + room1.h/2)
        
    def create_rooms(self):
        self.rooms = []
        num_rooms = 8
        
        #creation phase
        for r in range(num_rooms):
            num_tries = 20
            for t in range(num_tries):
                w = random.randint(6, 14)
                h = random.randint(3, 7)
                top =  random.randint(1, self.H - h - 1)
                left = random.randint(1, self.W - w - 1)
                room = Room(top, left, w, h)
                if self.is_room_solid(room, 1):
                    self.carve_room(room)
                    self.rooms.append(room)
                    break
                elif t == num_tries - 1:
                    #last chance, make it anyway!
                    print("last chance")
                    self.carve_room(room)
                    self.rooms.append(room)

        #connection phase
        room_connections = [[]]*num_rooms
        connect_it = 0
        all_rooms_connected = False

        for r in range(0, num_rooms-1):
            r_other = random.randint(r+1, num_rooms-1)

            #if r_other is already connected, don't connect
            if len(room_connections[r_other]):
                continue
            
            room_connections[r].append(r_other)
            room_connections[r_other].append(r)
        
        for r in range(0, num_rooms):
            for r_index in range(len(room_connections[r])):
                r_other = room_connections[r][r_index]
                self.connect_rooms(self.rooms[r], self.rooms[ r_other ])
                
    def __init__(self):
        self.initial_level_gen()
        self.create_rooms()

        
    def display(self):
        for y in range(self.H):
            s = ""
            for x in range(self.W):
                s += self._level[y][x]
            
            print(s)

    

if __name__ == "__main__":
    # verbose = False
    
    if len(sys.argv) >= 2:
        seed = int(sys.argv[1])
    else:
        seed = random.randint(0, 32000)
    print("Seed: " + str(seed))
    random.seed(seed)

    level = Level()
    level.display()
