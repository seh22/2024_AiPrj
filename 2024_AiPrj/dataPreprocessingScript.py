import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

#한국어 처리 모델 로드
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

#Excel 파일 로드
df = pd.read_excel('Text_1.xlsx')

#Excle 파일 데이터 전처리
df = df[~df['챗봇'].isna()] # 챗봇 열 Null일 경우 행 삭제
df['embedding'] = pd.Series([[]] * len(df)) #embedding 값 저장을 위한 열 추가
df['embedding'] = df['유저'].map(lambda x: list(model.encode(x).tolist())) #유저 행 데이터를 기반으로 embedding 값 계산 후 열에 데이터 추가

#처리된 데이터 Excel 저장
df.to_csv("PreprocessingData.csv",index=False)


