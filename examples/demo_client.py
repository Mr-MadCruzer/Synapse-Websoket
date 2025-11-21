# demo_client.py
import asyncio
from synapse_ws.client import call_add_numbers


async def main():
    inputs = [(1, 2), (3.5, 4.5), (-1, 10)]
    for a, b in inputs:
        try:
            result = await call_add_numbers(a, b)
            print(f"add_numbers({a}, {b}) -> {result}")
        except Exception as exc:
            print("Error:", exc)


if __name__ == "__main__":
    asyncio.run(main())
