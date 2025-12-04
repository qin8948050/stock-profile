import re
from typing import Any, Dict, List, Union


def to_snake_case(name: str) -> str:
    """将字符串从 camelCase 转换为 snake_case。"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_keys_to_snake_case(data: Any) -> Any:
    """
    递归地将字典或字典列表中的所有键从 camelCase 转换为 snake_case。
    """
    if isinstance(data, dict):
        return {to_snake_case(k): convert_keys_to_snake_case(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_keys_to_snake_case(i) for i in data]
    return data


def format_value_to_bit(v):
    if v >= 1e8:
        return f"{v/1e8:.2f} 亿"
    elif v >= 1e4:
        return f"{v/1e4:.2f} 万"
    return str(v)