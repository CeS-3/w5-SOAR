#!/usr/bin/env python
# encoding:utf-8
from . import *
# {
#   "analysis_id": "UUID",
#   "timestamp": "ISO 8601 时间格式",
#   "related_alerts": ["alert_id1", "alert_id2"],  （关联事件，如果有的话，没有就为空）
#   "attack_summary": "简要描述攻击行为",
#   "impact_analysis": {
#     "affected_systems": ["IP/主机名"],
#     "potential_risk": "对业务的影响（如数据泄露、服务中断）"
#   },
#   "recommended_actions": [
#     "采取的防御措施",
#     "补丁建议",
#     "阻断攻击的具体步骤"
#   ],
#   "notes": "额外补充说明"
# }
@r.route("/get/analysis/message", methods=['GET', 'POST'])
def get_analysis_message():
    
    

    data = {"message" : "this is a test!"}
    return Response.re(data=data)