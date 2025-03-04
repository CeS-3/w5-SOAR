#!/usr/bin/env python
# encoding:utf-8
from . import *
import json
from datetime import datetime
import re
import uuid
import random
import requests
from requests.exceptions import HTTPError
import logging
from flask import request

logger = logging.getLogger(__name__)
def add_workflow(data, user_id):
    # 根据传入的数据构造 workflow 字典
    uuid = Random.make_uuid()
    base_data = {
        'uuid': str(uuid),
        "type_id": 1,
        "user_id": user_id,
        'update_time': Time.get_date_time(),
        'create_time': Time.get_date_time()
    }
    
    if data.get("type", 0) == 0:
        base_data.update({
            'name': "未命名 " + Time.get_date_time(),
            'start_app': "",
            'end_app': "",
            'input_app': "",
            'webhook_app': "",
            'timer_app': "",
            'for_list': "",
            "if_list": "",
            "audit_list": "",
            'flow_json': "",
            'flow_data': "",
            'controller_data': "",
            'local_var_data': "none",
            'remarks': "",
            'status': 0,
            'grid_type': "dot",
            'edge_marker': "block",
            'edge_color': "#c7342e",
            'edge_connector': "normal",
            'edge_router': "metro",
            'thumbnail': ""
        })
    elif data.get("type") == 1:
        # 提取其它字段
        base_data.update({
            'name': data.get("name", ""),
            'start_app': data.get("start_app", ""),
            'end_app': data.get("end_app", ""),
            'input_app': data.get("input_app", ""),
            'webhook_app': data.get("webhook_app", ""),
            'timer_app': data.get("timer_app", ""),
            'for_list': data.get("for_list", ""),
            "if_list": data.get("if_list", ""),
            "audit_list": data.get("audit_list", ""),
            'flow_json': data.get("flow_json", ""),
            'flow_data': data.get("flow_data", ""),
            'controller_data': data.get("controller_data", ""),
            'local_var_data': data.get("local_var_data", ""),
            'remarks': data.get("remarks", ""),
            'status': 0,
            'grid_type': data.get("grid_type", ""),
            'edge_marker': data.get("edge_marker", ""),
            'edge_color': data.get("edge_color", ""),
            'edge_connector': data.get("edge_connector", ""),
            'edge_router': data.get("edge_router", ""),
            'thumbnail': data.get("thumbnail", "")
        })
    
    Workflow.insert(base_data)
    return uuid

# 测试设置 
host_ip = "127.0.0.1"
for_map = ["","数组循环","字典循环","次数循环"]
if_map = ["","==","!=","正则表达式", "JSON 解析器"]

def var_parse(data,node_uuid_map):
    app_var = r'@\(([a-f0-9\-]+)\.'
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):  # 确保值是字符串
                match = re.search(r'@\(([^\.]+)\.', value)
                if match:
                    # 获取匹配的UUID部分
                    node = match.group(1)
                    # 替换成新值（你可以在这里选择替换为不同的值）
                    data[key] = value.replace(node, node_uuid_map[node])
    # 用于解析controller_data中的text字段
    elif isinstance(data, str):
        match = re.search(r'@\(([^\.]+)\.',data)
        if match:
            node = match.group(1)
            data = data.replace(node, node_uuid_map[node])
    return data

def assign_basic_app_data(value):
    app_id = value["app_id"]
    if app_id == "start":
        data = {
            "icon": f"{host_ip}/app/basic/start.png",
            "name": "开始",
            "app_dir": "start",
            "action": ""
        }
    elif app_id == "end":
        data = {
            "icon": f"{host_ip}/app/basic/end.png",
            "name": "结束",
            "app_dir": "end",
            "action": ""
        }
    elif app_id == "audit":
        data = {
            "icon": f"{host_ip}/app/basic/audit.png",
            "name": "人工审计",
            "app_dir": "end",
            "action": ""
        }
    elif app_id == "webhook":
       data = {
            "icon": f"{host_ip}/app/basic/webhook.png",
            "name": "webhook",
            "app_dir": "webhook",
            "action": "trigger_webhook"
        }
    elif app_id == "timer":
       data = {
            "icon": f"{host_ip}/app/basic/timer.png",
            "name": "定时器",
            "app_dir": "timer",
            "action": "set_timer"
        }
    elif app_id == "input":
       data = {
            "icon": f"{host_ip}/app/basic/input.png",
            "name": "输入",
            "app_dir": "input",
            "action": "get_input"
        }
    elif app_id == "if":
       action_num = value["information"]["action"]
       data = {
            "icon": f"{host_ip}/app/basic/if.png",
            "name": "IF",
            "app_dir": "if",
            "action": f"{if_map[action_num]}"
        }
    elif app_id == "for":
       action_num = value["information"]["action"]
       data = {
            "icon": f"{host_ip}/app/basic/for.png",
            "name": "FOR",
            "app_dir": "for",
            "action": f"{for_map[action_num]}"
        }
    
    return data
# 此函数用于处理port下的items词条
def assign_items(key, edge_info):
    items = []
    for edge in edge_info:
        # 如果当前节点是 source
        if edge["source"]["cell"] == key:
            items.append({"id": edge["source"]["port"], 
                          "group": "right",
                          "args": {
                                "x": 70,
                                "y": 55
                            },
                          "attrs": {
                            "line": {
                                "stroke": "#787878"
                            }
                        }
                            })
        # 如果当前节点是 target
        if edge["target"]["cell"] == key:
            items.append({"id": edge["target"]["port"], 
                          "group": "left",
                            "args": {
                                "x": 0,
                                "y": 55
                            },
                            "attrs": {
                                "line": {
                                    "stroke": "#787878"
                                }
                            }
                            })
    return items

def assign_node(node_info, edge_info):
    # graph = nx.DiGraph()

    # for key in node_info.keys():
    #     graph.add_node(key)

    # for edge in edge_info:
    #     source = edge["source"]["cell"]
    #     target = edge["target"]["cell"]
    #     graph.add_edge(source, target)


    flow_json = {"cells":[]}
    
    flow_data = {}

    # 原始数据中的node使用"nodex"来代替，此处为每个节点生成 UUID，构建一张哈希表
    node_ids = node_info.keys()
    node_uuid_map = {node_id: str(uuid.uuid4()) for node_id in node_ids}

    # 处理flow_data,flow_data只有自定义app需要记录
    for key, value in node_info.items():
        # 若为自定义app
        if  value["app_type"] == 1:
            # 需要将其数据填入flow_data字段
            # 从map中取出该node对应的node_id的值
            flow_data[node_uuid_map[key]] = value["information"]

    # 然后处理flow_json

    # 首先进行点信息的处理
    zIndex = 1
    for key, value in node_info.items():
        #边信息中获取具体的端口信息
        items = assign_items(key, edge_info)
        cell = {
            "position": {
                # TODO： 书写节点坐标的分配函数
                "x": random.randint(-500,500),
                "y": random.randint(-600,600)
            },
            "size": {
                "width": 70,
                "height": 140
            },
            "view": "html-view",
            "shape": "html",
            "id": node_uuid_map[key],
            "html": "w5NodeDark",
            "data": 
            {
                "icon": f"{host_ip}/app/{value.get('information').get('icon')}",
                "name": f"{value['information']['name']}",
                "app_dir": f"{value['information']['app_dir']}",
                "action": f"{value['information']['data']['action']}"
            } if value["app_type"] == 1 else assign_basic_app_data(value),
            "ports":{
                "items": items,
                "groups": {
                        "left": {
                            "position": {
                                "name": "absolute"
                            },
                            "markup": [
                                {
                                    "tagName": "line",
                                    "selector": "line"
                                }
                            ],
                            "attrs": {
                                "line": {
                                    "y1": -9,
                                    "y2": 9,
                                    "magnet": "true",
                                    "strokeWidth": 5,
                                    "stroke": "#787878"
                                }
                            }
                        },
                        "right": {
                            "position": {
                                "name": "absolute"
                            },
                            "attrs": {
                                "circle": {
                                    "r": 7,
                                    "magnet": "true",  #这里可能有问题
                                    "strokeWidth": 0,
                                    "fill": "#787878",
                                    "stroke": "#787878"
                                }
                            }
                        }
                    }
                },
            "zIndex": zIndex
        }


        flow_json["cells"].append(cell)
        
            
        zIndex += 1
    
    # 添加边的信息
    for edge in edge_info:
        cell = {
                "shape": "w5Edge",
                "attrs": {
                    "line": {
                        "stroke": "#c7342e",
                        "targetMarker": {
                            "name": "block",
                            "args": {
                                "size": "8"
                            }
                        },
                        "strokeDasharray": 0
                    }
                },
                # "defaultLabel": {
                #     "markup": [
                #         {
                #             "tagName": "rect",
                #             "selector": "body"
                #         },
                #         {
                #             "tagName": "text",
                #             "selector": "label"
                #         }
                #     ],
                #     "attrs": {
                #         "label": {
                #             "fill": "#efefef",
                #             "fontSize": 14,
                #             "textAnchor": "middle",
                #             "textVerticalAnchor": "middle",
                #             "pointerEvents": "none"
                #         },
                #         "body": {
                #             "ref": "label",
                #             "fill": "#323232",
                #             "rx": 4,
                #             "ry": 4,
                #             "refWidth": "140%",
                #             "refHeight": "140%",
                #             "refX": "-20%",
                #             "refY": "-20%"
                #         }
                #     },
                #     "position": {
                #         "distance": 200,
                #         "options": {
                #             # TODO true可能存在错误，需要测试
                #             "absoluteDistance": True,
                #             "reverseDistance": True
                #         }
                #     }
                # },
                "id":str(uuid.uuid4()),  #随机分配一个uuid
                # "connector": {
                #     "name": "normal"
                # },
                # "router": {
                #     "name": "metro"
                # },
                "source": {
                    "cell": node_uuid_map[edge["source"]["cell"]],
                    "port": edge["source"]["port"]
                },
                "target": {
                    "cell": node_uuid_map[edge["target"]["cell"]],
                    "port": edge["target"]["port"]
                },
                "zIndex": zIndex
        }
        flow_json["cells"].append(cell)
        zIndex += 1

    return flow_json, flow_data, node_uuid_map


def expend_playbook(input_data):
    play_book = {
        "name": input_data.get("name", "未命名"),
        "remarks": input_data.get("remarks", ""),
        "start_app": "",
        "end_app": "",
        "input_app": "",
        "webhook_app": "",
        "timer_app": "",
        "for_list": "",
        "if_list": "",
        "audit_list": "",
        "flow_json": {"cells": []},
        "flow_data": {},
        "local_var_data": input_data.get("local_var_data", []),
        "controller_data": {},
        "grid_type": "dot",
        "edge_marker": "block",
        "edge_color": "#c7342e",
        "edge_connector": "normal",
        "edge_router": "metro",
        "thumbnail": "",
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    node_info = input_data.get("node_info", {})
    edge_info = input_data.get("edge_info", [])
    
    # 根据输入的点与边生成flow_json与flow_data字段
    flow_json, flow_data, node_uuid_map = assign_node(node_info, edge_info)


    # 初始化列表存储多节点信息
    for_list = []
    if_list = []
    audit_list = []
    
    # 根据 app_dir 分类加入剧本头的基础app列表
    for key, value in node_info.items():
        app_id = value["app_id"]
        if app_id == "start":
            play_book["start_app"] = node_uuid_map[key]
        elif app_id == "end":
            play_book["end_app"] = node_uuid_map[key]
        elif app_id == "input":
            play_book["input_app"] = node_uuid_map[key]
        elif app_id == "webhook":
            play_book["webhook_app"] = node_uuid_map[key]
        elif app_id == "timer":
            play_book["timer_app"] = node_uuid_map[key]
        elif app_id == "audit":
            audit_list.append(node_uuid_map[key])
        # 以下两项为控制节点
        elif app_id == "for":
            for_list.append(node_uuid_map[key])
            play_book["controller_data"][node_uuid_map[key]] = {
                "node_name": f"{value['information']['name']}",
                "action": f"{value['information']['action']}",
                "text": f"{value['information']['text']}"
            }
        elif app_id == "if":
            if_list.append(node_uuid_map[key])
            play_book["controller_data"][node_uuid_map[key]] = {
                "node_name": f"{value['information']['name']}",
                "action": f"{value['information']['action']}",
                "text": f"{value['information']['text']}"
            }


    # 将列表转换为逗号分隔字符串
    play_book["for_list"] = ",".join(for_list)
    play_book["if_list"] = ",".join(if_list)
    play_book["audit_list"] = ",".join(audit_list)

    #进行变量解析
    for key,value in flow_data.items():
        flow_data[key]["data"] = var_parse(value["data"],node_uuid_map)
    for key,value in play_book["controller_data"]:
        play_book["controller_data"][key]["text"] = var_parse(value["text"])

    play_book["flow_json"] = flow_json
    play_book["flow_data"] = flow_data

    play_book = {"type": 1, **play_book}
    del play_book["update_time"]
    del play_book["create_time"]
    escaped_flow_json = json.dumps(play_book["flow_json"], ensure_ascii=False)
    escaped_flow_data = json.dumps(play_book["flow_data"], ensure_ascii=False)
    escaped_controller_data = json.dumps(play_book["controller_data"],ensure_ascii=False)
    escaped_local_var_data = json.dumps(play_book["local_var_data"],ensure_ascii=False)
    play_book["flow_json"] = escaped_flow_json
    play_book["flow_data"] = escaped_flow_data
    play_book["controller_data"] = escaped_controller_data
    play_book["local_var_data"] = escaped_local_var_data
    play_book = json.dumps(play_book, ensure_ascii=False)
    return play_book


@r.route("/get/workflow/list", methods=['GET', 'POST'])
def get_user_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        type = request.json.get("type", "0")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

        workflow_list = Workflow.join(
            Users.__table__,
            Workflow.__table__ + '.user_id',
            '=',
            Users.__table__ + '.id'
        ).join(
            Types.__table__,
            Workflow.__table__ + '.type_id',
            '=',
            Types.__table__ + '.id'
        ).select(
            Workflow.__table__ + '.id',
            Workflow.__table__ + '.uuid',
            Workflow.__table__ + ".type_id",
            Workflow.__table__ + '.name',
            Workflow.__table__ + '.update_time',
            Workflow.__table__ + '.create_time',
            Users.__table__ + '.nick_name',
            Types.__table__ + '.name as type_name',
            Workflow.__table__ + '.remarks',
            Workflow.__table__ + '.status',
            Workflow.__table__ + '.timer_app',
            Workflow.__table__ + '.webhook_app',
            Workflow.__table__ + '.input_app',
            Workflow.__table__ + '.for_list',
            Workflow.__table__ + '.thumbnail'
        )

        if str(type) != "0":
            workflow_list = workflow_list.where(Workflow.__table__ + ".type_id", type)

        if str(keywords) == "":
            workflow_list = workflow_list.order_by(Workflow.__table__ + '.id', 'desc').paginate(page_count, page)
        else:
            workflow_list = workflow_list.where(
                Workflow.__table__ + '.name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by(Workflow.__table__ + '.id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=workflow_list).to())


@r.route("/get/workflow/simple_list", methods=['GET', 'POST'])
def get_workflow_simple_list():
    if request.method == "POST":
        sql = '''
        select uuid,name from `w5_workflow` ORDER BY CONVERT(name USING GBK);
        '''
        result = db.select(sql)
        return Response.re(data=result)


@r.route("/post/workflow/add", methods=['GET', 'POST'])
def post_workflow_add():
    if request.method == "POST":
        data = request.get_json()
        token = request.headers.get("token")
        user_id = redis.get(token)
        uuid = add_workflow(data, user_id)
        return Response.re(data={"uuid": uuid})


@r.route("/post/workflow/import", methods=['POST'])
def post_workflow_import():
    try:
        # 获取请求数据
        data = request.get_json()
        logger.info("Received JSON data: %s", data)

        # 认证方式判断
        api_key = request.json.get("key", "")
        token = request.headers.get("token")
        
        # 如果提供了 API Key，使用 API Key 认证
        if api_key:
            if str(api_key).strip() == "":
                return Response.re(err=ErrWebhookkey)

            key = "api_key"
            if redis.exists(key) == 0:
                setting = Setting.select('value').where("key", "api_key").first()
                value_key = setting.value
                redis.set("api_key", str(value_key))
            else:
                value_key = redis.get(key).decode()

            if str(api_key) != str(value_key):
                return Response.re(err=ErrWebhookKeyNot)
            
            data = request.json.get("workflow_data", "")
            # API Key 认证成功，使用系统默认用户ID
            user_id = 1  # 或其他系统默认用户ID
            logger.info("API Key authentication successful, using system default user")
        # 如果提供了 Token，使用 Token 认证
        elif token:
            user_id = redis.get(token)
            if not user_id:
                return Response.re(err=ErrToken)
            logger.info("Token authentication successful, user_id: %s", user_id)
        # 如果都没有提供，返回认证错误
        else:
            return Response.re(err=ErrWebhookKeyNot)

        # 数据转换
        transformed_data = expend_playbook(data)
        logger.info("Transformed data: %s", transformed_data)

        # 添加 workflow 并返回 uuid
        logger.info("transformed_data type: %s", type(transformed_data))
        uuid = add_workflow(json.loads(transformed_data), user_id)
        logger.info("Workflow added successfully with uuid: %s", uuid)

        return Response.re(data={"uuid": uuid})
    except Exception as e:
        # 输出异常日志，便于排查具体问题
        logger.exception("Error processing workflow import: %s", e)
        return Response.re(code=400, msg="Error processing request", data={})



@r.route("/post/workflow/detail", methods=['GET', 'POST'])
def get_workflow_detail():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")

        workflow_info = Workflow.select(
            'uuid',
            'name',
            'start_app',
            'end_app',
            'input_app',
            'webhook_app',
            'timer_app',
            'for_list',
            'if_list',
            'audit_list',
            'flow_json',
            'flow_data',
            'controller_data',
            'type_id',
            'remarks',
            'local_var_data',
            'status',
            'grid_type',
            'edge_marker',
            'edge_color',
            'edge_connector',
            'edge_router',
            'thumbnail',
            'update_time',
            'create_time'
        ).where("uuid", uuid).first()

        return Response.re(data=workflow_info.serialize())


@r.route("/post/workflow/update", methods=['GET', 'POST'])
def post_workflow_update():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        name = request.json.get("name", "")
        start_app = request.json.get("start_app", "")
        end_app = request.json.get("end_app", "")
        input_app = request.json.get("input_app", "")
        webhook_app = request.json.get("webhook_app", "")
        timer_app = request.json.get("timer_app", "")
        for_list = request.json.get("for_list", "")
        if_list = request.json.get("if_list", "")
        audit_list = request.json.get("audit_list", "")
        flow_json = request.json.get("flow_json", "")
        flow_data = request.json.get("flow_data", "")
        controller_data = request.json.get("controller_data", "")
        type_id = request.json.get("type_id", "")
        remarks = request.json.get("remarks", "")
        local_var_data = request.json.get("local_var_data", "")
        grid_type = request.json.get("grid_type", "")
        edge_marker = request.json.get("edge_marker", "")
        edge_color = request.json.get("edge_color", "")
        edge_connector = request.json.get("edge_connector", "")
        edge_router = request.json.get("edge_router", "")
        thumbnail = request.json.get("thumbnail", "")

        if str(controller_data) != "{}":
            is_exist = json.loads(controller_data).get(timer_app)

            work_info = Workflow.select("timer_app").where('uuid', uuid).first()

            if work_info:
                if str(work_info.timer_app) == "" or str(work_info.timer_app) == "None" or work_info.timer_app is None:
                    w_timer_app = ""
                else:
                    w_timer_app = work_info.timer_app

                conn = rpyc.connect('localhost', 53124)

                if is_exist:
                    conn.root.exec(uuid, timer_app, w_timer_app, controller_data)
                else:
                    conn.root.exec(uuid, "", w_timer_app, controller_data)

                conn.close()
            else:
                return Response.re(err=ErrIsNotPlayBook)

        Workflow.where('uuid', uuid).update({
            'name': name,
            'start_app': start_app,
            'end_app': end_app,
            'input_app': input_app,
            'webhook_app': webhook_app,
            'timer_app': timer_app,
            'for_list': for_list,
            'if_list': if_list,
            'audit_list': audit_list,
            'flow_json': flow_json,
            'flow_data': flow_data,
            'controller_data': controller_data,
            'type_id': type_id,
            'remarks': remarks,
            'local_var_data': local_var_data,
            'grid_type': grid_type,
            'edge_marker': edge_marker,
            'edge_color': edge_color,
            'edge_connector': edge_connector,
            'edge_router': edge_router,
            'thumbnail': thumbnail,
            'update_time': Time.get_date_time()
        })

        return Response.re()


@r.route("/post/workflow/del", methods=['GET', 'POST'])
def post_workflow_del():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")

        work_info = Workflow.select("timer_app").where('uuid', uuid).first()

        if work_info:
            if str(work_info.timer_app) == "" or str(work_info.timer_app) == "None" or work_info.timer_app is None:
                pass
            else:
                conn = rpyc.connect('localhost', 53124)
                conn.root.remove(work_info.timer_app)
                conn.close()
        else:
            return Response.re(err=ErrIsNotPlayBook)

        Workflow.where('uuid', uuid).delete()
        return Response.re()


@r.route("/post/workflow/status", methods=['GET', 'POST'])
def post_workflow_status():
    if request.method == "POST":
        id = request.json.get("id", "")
        status = request.json.get("status", "")

        Workflow.where('id', id).update(
            {
                "status": status,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()


@r.route("/get/workflow/import_url", methods=['GET', 'POST'])
def post_workflow_import_url():
    if request.method == "POST":
        url = request.json.get("url", "")
        try:
            r = requests.get(url=url, timeout=10)
            return Response.re(data={"data": r.json()})
        except:
            return Response.re(err=ErrImportUrl)


@r.route("/get/workflow/statistics", methods=['GET', 'POST'])
def post_workflow_statistics():
    if request.method == "POST":
        url = request.json.get("url", "")
        try:
            r = requests.get(url=url, timeout=10)
            return Response.re(data={"data": r.json()})
        except:
            return Response.re(err=ErrImportUrl)


@ws.route('/echo')
def echo_socket(s):
    while not s.closed:
        message = s.receive()

        if message:
            req_data = json.loads(message)
            method = req_data["method"]

            if method == "ping":
                pass
            elif method == "run":
                uuid = req_data["data"]["uuid"]
                auto_execute(uuid, s=s)


def get_workflow_logs(uuid):
    logs_list = Logs.join(
        Workflow.__table__,
        Logs.__table__ + '.uuid',
        '=',
        Workflow.__table__ + '.uuid'
    ).select(
        Logs.__table__ + '.id',
        Logs.__table__ + '.only_id',
        Logs.__table__ + '.uuid',
        Logs.__table__ + ".app_name",
        Logs.__table__ + '.result',
        Logs.__table__ + '.create_time',
        Logs.__table__ + '.status',
        Logs.__table__ + '.args',
        Workflow.__table__ + '.name'
    ).where(
        Workflow.__table__ + '.uuid',
        uuid
    ).order_by(
        Workflow.__table__ + '.id',
        'desc'
    ).limit(100).get()

    return logs_list


@r.route("/get/workflow/logs", methods=['GET', 'POST'])
def get_workflow_logs_info():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        logs_list = get_workflow_logs(uuid)
        return Response.re(data=logs_list.serialize())


def get_workflow_sums(uuid):
    if redis.exists(uuid + "&&exec_sum") == 1:
        exec_sum = redis.get(uuid + "&&exec_sum")
    else:
        exec_sum = 0

    return exec_sum


@r.route("/get/workflow/sums", methods=['GET', 'POST'])
def get_workflow_sums_info():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        exec_sum = get_workflow_sums(uuid)

        data = {
            "exec_sum": exec_sum
        }

        return Response.re(data=data)


def get_workflow_success_fail(uuid):
    sql1 = '''
    SELECT
        COUNT(1) as x 
    FROM
        w5_logs 
    WHERE
        uuid = "{uuid}" 
    GROUP BY
        only_id
    '''.format(uuid=uuid)

    sql2 = '''
    SELECT
        COUNT(1) as x 
    FROM
        w5_logs 
    WHERE
        `status` != 0 
        AND uuid = "{uuid}"
    GROUP BY
        only_id
    '''.format(uuid=uuid)

    r1 = db.select(sql1)
    r2 = db.select(sql2)

    return len(r1), len(r1) - len(r2), len(r2)


@r.route("/get/workflow/workflow", methods=['GET', 'POST'])
def get_workflow_workflow():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        sum, success_sum, fail_sum = get_workflow_success_fail(uuid)

        result = [
            {
                "name": "成功",
                "sum": success_sum
            },
            {
                "name": "失败",
                "sum": fail_sum
            }
        ]

        if redis.exists(uuid + "&&exec_sum") == 1:
            exec_sum = redis.get(uuid + "&&exec_sum")
        else:
            exec_sum = 0

        data = {
            "result": result,
            "exec_sum": exec_sum
        }

        return Response.re(data=data)


def get_workflow_exec(uuid):
    sql = '''
        SELECT
            DATE_FORMAT( create_time, '%%m-%%d#%%H' ) AS time,
            count(id) AS value 
        FROM
            {logs} 
        WHERE
            DATE( create_time ) > DATE_SUB( CURDATE(), INTERVAL 1 DAY ) 
        AND uuid="{uuid}"
        GROUP BY
            time;
        '''.format(
        logs=Logs.__table__,
        uuid=uuid
    )

    exec_data = db.select(sql)

    time_data = {}

    for t in Time.get_hour():
        time_data[t] = 0

    for t in exec_data:
        arr = str(t.time).split("#")
        time_data[arr[1]] = t.value

    result = []

    for t in time_data:
        data = {
            "time": t,
            "value": time_data[t]
        }

        result.append(data)

    return result


@r.route("/get/workflow/exec", methods=['GET', 'POST'])
def get_workflow_exec_info():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        result = get_workflow_exec(uuid)
        return Response.re(data=result)
