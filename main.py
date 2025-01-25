"""
Raspberry Pi 5 Project: Controls two Nema 23 stepper motors via TB6600 drivers.
Moves a camera on a two-axis platform to capture images at specific positions.
The images are returned through a Flask API.
"""

import time
import base64
import logging
import cv2
from flask import Flask, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO


# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Flask setup
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Camera setup
CAM_RESOLUTION = [4504, 4504]
CAM_INDEX = 0

# Camera initialization
cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    logger.error("Failed to initialize the camera.")
    exit(1)

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Motor control pins
X_DIR = 5          # Direction control for X-axis motor
X_STEP = 6         # Step control for X-axis motor
Y_DIR = 13         # Direction control for Y-axis motor
Y_STEP = 19        # Step control for Y-axis motor

# Sensor pins
X_MIN_SENSOR = 17  # Sensor to detect X-axis minimum position
X_MAX_SENSOR = 27  # Sensor to detect X-axis maximum position
Y_MIN_SENSOR = 22  # Sensor to detect Y-axis minimum position
Y_MAX_SENSOR = 4   # Sensor to detect Y-axis maximum position

# Motor driver settings
STEP_DELAY = 0.0005

# Motor control pins setup
GPIO.setup(X_DIR, GPIO.OUT)
GPIO.setup(X_STEP, GPIO.OUT)
GPIO.setup(Y_DIR, GPIO.OUT)
GPIO.setup(Y_STEP, GPIO.OUT)

# Sensor pins setup
GPIO.setup(X_MIN_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(X_MAX_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Y_MIN_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Y_MAX_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def move_to_sensor(dir_pin: int, step_pin: int, target_sensor: int, direction: int) -> None:
    """
    Move an axis until the target sensor is activated.

    Args:
        dir_pin (int): GPIO pin for direction control.
        step_pin (int): GPIO pin for step control.
        target_sensor (int): GPIO pin for the target sensor.
        direction (int): GPIO.HIGH or GPIO.LOW for movement direction.
    """
    GPIO.output(dir_pin, direction)
    while GPIO.input(target_sensor):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(STEP_DELAY)


def move_to_position_1() -> None:
    """Move to Position 1 (X-min, Y-min)."""
    move_to_sensor(X_DIR, X_STEP, X_MIN_SENSOR, GPIO.LOW)
    move_to_sensor(Y_DIR, Y_STEP, Y_MIN_SENSOR, GPIO.LOW)


def move_to_position_2() -> None:
    """Move to Position 2 (X-min, Y-max)."""
    move_to_sensor(X_DIR, X_STEP, X_MIN_SENSOR, GPIO.LOW)
    move_to_sensor(Y_DIR, Y_STEP, Y_MAX_SENSOR, GPIO.HIGH)


def move_to_position_3() -> None:
    """Move to Position 3 (X-max, Y-min)."""
    move_to_sensor(X_DIR, X_STEP, X_MAX_SENSOR, GPIO.HIGH)
    move_to_sensor(Y_DIR, Y_STEP, Y_MIN_SENSOR, GPIO.LOW)


def move_to_position_4() -> None:
    """Move to Position 4 (X-max, Y-max)."""
    move_to_sensor(X_DIR, X_STEP, X_MAX_SENSOR, GPIO.HIGH)
    move_to_sensor(Y_DIR, Y_STEP, Y_MAX_SENSOR, GPIO.HIGH)


def movement_sequence() -> None:
    """Execute the movement and capture sequence for 2x2 matrix."""
    print("Starting movement sequence...")

    move_to_position_1()
    print("Position 1")

    move_to_position_2()
    print("Position 2")

    move_to_position_3()
    print("Position 3")

    move_to_position_4()
    print("Position 4")

    print("Returning to Position 1...")
    move_to_position_1()

    print("Movement completed")


# Define the movement sequence positions
positions = [
    move_to_position_1,
    move_to_position_2,
    move_to_position_3,
    move_to_position_4
]


@app.route('/api/move_motors', methods=['GET'])
def move_motors_api():
    """Trigger the movement sequence without capturing images."""
    logger.info("Executing motor movement sequence...")
    for move_function in positions:
        move_function()
    logger.info("Motor movement completed.")
    return jsonify({"status": "success", "message": "Motors moved to all positions."}), 200


@app.route('/api/movement_sequence_images', methods=['GET'])
def movement_sequence_with_images():
    """Execute the movement and capture sequence for 2x2 matrix."""
    logger.info("Starting movement and image capture sequence...")
    images = []

    for i, move_function in enumerate(positions, start=1):
        move_function()

        if not cap.isOpened():
            logger.error("Camera is not opened.")
            return jsonify({"status": "error", "message": "Camera initialization failed."}), 500

        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to capture frame at position %d.", i)
            return jsonify({"status": "error", "message": "Image capture failed."}), 500

        retval, buffer = cv2.imencode('.jpg', frame)
        if not retval:
            logger.error("Failed to encode frame at position %d.", i)
            return jsonify({"status": "error", "message": "Image encoding failed."}), 500

        img_base64 = base64.b64encode(buffer).decode('utf-8')
        images.append({f"image_number_{i}": img_base64})

    logger.info("Image capture sequence completed.")
    return jsonify({"status": "success", "images": images}), 200


def main():
    """Main function to start the Flask application."""
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        logger.info("Application terminated by user.")
    finally:
        if cap.isOpened():
            cap.release()
        GPIO.cleanup()
        logger.info("Resources cleaned up. Exiting application.")


if __name__ == "__main__":
    main()
