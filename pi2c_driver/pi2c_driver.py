#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2024 University of Leeds
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import smbus2
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8

# Default on RPi is /dev/i2c-1
I2C_BUS = 1
# I2C address of the device.
I2C_ADDRESS = 0x42
# Maximum value to be written to the I2C device.
MAX_VALUE = 15


class I2CDriver(Node):
    def __init__(self):
        # Set up node.
        super().__init__("pi2c")
        # Set up subscriber
        self.imu_calibrate_server = self.create_subscription(
            UInt8, "pi2c", self.callback_send_i2c_message, 10
        )
        self.get_logger().info("PI2C started...")

    def callback_send_i2c_message(self, value: UInt8):
        if value.data > MAX_VALUE:
            self.get_logger().warn(
                "Value %d exceeds maximum value of %d. Ignoring...",
                value.data,
            )
        else:
            try:
                with smbus2.SMBus(I2C_BUS) as bus:
                    bus.write_byte(I2C_ADDRESS, value.data)
            except Exception as e:
                error_string = "Failed to write value {} to I2C device: {}".format(
                    value.data, str(e)
                )
                self.get_logger().error(error_string)


def main(args=None):
    rclpy.init(args=args)
    node = I2CDriver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main__":
    main()
