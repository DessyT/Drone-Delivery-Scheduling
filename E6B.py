import math as m
#Calculates the actual angle and speed the drone will have accounting for wind

class E6B:

    def __init__(self):
        pass

    def getCorrectedDirection(self,windSpeed,windDir,droneDir,droneSpeed):
        angle = m.asin(windSpeed * m.sin(windDir - droneDir) / droneSpeed)

        correctAngle = droneDir - angle
        return correctAngle,angle

    def getCorrectedSpeed(self,windSpeed,windDir,droneDir,droneSpeed,correctAngle):

        groundSpeed = m.sqrt(m.pow(droneSpeed,2) + m.pow(windSpeed,2) - 2 *
                            droneSpeed * windSpeed * m.cos(droneDir - windDir + correctAngle))

        #print(f"droneSpeed = {droneSpeed}\nwindSpeed = {windSpeed}\ndroneDir = {droneDir}\nwindDir = {windDir}\ncorrectAngle = {correctAngle}")

        return groundSpeed

#Testing
'''
#Sample wind speed and bearing
windSpeed = 10
windDir = m.radians(90)

#Sample drone speed and bearing
droneDir = m.radians(180)
droneSpeed = 15

test = E6B()

correctedDir,dir = test.getCorrectedDirection(windSpeed,windDir,droneDir,droneSpeed)
speed = test.getCorrectedSpeed(windSpeed,windDir,droneDir,droneSpeed,dir)

print("Drone direction =",m.degrees(droneDir))
print("Wind from =",m.degrees(windDir))


print("Direction test",float(m.degrees(correctedDir)))
print("Direction correction", float(m.degrees(dir)))


print("Speed test",speed,"m/s")
'''
