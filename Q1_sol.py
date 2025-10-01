import csv                                                                     #function to read the csv file: 

class _voltage_to_torque_:
    def __init__(self, file):
        self.data = self._read_file(file)  # Try to read calibration file

    # function to read the csv file
    def _read_file(self, file):
        with open(file, newline="") as f:
            csv_read = csv.reader(f)                                            # read csv filename
            next(csv_read)                                                      # skip header line
            data = [(float(row[1]), float(row[0])) for row in csv_read if row]  # parse voltage and torque as (v,t) tuples
        return sorted(data)                                                     # sort data based on V levels and return (if calibrated is not in order)

    # function to find indices of calibration Voltages - using Binary Search
    def _bin_search_data(self, volt):
        l = 0
        r = len(self.data) - 1                                          # lower and upper limits
        
        while l <= r:
            m = (l + r) // 2                                                  # midpoint voltage
            
            if self.data[m][0] == volt:
                return m, m                                                   # exact match
            elif self.data[m][0] < volt:
                l = m + 1                                                     # search right half
            else:
                r = m - 1                                                     # search left half

        return r, l                                                           # return bracketing indices if no exact match

    # function to convert V to torque based on parsed csv data
    def _vt_convert(self, volt):
        if volt < self.data[0][0] or volt > self.data[-1][0]:                 # check voltage range if within -10 and 10
            raise ValueError("Voltage outside calibration range")
        i1, i2 = self._bin_search_data(volt)                                     # find bracketing indices
        if i1 == i2:                                                          # exact match
            return self.data[i1][1]
        v1, t1 = self.data[i1]                                                # interpolate between two points
        v2, t2 = self.data[i2]
        return t1 + (t2 - t1) * (volt - v1) / (v2 - v1)                       # linear interpolation


# main fn
if __name__ == "__main__":
    filename = input("Enter Calibration File: ")                              # user input - filename
    try:
        converter = _voltage_to_torque_(filename)                             # create converter instance
    except FileNotFoundError:
        print(f"{filename} Entered Is Missing")                               # print error and exit
        exit(1)

    # User Input Voltage List
    for v_str in input("Enter test voltages (no units, space-separated): ").split():  # iterate through each input value
        print("______________________________________________________________")
        try:
            v = float(v_str)                                                          # convert to float
            print(f"VOLTAGE: {v}V   →  TORQUE = {converter._vt_convert(v):.3f}")  #print result
        except ValueError:
            print(f"!Voltage {v_str}V     ->   Voltage Out of Caliberation Range")                        # For invalid inputs or out-of-range
