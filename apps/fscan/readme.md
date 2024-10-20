## APP说明

**本机需要安装 fscan 工具**

## 动作列表

### 弱口令检测

**参数**

|参数	|类型 |必填 |备注|
|  ----  | ----  |  ----  |  ----  |
|**target**	|text|	`是`	|IP 或 域名|
|**ports**	|text|	`否`	|端口类别，多个英文逗号分隔，列如 22,3306 |

**返回值：**

```
返回 json 数据
{
  "status": 0,
  "result": "start infoscan\n127.0.0.1:22 open\n[*] alive ports len is: 1\nstart vulscan\n已完成 0/1 [-] ssh 127.0.0.1:22 root root@2019 ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain \n已完成 0/1 [-] ssh 127.0.0.1:22 root abc123456 ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain \n已完成 0/1 [-] ssh 127.0.0.1:22 root Aa123456789 ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain \n已完成 0/1 [-] ssh 127.0.0.1:22 admin admin@123 ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain \n已完成 0/1 [-] ssh 127.0.0.1:22 admin 000000 ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain \n已完成 0/1 [-] ssh 127.0.0.1:22 admin Aa123456! ssh: handshake failed: ssh: unable to authenticate, attempted methods [none password], no supported methods remain \n已完成 1/1\n[*] 扫描结束,耗时: 6m28.611736031s\n"
}
```