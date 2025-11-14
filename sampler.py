import serial
import serial.tools.list_ports

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
    
    def write_file(self, data):
        if not self.is_connected():
            raise ConnectionError("Sampler device is not connected.")
        
        try:
            with open("graph_data.txt", "a") as file:
                while self.is_connected():
                    if self.serial_connection.in_waiting > 0:
                        data = self.serial_connection.readline().decode('utf-8').strip()
                        if data:
                            # Validate format: number,number
                            parts = data.split(',')
                            if len(parts) == 2:
                                try:
                                    float(parts[0])
                                    float(parts[1])
                                    file.write(data + "\n")
                                    file.flush()
                                except ValueError:
                                    pass
        except Exception as e:
            print(f"Error writing to file: {e}")