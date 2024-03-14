from netmiko import ConnectHandler
from .nas_inventory import get_host

class NetworkDevice:
    """
    Represents a network device.

    Attributes:
        hostname (str): The hostname of the network device.
        net_connect: The Netmiko connection object for the device.
    """
    def __init__(self, hostname):
        self.hostname = hostname
        self.net_connect = self.get_netmiko_connection()

    def get_netmiko_connection(self):
        """
        Establishes a Netmiko connection to a network device.

        Returns:
            net_connect (Netmiko SSH connection): The Netmiko SSH connection object.

        Raises:
            Exception: If there is an error establishing the connection.

        """
        host = get_host(hostname=self.hostname)
        device_params = {
            "host": host["ip"],
            "username": host["user"],
            "password": host["password"],
            "secret": host["password"],
            "device_type": "vyos" if host["vendor"] == "VyOS" else "juniper" if host["vendor"] == "Juniper" else "cisco_ios"
        }
        try:
            net_connect = ConnectHandler(**device_params)
            return net_connect
        except Exception as e:
            print(f'Error: {e}')
            return None

    def send_command(self, command:str):
        """
        Sends a command to the network controller and returns the output.

        Args:
            command (str): The command to be sent to the network controller.

        Returns:
            str: The output of the command execution.

        Raises:
            Exception: If an error occurs while sending the command.

        """
        try:
            output = self.net_connect.send_command(command)
            return output
        except Exception as e:
            print(f'Error: {e}')
        return None

    def get_backup(self):
        """
        Retrieves the backup configuration from the network device.

        Returns:
            str: The backup configuration if successful, otherwise an error message.

        Raises:
            Exception: If there is an error sending the command or connecting to the device.
        """
        if self.net_connect:
            try:
                if self.net_connect.device_type == "vyos":
                    output = self.send_command("show configuration")
                else:
                    self.net_connect.enable()
                    output = self.send_command("show running-config")
                if output:
                    return output
                return "Error retrieving backup"
            except Exception as e:
                return f"Error sending command: {e}"
            finally:
                self.net_connect.disconnect()
        else:
            return "Error connecting to the device"

    def get_version(self):
        """
        Retrieves the version information of the network device.

        Returns:
            str: The version information of the network device.
        
        Raises:
            str: If there is an error retrieving the version information or connecting to the device.
        """
        if self.net_connect:
            try:
                if self.net_connect.device_type == "vyos":
                    output = self.send_command("show version")
                else:
                    self.net_connect.enable()
                    output = self.send_command("show version")
                if output:
                    return output
                return "Error retrieving version"
            except Exception as e:
                return f"Error sending command: {e}"
            finally:
                self.net_connect.disconnect()
        else:
            return "Error connecting to the device"

    def configure_device(self, config: str) -> str:
        """
        Configures the device with the provided configuration.

        Args:
            config (str): The configuration to be sent to the device.

        Returns:
            str: The output of the configuration command if successful, otherwise an error message.

        Raises:
            Exception: If there is an error sending the configuration.

        """
        if self.net_connect:
            try:
                output = self.net_connect.send_config_set(config)
                if output:
                    return output
                return "Error sending configuration"
            except Exception as e:
                return f"Error sending configuration: {e}"
            finally:
                self.net_connect.disconnect()
        else:
            return "Error connecting to the device"
