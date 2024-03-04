import os
from dotenv import load_dotenv
import configparser

def load_config():
    # Load environment variables from .env file
    load_dotenv()

    # Get the environment from the .env file
    environment = os.getenv("PYENV", "dev")

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the environment-specific configuration file
    # config_file = '../../config/' + f'{environment.lower()}.ini'
    script_directory = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(os.path.dirname(script_directory), f'config/{environment.lower()}.ini')
    print(config_file)
    
    config.read(config_file)
    print("wow----------------")

    print(config.get('DB', 'database_url'))

    return config

def main():
    # Load the configuration for the specified environment
    config = load_config()

    # Access the variables using the get() method
    database_url = config.get('DEFAULT', 'database_url')
    api_key = config.get('DEFAULT', 'api_key')
    debug_mode = config.getboolean('DEFAULT', 'debug')

    # Example usage
    print(f"Database URL: {database_url}")
    print(f"API Key: {api_key}")
    print(f"Debug Mode: {debug_mode}")

# if __name__ == "__main__":
#     main()
