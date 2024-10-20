from loguru import logger
import asyncio
import subprocess

async def scan(target, ports=None):
    try:
        # 构建 fscan 命令
        command = ['fscan', '-h', target]
        
        if ports:
            command += ['-p', ports]
        
        # 运行命令并捕获输出
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logger.error(f"[fscan] 执行失败: {stderr.decode('utf-8')}")
            return {"status": 2, "result": stderr.decode('utf-8')}
        
        # 成功执行，返回输出
        logger.info(f"[fscan] 执行成功: {stdout.decode('utf-8')}")
        return {"status": 0, "result": stdout.decode('utf-8')}

    except Exception as e:
        logger.error(f"[fscan] 运行时发生异常: {str(e)}")
        return {"status": 1, "result": str(e)}