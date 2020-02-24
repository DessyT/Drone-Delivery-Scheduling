import math as m
#Calculates the actual angle and speed the drone will have accounting for wind

#Sample wind speed and bearing
windSpeed = 10
windDir = m.radians(5)

'''
print("pre",m.degrees(windDir))
if(m.degrees(windDir) > 360):
    windDir = windDir - m.radians(360)

print("post",m.degrees(windDir))'''
#Sample route direction
droneDir = m.radians(300)

#Actual wind speed of drone (max speed)
droneSpeed = 15

angle = m.asin(windSpeed * m.sin(windDir - droneDir) / droneSpeed)
print("Drone direction =",m.degrees(droneDir))
print("Wind from =",m.degrees(windDir))
print("Degree adjustment  =", float(m.degrees(angle)))

heading = droneDir + angle
print("Direction of travel =", float(m.degrees(heading)))


### Now lets get ground speed

groundSpeed = m.sqrt(m.pow(droneSpeed,2) + m.pow(windSpeed,2) - 2 *
                    droneSpeed * windSpeed * m.cos(droneDir - windDir + angle))

print("Ground speed =",groundSpeed, "m/s")
