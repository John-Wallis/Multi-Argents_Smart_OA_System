

from flask import Flask
from cozepy import Coze, TokenAuth


class ConversationController:
    """
    会话控制器
    负责初始化和管理 Coze 实例
    """
    def __init__(self):
        self.coze = None

    def init_coze(self, app: Flask):
        coze = Coze(
            auth=TokenAuth(token=app.config['COZE_API_TOKEN']),
            base_url=app.config['COZE_API_BASE']
        )

        self.coze = coze
        app.extensions['coze'] = coze