#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests

async def get_events():
    logger.info("[事件信息接收] 请求获取安全事件信息")

    url = "https://api.intelligent_detection.com/api/events/get"
    r = requests.get(url=url)
    if r.status == 200:
        data = r.json()
        return {"status": 0, "message": data["message"]}    # 直接返回解析后的JSON，假设它符合预期格式
    else
        return {"status": 2, "message": "请求失败"}
