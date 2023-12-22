from typing import Any

import anyio.to_thread
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette_admin.contrib.sqla.ext.pydantic import ModelView


class MyModelView(ModelView):
    async def create(self, request: Request, data: dict[str, Any]) -> Any:
        try:
            data = await self._arrange_data(request, data)
            await self.validate(request, data)
            data = self.on_before_create(request, data)
            session: Session | AsyncSession = request.state.session
            obj = await self._populate_obj(request, self.model(), data)
            session.add(obj)
            if isinstance(session, AsyncSession):
                await session.commit()
                await session.refresh(obj)
            else:
                await anyio.to_thread.run_sync(session.commit)
                await anyio.to_thread.run_sync(session.refresh, obj)
            return obj
        except Exception as e:
            return self.handle_exception(e)

    def on_before_create(self, request: Request, data: dict) -> dict:
        return data