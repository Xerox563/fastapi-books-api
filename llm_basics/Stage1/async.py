import asyncio
# asyncio is Python’s library for asynchronous programming.
# It helps run multiple waiting operations at the same time without blocking the program.

async def fetch_user(user_id: int) -> dict:
    """Simulate fetching user from API."""
    await asyncio.sleep(1)  # Pretend API call (1 second)
    return {"user_id": user_id, "name": f"User{user_id}"}

async def fetch_tasks(user_id: int) -> list:
    """Simulate fetching tasks from API."""
    await asyncio.sleep(1)  # Pretend API call (1 second)
    return [f"Task{i}" for i in range(3)]

async def main():
    print("Fetching data...")
    
    # Sequential (slow, one after another) - 2 seconds
    # user = await fetch_user(1)
    # tasks = await fetch_tasks(1)
    
    # Concurrent (fast, at same time) - 1 second
    user, tasks = await asyncio.gather(
        fetch_user(1),
        fetch_tasks(1)
    )
    
    print(user)      # Output: {'user_id': 1, 'name': 'User1'}
    print(tasks)     # Output: ['Task0', 'Task1', 'Task2']
    print("Done!")

asyncio.run(main())

'''
- Start fetch_user
- Start fetch_tasks
- Both wait together
- Finish together

| Keyword            | Meaning                |
| ------------------ | ---------------------- |
| `async def`        | Create async function  |
| `await`            | Wait without blocking  |
| `asyncio.sleep()`  | Non-blocking delay     |
| `asyncio.gather()` | Run tasks concurrently |
| `asyncio.run()`    | Start async program    |

'''