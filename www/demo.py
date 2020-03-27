
import asyncio
import orm

from models import User, Blog, Comment

async def test():
    await orm.create_pool(user='root', password='mapei123', db='awesome')

    u = User(name='Test1', email='test1@example.com', passwd='1234567890', image='about:blank')

    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.run_forever()