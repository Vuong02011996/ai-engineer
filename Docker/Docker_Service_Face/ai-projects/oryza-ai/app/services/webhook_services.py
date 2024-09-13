from odmantic import ObjectId
from fastapi import HTTPException

from app.models.type_service_model import TypeService
from app.models.webhook_model import Webhook
from app.models.user_model import User
from app.schemas.webhook_schemas import WebhookCreate, WebhookUpdate
from app.core.config import settings
from app.services.base_services import CRUDBase
from app.services.type_service_services import CRUDTypeService

type_service_services = CRUDTypeService(TypeService)


class CRUDWebhook(CRUDBase[Webhook, WebhookCreate, WebhookUpdate]):
    def get_webhook(self, *, user: User, id: str) -> Webhook:
        webhook = super().get(id=id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        if not user.is_superuser:
            if user.company != webhook.company:
                raise HTTPException(status_code=400, detail="Not enough permissions")
        return webhook

    def create_webhook(self, *, user: User, obj_in: WebhookCreate) -> Webhook:
        obj_in = obj_in.model_dump()
        type_service: TypeService = type_service_services.get_type_service(
            id=obj_in["type_service_id"]
        )
        webhook = self.engine.find_one(
            Webhook,
            Webhook.company == user.company.id,
            Webhook.endpoint == obj_in["endpoint"],
            Webhook.type_service == type_service.id,
        )
        if webhook:
            raise HTTPException(status_code=400, detail="Webhook already used")

        # Add company_id to the object
        obj_in["company"] = user.company
        obj_in["type_service"] = type_service
        # Create the object
        return super().create(obj_in=obj_in)

    def get_webhooks(
        self,
        *,
        user: User,
        page: int = 0,
        page_break: bool = False,
        data_search: str = None,
    ) -> list[Webhook]:
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        # if user.is_superuser:
        #     webhooks = self.engine.find(Webhook, **offset)
        #     return list(webhooks)
        if data_search:
            webhooks = self.engine.find(
                Webhook,
                {"company": ObjectId(user.company.id)},
                Webhook.name.match(f".*{data_search}.*"),
                **offset,
                sort=Webhook.created.desc(),
            )
            return list(webhooks)
        webhooks = self.engine.find(
            Webhook,
            {"company": ObjectId(user.company.id)},
            **offset,
            sort=Webhook.created.desc(),
        )
        return list(webhooks)

    def get_count(self, *, user: User, data_search: str = None) -> int:
        # if user.is_superuser:
        #     webhooks = self.engine.find(Webhook, **offset)
        #     return list(webhooks)
        if data_search:
            count = self.engine.count(
                Webhook,
                Webhook.company == ObjectId(user.company.id),
                Webhook.name.match(f".*{data_search}.*"),
            )
            return count
        count = self.engine.count(
            Webhook,
            Webhook.company == ObjectId(user.company.id),
        )
        return count

    def check_input_fields_valid(self, obj_in: dict, user: User) -> dict:
        if obj_in.get("type_service_id"):
            type_service = type_service_services.get_type_service(
                id=obj_in["type_service_id"]
            )
            obj_in["type_service"] = type_service
            if obj_in.get("endpoint"):
                webhook = self.engine.find_one(
                    Webhook,
                    Webhook.company == user.company.id,
                    Webhook.endpoint == obj_in["endpoint"],
                    Webhook.type_service == type_service.id,
                )
                if webhook:
                    raise HTTPException(status_code=400, detail="Webhook already used")
            if obj_in.get("name"):
                webhook = self.engine.find_one(
                    Webhook,
                    Webhook.company == user.company.id,
                    Webhook.name == obj_in["name"],
                    Webhook.type_service == type_service.id,
                )
                if webhook:
                    raise HTTPException(status_code=400, detail="Webhook already used")
            del obj_in["type_service_id"]
        return obj_in

    def update_webhook(self, *, user: User, id: str, obj_in: WebhookUpdate) -> Webhook:
        # Clean the input
        obj_in = super().clean_update_input(obj_in=obj_in)
        # Check if the fields are unique
        obj_in = self.check_input_fields_valid(obj_in, user)
        # Update the object
        webhook = self.get_webhook(user=user, id=id)
        return super().update(db_obj=webhook, obj_in=obj_in)

    def remove_webhook(self, *, id: str) -> None:
        return super().remove(id=id)

    def get_by_company_and_type_service(
        self, company_id: str, type_service_id: str
    ) -> list[Webhook]:
        webhooks = self.engine.find(
            Webhook,
            Webhook.company == ObjectId(company_id),
            Webhook.type_service == ObjectId(type_service_id),
        )
        return list(webhooks)

    def get_by_type_service(self, *, type_service_id: str):
        webhooks = self.engine.find(
            Webhook,
            Webhook.type_service == ObjectId(type_service_id),
        )
        return list(webhooks)

    def remove_field_type_service(self, *, type_service_id: str, null_obj: TypeService):
        webhooks = self.get_by_type_service(type_service_id=type_service_id)
        for webhook in webhooks:
            self.update(db_obj=webhook, obj_in={"type_service": null_obj})


webhook_services = CRUDWebhook(Webhook)

# if __name__ == "__main__":
#     data_in = {
#         "name": "Webhook 2",
#         "endpoint": "https://webhook1.com",
#         "status": True,
#         "type_service_id": "6637441a4e09c9b80518fcca"
#     }
#     from app.services.user_services import CRUDUser
#     user_services = CRUDUser(User)
#     user = user_services.get(id="6637135e4b0e6af194e68388")
#     webhook_services = CRUDWebhook(Webhook)
#     webhook = webhook_services.create_webhook(user=user, obj_in=WebhookCreate(**data_in))
#     company_id = "663711e520503aed00953911"
#     type_service_id = "6637441a4e09c9b80518fcca"
#     webhook_services = CRUDWebhook(Webhook)
#     webhook = webhook_services.remove_field_type_service(type_service_id=type_service_id)
