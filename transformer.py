import json
from datetime import datetime
import re
import uuid
import random
import requests
from requests.exceptions import HTTPError
import logging
# from functools import * 
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('requests').setLevel(logging.DEBUG)
# # 特别为 urllib3 设置日志级别为 DEBUG
# logging.getLogger('urllib3').setLevel(logging.DEBUG)

# 启用 requests 的调试模式
# requests.debug = True

# import networkx as nx
host_ip = "http://localhost:8888"
account = "admin"
passwd = "12345678"


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

    # 原始数据中的node使用“nodex”来代替，此处为每个节点生成 UUID，构建一张哈希表
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


def translate_script(input_data):
    output_data = {
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
            output_data["start_app"] = node_uuid_map[key]
        elif app_id == "end":
            output_data["end_app"] = node_uuid_map[key]
        elif app_id == "input":
            output_data["input_app"] = node_uuid_map[key]
        elif app_id == "webhook":
            output_data["webhook_app"] = node_uuid_map[key]
        elif app_id == "timer":
            output_data["timer_app"] = node_uuid_map[key]
        elif app_id == "audit":
            audit_list.append(node_uuid_map[key])
        # 以下两项为控制节点
        elif app_id == "for":
            for_list.append(node_uuid_map[key])
            output_data["controller_data"][node_uuid_map[key]] = {
                "node_name": f"{value['information']['name']}",
                "action": f"{value['information']['action']}",
                "text": f"{value['information']['text']}"
            }
        elif app_id == "if":
            if_list.append(node_uuid_map[key])
            output_data["controller_data"][node_uuid_map[key]] = {
                "node_name": f"{value['information']['name']}",
                "action": f"{value['information']['action']}",
                "text": f"{value['information']['text']}"
            }


    # 将列表转换为逗号分隔字符串
    output_data["for_list"] = ",".join(for_list)
    output_data["if_list"] = ",".join(if_list)
    output_data["audit_list"] = ",".join(audit_list)

    #进行变量解析
    for key,value in flow_data.items():
        flow_data[key]["data"] = var_parse(value["data"],node_uuid_map)
    for key,value in output_data["controller_data"]:
        output_data["controller_data"][key]["text"] = var_parse(value["text"])

    output_data["flow_json"] = flow_json
    output_data["flow_data"] = flow_data

    return output_data

def login():
    login_url = f"{host_ip}/api/v1/w5/login"
    payload = {
        'account':account ,
        'passwd': passwd
    }

    # 设置请求头部
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36',
        # 其他可能需要的头部信息
    }

    # 发送POST请求
    try:
        response = requests.post(login_url, json=payload, headers=headers)
        # 检查响应的状态码
        response.raise_for_status()
        # 打印响应内容
        re = response.json()
        return re
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'An error occurred: {err}')


def import_play_book(play_book):
    auth_info = login()

    token = auth_info['data']['token']
    account = auth_info['data']['account']
    nick_name = auth_info['data']['nick_name']
    user_id = auth_info['data']['user_id']

    import_url = f"{host_ip}/api/v1/w5/post/workflow/add"

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Origin': f'{host_ip}',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'{host_ip}',
        'sec-ch-ua': '"Chromium";v="121", "Not A(Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Connection': 'close',
        'account': f'{account}',  
        'user_id': f'{user_id}',
        # 'requestId': '99202412107160',
        # 'timestamp': '1733809401409',
        'token': f'{token}',
    }

    cookies = {
        'token': f'{token}',
        'nick_name': f'{nick_name}',
        'account': f'{account}',
        'user_id': f'{user_id}',
        'theme': 'dark',
        'user_nav': '%2CWorkflowEdit%2CDashboard%2CWorkflowHome%2CTimerHome%2CLogsHome%2CAppHome%2CAuditHome%2CVariablenHome%2CUserHome%2CSystemHome'
    }
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
    try:
        
        response = requests.post(import_url,headers=headers,cookies=cookies,data=play_book)
        # 检查响应的状态码
        response.raise_for_status()
        # proxies = {
        #     "http": 'http://127.0.0.1:8080',
        #     "https": 'http://127.0.0.1:8080'
        # }
        # requests_request = partial(requests.request, proxies=proxies, verify=False, allow_redirects=False)
        # response = requests_request('POST',import_url,headers=headers,cookies=cookies,data=play_book)
        # response.raise_for_status()
        print("import successfully!")        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'An error occurred: {err}')

def main():
    # 测试数据
    input_data = {
        "name": "DDOS",
        "remarks": "",
        "node_info": {
            "node1": {
                "app_id": "start",
                "app_type": 0
            },
            "node2": {
                "app_id": "end",
                "app_type": 0
            },
            "node3": {
                "app_id": "suricata",
                "app_type": 1,
                "information": {
                    "action": [
                        {
                            "name": "日志处理",
                            "func": "process_logs"
                        }
                    ],
                    "app_dir": "suricata",
                    "args": {
                        "process_logs": [
                            {
                                "key": "log_type",
                                "type": "text",
                                "required": True
                            }
                        ]
                    },
                    "description": "",
                    "icon": "suricata/icon.png",
                    "identification": "w5soar",
                    "is_public": True,
                    "name": "suricata",
                    "type": "ids",
                    "version": "0.1",
                    "data": {
                        "node_name": "suricata",
                        "action": "process_logs",
                        "log_type": "0",
                        "action_name": "日志处理",
                        "description": ""
                    }
                }
            },
            "node4": {
                "app_id": "firewalld",
                "app_type": 1,
                "information": {
                    "action": [
                        {
                            "name": "添加端口到区域",
                            "func": "add_port_to_zone"
                        },
                        {
                            "name": "移除端口从区域",
                            "func": "remove_port_from_zone"
                        },
                        {
                            "name": "重新加载防火墙规则",
                            "func": "reload_firewalld"
                        },
                        {
                            "name": "阻止IP",
                            "func": "block_ip"
                        }
                    ],
                    "app_dir": "firewalld",
                    "args": {
                        "add_port_to_zone": [
                            {
                                "key": "host",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "port",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "user",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "passwd",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "target_port",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "zone",
                                "type": "text",
                                "required": True,
                                "data": [
                                    "public",
                                    "external",
                                    "dmz",
                                    "work",
                                    "home",
                                    "internal",
                                    "trusted",
                                    "block",
                                    "drop"
                                ]
                            }
                        ],
                        "remove_port_from_zone": [
                            {
                                "key": "host",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "port",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "user",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "passwd",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "target_port",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "zone",
                                "type": "text",
                                "required": False,
                                "data": [
                                    "public",
                                    "external",
                                    "dmz",
                                    "work",
                                    "home",
                                    "internal",
                                    "trusted",
                                    "block",
                                    "drop"
                                ]
                            }
                        ],
                        "reload_firewalld": [
                            {
                                "key": "host",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "port",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "user",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "passwd",
                                "type": "text",
                                "required": True
                            }
                        ],
                        "block_ip": [
                            {
                                "key": "host",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "port",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "user",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "passwd",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "ip_address",
                                "type": "text",
                                "required": True
                            }
                        ]
                    },
                    "description": "一个管理防火墙规则的工具",
                    "icon": "firewalld/icon.png",
                    "identification": "w5soar",
                    "is_public": True,
                    "name": "firewalld_manager",
                    "type": "安全管理",
                    "version": "0.1",
                    "data": {
                        "node_name": "firewalld",
                        "action": "block_ip",
                        "host": "192.168.1.123",
                        "port": "22",
                        "user": "root",
                        "passwd": "root",
                        "ip_address": "@(node3.result)",
                        "action_name": "阻止ip",
                        "description": ""
                    }
                }
            },
            "node5": {
                "app_id": "feishu",
                "app_type": 1,
                "information": {
                    "action": [
                        {
                            "name": "飞书通知",
                            "func": "send"
                        }
                    ],
                    "app_dir": "feishu",
                    "args": {
                        "send": [
                            {
                                "key": "hook_uuid",
                                "type": "text",
                                "required": True
                            },
                            {
                                "key": "msg",
                                "type": "text",
                                "required": True
                            }
                        ]
                    },
                    "description": "飞书消息通知",
                    "icon": "feishu/icon.png",
                    "identification": "w5soar",
                    "is_public": True,
                    "name": "飞书通知",
                    "type": "消息通知",
                    "version": "0.1",
                    "data": {
                        "node_name": "飞书通知",
                        "action": "send",
                        "hook_uuid": "",
                        "msg": "封禁ip",
                        "action_name": "飞书通知",
                        "description": ""
                    }
                }
            }
        },
        "edge_info": [
            {
                "source": {
                    "cell": "node1",
                    "port": "right"
                },
                "target": {
                    "cell": "node3",
                    "port": "left"
                }
            },
            {
                "source": {
                    "cell": "node3",
                    "port": "right"
                },
                "target": {
                    "cell": "node4",
                    "port": "left"
                }
            },
            {
                "source": {
                    "cell": "node4",
                    "port": "right"
                },
                "target": {
                    "cell": "node5",
                    "port": "left"
                }
            },
            {
                "source": {
                    "cell": "node5",
                    "port": "right"
                },
                "target": {
                    "cell": "node2",
                    "port": "left"
                }
            }
        ],
        "local_var_data": [],
        "controller_data": {}
    }
    # 执行翻译
    play_book = translate_script(input_data)
    import_play_book(play_book)
    # 打印输出结果
    with open("test_playbook.json","w", encoding='utf-8') as f:
        f.write(json.dumps(play_book, indent=4, ensure_ascii=False))
    print("play book generate successfully!")



# 进行测试
main()
