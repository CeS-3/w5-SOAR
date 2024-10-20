from loguru import logger

async def my_hello_world(name1,name2):
    try:
        import requests
    except:
        logger.info("[Hello World] 导入 requests 模块失败, 请输入命令 pip install requests")
        return 2, "缺少 requests 模块"


    logger.info("[Hello World] 该 APP 执行参数为: {name}", name=name1)
    return {"status":0,"result":"Hello," + name1 + " and " + name2,"html": '''<span style="color:red">success</span>'''}