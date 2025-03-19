import tomllib
from pathlib import Path

from pydantic import BaseModel


# 定义配置模型，所有字段都是字符串
class AppleMusic2FLACConfig(BaseModel):
    folder_name: str
    track_name: str
    output_folder: str

# 读取和解析配置的函数
def load_config() -> AppleMusic2FLACConfig:
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    # 构建 config.toml 的路径
    config_path = current_dir / "config.toml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open('rb') as f:
        config_data = tomllib.load(f)

    return AppleMusic2FLACConfig(**config_data)
