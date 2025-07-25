import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSV 시각화 앱", layout="wide")

st.title("📊 CSV 파일 시각화 앱")
st.write("업로드한 CSV 파일을 다양한 방식으로 시각화할 수 있습니다.")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.subheader("📄 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    # 컬럼 선택
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_cols = df.columns.tolist()

    if numeric_cols:
        st.subheader("📈 그래프 설정")
        chart_type = st.selectbox("차트 종류", ["선 그래프", "막대 그래프", "산점도"])

        x_axis = st.selectbox("X축 선택", all_cols)
        y_axis = st.multiselect("Y축 선택 (하나 이상)", numeric_cols, default=numeric_cols[:1])

        if x_axis and y_axis:
            for y in y_axis:
                if chart_type == "선 그래프":
                    fig = px.line(df, x=x_axis, y=y, title=f"{y} vs {x_axis}")
                elif chart_type == "막대 그래프":
                    fig = px.bar(df, x=x_axis, y=y, title=f"{y} vs {x_axis}")
                elif chart_type == "산점도":
                    fig = px.scatter(df, x=x_axis, y=y, title=f"{y} vs {x_axis}")

                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("시각화할 수 있는 숫자형 컬럼이 없습니다.")
