#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math

class alphabot(Robot): #Create a Robot
    
    flag = False
    onTargetFlag = False
    firstOnTarget = True

    def init(self):    #To initialyse your robot
        #Set the bot color in RGB
        self.setColor(0, 0, 0)
        self.setGunColor(255, 255, 255)
        self.setRadarColor(255, 60, 0)
        self.setBulletsColor(255, 150, 150)

        self.radarVisible(True) # if True the radar field is visible
        
        self.lockRadar("gun")
        self.setRadarField("thin")
        
    def run(self): #main loop to command the bot
        pos = self.getPosition()
        x = pos.x()
        y = pos.y()
        width = self.getMapSize().width()
        height = self.getMapSize().height()
        angle = self.getHeading()
        angle = angle + 90
        angle = angle % 360
        angle = (360 - angle) % 360
        if self.onTargetFlag == False:
            if x + 50 < width and x - 50 > 0 and y + 50 < height and y - 50 > 0:
                self.move(10)
                self.turn(10)
                self.gunTurn(10)
                self.flag = False
            else:
                if x >= width / 2 and y <= height / 2:
                    a = math.sqrt((x-width/2)**2 + (y - height/2)**2)
                    b = width - x
                    c = math.sqrt((width/2)**2 + (y - height/2)**2)
                    cotheta = (a**2 + b**2 - c**2) / (2*a*b)
                    theta = math.degrees(math.acos(cotheta))
                    theta = 360-theta
                    if not(self.flag):
                        self.turn(10)
                        self.gunTurn(10)
                        if abs(int(angle) - int(theta)) < 10:
                            self.move(100)
                            self.flag = True
                elif x <= width / 2 and y < height / 2:
                    a = math.sqrt((x-width/2)**2 + (y - height/2)**2)
                    b = x
                    c = math.sqrt((width/2)**2 + (y - height/2)**2)
                    cotheta = (a**2 + b**2 - c**2) / (2*a*b)
                    theta = math.degrees(math.acos(cotheta))
                    theta = 180+theta
                    if not(self.flag):
                        self.turn(10)
                        self.gunTurn(10)
                        if abs(int(angle) - int(theta)) < 10:
                            self.move(100)
                            self.flag = True
                elif x < width / 2 and y >= height / 2:
                    a = math.sqrt((x-width/2)**2 + (y - height/2)**2)
                    b = x
                    c = math.sqrt((width/2)**2 + (y - height/2)**2)
                    cotheta = (a**2 + b**2 - c**2) / (2*a*b)
                    theta = math.degrees(math.acos(cotheta))
                    theta = 180 - theta
                    if not(self.flag):
                        self.turn(10)
                        self.gunTurn(10)
                        if abs(int(angle) - int(theta)) < 10:
                            self.move(100)
                            self.flag = True
                elif x > width / 2 and y > height / 2:
                    a = math.sqrt((x-width/2)**2 + (y - height/2)**2)
                    b = width - x
                    c = math.sqrt((width/2)**2 + (y - height/2)**2)
                    cotheta = (a**2 + b**2 - c**2) / (2*a*b)
                    theta = math.degrees(math.acos(cotheta))
                    if not(self.flag):
                        self.turn(10)
                        self.gunTurn(10)
                        if abs(int(angle) - int(theta)) < 10:
                            self.move(100)
                            self.flag = True

    def onHitWall(self):
        self.reset() #To reset the run function to the begining (auomatically called on hitWall, and robotHit event) 
        self.pause(5)
        self.move(-30)

        self.rPrint('ouch! a wall !')

    def sensors(self): #NECESARY FOR THE GAME
        pass
        
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        self.stop()
        self.fire(10)
        self.stop()
        self.rPrint('collision with:' + str(robotId))
        
    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.rPrint ("hit by " + str(bulletBotId) + "with power:" +str( bulletPower))
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str( botId))
        
    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.stop()
        self.turn(1)
        self.gunTurn(1)
        self.stop()
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("damn I'm Dead")
        
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        self.onTargetFlag = True        
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))

        pos = self.getPosition()
        x = pos.x()
        y = pos.y()
        dist = math.sqrt((x-botPos.x())**2 + (y - botPos.y())**2)

        if self.firstOnTarget == True:
            self.stop()
            if dist > 300:
                print("so far")
                self.turn(2)
                self.gunTurn(2)
            else:
                print("so good?")
                self.turn(3)
                self.gunTurn(3)
            self.firstOnTarget = False

        self.stop()
        if dist < 200:
            self.move(3)
        else:
            self.move(15)
        self.fire(5)
        self.stop()
        self.onTargetFlag = False