from afeng_tools.fastapi_tool.common.po_service.link_po_service_ import LinkPoService
from afeng_tools.fastapi_tool.common.service import icon_base_service
from afeng_tools.fastapi_tool.common.service.base_service import BaseService
from afeng_tools.pydantic_tool.model.common_models import LinkItem


class LinkService(BaseService):
    """
    使用示例：link_service = LinkService(app_info.db_code, LinkInfoPo)
    """

    po_service_type = LinkPoService

    @classmethod
    def convert_po_2_item(cls, data_list: list) -> list[LinkItem]:
        return [LinkItem(
            href=tmp.link_url,
            code=f'{tmp.type_code}|{tmp.code}',
            title=tmp.title,
            description=tmp.description,
            image=icon_base_service.get_icon_code(tmp.icon_type, tmp.icon_value, tmp.title),
        ) for tmp in data_list] if data_list else []
