import json
import os
from ..logger import LoggingManager

logger = LoggingManager("Evoker.Config")

class ConfigManager:
    def __init__(self, path: str, template: dict | None = None, max_retries: int = 3):
        """
        Initialize a Config object.

        Args:
            path (str): The path to the configuration file.
            template (dict | None): The template for the configuration file.

        Returns:
            None
        """
        self.fault_retry_treshold = max_retries
        self.fault_retry_count = 0

        self.path = path

        self.data = template
        self.load()

    def load(self):
        """
        Load the configuration data from the file.

        If the file does not exist, it will be created.

        Returns:
            None
        """
        if not os.path.exists(self.path):
            with open(self.path, "x") as file: file.write("{}")
        
        try:
            with open(self.path, 'r', encoding="utf-8") as file:
                data = json.loads(file.read())
                for key, value in data.items():
                    self.data[key] = value
                    
            self.save()

        except Exception as e:
            self.fault_retry_count += 1

            if self.fault_retry_count >= self.fault_retry_treshold:
                logger.error(f"Unable to load configuration file, automatic overwrite aborted (max retries exceeded)")
                self.save()
                return

            logger.warning(f"Unable to load configuration file, attempting automatic overwrite ({self.fault_retry_count}/{self.fault_retry_treshold})")

            self.load()
    
    def get(self, key: str, default=None):
        """
        Get a configuration value.

        Args:
            key (str): The key of the configuration value.
            default: The default value to return if the key does not exist.

        Returns:
            The value associated with the key, or the default value if the key does not exist.
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value):
        """
        Set a configuration value.

        Args:
            key (str): The key of the configuration value.
            value: The value to be set.

        Returns:
            None
        """
        self.data[key] = value
        self.save()

    def delete(self, key: str):
        """
        Delete a configuration value.

        Args:
            key (str): The key of the configuration value to be deleted.

        Returns:
            None
        """
        if key in self.data:
            del self.data[key]
            self.save()

    def save(self):
        """
        Save the configuration data to the file.

        Returns:
            None
        """
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent=4)