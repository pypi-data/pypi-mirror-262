import asyncio

from meta import ctx


async def afunc(t):
    print(ctx.get(), t)


def func(t):
    print(ctx.get(), t)


async def aamain(v, t):
    ctx.set(v)
    await afunc(t)
    func(t)
    asyncio.create_task(afunc(t))


async def amain():
    await aamain(456, "1")
    await aamain(789, "2")
    await aamain(1024, "3")


def smain(v: int):
    ctx.set(v)
    func(1)
    func(1)
    func(1)


def smain2(v: int):
    ctx.set(v)
    func(2)
    func(2)
    func(2)


# asyncio.run(amain())


class A:
    def f2(self):
        ctx.set(32)

    def func(self):
        import test2


a = A()
a.f2()
a.func()
b = A()
b.func()
