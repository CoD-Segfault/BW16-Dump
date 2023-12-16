import serial
import serial.tools.list_ports
import struct

# Define a function to swap the endianness of a number
def swap_endianness(byte_array):
    # Convert the bytearray to a bytes object
     
    byte_obj = bytes(byte_array)
    # Unpack the bytes object as a 32-bit integer in big-endian byte order
    num = struct.unpack(">I", byte_obj)[0]
    # Pack the number as a 32-bit integer in little-endian byte order
    swapped_bytes = struct.pack("<I", num)
    # Convert the bytes object back to a bytearray
    swapped_byte_array = bytearray(swapped_bytes)
    # Return the swapped bytearray
    return swapped_byte_array

ports = serial.tools.list_ports.comports()

print("Serial devices detected:")

for p in ports:
    print(p.device)

#serial_device = input('\nWhich port to use?\n')

serial_device = "COM4"

print(f'\nUsing {serial_device}.')

serial_conn = serial.Serial(port=serial_device, baudrate=115200, timeout=1)

#serial_conn.write(b'FLASH read 0 32\r\n')
serial_conn.write(b'FLASH read 0 524288\r\n')

data = serial_conn.readlines()

binary = bytearray()

for line in data:
    hex_data = line.decode()[11:].strip().split()
    if len(hex_data) == 4:
        for hex in hex_data:
            byte = bytearray.fromhex(hex)
            binary.extend(swap_endianness(byte))

with open("firmware.bin", "wb") as binary_file:
    binary_file.write(binary)
