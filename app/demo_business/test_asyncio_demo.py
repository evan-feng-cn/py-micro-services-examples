import asyncio

async def test_A():
    print("=======A执行开始=======")
    await test_B()
    print("=======A执行完成=======")

async def test_B():
    print("=======B执行开始=======")
    await asyncio.sleep(5)
    print("=======B执行完成=======")

async def test_C():
    print("=======C执行开始=======")
    await test_D()
    print("=======C执行完成=======")

async def test_D():
    print("=======D执行开始=======")
    await asyncio.sleep(5)
    print("=======D执行完成=======")

async def test_E():
    print("=======E执行开始=======")
    for i in range(10):
        print(f"=======E执行循环模拟逻辑{i}=======")
    print("=======E执行完成=======")

async def main():
    await asyncio.gather(
        test_A(),
        test_B(),
        test_C(),
        test_E()
    )

if __name__ == '__main__':
    asyncio.run(main())