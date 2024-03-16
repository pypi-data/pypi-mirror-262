# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:51:44 2023

@author: Matt Jamieson
"""

class PM5:
    """ A class that wraps the pyvisa object and allows for automatic power readings and
    range changes. The "powermeter" object contains the original pyvisa object that is used for
    communication. The read_power function basically sends a write/read command and interprets the returned information.
    """
    def __init__(self):
        import pyvisa 
        self.rm = pyvisa.ResourceManager()
        self.powermeter = None
        self.range_setting = None
        self.cal_factor = None
        self.auto_range = None
        self.ranges = ["200uW", "2mW", "20mW", "200mW","200uW auto", "2mW auto", "20mW auto", "200mW auto"]
        self.range_hold_string = ["Off", "On"]
        self.auto_range_string = ["In auto range", "Not in auto range"]
        return
        
    def connect(self, COMport):
        """Connect device using COM port
        Args:
            COMport (str): string containing COM port as listed by rm.list_resources(), e.g ASRL16::INSTR
        """
        try:
            self.powermeter = self.rm.open_resource(COMport)
            print(f"Powermeter successfully connected: {self.powermeter.query('*IDN?')[:-1]}")
        except Exception as e:
            print(f"Connection failed: {e}")
        return

    def close(self):
        self.powermeter.close()
        print("Powermeter successfully closed")
        return

    def write(self, x):
        """ Allows access to native pyvisa object write function
        """
        self.powermeter.write(x)
        return

    def read(self, num_of_bytes):
        """ Allows access to native pyvisa object read_bytes function
        Args:
            num_of_bytes (int): number of bytes to be read by function
        """
        data = self.powermeter.read_bytes(num_of_bytes)
        return data

    def read_power(self):
        """ Returns the a single reading in units of watts, and updates
        range_setting and cal_factor properties. Note that currently the conversion assumes a positive reading, as
        it uses unsigned integers
        """
        ACK = 0x06  # acknowledged
        NAK = 0x015  # not acknowledged
        self.powermeter.write("?D10000\r")
        data_string = self.powermeter.read_bytes(7)
        parse_check_byte = data_string[0]
        identifier_byte = data_string[1]
        LSB_byte = data_string[2]
        MSB_byte = data_string[3]
        status_byte_1 = data_string[4]
        status_byte_2 = data_string[5]
        status_byte_3 = data_string[6]

        if parse_check_byte != ACK:
            print("Write request parsed incorrectly")

        attempts = 0
        while identifier_byte != 68 and attempts < 3:
            print("Read request failed, clearing buffer")
            try:
                self.powermeter.read_bytes(100)
            except Exception as e:
                print("Buffer cleared")
                self.powermeter.write("?D10000\r")
                data_string = self.powermeter.read_bytes(7)
                parse_check_byte = data_string[0]
                identifier_byte = data_string[1]
                LSB_byte = data_string[2]
                MSB_byte = data_string[3]
                status_byte_1 = data_string[4]
                status_byte_2 = data_string[5]
                status_byte_3 = data_string[6]
                attempts += 1  # times out if

        if attempts > 3:
            print("Maximum number of attempted data reads reached. Read failed: exiting function")
            return None

        status_byte_3_in_bits = format(status_byte_3, '#010b')[2:]
        range_binary = status_byte_3_in_bits[:3]
        if range_binary == '000':
            range_setting = 0
        elif range_binary == '001':
            range_setting = 200e-6
            range_index = 1
        elif range_binary == '010':
            range_setting = 2e-3
            range_index = 2
        elif range_binary == '011':
            range_setting = 20e-3
            range_index = 3
        else:
            range_setting = 200e-3
            range_index = 4
        #print(f"range binary = {range_binary}")
        # print(f"range setting = {range_setting}")
        self.range_setting = self.ranges[range_index-1]
        cal_factor_bits = format(status_byte_2, '#010b')[2:]
        cal_factor_ones = int(cal_factor_bits[0:4], base=2)
        cal_factor_decimals = int(cal_factor_bits[4:8], base=2)
        cal_factor_tens = int(status_byte_3_in_bits[4:8], base=2)
        if status_byte_3_in_bits[3] == 1:
            cal_factor_sign = -1
        else:
            cal_factor_sign = 1
        cal_factor = cal_factor_sign * 10 * cal_factor_tens + cal_factor_ones + 0.1 * cal_factor_decimals
        self.cal_factor = cal_factor
        # print(f"cal factor:{cal_factor}")
        
        auto_range = format(status_byte_1, '#010b')[2:][0]
        if auto_range == 1:
            self.auto_range = "In auto range"
        else:
            self.auto_range = "Not in auto range"
        
        count_value = LSB_byte + MSB_byte * 256
        reading = count_value * 2.0 * range_setting / 59576

        if cal_factor != 0:
            reading = reading * 10 ** (cal_factor / 10)

        return reading
    
    def set_zero(self):
        """ Remotely zeros the powermeter
        """
        self.powermeter.write("!SZ0000\r")
        print("Power meter zeroed")
        return
    
    def set_range(self,range_index,range_hold = 1):
        """ Manually set the reading range, whilst the front panel is set to "Remote".
        Args:
            range_index (int) : index corresponding to the chosen power meter range
                1 : 200 microW
                2 : 2 mW
                3 : 20 mW
                4 : 200 mW
                5 : 200 uW auto
                6 : 2 mW auto
                7 : 20 mW auto
                8 : 200 mW auto
            range_hold (int): variable to choose whether to activate range hold mode, i.e to stop it
                automatically changing.
                0 : Range hold off
                1 : Range hold on
        """
        #ranges = ["200uW", "2mW", "20mW", "200mW","200uW auto", "2mW auto", "20mW auto", "200mW auto"]
        write_string = "!R" + str(range_index) + str(range_hold) + "000\r"
        self.powermeter.write(write_string)
        self.range_setting = self.ranges[range_index]
        self.auto_range = self.auto_range_string[range_hold]
        print(f"Range set to {self.ranges[range_index-1]}, Range Hold = {self.range_hold_string[range_hold]}")
        return