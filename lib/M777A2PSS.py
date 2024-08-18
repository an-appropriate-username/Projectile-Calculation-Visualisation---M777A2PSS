import tkinter as tk
from Location3D import Location3D  
from tkinter import messagebox
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from styles import InputButton, InputLabel

class M777A2PSSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("M777 A2 PSS")
        self.root.geometry("300x600") 

        #--- FRAME ---
        frame = tk.Frame(root, bg="grey", padx=5, pady=10) 
        frame.pack(fill=tk.BOTH, expand=True)  

        #--- INPUT FIELDS ---#
        self.howitzer_x_entry = tk.Entry(frame)
        self.howitzer_y_entry = tk.Entry(frame)
        self.howitzer_z_entry = tk.Entry(frame)

        self.target_x_entry = tk.Entry(frame)
        self.target_y_entry = tk.Entry(frame)
        self.target_z_entry = tk.Entry(frame)

        #--- CONNECT TO GRID ---#
        self.howitzer_x_entry.grid(row=0, column=1, padx=5, pady=5)
        self.howitzer_y_entry.grid(row=1, column=1, padx=5, pady=5)
        self.howitzer_z_entry.grid(row=2, column=1, padx=5, pady=5)

        self.target_x_entry.grid(row=3, column=1, padx=5, pady=5)
        self.target_y_entry.grid(row=4, column=1, padx=5, pady=5)
        self.target_z_entry.grid(row=5, column=1, padx=5, pady=5)

        #--- LABEL & STYLE ---#
        InputLabel(frame, text="Howitzer X:").grid(row=0, column=0, padx=5, pady=5)
        InputLabel(frame, text="Howitzer Y:").grid(row=1, column=0, padx=5, pady=5)
        InputLabel(frame, text="Howitzer Z:").grid(row=2, column=0, padx=5, pady=5)

        InputLabel(frame, text="Target X:").grid(row=3, column=0, padx=5, pady=5)
        InputLabel(frame, text="Target Y:").grid(row=4, column=0, padx=5, pady=5)
        InputLabel(frame, text="Target Z:").grid(row=5, column=0, padx=5, pady=5)

        InputButton(frame, text="Calculate", command=self.calculate).grid(row=6, column=1, pady=10)
        InputButton(frame, text="Clear", command=self.confirm_clear, bg = "darkgrey").grid(row=6, column=0, pady=10)

        #--- DISPLAY RESULTS ---#
        self.result_text = tk.Text(frame, height=20, width=30)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=15, pady=5)

    #--- CALCULATE ---#
    def calculate(self):
        try:
            howitzer_x = float(self.howitzer_x_entry.get())
            howitzer_y = float(self.howitzer_y_entry.get())
            howitzer_z = float(self.howitzer_z_entry.get())

            target_x = float(self.target_x_entry.get())
            target_y = float(self.target_y_entry.get())
            target_z = float(self.target_z_entry.get())

            #--- Location3D INSTANCES ---#
            howitzer = Location3D(howitzer_x, howitzer_y, howitzer_z)
            target = Location3D(target_x, target_y, target_z)

            #--- GET DIST FROM COORD ---#
            distance = howitzer.distance_to(target)
            if distance >= 24001:
                self.distance_error()
            distance_km = distance/1000

            #--- GET ROTATION, DIRECTION AND DESIRED HEADING FROM COORD ---#
            rotation_needed, direction, final_facing = howitzer.calculate_rotation(target)

            #--- GET CHARGE ZONE AND VELOCITY FROM DIST ---#
            zone, velocity = howitzer.set_charge_zone(distance)

            #--- GET LAUNCH ANGLE AND TIME ---#
            _, low_angle = howitzer.calculate_launch_angles(distance, velocity)
            time_to_target = distance/velocity

            #--- ALT ANGLE ---#
            high_angle, alt_velocity, alt_zone = howitzer.alternative_setting(distance)
            alt_time_to_target = distance/alt_velocity

            #--- DISPLAY RESULT ---#
            result = (
                f"Distance: {distance:.2f} Meters\n"
                f"Distance: {distance_km:.2f} Kilometers\n\n"
                f"Reference heading: 90°\n"
                f"Rotate: {rotation_needed:.2f}°\n"
                f"Direction: {direction}\n"
                f"Final heading: {final_facing:.2f}°\n\n"
                f"Charge zone: {zone}\n"
                f"Velocity: {velocity} (m/s)\n"
                f"Pitch: {low_angle:.2f}°\n"
                f"Time to target: {time_to_target:.2f}s\n\n"
                f"ALT Charge zone: {alt_zone}\n"
                f"ALT Velocity: {alt_velocity} (m/s)\n"
                f"ALT Pitch: {high_angle:.2f}°\n"
                f"ALT Time to target: {alt_time_to_target:.2f}s\n"
            )

            #--- DELETE & INSERT ---#
            self.result_text.delete(1.0, tk.END) 
            self.result_text.insert(tk.END, result)

            #--- CALL generate_map() ---'
            self.generate_map(howitzer_x, howitzer_y, target_x, target_y)

        except ValueError:
            print("Invalid input. Please enter numerical values.")

    #--- GENERATE MAP ---#
    def generate_map(self, howitzer_x, howitzer_y, target_x, target_y):
        
        def convert_to_degrees(x_m, y_m):
            lat_deg = y_m / 111000  
            lon_deg = x_m / 111000  
            return lat_deg, lon_deg

        #--- X & Y TO DEGREES ---#
        howitzer_latlon = convert_to_degrees(howitzer_x, howitzer_y)
        target_latlon = convert_to_degrees(target_x, target_y)

        #--- DEFINE CENTER ---#
        center_lat = howitzer_latlon[0]
        center_lon = howitzer_latlon[1]

        #--- RELATIVE COORD ---#
        relative_lat = target_latlon[0] - center_lat
        relative_lon = target_latlon[1] - center_lon

        #--- DEFINE EXTENT ---#
        extent_km = 40  
        lat_range = extent_km / 111  
        lon_range = extent_km / 111  

        #--- FIGURE & AXIS ---#
        fig = plt.figure(figsize=(7, 7))
        ax = plt.axes(projection=ccrs.PlateCarree())

        #--- PLOT POINTS ---#
        ax.plot(0, 0, marker='o', color='red', markersize=10, label=f"M777 ({howitzer_x}, {howitzer_y})")
        ax.plot(relative_lon, relative_lat, marker='o', color='blue', markersize=10, label=f"Target ({target_x}, {target_y})")

        #--- DRAW LINE ---#
        ax.plot([0, relative_lon], [0, relative_lat], color='black', linewidth=2)

        #--- SET POV TO SUBJECT ---#
        ax.set_extent([center_lon - lon_range / 2, center_lon + lon_range / 2, 
                    center_lat - lat_range / 2, center_lat + lat_range / 2], crs=ccrs.PlateCarree())

        #--- GRIDLINES ---#
        grid_interval_km = 1 
        grid_interval_deg = grid_interval_km / 111  
        lat_ticks = np.arange(center_lat - lat_range / 2, center_lat + lat_range / 2 + grid_interval_deg, grid_interval_deg)
        lon_ticks = np.arange(center_lon - lon_range / 2, center_lon + lon_range / 2 + grid_interval_deg, grid_interval_deg)
        ax.set_xticks(lon_ticks, minor=True)
        ax.set_yticks(lat_ticks, minor=True)

        #--- MAJOR GRIDLINES ---'
        major_grid_interval_km = 5 
        major_grid_interval_deg = major_grid_interval_km / 111 
        major_lat_ticks = np.arange(center_lat - lat_range / 2, center_lat + lat_range / 2 + major_grid_interval_deg, major_grid_interval_deg)
        major_lon_ticks = np.arange(center_lon - lon_range / 2, center_lon + lon_range / 2 + major_grid_interval_deg, major_grid_interval_deg)
        ax.set_xticks(major_lon_ticks, minor=False)
        ax.set_yticks(major_lat_ticks, minor=False)

        #--- LABELS ---#
        def format_labels(x, pos):
            return f'{x * 111:.0f} km'
        
        def format_lat_labels(y, pos):
            return f'{y * 111:.0f} km'

        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_labels))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(format_lat_labels))

        #--- TITLE & LEGEND ---#
        plt.title("Map of M777 and Target Locations")
        plt.grid()
        plt.legend()

        #--- POSITION OF WINDOW ---#
        manager = plt.get_current_fig_manager()
        screen_width = manager.window.winfo_screenwidth()
        screen_height = manager.window.winfo_screenheight()
        fig_width, fig_height = fig.get_size_inches() * fig.dpi
        x_position = (screen_width - fig_width) // 2 + 100
        y_position = (screen_height - fig_height) // 2

        manager.window.geometry(f'{int(fig_width)}x{int(fig_height)}+{int(x_position)}+{int(y_position)}')
        plt.show()

    #--- CONFIRM CLEAR ---#
    def confirm_clear(self):
        response = messagebox.askyesno("Clear Inputs", "Are you sure you want to clear all inputs?")
        if response:
            self.clear_inputs()

    #--- CLEAR INPUTS ---#
    def clear_inputs(self):
        self.howitzer_x_entry.delete(0, tk.END)
        self.howitzer_y_entry.delete(0, tk.END)
        self.howitzer_z_entry.delete(0, tk.END)
        self.target_x_entry.delete(0, tk.END)
        self.target_y_entry.delete(0, tk.END)
        self.target_z_entry.delete(0, tk.END)

        self.result_text_1.delete(1.0, tk.END)

    #--- DISTANCE ERROR ---#
    def distance_error(self):
        response = messagebox.askyesno("Distance Error", "Distance exceeds maximum range.\nDo you want to input new data?")
        if response:
            self.clear_inputs()
        else:
            exit()

root = tk.Tk()
app = M777A2PSSApp(root)
root.mainloop()
