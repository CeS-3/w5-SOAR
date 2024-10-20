#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests

async def send_event(event_info):
    logger.info("[事件信息传递] 发送事件参数: {}", event_info)

    url = "https://api.yourservice.com/api/events/send"
    try:
        r = requests.post(url=url, json=event_info)
        r.raise_for_status()
    except Exception as e:
        logger.error("[事件信息传递] 请求API失败: {}", e)
        return {"status": 2, "message": "请求事件信息传递API失败"}

    response_data = r.json()
    if response_data["status"] == "success":
        return {"status": 0, "message": response_data["message"]}
    else:
        return {"status": 2, "message": "事件信息发送失败"}

async def get_response_suggestions(event_id):
    logger.info("[响应策略建议] 查询事件ID: {}", event_id)

    url = f"https://api.yourservice.com/api/decision/response_suggestions?event_id={event_id}"
    try:
        r = requests.get(url=url)
        r.raise_for_status()
    except Exception as e:
        logger.error("[响应策略建议] 请求API失败: {}", e)
        return {"status": 2, "message": "请求响应策略建议API失败"}

    response_data = r.json()
    if response_data["status"] == "success":
        return {"status": 0, "suggestions": response_data["suggestions"]}
    else:
        return {"status": 2, "message": "获取响应策略建议失败"}


async def update_event_status(event_id, new_status):
    logger.info("[事件状态更新] 更新事件ID: {}, 新状态: {}", event_id, new_status)

    url = "https://api.yourservice.com/api/events/update_status"
    body = {
        "event_id": event_id,
        "new_status": new_status
    }
    try:
        r = requests.post(url=url, json=body)
        r.raise_for_status()
    except Exception as e:
        logger.error("[事件状态更新] 请求API失败: {}", e)
        return {"status": 2, "message": "请求事件状态更新API失败"}

    response_data = r.json()
    if response_data["status"] == "success":
        return {"status": 0, "message": response_data["message"]}
    else:
        return {"status": 2, "message": "更新事件状态失败"}




# if __name__ == '__main__':
#     # 导入异步库
#     import asyncio


#     # 测试函数
#     async def test():
#         result = await send_event()
#         print(result)


#     # 加入异步队列
#     async def main(): await asyncio.gather(test())


    # 启动执行
    # asyncio.run(main())