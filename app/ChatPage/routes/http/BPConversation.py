from flask import Blueprint, jsonify
from flask import current_app

bp = Blueprint('conversation', __name__, url_prefix='/chat')


@bp.route('/get_conversations_list', methods=['GET'])
def get_conversations_list():
    from cozepy import Coze
    coze: Coze = current_app.extensions.get('coze')
    bot_id = current_app.config.get('BOT_ID')

    if not coze:
        return (
            {
                'status': "error",
                'msg': "Coze instance not initialized",
                'data': {}
            },
            500
        )
    if not bot_id:
        return (
            {
                'status': "error",
                'msg': "Bot ID not configured",
                'data': {}
            },
            500
        )

    page = 1
    has_more = True
    conversations_list = []
    while has_more:
        respond = coze.conversations.list(bot_id=bot_id, page_num=page, page_size=50)
        conversations_list.extend(respond.items)
        has_more = respond.has_more
        page += 1

    return {
        'status': "success",
        'msg': "Fetched conversations successfully",
        'data': conversations_list
    }






