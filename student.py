from teacher import PiggyParent
import sys
import time
class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  
        self.load_defaults()# what servo command (1000-2000) is straight forward for your bot?
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        # print("I don't know how to dance. \nPlease give my programmer a zero.")
        # higher ordered
        #check to see its safe
        if not self.safe_to_dance():
            print("It is too dangerouse to dance")
            return
        else:
            print("time to dance")
        for x in range(3):
            self.twist()
            self.spin()
            self.chacha()
            self.shuffle()


    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        found_something = False
        count = 0
        starting_postion = self.get_heading()
        self.right(primary=60, counter=60)
        time.sleep(0.5)
        while self.get_heading() != starting_postion:
            if self.read_distance() < 250 and not found_something:
                found_something = True
                count += 1
                print ("I found something")
            elif self.read_distance() > 250 and found_something:
                found_something = False
                print("I have a clear view")
        self.stop()

        print("I have found this many things: %d" % count)
        return count
    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        #print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        while True:
            while self.read_distance() > 150:
                self.fwd()
                time.sleep(0.01)
            self.turn_by_deg(45)
            


    def twist(self):
        """ turns right then left"""
        self.right()
        time.sleep(1)
        self.stop()
        self.left()
        time.sleep(1)
        self.stop()

    def spin(self):
        """ one full circle right & one full circle left """
        self.fwd()
        time.sleep(1)
        self.right()
        time.sleep(3)
        self.stop() 
        self.back()
        time.sleep(1)
        self.left()
        time.sleep(3.5)
        self.stop()

    def chacha(self):
        """turns right the goes backward and turns its head left goes forward and its head turns right then turn left """
        self.right()
        time.sleep(2)
        self.stop()
        self.back()
        time.sleep(1)
        self.servo(1000)
        time.sleep(1)
        self.stop()
        self.fwd()
        time.sleep(1)
        self.stop()
        self.servo(2000)
        time.sleep(1)
        self.stop()
        self.left()
        time.sleep(2)
        self.stop()


        
    def shuffle(self):
        """turns 20 degrees and then moves forward and back then turns -40 degrees and goes forward and back"""
        self.turn_by_deg(20)
        time.sleep(.25)
        self.fwd()
        time.sleep(1)
        self.stop()
        self.back()
        time.sleep(1)
        self.stop()
        self.turn_by_deg(-40)
        time.sleep(.25)
        self.fwd()
        time.sleep(1)
        self.back()
        time.sleep(1)
        self.stop()







    
    def safe_to_dance(self):
        for x in range(4):
            for ang in range(1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance()<250:
                    return False
            self.turn_by_deg(90)
        return True



###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
