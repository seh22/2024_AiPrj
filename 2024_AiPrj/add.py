from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import openai

app = Flask(__name__)

# OpenAI API 키 설정 (유효한 키로 변경 필요)
openai.api_key = ''

# 모델 로드
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 데이터 파일 경로
DATA_FILE = 'PreprocessingData.csv'
GPT_DATA_FILE = 'GptNullData.csv'
USER_DATA_FILE = 'UserData.csv'

# 초기 데이터 병합 (서버 시작 시에만 호출)
df = pd.concat([
    pd.read_csv(DATA_FILE).assign(embedding=lambda x: x['embedding'].apply(json.loads)),
    pd.read_csv(GPT_DATA_FILE).assign(embedding=lambda x: x['embedding'].apply(json.loads))
], ignore_index=True)

# ChatGPT 응답 생성 함수
def get_gpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 심리 상담가야 상담시 줄 수 있는 짧은 답변을 줘 전문가 상담 권유는 심각할 때만 해줘"},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200,
            temperature=0.6
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error with GPT API: {e}")
        return "죄송합니다. 현재 응답을 생성할 수 없습니다."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')  # 사용자 입력 메시지
    embedding = model.encode(user_input)  # 입력 텍스트 임베딩 생성

    # 데이터 파일 로드
    data_df = pd.concat([
        pd.read_csv(DATA_FILE).assign(embedding=lambda x: x['embedding'].apply(json.loads)),
        pd.read_csv(GPT_DATA_FILE).assign(embedding=lambda x: x['embedding'].apply(json.loads)),
        pd.read_csv(USER_DATA_FILE).assign(embedding=lambda x: x['embedding'].apply(json.loads)) if USER_DATA_FILE else pd.DataFrame()
    ], ignore_index=True)

    # 유사도 계산
    data_df['distance'] = data_df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    max_similarity = data_df['distance'].max()
    answer = data_df.loc[data_df['distance'].idxmax()]  # 가장 유사한 질문 가져오기

    # 유사도가 90% 이하인 경우 GPT로 응답 생성
    if max_similarity < 0.90:
        bot_answer = get_gpt_response(user_input)
        category = answer['구분']  # 새로운 데이터의 기본 카테고리

        # 새로운 데이터 추가
        new_entry = {
            '구분': category,
            '유저': user_input,
            '챗봇': bot_answer,
            'embedding': json.dumps(embedding.tolist())
        }

        # 기존 데이터 파일에 추가 저장
        try:
            user_data_df = pd.read_csv(USER_DATA_FILE).assign(embedding=lambda x: x['embedding'].apply(json.loads))
        except FileNotFoundError:
            user_data_df = pd.DataFrame()

        user_data_df = pd.concat([user_data_df, pd.DataFrame([new_entry])], ignore_index=True)
        user_data_df.to_csv(USER_DATA_FILE, index=False)
    else:
        bot_answer = answer['챗봇']
        category = answer['구분']

    # 응답 반환
    response = {
        'category': category,
        'bot_answer': bot_answer,
        'similarity': max_similarity
    }
    return jsonify(response)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # HTML 파일 반환

if __name__ == '__main__':
    app.run(debug=True)
