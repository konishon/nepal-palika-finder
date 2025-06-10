import yaml
from pathlib import Path

def load_config():
    """
    Loads the application configuration from config.yml in the project root.
    """
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config
