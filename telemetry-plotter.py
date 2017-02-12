import os
import sys
import binascii
import ctypes
import matplotlib.pyplot as plt
import numpy as np

class TELEMETRY_UNION(ctypes.Union):
    _fields_ = [("i", ctypes.c_int),
                ("f", ctypes.c_float)]

class TELEMETRY_SOURCE(ctypes.Structure):
    _fields_ = [("topic_id", ctypes.c_uint8),
                ("telemetry_data_type", ctypes.c_int),
                ("subsystem_id", ctypes.c_uint8)]
                
class TELEMETRY_PACKET(ctypes.Structure):
    _fields_ = [("source", TELEMETRY_SOURCE),
                ("data", TELEMETRY_UNION),
                ("timestamp", ctypes.c_uint16)] 
    def __init__(self, bytes):
        fit = min(len(bytes), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), bytes, fit)

def main():
    
    timestamp_list = []
    value_list = []
    label_for_plot = "test"

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print('Log file not found')
        return

    try:
        telemetry_log = open(file_path, "r")
    except IOError:
        print('There was an error opening the log file')
        return

    for line in iter(telemetry_log):
        packet = line.split()
        packed_data = binascii.unhexlify(packet[2])
        telemetry_packet = TELEMETRY_PACKET(packed_data)
        
        timestamp_list.append(telemetry_packet.timestamp)
        value_list.append(telemetry_packet.data.i)
        
    telemetry_log.close() 

    plt.plot(np.asarray(timestamp_list),               # X Axis
                        np.asarray(value_list),        # Y Axis
                        'o', label=label_for_plot,     # Circle marker and legend
                        picker=5)                      # 5 points tolerance
    
    plt.ylabel('Value', picker=True)
    plt.xlabel('Time',  picker=True)
    plt.gcf().autofmt_xdate()           # Beautify time x axis
    plt.grid(True)
    plt.title('Telemetry Plotter')
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)
    plt.show()

if __name__ == '__main__':
    main()
