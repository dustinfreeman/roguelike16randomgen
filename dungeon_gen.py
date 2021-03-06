
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

def gen_room_names():
    room_names = ["toilet", "foyer", "temple", "bedroom", "kitchen", "jail", "dump", "board room", "storage", "atrium", "workshop", "fireplace"]
    room_names+= ["torture chamber", "rubble", "garden", "well", "morgue", "games room", "stage", "shower", "library"]
    room_names+= ["brewery", "tavern", "abyss", "crypt", "pool", "barber"]
    room_names+= ["showers", "barracks", "granary", "nursery", "lab"]
    room_names+= ["armoury", "classroom", "lounge", "theatre", "concert hall"]
    room_names+= ["throne room", "waiting room", "hospital", "lectural hall", "ready room", "zoo", "ballroom", "hearth"]
    room_names+= ["entertainment centre", "command centre", "map room", "computer room", "steam baths", "mess hall", "dining hall"]
    room_names+= ["ritual chamber", "parking garage", "trapdoor", "excercise room", "gallery", "cinema", "server room", "vault"]
    room_names+= ["office space", "loft", "warehouse", "shop", "crematorium", "sports court", "cold storage", "tailor", "laundry room"]

    return room_names
    
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
        passage0 = Room(y0, min(x0,x1), abs(x1 - x0) + 1, 1)
        self.carve_room(passage0, "carve_passage")
        #y
        passage1 = Room(min(y0,y1), x1, 1, abs(y1 - y0))
        self.carve_room(passage1, "carve_passage")
            
    def connect_rooms(self, room0, room1):
        self.carve_passage(room0.left + room0.w/2, room0.top + room0.h/2, room1.left + room1.w/2, room1.top + room1.h/2)
        
    def connect_rooms_naive(self, rooms):
        room_connections = [[]]*len(rooms)
        connect_it = 0
        all_rooms_connected = False

        for r in range(0, len(rooms)-1):
            r_other = random.randint(r+1, len(rooms)-1)

            #if r_other is already connected, don't connect
            if len(room_connections[r_other]):
                continue
            
            room_connections[r].append(r_other)
            room_connections[r_other].append(r)
        
        for r in range(0, len(rooms)):
            for r_index in range(len(room_connections[r])):
                r_other = room_connections[r][r_index]
                self.connect_rooms(rooms[r], rooms[ r_other ])

    def connect_rooms_linear(self, rooms):
        for r in range(0, len(rooms)-1):
            self.connect_rooms(rooms[r], rooms[r+1])

    def label(self, x, y, phrase):
        words = phrase.split()
        y0 = y - len(words)/2
        for w in range(len(words)):
            word = words[w]
            x0 = x - len(word)/2
            for i in range(0, len(word)):
                self._level[y0+w][x0 + i] = word[i]
        
    def label_rooms(self, rooms):
        room_names = gen_room_names()
        for r in range(len(rooms)):
            rni = random.randint(0, len(room_names)-1)
            room_type = room_names[rni]
            room = rooms[r]
            self.label(room.left + room.w/2, room.top + room.h/2, room_type)
        
    def create_rooms_scatter(self, num_rooms = 8):
        rooms = []
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
                    rooms.append(room)
                    break
                elif t == num_tries - 1:
                    #last chance, make it anyway!
                    print("last chance")
                    self.carve_room(room)
                    rooms.append(room)

        return rooms

    def create_rooms(self):
        num_rooms = random.randint(6, 12)

        #creation phase
        rooms = self.create_rooms_scatter(num_rooms)

        #connection phase
        #self.connect_rooms_naive(rooms)
        self.connect_rooms_linear(rooms)

        self.label_rooms(rooms)
        
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
