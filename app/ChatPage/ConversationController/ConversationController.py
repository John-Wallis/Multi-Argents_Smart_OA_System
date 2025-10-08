import flask
from flask import Blueprint, render_template, request, redirect, url_for, session

from cozepy import Coze, TokenAuth


class ConversationController:
    def __init__(self):
        self.coze = None

    def init_coze(self, app: flask.Flask):
        coze = Coze(
            auth=TokenAuth(token=app.config['COZE_API_TOKEN']),
            base_url=app.config['COZE_API_BASE']
        )

        self.coze = coze
        app.extensions






