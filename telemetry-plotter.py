import os
import sys
import binascii
import ctypes
import matplotlib.pyplot as plt
import numpy as np
import enum


class TELEMETRY_DATA_TYPE(enum.Enum):
    TELEMETRY_TYPE_INT = 0
    TELEMETRY_TYPE_FLOAT = 1

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

class telemetry_plotter(object):
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values
    
    def plot(self):
        label_for_plot = "test"
        plt.plot(np.asarray(self.x_values),           # X Axis
                        np.asarray(self.y_values),    # Y Axis
                        'o', label=label_for_plot,    # Circle marker and legend
                        picker=5)                     # 5 points tolerance
    
        plt.ylabel('Value', picker=True)
        plt.xlabel('Time',  picker=True)
        plt.gcf().autofmt_xdate()           # Beautify time x axis
        plt.grid(True)
        plt.title('Telemetry Plotter')
        plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)
        plt.show()


class get_telemetry(object):
    def __init__(self, file_path):

        self.x_value_list = []
        self.y_value_list = []
        
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
            self.x_value_list.append(telemetry_packet.timestamp)
            self.y_value_list.append(telemetry_packet.data.i)
        telemetry_log.close()


def main():
    file_path = sys.argv[1]
    telemetry = get_telemetry(file_path)
    plotter = telemetry_plotter(telemetry.x_value_list, telemetry.y_value_list)
    plotter.plot()


if __name__ == '__main__':
    main()
