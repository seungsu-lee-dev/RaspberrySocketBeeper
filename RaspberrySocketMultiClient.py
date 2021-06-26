import RPi.GPIO as GPIO
import time
import drivers
import drivers2
from socket import *
import sys
from threading import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
display = drivers.Lcd()
display2 = drivers2.Lcd()

R1 = 23
R2 = 24
R3 = 25
R4 = 8

C1 = 19
C2 = 13
C3 = 6
C4 = 5

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

keypadPressed = -1
input=""
LCD_print=""
before_C=""
inputBool = False

#부저 설정
buzzer = 18
LED = 17

scale = [261,294,329,349,392,440,493,523]
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)


pwm = GPIO.PWM(buzzer, 1.0)
pwm.start(0)



class ClientInit:
    HOST = 'localhost'
    PORT = 9999
    ADDR = (HOST, PORT)

    def __init__(self):
        super().__init__()
        self.clientSocket = None
        
    def conn(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            self.clientSocket.connect(ClientInit.ADDR)
        except Exception as e:
            print("clientInit")
            print('%s:%s' % ClientInit.ADDR)
            print(e)
            sys.exit()
        
    def run(self):
        self.conn()
        t2 = ClientSender(self.clientSocket)
        t2.start()
        t3 = ClientReceiver(self.clientSocket)
        t3.start()
            
class ClientSender(Thread):
    global LCD_print
    global input
    global inputBool
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
        
    def run(self):
        global input
        global inputBool
        while True:
            if inputBool:
                inputBool = False
                sendData = input
                if sendData:
                    self.clientSocket.sendall(sendData.encode())
                    if sendData == '\stop':
                        break
        print("ClientSenderThread Stop")

class ClientReceiver(Thread):
    global pwm
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
        
    def Buzzer_LED(self):
        global pwm
        pwm.ChangeDutyCycle(50)
        for i in range(3):
            GPIO.output(LED, True)
            pwm.ChangeFrequency(scale[i])
            print(scale[i])
            time.sleep(0.5)
            GPIO.output(LED, False)
            time.sleep(0.5)
        pwm.ChangeDutyCycle(0)
        
        
    def run(self):
        pre = ""
        while True:
            while True:
                data = self.clientSocket.recv(1024)
                if data != pre:
                    break
            display2.lcd_display_string(data.decode(),1)
            if data:
                try:
                    self.Buzzer_LED()
                    print("stop")

                finally:
                    pass
                print(repr(data.decode())[1:-1])
                if data == '\stop':
                    break
            pre = data
        self.clientSocket.close()
        print("ClientReceiverThread Stop")

c = ClientInit()
c.run()

def keypadCallback(channel):
    global keypadPressed
    
    if(keypadPressed == -1):
        keypadPressed = channel
        
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

def setAllLines(state):
    GPIO.output(R1, state)
    GPIO.output(R2, state)
    GPIO.output(R3, state)
    GPIO.output(R4, state)


def specialKeyPress():
    global input
    global LCD_print
    global before_C
    global inputBool
    pressed = False
    
    GPIO.output(R4, GPIO.HIGH)
    
    if(GPIO.input(C3) == 1):
        print("delete: ")
        display.lcd_clear()
        LCD_print=LCD_print.rstrip(before_C)
        display.lcd_display_string(LCD_print,1)
        input=input.rstrip(before_C)
        
        pressed=True
        
    GPIO.output(R4, GPIO.LOW)
    GPIO.output(R3, GPIO.HIGH)
    
    if(not pressed and GPIO.input(C4) == 1):
        inputBool = True
        display.lcd_clear()
        print("send: "+input)
        pressed = True
        
        input = ""
        LCD_print= ""
    GPIO.output(R3, GPIO.LOW)    
        
    return pressed

def printCharacter(row, character):
    global input
    global LCD_print
    global before_C
    
    GPIO.output(row, GPIO.HIGH)       
    if(GPIO.input(C1) == 1):             
        LCD_print=LCD_print+character[0]
        display.lcd_display_string(LCD_print,1)
        input = input + character[0]
        before_C=character[0]
    if(GPIO.input(C2) == 1):
        LCD_print=LCD_print+character[1]
        display.lcd_display_string(LCD_print,1)
        input = input + character[1]
        before_C=character[1]
    if(GPIO.input(C3) == 1):
        LCD_print=LCD_print+character[2]
        display.lcd_display_string(LCD_print,1)
        input = input + character[2]
        before_C=character[2]
    if(GPIO.input(C4) == 1):
        LCD_print=LCD_print+character[3]
        display.lcd_display_string(LCD_print,1)
        input = input + character[3]
        before_C=character[3]
    GPIO.output(row, GPIO.LOW)
    
    


try:        
    while True:        
        if(keypadPressed != -1):
            setAllLines(GPIO.HIGH)
            if(GPIO.input(keypadPressed)==0):
                keypadPressed = -1
            else:
                time.sleep(0.1)
        else:
            if(not specialKeyPress()):
                printCharacter(R1, ["1", "2", "3", "up"])            
                printCharacter(R2, ["4", "5", "6", "down"])
                printCharacter(R3, ["7", "8", "9", "Ok"])
                printCharacter(R4, ["_", "0", "delete", "D"])
                time.sleep(0.1)
                         
            else:
                time.sleep(0.1)
            

except KeyboardInterrupt:
    print("Stopped")
    
    

