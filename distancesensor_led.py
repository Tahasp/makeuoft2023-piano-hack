#Libraries
import RPi.GPIO as GPIO
import time

 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#LED
GPIO.setmode(GPIO.BCM)  # choose BCM numbering scheme for LED
#set GPIOI direction for LED
GPIO.setup(17, GPIO.OUT)# set GPIO 17 as output for white led  
GPIO.setup(27, GPIO.OUT)# set GPIO 27 as output for red led  
GPIO.setup(22, GPIO.OUT)# set GPIO 22 as output for red led

#change to what we want
hz = input('Please define the frequency in Herz(recommended:75): ') 
reddc = input('Please define the red LED Duty Cycle: ')
greendc = input('Please define the green LED Duty Cycle: ')
bluedc = input('Please define the blue LED Duty Cycle: ')

red = GPIO.PWM(17, hz)    # create object red for PWM on port 17  
green = GPIO.PWM(27, hz)      # create object green for PWM on port 27   
blue = GPIO.PWM(22, hz)      # create object blue for PWM on port 22 
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

if __name__ == '__main__':
    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)
    time.sleep(1)
    red.start((reddc/2.55)) #start red light
    green.start((greendc/2.55)) #start green led
    blue.stop() #stop blue led

    




 







       