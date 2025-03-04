#!/usr/bin/env python
# encoding:utf-8
from . import *
import requests
import json
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
@r.route("/get/alert/message", methods=['GET', 'POST'])
def get_alert_message():

    data = {"message" : "this is a test!"}
    # 从数据库中调取告警信息
    alert_list = Alert.all()
    return Response.re(data=data)