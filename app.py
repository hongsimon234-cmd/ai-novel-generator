from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app) # 구글 시트와의 통신 허용

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        return "✅ Novel Server is Active!"
    
    try:
        data = request.json
        topic = data.get('topic', '')
        if not topic:
            return jsonify({"error": "주제가 없습니다."}), 400

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 천재 소설가입니다. 깊이 있는 서사와 대사를 작성하세요."},
                {"role": "user", "content": f"주제: {topic}"}
            ],
            temperature=0.8
        )
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
