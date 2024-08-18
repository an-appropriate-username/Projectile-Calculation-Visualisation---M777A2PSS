M777 A2 Projectile Support Software
Overview
The M777 A2 Projectile Support Software is a tool designed to assist in calculating various parameters for the M777 A2 Howitzer using a 155mm shell. It accepts coordinates in meters and returns critical data, including time to target, distance, rotation, pitch and recommended charge zones. The software also generates a small top-down map view showing the required rotation, providing a visual perspective of the situation.
Features
    • Distance Calculation: Computes the distance between the howitzer and the target.
    • Rotation Calculation: Determines the necessary rotation and direction for the howitzer.
    • Pitch Calculation: Computes the correct pitch for the projectile to impact the target area.
    • Charge Zone Recommendation: Suggests appropriate charge zones based on the distance.
    • High and Low Angle Calculation: Provides both high and low launch angles based on the charge zone.
    • Map Generation: Generates a small map representing the situation from a top-down perspective, including the needed rotation.
Dependencies
To run this app, you need the following Python libraries:
    • Tkinter: For creating the GUI.
    • Matplotlib: For generating the map and visualizing the situation.
    • Cartopy: For map projection and geographic data visualization.
    • numpy: For numerical operations, particularly in the calculation of coordinates.
Usage
    1. Input Coordinates: Enter the x, y, and z coordinates for both the howitzer and the target in meters.
    2. Calculate: Click the "Calculate" button to process the input and get the necessary data.
    3. View Results: The calculated data, including distance, rotation, pitch, and charge zone recommendations, will be displayed in the text area.
    4. Generate Map: A top-down map will be generated, providing a visual representation of the howitzer’s rotation and the target's location.

