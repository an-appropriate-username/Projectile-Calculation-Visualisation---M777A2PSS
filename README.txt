# M777 A2 Projectile Simulation Software

A physics-inspired simulator for calculating projectile parameters for the M777 A2 howitzer using a 155mm shell.

## Table of Contents
- [Overview](#overview)
- [Core Calculations](#core-calculations)
- [Component Architecture](#component-architecture)
- [Parameter Configuration](#parameter-configuration)
- [Output Metrics](#output-metrics)
- [Installation and Usage](#installation-and-usage)

## Overview

The M777 A2 Projectile Simulation Software takes coordinates (in meters) for both the howitzer and a target, and calculates key data including:
- Distance to target
- Required rotation
- Pitch angle
- Recommended charge zone
- High and low launch angle solutions

It also generates a top-down map showing the orientation of the howitzer relative to the target.

## Core Calculations

### 1. **Distance Calculation**
- Computes Euclidean distance between howitzer and target.
- Displays both meters and kilometers.

### 2. **Rotation and Heading**
- Calculates required rotation from a reference heading.
- Outputs direction (left/right) and final heading.

### 3. **Charge Zone and Velocity**
- Suggests a charge zone based on distance.
- Determines corresponding muzzle velocity.

### 4. **Launch Angles**
- Computes low and high angle solutions.
- Provides pitch angles and estimated time-to-target.

## Component Architecture

| Component        | Key Functions | Parameters |
|------------------|---------------|------------|
| **Location3D**   | Represents a 3D coordinate | `x`, `y`, `z` |
| **Distance Calc**| Computes howitzer-to-target distance | `meters`, `kilometers` |
| **Rotation Calc**| Calculates heading and direction | `rotation_needed`, `direction`, `final_heading` |
| **Charge Zone**  | Maps distance to velocity and zone | `zone`, `velocity` |
| **Launch Angles**| Computes pitch angles and alt solutions | `low_angle`, `high_angle` |
| **Map Gen**      | Generates a simple top-down map | `matplotlib`, `cartopy` |

## Parameter Configuration

### Input Coordinates
- HOWITZER X, Y, Z (meters)
- TARGET X, Y, Z (meters)

### Charge Zones
- Zone determined by distance bands
- Velocity assigned accordingly

### Map Settings
- Top-down projection
- ~40 km extent
- Gridlines for spatial reference

## Output Metrics

### Terminal / GUI Output
- Distance (meters & km)
- Rotation, direction, heading
- Charge zone & velocity
- Pitch (low and high)
- Time to target

### Graphical Output
- Top-down map of howitzer and target positions
- Line indicating trajectory vector
- Gridlines with km markers

## Installation and Usage

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd M777-A2-PSS
   ```

2. Install requirements:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python M777A2PSS.py
   ```

4. Enter coordinates for howitzer and target in the GUI.

5. View calculated outputs in the GUI text area.

6. Generate a map for visualization.

---

⚠️ **Note**: This project is intended for simulation and educational purposes only.

