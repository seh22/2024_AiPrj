from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)
# 모델 로드
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 데이터 로드
df = pd.read_csv('PreprocessingData.csv')  # 데이터 파일
df['embedding'] = df['embedding'].apply(json.loads)  # JSON 문자열을 리스트로 변환

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    embedding = model.encode(user_input)  # 입력 텍스트 임베딩
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]  # 가장 유사한 응답 찾기

    response = {
        'category': answer['구분'],
        'bot_answer': answer['챗봇'],
        'similarity': answer['distance']
    }
    return jsonify(response)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # HTML 파일 서빙

if __name__ == '__main__':
    app.run(debug=True)
