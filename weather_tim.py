# Raspberry Pi Weather station backend script
# Version 1.5
from sense_hat import SenseHat
import time
from firebase import firebase
from datetime import date
from threading import Timer
import calendar

firebase = firebase.FirebaseApplication('https://weather-station-13bc2.firebaseio.com/', None)

OFFSET_LEFT = 1
OFFSET_TOP = 2

sense = SenseHat()

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

counter = 0
present = date.today()

avgtemp = 0
avghumidity = 0
avgpressure = 0

# Class that handles timer objects that run a specified function after a specified duration

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# Take in values every 30 mins to calculate average Temperature, Pressure and Humidty for the day
def halfhouract():
    pressure = sense.pressure
    humidity = sense.humidity
    temp = sense.temp
    
    global avgtemp
    global avghumidity
    global avgpressure
    global counter
    global present

    avgtemp = avgtemp + int(temp)
    print(avgtemp)
    avghumidity= avghumidity + int(humidity)
    print(avghumidity)
    avgpressure = avgpressure + int(pressure)
    print(avgpressure)
    counter = counter + 1

    #if present==date.today() and counter!=0:
    if counter!=0:
        avgtemp = int(avgtemp/counter)
        avgpressure = int(avgpressure/counter)
        avghumidity = int(avghumidity/counter)

        avgresult = firebase.put('Data/Temperature', calendar.day_name[present.weekday()], int(avgtemp))
        avgresult = firebase.put('Data/Pressure', calendar.day_name[present.weekday()], int(avgpressure))
        avgresult = firebase.put('Data/Humidity', calendar.day_name[present.weekday()], int(avghumidity))

        present = date.today()
        avgtemp = 0
        avghumidity = 0
        avgpressure = 0
        counter = 0

t = RepeatedTimer(10, halfhouract)
t.start()



# Third Party Driver to display numbers on the sensehat

def show_t():

  sense.show_letter("T", back_colour = red)

  time.sleep(.5)



def show_p():

  sense.show_letter("P", back_colour = green)

  time.sleep(.5)



def show_h():

  sense.show_letter("H", back_colour = blue)

  time.sleep(.5)



NUMS =[0.5,0.5,0.5,0.5,1,0.5,0.5,1,0.5,0.5,1,0.5,0.5,0.5,0.5,  # 0
       1,0.5,1,1,0.5,1,1,0.5,1,1,0.5,1,1,0.5,1,                # 1
       0.5,0.5,0.5,1,1,0.5,1,0.5,1,0.5,1,1,0.5,0.5,0.5,        # 2
       0.5,0.5,0.5,1,1,0.5,0.5,0.5,0.5,1,1,0.5,0.5,0.5,0.5,    # 3
       0.5,1,1,0.5,1,0.5,0.5,0.5,0.5,1,1,0.5,1,1,0.5,          # 4
       0.5,0.5,0.5,0.5,1,1,0.5,0.5,0.5,1,1,0.5,0.5,0.5,0.5,    # 5
       0.5,0.5,0.5,0.5,1,1,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,  # 6
       0.5,0.5,0.5,1,1,0.5,1,0.5,1,0.5,1,1,0.5,1,1,            # 7
       0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,# 8
       0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,1,1,0.5,1,1,0.5]      # 9



# Displays a single digit (0-9)

def show_digit(val, xd, yd, r, g, b):

  offset = val * 15

  for p in range(offset, offset + 15):

    xt = p % 3

    yt = (p-offset) // 3
    
    if NUMS[p]==0.5 :
      sense.set_pixel(xt+xd, yt+yd, int(510*NUMS[p]), int(510*NUMS[p]), int(510*NUMS[p]))
    else:
      sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])
    
    



# Displays a two-digits positive number (0-99)

def show_number(val, r, g, b):

  abs_val = abs(val)

  tens = abs_val // 10

  units = abs_val % 10

  if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)

  show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)





def update_screen(mode, show_letter = False):

  if mode == "temp":

    if show_letter:

      show_t()

    temp = sense.temp

    sense.clear(255,0,0)

    show_number(int(temp),255,0,0)

    pressure = sense.pressure
    humidity = sense.humidity

    result = firebase.put('BackendData', 'Temperature', int(temp))
    result = firebase.put('BackendData', 'Humidity', int(humidity))
    result = firebase.put('BackendData', 'Pressure', int(pressure))

    time.sleep(1)



  elif mode == "pressure":

    if show_letter:

      show_p()

    pressure = sense.pressure

    sense.clear(0,255,0)

    sense.show_message(str(round(pressure)),

    text_colour=[255, 255, 255],

    back_colour=[0, 255, 0])

    temp = sense.temp
    humidity = sense.humidity

    result = firebase.put('BackendData', 'Temperature', int(temp))
    result = firebase.put('BackendData', 'Humidity', int(humidity))
    result = firebase.put('BackendData', 'Pressure', int(pressure))

    time.sleep(1)



  elif mode == "humidity":

    if show_letter:

      show_h()

    humidity = sense.humidity

    sense.clear(0,0,255)

    show_number(int(humidity),0,0,255)

    temp = sense.temp
    pressure = sense.pressure

    result = firebase.put('BackendData', 'Temperature', int(temp))
    result = firebase.put('BackendData', 'Humidity', int(humidity))
    result = firebase.put('BackendData', 'Pressure', int(pressure))

    time.sleep(1)



##################
# Intro Animation#
##################

show_t()
show_p()
show_h()


update_screen("temp")



index = 0
sensors = ["temp", "pressure", "humidity"]



####

# Main loop

####



while True:

  selection = False

  events = sense.stick.get_events()

  for event in events:

    if event.action != "released":

      if event.direction == "left":
        index -= 1
        selection = True

      elif event.direction == "right":

        index += 1
        selection = True

      if selection:

        current_mode = sensors[index % 3]
        update_screen(current_mode, show_letter = True)

  if not selection:      

    current_mode = sensors[index % 3]
    update_screen(current_mode)

  
