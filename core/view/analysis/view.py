#!/usr/bin/env python
# encoding:utf-8
from . import *
import json
from core.model import Analysis, AlertAnalysis
from datetime import datetime
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
@r.route("/get/analysis/message", methods=['GET'])
def get_analysis_message():
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 获取总记录数
        total_count = Analysis.count()
        
        # 从数据库中获取分页后的分析信息
        analyses = Analysis.offset(offset).limit(page_size).all()
        
        # 格式化分析信息
        analysis_list = []
        for analysis in analyses:
            # 获取关联的告警ID列表
            related_alerts = AlertAnalysis.where('analysis_id', analysis.analysis_id).get()
            alert_ids = [aa.alert_id for aa in related_alerts] if related_alerts else []
            
            # 解析JSON格式的字段
            try:
                affected_systems = json.loads(analysis.affected_systems)
            except:
                affected_systems = []
                
            try:
                recommended_actions = json.loads(analysis.recommended_actions)
            except:
                recommended_actions = []
            
            analysis_dict = {
                "analysis_id": analysis.analysis_id,
                "timestamp": analysis.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "related_alerts": alert_ids,
                "attack_summary": analysis.attack_summary,
                "impact_analysis": {
                    "affected_systems": affected_systems,
                    "potential_risk": analysis.potential_risk
                },
                "recommended_actions": recommended_actions,
                "notes": analysis.notes,
                "status": analysis.status,
                "create_time": analysis.create_time.strftime("%Y-%m-%d %H:%M:%S") if analysis.create_time else None,
                "update_time": analysis.update_time.strftime("%Y-%m-%d %H:%M:%S") if analysis.update_time else None
            }
            analysis_list.append(analysis_dict)
        
        # 计算总页数
        total_pages = (total_count + page_size - 1) // page_size
        
        return Response.re(data={
            "code": 200,
            "message": "获取分析信息成功",
            "data": {
                "list": analysis_list,
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
            "message": f"获取分析信息失败: {str(e)}",
            "data": None
        })