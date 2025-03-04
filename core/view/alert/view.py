#!/usr/bin/env python
# encoding:utf-8
from . import *
import requests
import json
from core.model import Alert
from datetime import datetime
# 用于从数据库中调取告警信息返回给前端
# 1. 入侵检测后的报警告警信息数据结构
# {
#   "alert_id": "UUID", 
#   "timestamp": "ISO 8601 时间格式",
#   "source_ip": "攻击来源IP",
#   "destination_ip": "受害者IP",
#   "source_port": "攻击来源端口",
#   "destination_port": "受害者端口",
#   "protocol": "TCP/UDP/ICMP等",
#   "attack_type": "攻击类型（如DDoS、SQL注入等）",
#   "severity": "告警级别（低/中/高/严重）",   （这个后续可以专门做词条规定）
#   "signature": "匹配的规则/特征",
#   "detection_system": "触发告警的IDS/IPS名称",
#   "correlation_id": "如果是关联事件，关联的告警ID"  （这里考虑到可能是同一攻击者发起多次不同来源的相似类型攻击）
# }
@r.route("/get/alert/message", methods=['GET'])
def get_alert_message():
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 获取总记录数
        total_count = Alert.count()
        
        # 从数据库中获取分页后的告警信息
        alerts = Alert.offset(offset).limit(page_size).all()
        
        # 格式化告警信息
        alert_list = []
        for alert in alerts:
            alert_dict = {
                "alert_id": alert.alert_id,
                "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": alert.source_ip,
                "destination_ip": alert.destination_ip,
                "source_port": alert.source_port,
                "destination_port": alert.destination_port,
                "protocol": alert.protocol,
                "attack_type": alert.attack_type,
                "severity": alert.severity,
                "signature": alert.signature,
                "detection_system": alert.detection_system,
                "correlation_id": alert.correlation_id,
                "status": alert.status,
                "create_time": alert.create_time.strftime("%Y-%m-%d %H:%M:%S") if alert.create_time else None,
                "update_time": alert.update_time.strftime("%Y-%m-%d %H:%M:%S") if alert.update_time else None
            }
            alert_list.append(alert_dict)
        
        # 计算总页数
        total_pages = (total_count + page_size - 1) // page_size
        
        return Response.re(data={
            "code": 200,
            "message": "获取告警信息成功",
            "data": {
                "list": alert_list,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": total_pages
                }
            }
        })
    except Exception as e:
        return Response.re(data={
            "code": 500,
            "message": f"获取告警信息失败: {str(e)}",
            "data": None
        })