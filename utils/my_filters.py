from vkwave.bots import SimpleBotEvent
from vkwave.bots.core.dispatching.filters import base


class JoinFilter(base.BaseFilter):
    """
    Проверяет событие ли вступление в группу
    """

    async def check(self, event: SimpleBotEvent) -> base.FilterResult:
        return base.FilterResult(event.object.type == "group_join")


class LeaveFilter(base.BaseFilter):
    """
    Проверяет событие ли выход из группу
    """

    async def check(self, event: SimpleBotEvent) -> base.FilterResult:
        return base.FilterResult(event.object.type == "group_leave")


class NewPostFilter(base.BaseFilter):
    """
    Проверяет событие пост ли это
    """

    async def check(self, event: SimpleBotEvent) -> base.FilterResult:
        return base.FilterResult(event.object.type == "wall_post_new")


class HasPayloadFilter(base.BaseFilter):
    """
    Проверяет прикреплена ли к сообщению гео-метка
    """

    async def check(self, event: SimpleBotEvent) -> base.FilterResult:
        return base.FilterResult(event.object.type == "message_new" and event.object.object.message.payload is not None)
