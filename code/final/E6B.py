import math as m
#Calculates the actual angle and speed the drone will have accounting for wind

#Sample wind speed and bearing
windSpeed = 8
windDir = m.radians(110)
#Sample route direction
routeDir = m.radians(30)

#Actual wind speed of drone (max speed)
actualSpeed = 15

angle = m.asin(windSpeed * m.sin(windDir - routeDir) / actualSpeed)
print("Difference in degrees =",m.degrees(angle))

heading = routeDir - angle
print("Direction of travel =", m.degrees(heading))


### Now lets get ground speed

groundSpeed = m.sqrt(m.pow(actualSpeed,2) + m.pow(windSpeed,2) - 2 *
                    actualSpeed * windSpeed * m.cos(routeDir - windDir + angle))

print("Ground speed =",groundSpeed, "m/s")
