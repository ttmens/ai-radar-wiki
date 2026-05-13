#!/usr/bin/env python3
"""
AI Radar 统一配置模块

所有飞书相关凭证必须通过环境变量提供。
缺失任何必需配置时，立即报错退出——绝不在代码中保留默认值。

使用方式：
    from config import require_env
    app_id = require_env("FEISHU_APP_ID")
    app_secret = require_env("FEISHU_APP_SECRET")

    或直接使用预置的配置对象：
    from config import FEISHU_CONFIG
    app_id = FEISHU_CONFIG.app_id
"""

import os
import sys


class ConfigError(Exception):
    """配置缺失或无效时抛出"""
    pass


def require_env(key: str) -> str:
    """获取环境变量，缺失则报错退出"""
    value = os.environ.get(key, "").strip()
    if not value:
        raise ConfigError(
            f"缺少必需的环境变量: {key}\n"
            f"请复制 scripts/.env.example 为 .env 并填入真实值，\n"
            f"或在运行环境中设置 {key}"
        )
    return value


def get_env_optional(key: str, default: str = "") -> str:
    """获取可选环境变量，缺失返回默认值（仅限非敏感配置）"""
    return os.environ.get(key, default).strip()


class FeishuConfig:
    """飞书相关配置"""

    def __init__(self):
        self.app_id: str = require_env("FEISHU_APP_ID")
        self.app_secret: str = require_env("FEISHU_APP_SECRET")


class BitableConfig:
    """多维表格相关配置"""

    def __init__(self):
        self.app_token: str = require_env("BITABLE_APP_TOKEN")
        self.table_id: str = require_env("BITABLE_TABLE_ID")


class RadarConfig:
    """AI Radar 通用路径配置"""

    # 这些是文件系统路径，不是敏感信息
    CRON_OUTPUT_DIR = os.environ.get("CRON_OUTPUT_DIR", "/home/admin/.hermes/cron/output")
    ENV_PATH = os.environ.get("ENV_PATH", "/home/admin/.hermes/.env")
    STATE_FILE = os.environ.get("STATE_FILE", "/home/admin/.hermes/cron/bitable_sync_state.json")


# 预创建单例，方便直接导入使用
_feishu = None
_bitable = None


def get_feishu_config() -> FeishuConfig:
    global _feishu
    if _feishu is None:
        _feishu = FeishuConfig()
    return _feishu


def get_bitable_config() -> BitableConfig:
    global _bitable
    if _bitable is None:
        _bitable = BitableConfig()
    return _bitable
