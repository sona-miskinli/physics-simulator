print("My physics simulator is starting!")
import math

angle_degrees = float(input("Enter launch angle (degrees): "))
speed = float(input("Enter launch speed (m/s): "))
gravity = 9.8

angle_radians = math.radians(angle_degrees)

print("Launch angle:", angle_degrees, "degrees")
print("Launch speed:", speed, "m/s")
max_height = (speed ** 2) * (math.sin(angle_radians) ** 2) / (2 * gravity)
range_distance = (speed ** 2) * math.sin(2 * angle_radians) / gravity

print("Max height:", round(max_height, 2), "meters")
print("Range:", round(range_distance, 2), "meters")
import matplotlib.pyplot as plt

time_of_flight = (2 * speed * math.sin(angle_radians)) / gravity
time_points = [i * 0.01 for i in range(int(time_of_flight * 100) + 1)]

x_points = [speed * math.cos(angle_radians) * t for t in time_points]
y_points = [speed * math.sin(angle_radians) * t - 0.5 * gravity * t**2 for t in time_points]

plt.plot(x_points, y_points)
plt.title("Projectile Trajectory")
plt.xlabel("Distance (meters)")
plt.ylabel("Height (meters)")
plt.grid(True)
plt.show()