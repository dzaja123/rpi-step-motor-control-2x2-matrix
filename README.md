# Raspberry Pi Step Motor Control 2x2 Image Matrix

## Overview
This project is designed for the Raspberry Pi 5 and controls two Nema 23 stepper motors using TB660 drivers.
The motors operate a two-axis platform that holds a camera, allowing it to move to four designated positions to capture images.
The captured images are then used to create a 2x2 picture matrix for AI software that detects damage on industrial leather.

## Features
- Control of two Nema 23 stepper motors for precise movement.
- Automated camera positioning to take four images.
  
## Hardware Requirements
- Raspberry Pi 5
- 2 x Nema 23 Stepper Motors
- 2 x TB660 Motor Drivers
- 4 x PNP sensors for min and max positions
- Power supply for motors and Raspberry Pi

## Software Requirements
- Python 3.x

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dzaja123/rpi-step-motor-control-2x2-matrix.git
   cd rpi-step-motor-control-2x2-matrix
   ```

## Usage
1. Connect the hardware components as per the wiring diagram.
2. Run the control script:
   ```bash
   python control.py
   ```
3. Follow the on-screen instructions to capture images.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to the contributors and the community for their support.
