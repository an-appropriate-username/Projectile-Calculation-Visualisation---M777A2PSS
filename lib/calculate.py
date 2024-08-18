from Location3D import Location3D

#--- INPUT COORDINATES ---#
def get_coordinates(prompt):
    while True:
        try:
            print(prompt)
            x = float(input("Enter x coordinate: "))
            y = float(input("Enter y coordinate: "))
            z = float(input("Enter z coordinate: "))
            return Location3D(x, y, z)
        except ValueError:
            print("Invalid input. Please enter numeric values.")

#--- MAIN ---#
if __name__ == "__main__":

    #--- GET COORD FROM OPERATOR ---#
    howitzer = get_coordinates("\nEnter coordinates for the howitzer (in meters):")
    target = get_coordinates("\nEnter coordinates for the target (in meters):")

    #--- GET DIST FROM COORD ---#
    distance = howitzer.distance_to(target)

    if distance >= 24001:
        print("\nDistance exceeds maximum range.")
        exit()

    dist_km = distance/1000
    print(f"\nDistance:\n{distance:.2f} Meters\n{dist_km:.2f} Kilometers")

    #--- GET ROTATION, DIRECTION AND DESIRED HEADING FROM COORD ---#
    rotation_needed, direction, final_facing = howitzer.calculate_rotation(target)
    print("\nReference heading: 90°")
    print(f"Rotate: {rotation_needed:.2f}°")
    if rotation_needed == 0:
        pass
    else:
        print(f"Direction: {direction}")
    print(f"Final heading: {final_facing:.2f}°")

    #--- GET CHARGE ZONE AND VELOCITY FROM DIST ---#
    zone, velocity = howitzer.set_charge_zone(distance)
    print(f"\nCharge zone: {zone}")
    print(f"Velocity: {velocity} (m/s)")

    #--- GET LAUNCH ANGLE ---#
    _, low_angle = howitzer.calculate_launch_angles(distance, velocity)
    print(f"Pitch: {low_angle:.2f}°")

    high_angle, alt_velocity, alt_zone = howitzer.alternative_setting(distance)
    print(f"\nAlternative charge zone: {alt_zone}")
    print(f"Alternative Velocity: {alt_velocity} (m/s)")
    print(f"Alternative pitch: {high_angle:.2f}°")


