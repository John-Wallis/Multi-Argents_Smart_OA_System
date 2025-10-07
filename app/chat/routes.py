
from cozepy import (
    Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType
)
from flask import (
    Blueprint, render_template, redirect, request, url_for, session, current_app, Response, render_template_string
)

bp = Blueprint('chat', __name__, url_prefix='/api/v1/chat')


def stream_coze_response(bot_id, user_id, query, coze_api_token, coze_api_base):

    """
    一个生成器函数，用于流式传输来自 Coze API 的响应。
    """
    try:
        # 初始化 Coze 客户端
        coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

        # 流式调用 chat 方法
        for event in coze.chat.stream(
                bot_id=bot_id,
                user_id=user_id,
                query=query,
                additional_messages=[
                    Message.build_user_question_text("Tell a 500-word story."),
                ],
        ):
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                # 产生消息内容块
                yield event.message.content
            # 您可以在这里处理其他事件类型，例如错误或完成状态
            # elif event.event == ChatEventType.CONVERSATION_ERROR:
            #     yield f"Error: {event.error.message}"
            #     break

    except Exception as e:
        # 由于无法访问 current_app.logger，我们直接产生一个通用的错误信息
        # 可以在调用此函数的地方记录日志
        print(f"Coze stream error: {e}") # 使用 print 或标准 logging 记录错误
        yield "An error occurred while processing your request."


@bp.route('', methods=['GET'])
def chat_entry():
    # 鉴权操作
    # 失败重定向

    pass

@bp.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        request_data = request.get_json(silent=True)

        if request_data is None:
            return {'error': 'Invalid JSON'}, 400


        # 从请求或会话中获取用户ID，这里使用一个固定的测试值
        user_id = request_data.get('user_id', 'test_user')
        # Bot ID 应该从配置或请求中获取，这里使用一个固定的测试值
        bot_id = '7536524288745766951'
        conversation_id = int(request_data['conversation_id'])
        message = request_data.get('message', {})
        content = message.get('content')

        # 暂时忽略所有附加参数attachments, tools等
        # file处理逻辑
        # 附加工具启动逻辑

        if not content:
            return {'error': 'Message content is required'}, 400


        coze_api_token = current_app.config['COZE_API_TOKEN']
        coze_api_base = current_app.config['COZE_API_BASE']

        stream = stream_coze_response(bot_id, user_id, content, coze_api_token, coze_api_base)

        return Response(stream, mimetype='text/plain')


    return render_template_string('''
    <!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask聊天验证 - 流式传输与WebSocket</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 900px;
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 90vh;
        }
        
        .header {
            background: linear-gradient(to right, #4a6ee0, #6e46a3);
            color: white;
            padding: 20px;
            text-align: center;
            position: relative;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .header p {
            opacity: 0.9;
        }
        
        .protocol-toggle {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .protocol-toggle:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .content {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        .sidebar {
            width: 250px;
            background-color: #f8f9fa;
            border-right: 1px solid #e9ecef;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }
        
        input, textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input:focus, textarea:focus {
            border-color: #6e8efb;
            outline: none;
            box-shadow: 0 0 0 2px rgba(110, 142, 251, 0.2);
        }
        
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .send-btn {
            background: linear-gradient(to right, #4a6ee0, #6e46a3);
            color: white;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(74, 110, 224, 0.4);
        }
        
        .reset-btn {
            background-color: #f1f3f9;
            color: #666;
        }
        
        .reset-btn:hover {
            background-color: #e4e7f2;
        }
        
        .chat-area {
            flex: 1;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            background-color: #f9fafc;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            margin-bottom: 15px;
        }
        
        .message {
            margin-bottom: 15px;
            max-width: 80%;
        }
        
        .user-message {
            align-self: flex-end;
            background: linear-gradient(to right, #4a6ee0, #6e46a3);
            color: white;
            padding: 10px 15px;
            border-radius: 18px 18px 5px 18px;
        }
        
        .bot-message {
            align-self: flex-start;
            background-color: white;
            color: #333;
            padding: 10px 15px;
            border-radius: 18px 18px 18px 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .status-area {
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            font-size: 14px;
        }
        
        .status-area.connected {
            background-color: #e7f7ef;
            color: #2e7d32;
            border: 1px solid #c8e6c9;
        }
        
        .status-area.disconnected {
            background-color: #ffebee;
            color: #c62828;
            border: 1px solid #ffcdd2;
        }
        
        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 10px;
        }
        
        .connected .status-indicator {
            background-color: #4caf50;
            animation: pulse 2s infinite;
        }
        
        .disconnected .status-indicator {
            background-color: #f44336;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 10px 0;
        }
        
        .spinner {
            border: 3px solid rgba(0, 0, 0, 0.1);
            border-left-color: #4a6ee0;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .instructions {
            background-color: #f0f4ff;
            border-left: 4px solid #4a6ee0;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 0 8px 8px 0;
            font-size: 14px;
        }
        
        .instructions h3 {
            margin-bottom: 10px;
            color: #4a6ee0;
        }
        
        .instructions ul {
            padding-left: 20px;
        }
        
        .instructions li {
            margin-bottom: 5px;
        }
        
        .connection-info {
            margin-top: auto;
            padding-top: 15px;
            border-top: 1px solid #e9ecef;
            font-size: 12px;
            color: #6c757d;
        }
        
        @media (max-width: 768px) {
            .content {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                border-right: none;
                border-bottom: 1px solid #e9ecef;
            }
            
            .header h1 {
                font-size: 20px;
            }
            
            .protocol-toggle {
                position: static;
                transform: none;
                margin-top: 10px;
                display: inline-block;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Flask聊天验证</h1>
            <p>支持流式传输与WebSocket协议</p>
            <div class="protocol-toggle" id="protocolToggle">
                当前协议: HTTP
            </div>
        </div>
        
        <div class="content">
            <div class="sidebar">
                <div class="instructions">
                    <h3>使用说明</h3>
                    <ul>
                        <li>填写用户ID和对话ID（可选）</li>
                        <li>在消息框中输入您想发送的文本</li>
                        <li>点击"发送消息"按钮发送请求</li>
                        <li>查看右侧的实时流式响应</li>
                    </ul>
                </div>
                
                <div class="form-group">
                    <label for="user_id">用户ID</label>
                    <input type="text" id="user_id" value="test_user" placeholder="输入用户ID">
                </div>
                
                <div class="form-group">
                    <label for="conversation_id">对话ID</label>
                    <input type="number" id="conversation_id" value="1" placeholder="输入对话ID">
                </div>
                
                <div class="form-group">
                    <label for="message">消息内容</label>
                    <textarea id="message" placeholder="输入您想发送的消息...">你好，请介绍一下你自己。</textarea>
                </div>
                
                <div class="button-group">
                    <button class="send-btn" id="sendBtn">发送消息</button>
                    <button class="reset-btn" id="resetBtn">重置表单</button>
                </div>
                
                <div class="connection-info">
                    <p><strong>当前模式:</strong> HTTP流式传输</p>
                    <p><strong>端点:</strong> /api/v1/chat/send_message</p>
                    <p><strong>准备升级:</strong> WebSocket协议</p>
                </div>
            </div>
            
            <div class="main-content">
                <div class="status-area connected" id="statusArea">
                    <div class="status-indicator"></div>
                    <span>已连接到服务器 - 使用HTTP流式传输</span>
                </div>
                
                <div class="chat-area" id="chatArea">
                    <div class="message bot-message">
                        欢迎使用Flask聊天验证工具！请发送消息开始对话。
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>正在获取响应...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 协议切换功能（为未来WebSocket做准备）
        document.getElementById('protocolToggle').addEventListener('click', function() {
            const currentProtocol = this.textContent.includes('HTTP') ? 'HTTP' : 'WebSocket';
            const newProtocol = currentProtocol === 'HTTP' ? 'WebSocket' : 'HTTP';
            
            if (newProtocol === 'WebSocket') {
                alert('WebSocket协议功能正在开发中，当前仍使用HTTP流式传输');
                return;
            }
            
            this.textContent = `当前协议: ${newProtocol}`;
            updateConnectionStatus(newProtocol);
        });
        
        function updateConnectionStatus(protocol) {
            const statusArea = document.getElementById('statusArea');
            if (protocol === 'HTTP') {
                statusArea.className = 'status-area connected';
                statusArea.innerHTML = '<div class="status-indicator"></div><span>已连接到服务器 - 使用HTTP流式传输</span>';
            } else {
                statusArea.className = 'status-area disconnected';
                statusArea.innerHTML = '<div class="status-indicator"></div><span>WebSocket协议正在开发中</span>';
            }
        }
        
        // 重置表单
        document.getElementById('resetBtn').addEventListener('click', function() {
            document.getElementById('user_id').value = 'test_user';
            document.getElementById('conversation_id').value = '1';
            document.getElementById('message').value = '你好，请介绍一下你自己。';
            
            // 清空聊天区域，只保留欢迎消息
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = '<div class="message bot-message">欢迎使用Flask聊天验证工具！请发送消息开始对话。</div>';
        });
        
        // 发送消息
        document.getElementById('sendBtn').addEventListener('click', function() {
            const user_id = document.getElementById('user_id').value || 'test_user';
            const conversation_id = parseInt(document.getElementById('conversation_id').value) || 1;
            const message = document.getElementById('message').value;
            
            if (!message.trim()) {
                alert('请输入消息内容');
                return;
            }
            
            // 显示用户消息
            const chatArea = document.getElementById('chatArea');
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = message;
            chatArea.appendChild(userMessage);
            
            // 显示加载状态
            const loading = document.getElementById('loading');
            loading.style.display = 'block';
            
            // 创建机器人消息容器
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot-message';
            botMessage.textContent = '';
            chatArea.appendChild(botMessage);
            
            // 滚动到底部
            chatArea.scrollTop = chatArea.scrollHeight;
            
            // 使用Axios发送POST请求
            axios({
                method: 'POST',
                url: '/api/v1/chat/send_message',
                data: {
                    user_id: user_id,
                    conversation_id: conversation_id,
                    message: {
                        content: message
                    }
                },
                responseType: 'text', // 重要：设置响应类型为文本
                onDownloadProgress: function(progressEvent) {
                    // 处理流式响应
                    const response = progressEvent.event.target.response;
                    if (response) {
                        // 更新机器人消息内容
                        botMessage.textContent = response;
                        // 滚动到底部
                        chatArea.scrollTop = chatArea.scrollHeight;
                    }
                }
            })
            .then(function(response) {
                // 请求完成
                loading.style.display = 'none';
                
                // 如果流式传输没有完全填充内容，使用最终响应
                if (!botMessage.textContent) {
                    botMessage.textContent = response.data;
                }
                
                // 滚动到底部
                chatArea.scrollTop = chatArea.scrollHeight;
            })
            .catch(function(error) {
                // 错误处理
                loading.style.display = 'none';
                botMessage.textContent = `错误: ${error.message}`;
                console.error('Error:', error);
                
                // 滚动到底部
                chatArea.scrollTop = chatArea.scrollHeight;
            });
            
            // 清空消息输入框
            document.getElementById('message').value = '';
        });
        
        // 按Enter发送消息
        document.getElementById('message').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                document.getElementById('sendBtn').click();
            }
        });
        
        // 初始化
        document.addEventListener('DOMContentLoaded', function() {
            updateConnectionStatus('HTTP');
        });
    </script>
</body>
</html>
    ''')

# @bp.route('/send_message', methods=['GET', 'POST'])
# def send_message():
#     request_data = request.get_json(silent=True)
#
#     if request_data is None:
#         return {'error': 'Invalid JSON'}, 400
#
#
#     # 从请求或会话中获取用户ID，这里使用一个固定的测试值
#     user_id = request_data.get('user_id', 'test_user')
#     # Bot ID 应该从配置或请求中获取，这里使用一个固定的测试值
#     bot_id = '7536524288745766951'
#     conversation_id = int(request_data['conversation_id'])
#     message = request_data['message']
#     content = message['content']
#
#     # 暂时忽略所有附加参数attachments, tools等
#     # file处理逻辑
#     # 附加工具启动逻辑
#
#     if not content:
#         return {'error': 'Message content is required'}, 400
#
#     mimetypes = 'text/plain'
#     return Response(stream_coze_response(bot_id, user_id, content), mimetype='text/plain')