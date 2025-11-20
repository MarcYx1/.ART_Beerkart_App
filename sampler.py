import serial
import serial.tools.list_ports
import time
from datetime import datetime

class Sampler:
    """Class to manage the sampler device connection and operations."""

    def __init__(self, port=None, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def connect(self, port):
        """Establish a serial connection to the sampler device."""
        if port is None:
            raise ValueError("Port must be specified to connect.")
        self.serial_connection = serial.Serial(port, self.baudrate, timeout=self.timeout)

    def disconnect(self):
        """Close the serial connection to the sampler device."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None

    def is_connected(self):
        """Check if the sampler device is connected."""
        return self.serial_connection is not None and self.serial_connection.is_open
    
    def list_available_ports(self):
        """List all available serial ports."""
        return [port.device for port in serial.tools.list_ports.comports()]
    
    def write_file(self):
        """Read data from the sampler device and write to a timestamped file."""
        time_rn = datetime.now().strftime("%Y%m%d_%H%M%S")
        start_time = time.time()
        if not self.is_connected():
            raise ConnectionError("Sampler device is not connected.")
        
        try:
            while self.is_connected():
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('utf-8').strip()
                    if data:
                        # Validate format eg.:string(id)=number;string(id)=number~suffix
                        parts = data.split(';')
                        try:
                            for i in parts:
                                subparts = i.split('=')
                                with open(f'./live_graphs/{subparts[0]}_{time_rn}.txt', 'a') as file: # pl.: voltage_20230601_153045.txt
                                    file.write(f'{round(time.time() - start_time, 3)},{subparts[1]}' + "\n")
                                    file.flush()
                        except ValueError:
                            pass
        except Exception as e:
            print(f"[Sampler] Error writing to file: {e}")
    
    def send_data(self,type, data):
        """Send data to the sampler device."""
        if not self.is_connected():
            raise ConnectionError("Sampler device is not connected.")
        self.serial_connection.write(f'{type}={data}\n'.encode('utf-8'))