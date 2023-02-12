import asyncio


async def run(cmd: str):
    proc = await asyncio.create_subprocess_shell(cmd)
    await proc.communicate()
    return proc.returncode
