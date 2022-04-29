from fastapi import HTTPException
from sqlalchemy.sql.expression import delete, insert, select, update

from app import db
from app.models import Form
from app.schemas import FormMetadata, UserResponse


class FormService:
    @classmethod
    async def create_form(cls, form_metadata: FormMetadata, user: UserResponse):
        form = await db.execute(
            insert(Form).values(
                owner_id=user.id,
                title=form_metadata.title,
                description=form_metadata.description,
            )
        )
        return {"message": "Form created successfully", "form_id": form}

    @classmethod
    async def get_user_form(cls, form_id: str, user: UserResponse):
        form = await db.fetch_one(
            select([Form]).where(Form.id == form_id, Form.owner_id == user.id)
        )
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return form

    @classmethod
    async def get_form(cls, form_id: str):
        form = await db.fetch_one(select([Form]).where(Form.id == form_id))
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return form

    @classmethod
    async def update_form(
        cls, form_id: str, form_metadata: FormMetadata, user: UserResponse
    ):
        form = await cls.get_user_form(form_id, user)
        await db.execute(
            update(Form)
            .where(Form.id == form_id)
            .values(title=form_metadata.title, description=form_metadata.description)
        )
        return await cls.get_form(form_id, user)

    @classmethod
    async def delete_form(cls, form_id: str, user: UserResponse):
        form = await cls.get_user_form(form_id, user)
        await db.execute(delete(Form).where(Form.id == form_id))
        return {"message": "Form deleted successfully"}
