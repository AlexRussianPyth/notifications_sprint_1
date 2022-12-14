from http import HTTPStatus

import pika
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_db
from db.rabbit import get_rabbit
from models import schemas
from services import crud, publisher
from services.publisher import get_queue

router = APIRouter()


@router.post("/", summary="Create a notification")
async def create_notification(
        event: schemas.Event,
        session: AsyncSession = Depends(get_db),
        connection: pika.BlockingConnection = Depends(get_rabbit)
):
    """
    Create a notification with all the information:

    - **users**: list of id users to send a notification
    - **event**: event to notification
    - **data**: additional data to notification
    """
    db_template = await crud.get_template_by_event(session, event=event.event)
    if not db_template:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Event not found")
    notification = schemas.Notification(**event.dict(), template=db_template.text, subject=db_template.title)
    publisher.publish(message=notification.json(), connection=connection, queue=get_queue(db_template.instant_event))
    return HTTPStatus.OK
