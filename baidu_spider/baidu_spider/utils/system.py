import platform
import asyncio
system = platform.system().lower()
if system == 'windows':
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )