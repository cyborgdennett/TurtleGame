#Made By Casper Belier and Gazi Özdemir

import time as tm
import turtle as tr
from datetime import timedelta as dt




def compoundCar(length, width, color, name):
    shape = tr.Shape("compound")
    #body
    body = ((-.5*width,-.5*length),(-.5*width,.5*length),(.5*width,.5*length),(.5*width,-.5*length))
    shape.addcomponent(body, color, "black")
    #tires
    tire1 = ((.55 * width, -.35 * length), (.55 * width, -.15 * length), (.45 * width, -.15 * length),
            (.45 * width, -.35 * length))
    tire2 = ((-.55 * width, -.35 * length), (-.55 * width, -.15 * length), (-.45 * width, -.15 * length),
            (-.45 * width, -.35 * length))
    tire3 = ((-.55 * width, .35 * length), (-.55 * width, .15 * length), (-.45 * width, .15 * length),
            (-.45 * width, .35 * length))
    tire4 = ((.55 * width, .35 * length), (.55 * width, .15 * length), (.45 * width, .15 * length),
            (.45 * width, .35 * length))

    shape.addcomponent(tire1, "black", "black")
    shape.addcomponent(tire2, "black", "black")
    shape.addcomponent(tire3, "black", "black")
    shape.addcomponent(tire4, "black", "black")
    #backglass
    backwindow = ((width*-.35,length*-.3),(width*-.35,length*-.2),(width*.35,length*-.2),(width*.35,length*-.3))
    shape.addcomponent(backwindow, "darkgray","black")
    #frontglass
    frontwindow = ((width*-.40,length*.05),(width*-.40,length*.25),(width*.40,length*.25),(width*.40,length*.05))
    shape.addcomponent(frontwindow, "lightgrey", "black")
    #light front
    frontlight1 = ((width * -.45, length * .48), (width * -.45, length * .44), (width * -.30, length * .44),
                  (width * -.30, length * .48))
    frontlight2 = ((width * .45, length * .48), (width * .45, length * .44), (width * .30, length * .44),
                  (width * .30, length * .48))

    shape.addcomponent(frontlight1, "yellow", "orange")
    shape.addcomponent(frontlight2, "yellow", "orange")

    #light back
    backlight1 = ((width * -.45, length * -.48), (width * -.45, length * -.44), (width * -.22, length * -.44),
                  (width * -.22, length * -.48))
    backlight2 = ((width * .45, length * -.48), (width * .45, length * -.44), (width * .22, length * -.44),
                  (width * .22, length * -.48))
    shape.addcomponent(backlight1, "crimson", "silver")
    shape.addcomponent(backlight2, "crimson", "silver")


    tr.register_shape(name+"shape",shape)
    return shape

class Car(object):


    def __init__(self, NAM, name, color, maxSpeed, accel, decel, width, length):
        self.NAM = NAM
        self.name = name
        self.color = color
        self.maxSpeed = maxSpeed
        self.accel = accel
        self.decel = decel
        self.width = width
        self.length = length
        self.speed = 0
        compoundCar(self.length,self.width,self.color, self.name)

    def toCircuit(self, circuit, pos, direction, player, nextCorner, nextCornerDirection, nextCornerSpeed):
        self.circuit = circuit
        self.t = tr.Turtle(shape=self.name + "shape")
        self.t.ht()
        self.t.speed(0)
        self.t.pu()
        self.t.setpos(pos)
        self.t.setheading(direction)
        self.heading = direction
        self.t.forward(1)
        self.player = player
        self.t.st()
        self.nextCorner = nextCorner
        self.nextCornerDirection = nextCornerDirection
        self.nextCornerSpeed = nextCornerSpeed

        self.fwst = 0 #state of forward key
        self.brst = 0 #state of backward key

        self.driftState = 0  #state of going out of the corner

    def startRace(self):
        self.running = 1
        self.lap = 0
        self.setControls()


    def disableControls(self):
        controls = (("w", "s"), ("Up", "Down"))
        self.circuit.screen.onkey(None, controls[self.player][0])
        self.circuit.screen.onkey(None, controls[self.player][1])

    def setControls(self):
        controls = (("w", "s"), ("Up", "Down"))
        self.circuit.screen.onkeypress(self.fwn, controls[self.player-1][0])
        self.circuit.screen.onkeyrelease(self.fwf, controls[self.player-1][0])
        self.circuit.screen.onkeypress(self.brn, controls[self.player-1][1])
        self.circuit.screen.onkeyrelease(self.brf, controls[self.player-1][1])

    def fwn(self): #fwst is forward state. means if engine is going
        self.fwst = 1
    def fwf(self):
        self.fwst = 0

    def brn(self): #brst = brake state
        self.brst = 1
    def brf(self):
        self.brst = 0


    def drive(self, time):
        if self.running == 1:
            self.prevPos = self.t.pos()#save inital position

            #calculate distance and new speed
            if self.fwst == self.brst:
                self.forward = (time*self.speed)
            elif self.fwst == 1:
                if self.speed == self.maxSpeed:
                    self.forward = (self.maxSpeed*time)
                elif self.speed + (self.accel*time) > self.maxSpeed:
                    transitionTime = (self.maxSpeed-self.speed) / (self.accel*time) #
                    self.forward = (transitionTime*time * (self.maxSpeed + self.speed) / 2 + (1-transitionTime)*time*self.maxSpeed)
                    self.speed = self.maxSpeed
                else:
                    self.forward = (self.speed + (self.accel*time/2)*time)
                    self.speed = self.speed + self.accel * time
            elif self.brst == 1:
                if self.speed == 0:
                    pass
                elif (self.speed - (time*self.decel)) < 0:
                    self.forward = (0.5*self.speed**2/(self.decel*time))
                    self.speed = 0
                else:
                    self.forward = ((2*self.speed-(time*self.decel))/2*time)
                    self.speed = self.speed-(time*self.decel)

            #drift!
            if self.driftState:
                if self.totalOldTime >= 4:
                    return
                elif self.oldTime > .5:
                    self.t.left(60)
                    self.t.forward(self.forward)
                    self.totalOldTime += self.oldTime
                    self.oldTime = 0
                else:
                    self.t.forward(self.forward)
                    self.oldTime += time
                return

            #check if you would overextend the corner
            if self.t.heading() == 0:
                self.overExtended = self.t.pos()[0] + self.forward - self.nextCorner[0]
            elif self.t.heading() == 90:
                self.overExtended = self.t.pos()[1] + self.forward - self.nextCorner[1]
            elif self.t.heading() == 180:
                self.overExtended = -(self.t.pos()[0] - self.forward - self.nextCorner[0])
            elif self.t.heading() == 270:
                self.overExtended = -(self.t.pos()[1] - self.forward - self.nextCorner[1])

            #move around corner
            if self.overExtended >= 0:
                if self.speed >= self.nextCornerSpeed: #if you go to fast, this function will make you drift
                    self.disableControls() #stop input from user
                    self.brst = 1 #put on the brakes
                    self.fwst = 0 #stop going forward
                    self.speed -= 200
                    self.decel = 100 # put decelleration speed very fast
                    self.driftState = 1
                    self.oldTime = time
                    self.totalOldTime = time
                    return

                self.t.forward(self.forward-self.overExtended)#move forward to corner position
                self.t.setheading(self.nextCornerDirection)#change direction
                self.t.forward(self.overExtended)#move forward remaining
                self.nextCorner, self.nextCornerDirection, self.nextCornerSpeed = self.circuit.getNextCorner(self.nextCorner, self.player)
            #move forward
            else:
                self.t.forward(self.forward)

            if self.circuit.isFinish(self.prevPos, self.t.pos(), self.player, time):
                self.lap += 1





class Circuit:
    def __init__(self, name):
        self.name = name
        self.screen = tr.getscreen()

        #setup background
        self.screen.bgcolor('pink')
        self.width = 750
        self.height = 422
        self.screen.setup(width=self.width, height=self.height)
        #self.screen.setworldcoordinates(0,0,self.width,self.height)
        self.screen.bgpic("zandvoort.gif")

        # setup cornerpositions
        self.Corners = [None]*6,[None] * 6
        self.cornerDirection = [0,90,180,270,180,270]
        self.maxCornerSpeed = [300,400,350,250,600,400]


        #setup road
        self.t = tr.Turtle()
        self.t.speed(0)
        self.t.pu()
        self.t.goto(-(self.width/2)+100,-(self.height/2)+100)
        self.t.pd()
        self.t.pensize(30)
        self.t.pencolor("black")

        self.Corners[0][0] = self.t.pos()
        self.t.forward(400)
        self.Corners[0][1] = self.t.pos()
        self.t.left(90)
        self.t.forward(300)
        self.Corners[0][2] = self.t.pos()
        self.t.left(90)
        self.t.forward(200)
        self.Corners[0][3] = self.t.pos()
        self.t.left(90)
        self.t.forward(100)
        self.Corners[0][4] = self.t.pos()
        self.t.right(90)
        self.t.forward(200)
        self.Corners[0][5] = self.t.pos()
        self.t.left(90)
        self.t.forward(200)

        self.t.pu()
        self.t.pencolor("grey")

        self.t.left(90)

        self.t.goto(-(self.width/2)+100+40, -(self.height/2)+100-40)
        self.t.pd()
        self.Corners[1][0] = self.t.pos()
        self.t.forward(400)
        self.Corners[1][1] = self.t.pos()
        self.t.left(90)
        self.t.forward(300)
        self.Corners[1][2] = self.t.pos()
        self.t.left(90)
        self.t.forward(200)
        self.Corners[1][3] = self.t.pos()
        self.t.left(90)
        self.t.forward(100)
        self.Corners[1][4] = self.t.pos()
        self.t.right(90)
        self.t.forward(200)
        self.Corners[1][5] = self.t.pos()
        self.t.left(90)
        self.t.forward(200)
        self.t.ht()
        self.t.pu()


        #setup finishline
        self.Finish = [None] * 2
        self.t.goto(-(self.width / 2) +250, -(self.height / 2) +100+15)

        self.t.pd()
        self.t.pencolor('yellow')
        self.t.pensize(2)
        self.t.forward(15)
        self.Finish[0] = self.t.pos()
        self.t.forward(14)
        self.t.pu()

        self.t.goto(-(self.width / 2) +250+40, -(self.height / 2) +100 + 15-40)

        self.t.pd()
        self.t.pencolor('yellow')
        self.t.pensize(2)
        self.t.forward(15)
        self.Finish[1] = self.t.pos()
        self.t.forward(14)
        self.t.pu()

        #setup lap
        self.players = 0
        self.laps = 3
        self.laptime = [[0.0]*(self.laps+1)]*2#save laptimes
        self.currentLap = [0]*2 #save current lap time
        self.fastestlap =[0]*2#save fastest lap here!
        self.carlap = [0]*2 #save current lap of car
        self.reverse = 0

        self.startheading = 0

    def addPlayer(self,Car):
        self.players += 1
        Car.toCircuit(self, self.Finish[self.players-1],self.startheading,self.players,self.Corners[self.players-1][1],self.cornerDirection[1],self.maxCornerSpeed[1])

    def isFinish(self, prevPos, pos, player, time):
        if prevPos == pos:
            return
        self.currentLap[player - 1] += time
        x = self.Finish[player - 1][0]
        y = self.Finish[player - 1][1]

        if y == pos[1] and y == prevPos[1]: #check y-coordinate
            if prevPos[0] <= x and pos[0] >= x:
                self.laptime[player - 1][self.carlap[player - 1]] = self.currentLap[player - 1]
                print(self.currentLap[player - 1])
                if self.currentLap < self.fastestlap:
                    self.fastestlap = self.currentLap
                    print("Fastest!")
                self.currentLap[player - 1] = 0
                return 1



    def getNextCorner(self, lastCorner, player):
        cornerIndex = self.Corners[player-1].index(lastCorner)
        if(cornerIndex) == 5:
            return self.Corners[player-1][0],self.cornerDirection[0],self.maxCornerSpeed[0]
        else:
            return self.Corners[player-1][cornerIndex+1],self.cornerDirection[cornerIndex+1],self.maxCornerSpeed[cornerIndex+1]

    def updateTimer(self, time):
        pass


    '''

    
    def isLap(self):
    



    
    def printCircuit

    def timeDisplay(self, car):

    def fastestLap(self):
'''

class World:
    def __init__(self):
        self.auto = Car("HAM","Renault", "blue", 650, 50, 5, 20, 80),Car("VER","Renault1", "red", 120, 5, 5, 20, 80)
        self.circuit = Circuit("Zandvoort")
        self.score = tr.Turtle()
        self.score.ht()
        self.score.pu()


        self.circuit.addPlayer(self.auto[0])
        self.circuit.addPlayer(self.auto[1])

        self.auto[0].startRace()
        self.auto[1].startRace()

        self.screenTime = 9
        self.circuit.screen.listen()
        self.time = tm.time()

    def printScore(self):
        self.score.clear()
        self.score.color("magenta")
        style = ('Courier', 12, 'italic')
        textStyle = ('Courier', 12, 'italic')
        carStyle = ('Courier', 20, 'bold')
        for i in range(self.circuit.players):
            self.score.setpos(-360, 160-i*30)
            self.score.write(self.auto[i].NAM, font=carStyle, align='left')
        self.score.setpos(-310,190)
        self.score.write("currentLap",font=textStyle, align='left')
        self.score.setpos(-190,190)
        self.score.write("fastestLap",font=textStyle, align='left')

        for i in range(self.circuit.players):
            self.score.setpos(-310,165-30*i)
            time = self.format_result(self.circuit.currentLap[i])
            minutes, seconds = divmod(time.seconds, 60)
            millis = round(time.microseconds/ 1000, 0)
            self.score.write(f"{minutes:02}:{seconds:02}.{millis}",font=style, align='left')
        for i in range(self.circuit.players):
            self.score.setpos(-190, 165 - 30 * i)
            time = self.format_result(self.circuit.fastestlap[i])
            minutes, seconds = divmod(time.seconds, 60)
            millis = round(time.microseconds / 1000, 0)
            self.score.write(f"{minutes:02}:{seconds:02}.{millis}", font=style, align='left')

    def format_result(self, result):
        seconds = int(result)
        microseconds = int((result * 1000000) % 1000000)
        output = dt(0, seconds, microseconds)
        return output

    def fullScreen(self):
        self.screen.screensize()
        self.screen.setup(width=1.0, height=1.0)

    def run(self):
        while True:  # Main real-time simulation loop
            # BEGIN mandatory statements
            self.oldTime = self.time
            self.time = tm.time()  # The only place where the realtime clock is repeatedly queried
            self.deltaTime = self.time - self.oldTime
            # END mandatory statements

            # ... other code, using objects that are in the world, like a racetrack and cars
            self.auto[0].drive(self.deltaTime)
            self.auto[1].drive(self.deltaTime)
            self.screenTime += self.deltaTime
            if self.screenTime > 10:
                self.printScore()
                self.screenTime = 0

            self.circuit.screen.update()
            tm.sleep(0.02)  # Needed to free up processor for other tasks like I/O


mijnWereld = World()
mijnWereld.run()