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

# 데이터 로드 df 데이터 프레임에 저장
DATA_FILE = 'PreprocessingData.csv'
df = pd.read_csv(DATA_FILE)
df['embedding'] = df['embedding'].apply(json.loads)

# ChatGPT 응답 생성 함수
def get_gpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 상담가야 상담시 줄 수 있는 짧은 답변을 줘"},
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
    global df  # 전역 데이터프레임 업데이트
    user_input = request.json.get('message', '')  # 사용자 입력 메시지
    embedding = model.encode(user_input)  # 입력 텍스트 임베딩 생성
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    max_similarity = df['distance'].max()
    answer = df.loc[df['distance'].idxmax()]  # 가장 유사한 질문 가져오기

    # 유사도가 90% 이하인 경우 GPT로 응답 생성
    if max_similarity < 0.90:
        bot_answer = get_gpt_response(user_input)
        category = "GPT-Generated"  # 새로운 데이터의 기본 카테고리
        similarity = max_similarity

        # 새로운 데이터 추가
        new_entry = {
            '구분': category,
            '유저': user_input,
            '챗봇': bot_answer,
            'embedding': json.dumps(embedding.tolist())
        }
        user_df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

        print(user_df)
        # CSV 파일로 데이터 저장
        # new_file_name = 'UpdatedDataset.csv'  # 저장될 새로운 파일 이름
        # df.to_csv(new_file_name, index=False, encoding='utf-8-sig')  # UTF-8 인코딩으로 CSV 저장

    else:
        bot_answer = answer['챗봇']
        category = answer['구분']
        similarity = max_similarity

    # 응답 반환
    response = {
        'category': category,
        'bot_answer': bot_answer,
        'similarity': similarity
    }
    return jsonify(response)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # HTML 파일 반환

if __name__ == '__main__':
    app.run(debug=True)

