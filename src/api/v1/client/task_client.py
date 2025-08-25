"""Клиент"""

# -- Imports

import httpx
import asyncio
import logging
from src.core.log import conf_logging
from src.core.schemas.task_schemas import TaskOut
from src.core.constants import TASK_UUID, TASK_TITLE, TASK_DESCRIPTION, TASK_STATUS

# --


log = logging.getLogger(__name__)

# --


async def create():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        payload = {
            "task_title": TASK_TITLE,
            "task_description": TASK_DESCRIPTION,
        }
        response = await client.post(
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            url="/",
            data=payload,
        )
        response.raise_for_status()
        task = TaskOut(**response.json())
        log.info(
            "Создана таска: %s | Статус: %s",
            task.title,
            task.status.value,
        )


async def update():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        payload = {
            "task_title": TASK_UUID,
            "task_description": TASK_DESCRIPTION,
            "task_status": TASK_STATUS.value,
        }

        response = await client.put(
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            url=f"/update/{TASK_UUID}",
            data=payload,
        )
        task = TaskOut(**response.json())
        log.info(
            "Обновлена таска %s: %s, %s, %s",
            task.id,
            task.title,
            task.description,
            task.status.value,
        )


async def update_status():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        payload = {
            "task_status": TASK_STATUS.value,
        }

        response = await client.patch(
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            url=f"/update-status/{TASK_UUID}",
            data=payload,
        )
        log.info("Ответ сервера: %s", response)


async def get_task():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            url=f"/{TASK_UUID}",
        )
        task = TaskOut(**response.json())
        log.info(
            "UUID: %s Title: %s, Description: %s, Status: %s",
            task.id,
            task.title,
            task.description,
            task.status.value,
        )


async def get_all():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            url=f"/all",
        )
        tasks: list = response.json()
        log.info("Список тасок: %s", tasks)


async def delete():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete(
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            url=f"/delete/{TASK_UUID}",
        )
        data = response.json()
        log.info("Удалена таска: %s", data)
        return data

        # Обработать в случае если таски нет уже


async def main():
    conf_logging()
    actions = {
        "create": create,
        "update": update,
        "update_status": update_status,
        "get_task": get_task,
        "get_all": get_all,
        "delete": delete,
    }
    action_name = "create"

    await actions[action_name]()


if __name__ == "__main__":
    asyncio.run(main())
