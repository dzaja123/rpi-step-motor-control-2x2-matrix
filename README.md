# Raspberry Pi Stepper Motor Control 2x2 Image Matrix

## Overview
This project controls two Nema 23 stepper motors via TB660 motor drivers using a Raspberry Pi 5.
The motors maneuver a two-axis platform equipped with a camera.
The platform captures images from four specific positions, returning the images through a RESTful API.

## Features
- Precise motor control for a 2x2 movement matrix.
- Camera integration for capturing high-resolution images.
- RESTful API endpoints for triggering motor movements and image capture.

## Hardware Requirements
- **Raspberry Pi 5**
- **2 x Nema 23 Stepper Motors**
- **2 x TB660 Motor Drivers**
- **4 x PNP Sensors** (Min/Max detection) in this project are NJK-5002C sensors.
- **Power Supply** for motors (9-42VDC) and sensors (5-30VDC).
- **Camera** (USB or compatible with Raspberry Pi).

## Wiring Diagram

### Motor for X-Axis
- **Direction Control (DIR)**:
  - **DIR+** → GPIO 5 (X_DIR)
  - **DIR-** → Ground
- **Step Control (STEP)**:
  - **PUL+** → GPIO 6 (X_STEP)
  - **PUL-** → Ground
- **Coils**:
  - **Coil 1** → A+ / A-
  - **Coil 2** → B+ / B-

### Motor for Y-Axis
- **Direction Control (DIR)**:
  - **DIR+** → GPIO 13 (Y_DIR)
  - **DIR-** → Ground
- **Step Control (STEP)**:
  - **PUL+** → GPIO 19 (Y_STEP)
  - **PUL-** → Ground
- **Coils**:
  - **Coil 1** → A+ / A-
  - **Coil 2** → B+ / B-

- **Sensors**:
  - X-Min → GPIO 17
  - X-Max → GPIO 27
  - Y-Min → GPIO 22
  - Y-Max → GPIO 4

### Notes
   - The sensors used in this project are NPN sensors and are triggered when the motor reaches the end of its movement.
   - The VCC and GND pins for the sensors are connected directly to the 3.3V and GND pins on the Raspberry Pi.
      - Note: This approach is not recommended for production-grade systems, but it is sufficient for this Minimum Viable Product (MVP) implementation.

## Software Requirements
1. Python 3.x
2. Required libraries:
   - `Flask`
   - `Flask-CORS`
   - `opencv-python`
   - `RPi.GPIO`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dzaja123/rpi-step-motor-control-2x2-matrix.git
   cd rpi-step-motor-control-2x2-matrix
   ```

2. Install dependencies:
   ```bash
   pip install Flask Flask-CORS opencv-python RPi.GPIO
   ```

3. Connect all hardware components as per the wiring diagram.

4. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints

### 1. Move Motors
- **Endpoint**: `/api/move_motors`
- **Method**: `GET`
- **Description**: Triggers motor movement through all four positions without capturing images.
- **Response**:
  ```json
  {
      "status": "success",
      "message": "Motors moved to all positions."
  }
  ```

### 2. Movement Sequence with Images
- **Endpoint**: `/api/movement_sequence_images`
- **Method**: `GET`
- **Description**: Moves motors and captures an image at each position, returning the images encoded in Base64.
- **Response**:
  ```json
  {
      "status": "success",
      "images": [
          {"image_1": "<Base64 Image Data>"},
          {"image_2": "<Base64 Image Data>"},
          {"image_3": "<Base64 Image Data>"},
          {"image_4": "<Base64 Image Data>"}
      ]
  }
  ```

## Usage Instructions
1. Power on the Raspberry Pi and connect all hardware components.
2. Run the script:
   ```bash
   python main.py
   ```
3. Use a REST client or browser to access the API:
   - Trigger motor movement:
     ```
     http://localhost:5000/api/move_motors
     ```
   - Trigger movement with image capture:
     ```
     http://localhost:5000/api/movement_sequence_images
     ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
