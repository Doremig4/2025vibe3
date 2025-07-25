import streamlit as st
import random

st.title("가위바위보 게임")

choices = ["가위", "바위", "보"]
user_choice = st.radio("당신의 선택은?", choices, horizontal=True)

if st.button("결과 확인!"):
    computer_choice = random.choice(choices)
    st.write(f"컴퓨터의 선택: {computer_choice}")

    # 승패 판정
    if user_choice == computer_choice:
        result = "무승부!"
    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "승리!"
    else:
        result = "패배!"
    st.subheader(result)