import streamlit as st
import pandas as pd
import calendar

def show():
    st.subheader("📆 분기별 판매량")

    if "purchase_table" not in st.session_state:
        st.warning("구매내역 데이터가 없습니다. '엑셀 업로드' 탭에서 파일을 업로드하고 저장하세요.")
        return

    df = st.session_state["purchase_table"].copy()
    df["구매일"] = pd.to_datetime(df["구매일"])
    df["년도"] = df["구매일"].dt.year
    df["월"] = df["구매일"].dt.month

    # 현재 연도 기준 필터링
    current_year = pd.Timestamp.today().year
    df = df[df["년도"] == current_year]

    options = {
        "1분기": [1, 2, 3],
        "2분기": [4, 5, 6],
        "3분기": [7, 8, 9],
        "4분기": [10, 11, 12],
        "상반기": [1, 2, 3, 4, 5, 6],
        "하반기": [7, 8, 9, 10, 11, 12],
        "전기": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }

    period = st.radio("기간 선택", list(options.keys()) + ["직접 기간 선택"], horizontal=True)

    if period != "직접 기간 선택":
        selected_months = options[period]
        start_month = min(selected_months)
        end_month = max(selected_months)

        # 시작일과 종료일 계산
        start_date = pd.Timestamp(f"{current_year}-{start_month:02d}-01")
        last_day = calendar.monthrange(current_year, end_month)[1]
        end_date = pd.Timestamp(f"{current_year}-{end_month:02d}-{last_day}")
    else:
        with st.expander("📅 기간 직접 선택"):
            start_date = st.date_input("시작일", value=pd.to_datetime(f"{current_year}-01-01"), key="start_date")
            end_date = st.date_input("종료일", value=pd.to_datetime(f"{current_year}-12-31"), key="end_date")

    if start_date and end_date:
        filtered_df = df[(df["구매일"] >= pd.to_datetime(start_date)) & (df["구매일"] <= pd.to_datetime(end_date))]
    else:
        filtered_df = pd.DataFrame()

    if not filtered_df.empty:
        st.markdown(f"### 📦 판매량 요약 ({start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')})")
    else:
        st.markdown("### 📦 판매량 요약 (선택한 기간에 데이터가 없습니다.)")

    if filtered_df.empty:
        st.warning("선택한 기간에 해당하는 판매 데이터가 없습니다.")
        return

    st.write(f"총 판매 수: {len(filtered_df)}건")
    st.write(f"총 판매 금액: {filtered_df['가격'].sum():,}원")
    st.write(f"평균 책 가격: {filtered_df['가격'].mean():.2f}원")

    st.markdown("### 🧾 판매 테이블")
    st.dataframe(filtered_df)

    st.markdown("### 📊 월별 판매 건수")
    month_counts = filtered_df["월"].value_counts().sort_index()
    st.bar_chart(month_counts)