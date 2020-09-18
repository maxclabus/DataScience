import numpy as np

class world:
    def __init__(self, size=20, char_set='full'):
        self.size = size
        self.score = 0
        self.n_exits = 0
        self.n_coins = 0
        self.register = {0: 0}
        self.reg_counter = 1
        self.world_map = np.zeros((size,size))
        if char_set == 'full':
            self.img = ("__",
                        " "+"\U0001F60E",
                        " "+"\U000026F0",
                        " "+"\U0001F4B0",
                        " "+"\U0001F6AA")
            self.portrait = "\U0001F30E"
        elif char_set == 'simple':
            self.img = ("__",
                        " "+"\U00000040"+u" ",
                        " "+"\U000025B3"+u" ",
                        " "+"\U000020AC"+u" ",
                        " "+"\U000003A0"+u" ")
            self.portrait = "\U00000057"
        else:
            print("параметр 'char_set' должен быть или 'full', или 'simple'. Пожалуйста, загрузите модель заново.")
        print(u"{}: И тебе привет!".format(self.portrait))

    def test_img(self):
        print("{} - Пустая клетка".format(self.img[0]))
        print("{} - Боб".format(self.img[1]))
        print("{} - Камень".format(self.img[2]))
        print("{} - Монетка".format(self.img[3]))
        print("{} - Дверь".format(self.img[4]))
        print("{} - Мир".format(self.portrait))
        
    def update_map(self, ID, pos_new):
        if pos_new[0] > self.size - 1:
            pos_new[0] -= self.size
        if pos_new[1] > self.size - 1:
            pos_new[1] -= self.size
        if pos_new[0] < 0:
            pos_new[0] += self.size
        if pos_new[1] < 0:
            pos_new[1] += self.size
        # Check if the spot is occupied
        if self.world_map[pos_new[0]][pos_new[1]] == 0:
            self.world_map[self.register[ID].pos[0]][self.register[ID].pos[1]] = 0
            self.register[ID].pos = pos_new[:]
            self.world_map[pos_new[0]][pos_new[1]] = ID
            return True
        # If it's occupied, maybe it's a coin
        elif ((self.register[ID].subclass == 1) &
              (self.register[self.world_map[pos_new[0]][pos_new[1]]].subclass == 3)):
            self.world_map[self.register[ID].pos[0]][self.register[ID].pos[1]] = 0
            self.register[ID].pos = pos_new[:]
            self.register[ID].pick()
            self.delete_object(self.world_map[pos_new[0]][pos_new[1]])
            self.world_map[pos_new[0]][pos_new[1]] = ID
            return True
        # Or an exit
        elif ((self.register[ID].subclass == 1) &
              (self.register[self.world_map[pos_new[0]][pos_new[1]]].subclass == 4) &
              (self.n_coins == 0)):
            print("{}: Поздравляем, вы добрались до выхода!\nВаш счет {}.".format(self.portrait, self.score+1))
            self.reset()
            return True
        else:
            return False

    def print_score(self):
        print("{}: Ваш счет {}.".format(self.portrait, self.score))
        
    def reset(self):
        self.score = 0
        self.reg_counter = 1
        self.n_exits = 0
        self.n_coins = 0
        self.world_map = np.zeros((self.size, self.size))
        self.register = {}
        
    def show_map(self):
        counter = 0
        row = u"+ "
        for i in range(self.size):
            row = row + u"|{:<2d}".format(i) 
        print(row)
        for i in self.world_map:
            row = u"{:<2d}".format(counter)
            for j in i:
                if j == 0:
                    row = row+u"{:>3s}".format(self.img[0])
                else:
                    row = row+u"{:>1s}".format(self.img[int(self.register[j].subclass)])
            print(row)
            counter += 1
    
    def add_object(self, creation):
        if self.world_map[creation.pos[0]][creation.pos[1]] != 0:
            print("Эта клетка уже занята!")
            return None
        else:
            if creation.subclass == 4:
                if self.n_exits == 0:
                    self.n_exits += 1
                else:
                    print("{}: В этом мире уже есть {}!".format(self.portrait, self.img[creation.subclass]))
                    return None
            elif creation.subclass == 3:
                self.n_coins += 1
                
            counter = self.reg_counter
            self.register[self.reg_counter] = creation
            self.world_map[creation.pos[0]][creation.pos[1]] = self.reg_counter
            self.reg_counter += 1

            print("{}: Создан новый объект: {}.".format(self.portrait, self.img[creation.subclass]))
            return counter

    def delete_object(self, ID):
        if self.register.get(ID):
            if self.register[ID].subclass == 4:
                self.n_exits -= 1
            elif self.register[ID].subclass == 3:
                self.n_coins -= 1
            del self.register[ID]
            return True
        else:
            return False

    def load_scenario(self, number):
        self.reset()

        if number == 1:
            # This basic scenario just features Bob and the exit
            Bob = a_bob(self, [self.size/2, self.size/2])
            Door1 = the_exit(self, [int(self.size*0.1)+2, int(self.size*0.1)])
            check = True
        elif number == 2:
            # This scenario deals with a simple obstacle, which we want to pass in order to reach the exit
            Bob = a_bob(self, [self.size/2,self.size/2])
            Stone2 = obstacle(self, [self.size/2, self.size/2 + 5])
            Door2 = the_exit(self, [self.size/2, self.size/2 + 7])
            check = True
        elif number == 3:
            # This scenario is all about picking up coins in the least possible number of steps
            Bob = a_bob(self, [self.size/2, self.size/2])
            Door3 = the_exit(self, [self.size/2, self.size-1])
            Coin31 = coin(self, [self.size/4, self.size/4])
            Coin32 = coin(self, [self.size/4, self.size/2])
            Coin33 = coin(self, [self.size/4, 3*(self.size/4)])
            Coin34 = coin(self, [3*(self.size/4), self.size/4])
            Coin35 = coin(self, [3*(self.size/4), self.size/2])
            Coin36 = coin(self, [3*(self.size/4), 3*(self.size/4)])
            check = True
        elif number == 4:
            # This scenario features more coins and some obstacles, including double obstacles
            Bob = a_bob(self, [0, 0])
            Door4 = the_exit(self, [self.size-1, self.size/2])
            Coin41 = coin(self, [self.size/4, self.size/4+1])
            Coin42 = coin(self, [self.size/4-1, self.size/2])
            Coin43 = coin(self, [self.size/4, 3*(self.size/4+2)])
            Coin44 = coin(self, [3*(self.size/4)-2, self.size/4])
            Coin45 = coin(self, [3*(self.size/4), self.size/2+3])
            Coin46 = coin(self, [3*(self.size/4)-3, 3*(self.size/4)])
            Stone401 = obstacle(self, [0, 2])
            Stone402 = obstacle(self, [0, 3])
            Stone403 = obstacle(self, [2, 0])
            Stone404 = obstacle(self, [3, 0])
            Stone405 = obstacle(self, [self.size/4+1, self.size/2])
            Stone406 = obstacle(self, [3*(self.size/4), self.size/2])
            Stone407 = obstacle(self, [self.size/2, self.size/2])
            Stone408 = obstacle(self, [self.size-1, self.size/2-2])
            Stone409 = obstacle(self, [self.size-3, self.size/2])
            Stone410 = obstacle(self, [self.size-1, self.size/2+2])
            check = True
        elif number == 5:
            # A slightly trickier scenario, where you have to deal with corners
            Bob = a_bob(self, [self.size/2, self.size/2])
            Door5 = the_exit(self, [self.size-1, 3*(self.size/4)])
            Coin51 = coin(self, [self.size/4, self.size/4])
            Coin52 = coin(self, [self.size/4, 3*(self.size/4)])
            Coin53 = coin(self, [3*(self.size/4), self.size/4])
            Coin54 = coin(self, [3*(self.size/4), 3*(self.size/4)])
            Stone501 = obstacle(self, [self.size/2, self.size/4+2])
            Stone502 = obstacle(self, [self.size/2+1, self.size/4+3])
            Stone503 = obstacle(self, [self.size/4, self.size/4+2])
            Stone504 = obstacle(self, [self.size/4-1, self.size/4+3])
            Stone505 = obstacle(self, [3*(self.size/4), self.size/4+1])
            Stone506 = obstacle(self, [3*(self.size/4)+1, self.size/4+2])
            Stone507 = obstacle(self, [3*(self.size/4)-3, 3*(self.size/4)])
            Stone508 = obstacle(self, [3*(self.size/4)-2, 3*(self.size/4)-1])
            check = True
        elif number == 6:
            Bob = a_bob(self, [self.size/2, self.size/2])
            Door6 = the_exit(self, [self.size/2, self.size-1])
            Stone601 = obstacle(self, [self.size/4, 3*(self.size/4)])
            Stone602 = obstacle(self, [self.size/4+1, 3*(self.size/4)])
            Stone603 = obstacle(self, [self.size/4+2, 3*(self.size/4)])
            Stone604 = obstacle(self, [self.size/4+3, 3*(self.size/4)])
            Stone605 = obstacle(self, [self.size/4+4, 3*(self.size/4)])
            Stone606 = obstacle(self, [self.size/4+5, 3*(self.size/4)])
            Stone607 = obstacle(self, [self.size/4+6, 3*(self.size/4)])
            Stone608 = obstacle(self, [self.size/4+7, 3*(self.size/4)])
            Stone609 = obstacle(self, [self.size/4+8, 3*(self.size/4)])
            check = True
        else:
            print("{}: Что-то пошло не так: сценария с номером {} не существует.".format(self.portrait, number))
            check = False

        if check:
            print("{}: Сценарий {} запущен, отлажен и готов к работе!".format(self.portrait, number))
            return Bob
        else:
            return check

        
class creation:
    def __init__(self, world, pos, subclass, passable=0):
        self.pos = [int(i) for i in pos]
        self.subclass = subclass
        self.world = world
        self.id = world.add_object(self)
        self.passable = passable
        
class obstacle(creation):
    def __init__(self, world, pos):
        creation.__init__(self, world, pos, 2, 0)

class coin(creation):
    def __init__(self, world, pos):
        creation.__init__(self, world, pos, 3, 1)

class the_exit(creation):
    def __init__(self, world, pos):
        creation.__init__(self, world, pos, 4, 1)

class a_bob(creation):
    def __init__(self, world, pos):
        creation.__init__(self, world, pos, 1, 0)
        self.balance = 0
        
    def meet(self):
        print("{}: Привет, я Боб.".format(self.world.img[self.subclass]))
        
    def move(self, direction):
        if type(direction) != str:
            print("{}: Понятия не имею, что это значит!".format(self.world.img[self.subclass]))
            return -1
        
        pos_new = self.tell_pos(direction)[:]
        
        if self.world.update_map(self.id, pos_new):
            self.world.score += 1
        else:
            print("{}: Мне туда нельзя!".format(self.world.img[self.subclass]))

    
    def tell_pos(self, direction):
        if type(direction) != str:
            print("{}: Понятия не имею, что это значит!".format(self.world.img[self.subclass]))
            return -1
        
        if direction.lower()=='left':
            return [self.pos[0], self.pos[1]-1 if self.pos[1] > 0 else self.world.size - 1]
        
        elif direction.lower()=='right':
            return [self.pos[0], self.pos[1]+1 if self.pos[1] < self.world.size - 1 else 0]
        
        elif direction.lower()=='up':
            return [self.pos[0]-1 if self.pos[0] > 0 else self.world.size - 1, self.pos[1]]
        
        elif direction.lower()=='down':
            return [self.pos[0]+1 if self.pos[0] < self.world.size - 1 else 0, self.pos[1]]
        else:
            print("{}: Вот, куда я могу смотреть: 'Up', 'Down', 'Left' или 'Right'!".format(self.world.img[self.subclass]))
            return -1

    def tell_type(self, direction):
        spot = self.tell_pos(direction)
        ID = self.world.world_map[spot[0]][spot[1]]
        subclass = self.world.register[ID].subclass
        if subclass == 0:
            return 'Пусто'
        elif subclass == 1:
            return 'Боб'
        elif subclass == 2:
            return 'Камень'
        elif subclass == 3:
            return 'Монетка'
        elif subclass == 4:
            return 'Выход'
        else:
            return 'Что-то непонятное'
        
    def look(self, direction):
        spot = self.tell_pos(direction)
        spot_ID = self.world.world_map[spot[0]][spot[1]]
        if spot_ID==0:
            return True
        elif self.world.register[spot_ID].passable == 1:
            if self.world.register[spot_ID].subclass == 4:
                if self.world.n_coins == 0:
                    return True
                else:
                    return False
            return True
        else:
            return False

    def pick(self):
        if self.world.register[self.world.world_map[self.pos[0]][self.pos[1]]].subclass == 3:
            self.balance += 1
            print("{}: Класс, монетка! Теперь у меня их {}!".format(self.world.img[self.subclass], self.balance))
            return self.balance
        else:
            return False
