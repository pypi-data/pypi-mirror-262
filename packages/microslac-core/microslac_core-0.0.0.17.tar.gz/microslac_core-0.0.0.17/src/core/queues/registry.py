from core.queues import BaseQueue


class ConversationQueue(BaseQueue):
    _exchange = "conversations"
