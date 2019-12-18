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
        self.LEFT_DEFAULT = 90
        self.RIGHT_DEFAULT = 90
        self.MIDPOINT = 1500  
        self.corner_count = 0
        self.SAFE_DIST = 250
        self.starting_postion = 0
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
        menu = {"c": ("Calibrate", self.calibrate),
                "d": ("Dance", self.dance),
                "h": ("Hold position", self.hold_position),
                "n": ("Navigate", self.nav),
                "o": ("Obstacle count", self.obstacle_count),
                "q": ("Quit", self.quit),
                "v": ("Veer", self.slither)
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
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 50):
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
    
    def quick_check(self):
        """looks around as it moves to check the distance"""
        for ang in range(self.MIDPOINT-150, self.MIDPOINT+151, 150):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False
        return True

    def nav(self):
        """can navigate a maze by itself"""
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        #print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        
        
        self.starting_postion = self.get_heading()
        while True:
            while self.quick_check():
                self.fwd()
                time.sleep(0.01)
                self.corner_count = 0 #counts the corners so you can use it later to get out of them
            self.stop()
            self.corner_work()
            self.left_or_right()
            # how would you make it turn when it is going the wrong direction

    def corner_work(self):
        self.corner_count += 1
        if self.corner_count > 3:
            self.corner_check()


    def left_or_right(self):
        """turn left or right depending on averaged scan"""
        #traversal
        left_total = 0
        left_count = 0
        right_total = 0
        right_count = 0
        self.scan()
        for ang, dist in self.scan_data.items():
            if ang < self.MIDPOINT:
                right_total += dist
                right_count += 1
                print("Angle: %d // dist: %d // right_count: %d" % (ang, dist, right_count))
            else:
                left_total += dist
                left_count += 1
        left_avg = left_total / left_count
        right_avg = right_total / right_count
        if left_avg > right_avg:
            self.turn_by_deg(-45)
        else:
            self.turn_by_deg(45)
        # if robot is facing the wrong way it will turn it around
        self.exit_bias()

    def corner_check(self):
        self.turn_by_deg(180)
        self.deg_fwd(360)
        # what happens when it turns 180 but then goes to starting position  by turning another 180 landing in the same place?  
        # hopefully will stop the robot from going circles
        if self.read_distance() > self.SAFE_DIST:
            return
        else:
            self.turn_to_deg(self.starting_postion)
                
    def exit_bias(self):
        current_position = self.get_heading()
        if abs(self.starting_postion - current_position) >180:
            self.turn_to_deg(self.starting_postion)
            if self.quick_check():
                return
            else:
                self.left_or_right()
    def slither(self):
        """practice a smooth veer"""
        #writedown where we started
        starting_direction = self.get_heading()
        #start driving forward
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.fwd()
        # throttl down the left motor
        for power in range(self.LEFT_DEFAULT, 60,-10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
        #throttle up the left while lowring the right
        for power in range(60, self.LEFT_DEFAULT +1, 10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
        # throttl down the right motor
        for power in range(self.RIGHT_DEFAULT, 60,-10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
        #throttle up the right while lowring the right
        for power in range(60, self.RIGHT_DEFAULT +1, 10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
        left_speed = self.LEFT_DEFAULT
        right_speed = self.RIGHT_DEFAULT
        #straighten out
        while self.get_heading() != starting_direction:
            #if I need to veer right
            if self.get_heading() < starting_direction:
                right_speed -= 5
                left_speed += 5
            #if I need to veer left
            elif self.get_heading() > starting_direction:
                left_speed -= 5
                right_speed +=5
            self.set_motor_power(self.MOTOR_LEFT, left_speed)
            self.set_motor_power(self.MOTOR_RIGHT, right_speed)
            time.sleep(.1)


    def hold_position(self):
        start = self.get_heading()
        while True:
            time.sleep(.01)
            current = self.get_heading()
            if abs(start - current) > 20:
                self.turn_to_deg(start)


    def twist(self):
        """turns right then left"""
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
