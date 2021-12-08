from flask import Flask, request, jsonify
import handler
app = Flask(__name__)


@app.route('/forum', methods=['POST', 'GET'])
def forum():
    recv = request.get_json()  # 提取报文GEvent信息
    recv = handler.handler(recv)
    return jsonify(recv)  # 返回json报文


if __name__ == '__main__':
    # 多线程启动后端服务器
    app.run(host="0.0.0.0", debug=True, threaded=True)
