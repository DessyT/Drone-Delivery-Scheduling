import math as m
#Calculates the actual angle and speed the drone will have accounting for wind
'''
#Add 180 degrees so we have wind direction to instead of from
windSpeed = 10
windDir = m.radians(270) + m.radians(180)

#print("pre",m.degrees(windDir))
#Make sure we don't have >360 degrees
if(windDir > m.radians(360)):
    windDir = windDir - m.radians(360)

#print("post",m.degrees(windDir))
#Sample route direction
droneDir = m.radians(300)

#Actual wind speed of drone (max speed)
droneSpeed = 15

angle = m.asin(windSpeed * m.sin(windDir - droneDir) / droneSpeed)
print("Drone direction =",m.degrees(droneDir))
print("Wind direction =",m.degrees(windDir))
print("Degree adjustment  =", float(m.degrees(angle)))

heading = droneDir - angle
print("Direction of travel =", float(m.degrees(heading)))


### Now lets get ground speed

groundSpeed = m.sqrt(m.pow(droneSpeed,2) + m.pow(windSpeed,2) - 2 *
                    droneSpeed * windSpeed * m.cos(droneDir - windDir + angle))

print("Ground speed =",groundSpeed, "m/s")
'''
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

        return groundSpeed
'''
#Testing

#Sample wind speed and bearing
windSpeed = 15
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
