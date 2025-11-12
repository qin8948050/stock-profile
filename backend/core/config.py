import yaml
from pathlib import Path
from pydantic import BaseModel
import os

class AppInfo(BaseModel):
    name: str
    version: str
    port: int

class ServerConfig(BaseModel):
    host: str
    log_level: str
    reload: bool

class ApiConfig(BaseModel):
    prefix: str

class LoggingConfig(BaseModel):
    level: str
    file: str

class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str

class OpenTelemetryConfig(BaseModel):
    deployment_environment: str
    otlp_endpoint: str

class AppConfig(BaseModel):
    app: AppInfo
    server: ServerConfig
    api: ApiConfig
    logging: LoggingConfig
    database: DatabaseConfig
    opentelemetry: OpenTelemetryConfig

def merge_configs(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            base[key] = merge_configs(base[key], value)
        else:
            base[key] = value
    return base

def load_config() -> AppConfig:
    env = os.getenv("APP_ENV", "development")
    config_dir = Path(__file__).parent.parent / "config"
    
    with open(config_dir / "default.yaml", "r") as f:
        config_data = yaml.safe_load(f)

    env_config_path = config_dir / f"{env}.yaml"
    if env_config_path.exists():
        with open(env_config_path, "r") as f:
            env_config_data = yaml.safe_load(f)
        config_data = merge_configs(config_data, env_config_data)

    return AppConfig(**config_data)

config = load_config()
