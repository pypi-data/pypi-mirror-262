import struct

def hex_to_float(hex_data):
    # Combine the two registers into a single 32-bit integer
    raw_data = (hex_data[0] << 16) | hex_data[1]

    # Interpret the 32-bit integer as a float
    # Convert binary string to floating point using struct
    return struct.unpack('>f', struct.pack('>I', raw_data))[0]
