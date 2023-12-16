import u3

import u3

# Create a U3 object which will automatically try to open the first found U3
# via USB or Ethernet
device = u3.U3()

# To open a U3 via Ethernet, use:
# device = u3.U3(ethernet=True, ipAddress="192.168.1.209")

# To open a specific U3 via USB, use its serial number:
# device = u3.U3(serialNumber=123456789)

# Configuring the device. The U3 requires DAC1 to be disabled
# in order to read from more than 4 analog inputs.
device.configU3()

# Reading from an analog input (e.g., AIN0)
# Replace '0' with the appropriate channel number
ainValue = device.getAIN(0)

print(f"Voltage on AIN0: {ainValue} V")

# Close the device
device.close()

