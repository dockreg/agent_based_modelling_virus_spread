import pycxsimulator
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import urllib
import PIL

population = 900 # human population
p_covid = 0.1 # probability that person has covid
r_catch = 0.1 # probability that individual catches covid off nearby sick individual

# mask wearing and vaccine uptake
mask_wearing = 0
vaccinations = 0

# reduce chance of catching covid if mask wearing
if mask_wearing == 1:
    r_catch = r_catch/2

# reduce chance of catching covid if vaccinations have been used
if vaccinations == 1:
    r_catch = r_catch/2

# set parameters for movement and distance threshold
m = 0.01
dist = 0.0004

# define locations
class university:
    def __init__(self):
        self.x = 0.4
        self.y = 0.3

class cbd:
    def __init__(self):
        self.x = 0.6
        self.y = 0.7

# create human class 
class human:
    def __init__(self, i):
        self.x = random()
        self.y = random()
        self.home_x = self.x
        self.home_y = self.y
        self.covid_status = 'infected' if random() < p_covid else 'normal'
        self.job = 'student' if i < 300 else 'worker' if i < 600 else 'unemployed'

    def move(self, m, time):
        # send students to university and back home
        if self.job == 'student':
            if time < 300:
                #select portion of student to move towards university
                if random() < 0.7:
                    try:
                        x_move = (un.x - self.x) / abs(un.x - self.x)
                        y_move = (un.y - self.y) / abs(un.y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
                else:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
            # send students home 
            else:
                if random() < 0.7:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
                else:
                    x_move, y_move = 0, 0
            if x_move==0:
                self.x += uniform(-2*m, 2*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-2*m, 2*m)
            else:
                self.y += y_move*m


        # send workers to offices and back home
        elif self.job == 'worker':
            if time < 360:
                if random() < 0.7:
                    try:
                        x_move = (cbd.x - self.x) / abs(cbd.x - self.x)
                        y_move = (cbd.y - self.y) / abs(cbd.y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
                else:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
            else:
                if random() < 0.7:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        x_move, y_move = 0, 0
                        pass
                else:
                    x_move, y_move = 0, 0
            if x_move==0:
                self.x += uniform(-4*m, 4*m)
            else:
                self.x += x_move*m
            if y_move==0:
                self.y += uniform(-4*m, 4*m)
            else:
                self.y += y_move*m

                

        # unemployed movement around the map
        else:
            if time < 360:
                if random() < 0.9:
                    self.x += uniform(-m, m)
                    self.y += uniform(-m, m)
            else:
                if random() < 0.9:
                    try:
                        x_move = (self.home_x - self.x) / abs(self.home_x - self.x)
                        y_move = (self.home_y - self.y) / abs(self.home_y - self.y)
                    except ZeroDivisionError:
                        pass
                else:
                    x_move, y_move = 0, 0
                if x_move==0:
                    self.x += uniform(-m, m)
                else:
                    self.x += x_move*m
                if y_move==0:
                     self.y += uniform(-m, m)
                else:
                    self.y += y_move*m

            
            
        self.x = 1 if self.x > 1 else 0 if self.x < 0 else self.x
        self.y = 1 if self.y > 1 else 0 if self.y < 0 else self.y


    def infection(self, r_catch, dist):
        if self.covid_status == 'infected':
            return
        # detecting collision and simulating covid catching for students
        #increase distance for students and workers
        if self.job == 'student':
            dist = dist * 3
        if self.job == 'worker':
            dist = dist * 2
        temp = [h for h in humans if h.covid_status != self.covid_status]
        # find closest human
        if closest_human(self.x, self.y, temp) < dist:
            self.covid_status = 'infected' if random() < r_catch else self.covid_status

def closest_human(x, y, humans):
    point = np.array((x, y))
    humans = np.array([[h.x, h.y] for h in humans])
    distance = np.sum((humans - point)**2, axis=1)
    return np.argmin(distance)


def create_population():
    humans = []
    for i in range(population):
        h = human(i)
        humans.append(h)

    return humans


def set_up_abm_environment():
    global humans, infected_worker_data, infected_student_data, infected_unemployed_data, normal_worker_data, normal_student_data, normal_unemployed_data, time, cbd, un
    time = 0
    infected_worker_data = []
    infected_student_data = []
    infected_unemployed_data = []
    normal_worker_data = []
    normal_student_data = []
    normal_unemployed_data = []
    
    humans = create_population()
    un = university()
    cbd = cbd()


def display_model():
    global infected_worker_data, infected_student_data, infected_unemployed_data, normal_worker_data, normal_student_data, normal_unemployed_data, time, cbd, un

    subplot(3, 2, 1)
    cla()
    a = plt.imread('images/istockphoto-1317488792-612x612.jpeg')
    plt.imshow(a, extent=[0, 1, 0, 1])
    
    for h in humans:
        if h.covid_status == 'infected':
            if h.job == 'worker':
                plot(h.x, h.y, 'r^')
            elif h.job == 'student':
                plot(h.x, h.y, 'r.')
            else:
                plot(h.x, h.y, 'r+')
        else:
            if h.job == 'worker':
                plot(h.x, h.y, 'g^')
            elif h.job == 'student':
                plot(h.x, h.y, 'g.')
            else:
                plot(h.x, h.y, 'g+')

    axis('image')
    axis([0, 1, 0, 1])
    mins = time%60
    hours = time//60
    title('Time elapsed = ' + str(hours) + ':' + str(mins) + ' hours')

    subplot(3, 2, 2)
    cla()
    if time>0:
        titles=('worker', 'student', 'unemployed')
        values = [infected_worker_data[-1], infected_student_data[-1], infected_unemployed_data[-1]]
        x_pos = np.arange(len(titles))
        plt.bar(x_pos, values, color=('r', 'maroon', 'lightcoral'))
        plt.text(values[0], 0, " "+str(values[0]), color='black',va='center', fontweight='bold')
        plt.xticks(x_pos, titles)
        plt.title('Infected count')
        for i in range(len(values)):
            plt.annotate(str(values[i]), xy=(i,10), ha='center', va='bottom')
        plt.show()

    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.01, 
                    hspace=0.01)
    
    subplot(3, 1, 3)
    cla()
    plot(normal_worker_data, 'mediumseagreen', label = 'normal worker')
    plot(normal_student_data, 'darkgreen', label = 'normal student')
    plot(normal_unemployed_data, 'palegreen', label = 'normal unemployed')
    plot(infected_worker_data, 'r', label = 'infected worker')
    plot(infected_student_data, 'maroon', label = 'infected student')
    plot(infected_unemployed_data, 'lightcoral', label = 'infected unemployed')
    legend()





def move_all_one_step():
    global time
    time += 1
    
    # simulating movement through a day
    if time < 480:
        for h in humans:
            h.move(m, time)
            h.infection(r_catch, dist)

def refresh_model():
    global infected_worker_data, infected_student_data, infected_unemployed_data, normal_worker_data, normal_student_data, normal_unemployed_data
    move_all_one_step()

    # collate all data for graphing
    infected_worker_data.append(sum([1 for h in humans if h.covid_status == 'infected' and h.job == 'worker']))
    infected_student_data.append(sum([1 for h in humans if h.covid_status == 'infected' and h.job == 'student']))
    infected_unemployed_data.append(sum([1 for h in humans if h.covid_status == 'infected' and h.job == 'unemployed']))

    normal_worker_data.append(sum([1 for h in humans if h.covid_status == 'normal' and h.job == 'worker']))
    normal_student_data.append(sum([1 for h in humans if h.covid_status == 'normal' and h.job == 'student']))
    normal_unemployed_data.append(sum([1 for h in humans if h.covid_status == 'normal' and h.job == 'unemployed']))


pycxsimulator.GUI().start(func=[set_up_abm_environment, display_model, refresh_model])


