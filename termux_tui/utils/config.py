import json
import os

def get_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if not os.path.exists(config_path):
        # Create a default config if it doesn't exist
        default_config = {
            "theme": {
                "primary_color": "cyan",
                "secondary_color": "magenta",
                "background_color": "black",
                "text_color": "white"
            }
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        with open(config_path, 'r') as f:
            return json.load(f)

