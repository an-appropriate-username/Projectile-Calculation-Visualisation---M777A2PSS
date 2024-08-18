import math

#--- VARIABLES ---#
min_distance = 2800 
max_distance = 24000 

charge_zone = {
    "CZ0": 0,
    "CZ1": 350,
    "CZ2": 400,
    "CZ3": 450,
    "CZ4": 500,
    "CZ5": 550,
    "CZ6": 600,
    "CZ7": 650,
    "CZ8": 750
} # Velocity in m/s

#--- LOCATION CLASS ---#
class Location3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, target):
        """
        Calculate the Euclidean distance to another Location3D instance.
        """
        delta_x = self.x - target.x
        delta_y = self.y - target.y
        delta_z = self.z - target.z
        return math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
    
    def set_charge_zone(self, distance):
        """
        Determine the appropriate charge zone based on distance.
        """
        if distance <= min_distance:
            print(f"You are too close to the target.\nIncrease distance by {min_distance - distance:.2f}m")
            return "CZ0", charge_zone["CZ0"]
        elif distance <= 3000:
            return "CZ1", charge_zone["CZ1"]
        elif distance <= 6000:
            return "CZ2", charge_zone["CZ2"]
        elif distance <= 9000:
            return "CZ3", charge_zone["CZ3"]
        elif distance <= 12000:
            return "CZ4", charge_zone["CZ4"]
        elif distance <= 15000:
            return "CZ5", charge_zone["CZ5"]
        elif distance <= 18000:
            return "CZ6", charge_zone["CZ6"]
        elif distance <= 21000:
            return "CZ7", charge_zone["CZ7"]
        elif distance <= max_distance:
            return "CZ8", charge_zone["CZ8"]
        else:
            print(f"Distance exceeds maximum range.\nDecrease distance by {distance - max_distance:.2f}m")
            return "CZ0", charge_zone["CZ0"]

    def calculate_rotation(self, target, initial_heading=90):
        delta_x = target.x - self.x
        delta_y = target.y - self.y
        azimuth = math.atan2(delta_y, delta_x)
        azimuth_deg = math.degrees(azimuth)

        #--- ROTATION NEEDED ---#
        rotation_needed = azimuth_deg - initial_heading
        
        #--- DIRECTION ---#
        if rotation_needed < 0:
            direction = "clockwise"
            rotation_needed = -rotation_needed
            final_facing = initial_heading + rotation_needed
        else:
            direction = "counterclockwise"
            final_facing = initial_heading - rotation_needed
        
        return rotation_needed, direction, final_facing
    
    #--- ANGLE (PITCH) ---#
    def calculate_launch_angles(self, distance, velocity, gravity=9.81):
        """
        Calculate the launch angle to hit the target at a given distance
        with a given velocity.
        """
        sin_2theta = (distance * gravity) / (velocity ** 2)
        
        if -1 <= sin_2theta <= 1:
            theta_rad_low = 0.5 * math.asin(sin_2theta)
            theta_rad_high = 0.5 * (math.pi - math.asin(sin_2theta))
            theta_deg_low = math.degrees(theta_rad_low)
            theta_deg_high = math.degrees(theta_rad_high)
            return theta_deg_high, theta_deg_low
        else:
            raise ValueError("The distance and velocity provided are not feasible for hitting the target with the given conditions.")

    def alternative_setting(self, distance, gravity=9.81, min_angle=25, max_angle=70):
        """
        Find a suitable high angle that falls within the desired range.
        """
        for zone, velocity in charge_zone.items():
            if velocity == 0:  # Skip the zero velocity
                continue
            
            try:
                high_angle, _ = self.calculate_launch_angles(distance, velocity, gravity)
                if min_angle <= high_angle <= max_angle:
                    return high_angle, velocity, zone
            except ValueError:
                continue

        return 0, charge_zone["CZ0"], "CZ0"
