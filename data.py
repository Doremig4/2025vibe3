import pandas as pd
import plotly.graph_objects as go

# CSV 파일 불러오기 (적절한 인코딩 설정)
df = pd.read_csv("202506_202506_연령별인구현황_월간 남녀구분.csv", encoding='cp949', on_bad_lines='skip', header=None)

# 서울특별시 전체 행 선택
seoul_row = df.iloc[0]

# 연령대 열 추출
age_columns = [col for col in df.columns if '_계_' in col and any(str(i) in col or '100세 이상' in col for i in range(101))]
ages = [col.split('_')[-1].replace('"', '') for col in age_columns]
population = [int(str(seoul_row[col]).replace(" ", "").replace('"', '').replace(',', '')) for col in age_columns]

# Plotly 그래프
fig = go.Figure()
fig.add_trace(go.Scatter(x=ages, y=population, mode='lines+markers', name='서울특별시 연령별 인구'))
fig.update_layout(title='서울특별시 연령별 인구 (2025년 6월)', xaxis_title='연령', yaxis_title='인구 수', xaxis=dict(tickangle=45))
fig.show()
