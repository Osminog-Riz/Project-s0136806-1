import math
import random
import time
import pygame
import sys
import string
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QCheckBox,
                             QApplication, QLabel,  QTableWidget)


POPULATION = 200
ver_population = 180
RANDOME_POPULATION = 50

min_length_route = 0
count_gen = 0

class Target:

    def __init__(self, x, y):
        self.x_vertex = x
        self.y_vertex = y
        self.color = (0, 255, 0)

    def taken(self):
        self.color = (255, 255, 255)

    def reload(self):
        self.color = (0, 255, 0)


class Base:

    def __init__(self):
        self.x_vertex = 233
        self.y_vertex = 319
        self.color = (0, 0, 0)


class Vert:

    def __init__(self):
        self.x_vertex = 0
        self.y_vertex = 0

    def length(self, x):
        return math.sqrt((self.x_vertex - x.x_vertex) ** 2 + (self.y_vertex - x.y_vertex) ** 2)


class Drone:

    def __init__(self, N):
        self.x_vertex = 255
        self.y_vertex = 255
        self.color = (255, 0, 0)
        self.length_route = 0
        self.F = 0
        self.chromosome = [i for i in range(N)]
        random.shuffle(self.chromosome)

    def move(self, x, y):
        if (self.x_vertex - x) + (self.y_vertex - y) == 0:
            self.length_route += 100000
        else:
            self.length_route += math.sqrt((self.x_vertex - x) ** 2 + (self.y_vertex - y) ** 2)
            self.x_vertex = x
            self.y_vertex = y

    def mutation(self):
        random.shuffle(self.chromosome)


class GeneticAlgorithm(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # define table
        self.table = QTableWidget(self)  
        self.table.setGeometry(20, 60, 275, 420)
        self.table.setColumnCount(2)     
        self.table.setRowCount(1)
        
        self.table.setHorizontalHeaderLabels(["X coordinates", "Y coordinates"])

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

        # Button Start
        self.btns = QPushButton('Start', self)
        self.btns.move(20, 20)
        self.btns.clicked.connect(self.start)

        # Button Add
        self.btna = QPushButton('Add Point', self)
        self.btna.move(110, 20)
        self.btna.clicked.connect(self.add_row)

        # Button delete
        self.btna = QPushButton('Delete Point', self)
        self.btna.move(200, 20)
        self.btna.clicked.connect(self.del_row)

        # Resut
        self.rlab = QLabel("Result: ", self)
        self.rlab.move(400, 30)

        # Checkbox
        self.dlab = QLabel("View Process", self)
        self.dlab.move(500, 10)
        self.dop = QCheckBox(self)
        self.dop.setChecked(False)
        self.dop.move(600, 10)
        self.dop.stateChanged.connect(self.view_additional)
        
        # Additional Field
        self.dopf = QTextEdit(self)
        self.dopf.setGeometry(400, 60, 0, 0)
        
        self.res = QTextEdit(self)
        self.res.setGeometry(400, 60, 580, 420)
        self.res.setAlignment(QtCore.Qt.AlignCenter)
        
        self.setGeometry(500, 100, 1000, 500)
        self.setWindowTitle('GeneticAlgorithm')
        self.show()

    def view_additional(self, state):

        if state == False:
            self.res.setGeometry(400, 60, 580, 420) 
            self.dopf.setGeometry(400, 60, 0, 0)
        else:
            self.res.setGeometry(400, 60, 580, 180)
            self.dopf.setGeometry(400, 270, 580, 210)

            
    def start(self):
        rows = self.table.rowCount()
        vertexes = []
        flag = False
        for row in range(rows):
            try:
                vertexes.append([int(self.table.item(row,0).text()), int(self.table.item(row,1).text())])
            except:
                flag = True

        if flag:
            result = "Проверьте правильность введенных данных! \nКоординаты точек должны быть целыми числами."
        else:
            result = self.GA(vertexes, rows)
            
        self.res.setText(result)
        
        
    def add_row(self):
        rowPosition = self.table.rowCount()                               
        self.table.insertRow(rowPosition)

    def del_row(self):
        rowPosition = self.table.rowCount() - 1                              
        self.table.removeRow(rowPosition)

    def GA(self, vertexes, N):
        TARGET_NUM = N
        target_list = []
        checked = True
        
        for i in range(TARGET_NUM):
            a = Target(int(vertexes[i][0]), int(vertexes[i][1]))
            target_list.append(a)

        base = Base()

        drone_list = []
        for i in range(POPULATION):
            drone = Drone(N)
            drone_list.append(drone)

        # run process
        pygame.init()

        # Set up the drawing window
        screen = pygame.display.set_mode([500, 615])
        bg = pygame.image.load("map_.png")

        running = True
        step = 0
        gen = 0
        step_null = False
        while running:

            # INSIDE OF THE GAME LOOP
            screen.blit(bg, (0, 0))

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # drone go home
            if step % 4 == 0:
                new_x_vertex = base.x_vertex
                new_y_vertex = base.y_vertex
                drone_list[i].move(new_x_vertex, new_y_vertex)

            # Draw a solid black point. This is our base
            pygame.draw.circle(screen, base.color, (base.x_vertex, base.y_vertex), 10)

            # find tagrets
            for i in range(POPULATION):
                target_index = drone_list[i].chromosome[step]
                new_x_vertex = target_list[target_index].x_vertex
                new_y_vertex = target_list[target_index].y_vertex
                drone_list[i].move(new_x_vertex, new_y_vertex)
                target_list[target_index].taken()

            # new gen
            if step == TARGET_NUM-1:
                step_null = True
                gen += 1
                step = 0
                min_ = 10000000
                sum_ = 0
                min_num = 0

                # find min route to print
                for i in range(POPULATION):
                    if drone_list[i].length_route < min_:
                        min_ = drone_list[i].length_route
                        min_num = i

                for i in range(TARGET_NUM):
                    target_list[i].reload()

                for i in range(TARGET_NUM):
                    pygame.draw.circle(screen, target_list[i].color, (target_list[i].x_vertex, target_list[i].y_vertex), 5)

                pygame.draw.line(screen, (0, 0, 0),
                                 (base.x_vertex,
                                  base.y_vertex),
                                 (target_list[drone_list[min_num].chromosome[0]].x_vertex,
                                  target_list[drone_list[min_num].chromosome[0]].y_vertex),
                                 2)
                for i in range(TARGET_NUM - 1):
                    if i % 3 == 0 and i != 0:
                        pygame.draw.line(screen, (0, 0, 0),
                                         (target_list[drone_list[min_num].chromosome[i]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i]].y_vertex),
                                         (base.x_vertex,
                                          base.y_vertex),
                                         2)
                        pygame.draw.line(screen, (0, 0, 0),
                                         (base.x_vertex,
                                          base.y_vertex),
                                         (target_list[drone_list[min_num].chromosome[i + 1]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i + 1]].y_vertex),
                                         2)
                    else:
                        pygame.draw.line(screen, (255, 0, 0),
                                         (target_list[drone_list[min_num].chromosome[i]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i]].y_vertex),
                                         (target_list[drone_list[min_num].chromosome[i + 1]].x_vertex,
                                          target_list[drone_list[min_num].chromosome[i + 1]].y_vertex),
                                         2)
                    pygame.display.flip()

                pygame.draw.line(screen, (0, 0, 0),
                                 (target_list[drone_list[min_num].chromosome[TARGET_NUM - 1]].x_vertex,
                                  target_list[drone_list[min_num].chromosome[TARGET_NUM - 1]].y_vertex),
                                 (base.x_vertex,
                                  base.y_vertex),
                                 2)
                pygame.display.flip()
                # time.sleep(3)
                # find sum of result F
                for i in range(POPULATION):
                    drone_list[i].F = 1 / drone_list[i].length_route * 100000
                    sum_ += drone_list[i].F

                list_ver = []
                for i in range(POPULATION):
                    list_ver.append(drone_list[i].F / sum_)

                roulette = [0]
                for i in range(1, POPULATION):
                    roulette.append(list_ver[i] + roulette[i - 1])

                new_drones = []
                a = Drone(N)
                a.chromosome = list(drone_list[min_num].chromosome)
                new_drones.append(a)
                # childs with roulette
                for i in range(1, POPULATION):
                    a = Drone(N)
                    child_ = random.random()
                    child_num = 0
                    for j in range(1, POPULATION):
                        if roulette[j] > child_:
                            child_num = j - 1
                            break
                    a.chromosome = list(drone_list[child_num].chromosome)
                    new_drones.append(a)

                drone_list = list(new_drones)

                # mutation
                for i in range(1, POPULATION - RANDOME_POPULATION):
                    if random.randint(1, 200) < ver_population:
                        a_v = random.randint(0, TARGET_NUM - 1)
                        b_v = random.randint(0, TARGET_NUM - 1)
                        temp = drone_list[i].chromosome[b_v]
                        drone_list[i].chromosome[b_v] = drone_list[i].chromosome[a_v]
                        drone_list[i].chromosome[a_v] = temp

                for i in range(POPULATION-RANDOME_POPULATION, POPULATION):
                    drone_list[i].mutation()

                # reload target_list
                for i in range(TARGET_NUM):
                    target_list[i].reload()

                global min_length_route
                global count_gen

                if gen > 2 and min_length_route != min_:
                    min_length_route = min_
                    count_gen = 0
                elif (gen > 2):
                    count_gen += 1

                if count_gen == 30:
                    time.sleep(5)
                    file = open("result.txt", "w")
                    result = "Итоговый маршрут состоит из следующих точек: \n" 

                    for point in drone_list[i].chromosome:
                        result += str(point + 1) + " "

                    result += ". \nИтоговая длина минимального маршрута = " + str(min_length_route)

                    file.write(result)
                    running = False
            if (count_gen != 0) and checked:
                checked = False
                prom_result = "Поколение = " + str(gen) + "\n" + "Лучший результат = " + str(min_) + "\n"
                self.dopf.setText(prom_result)
            step += 1

            if step_null:
                step_null = False
                step = 0
                checked = True
                
        pygame.quit()
        
        return result

app = QApplication(sys.argv)
gui = GeneticAlgorithm()
sys.exit(app.exec_())

