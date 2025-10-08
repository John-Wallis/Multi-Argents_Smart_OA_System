import os
import config

from flask import Flask


from app.ChatPage.routes.http.BPConversation import bp as bp_conversation

# 创建Flask应用实例,【警告！改回环境标志为空！！】
def create_app(custom_config=None, env_flag='DEV'):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(bp_conversation, url_prefix=f'/api/{config.API_VERSION}')

    # 读取全局配置
    # app.config.from_pyfile('config.py')

    # 读取默认敏感环境配置
    if env_flag is None:
        app.config.from_pyfile('default_config.py', silent=True)

    # 读取指定环境配置,或自定义配置
    else:
        match env_flag:
            case 'dev' | 'DEV':
                app.config.from_pyfile('dev_config.py', silent=True)
            case 'test' | 'TEST':
                app.config.from_pyfile('test_config.py', silent=True)
            case _:
                app.config.from_mapping(custom_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


if __name__ == '__main__':
    app = create_app(env_flag='DEV')
    app.run()