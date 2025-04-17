import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Đọc và làm sạch dữ liệu
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")
movies_data = movies_data.dropna()  # Loại bỏ các hàng có giá trị thiếu

# Tiêu đề chính của trang web
st.title("Interactive Dashboard")
st.write("Interact with this dashboard using the widgets on the sidebar.")

# Sidebar: Các widget tương tác
st.sidebar.header("Bộ lọc dữ liệu")
score_range = st.sidebar.slider("Chọn khoảng điểm (score)", 
                                min_value=1.0, max_value=10.0, value=(3.0, 6.0), step=0.1)
genres = st.sidebar.multiselect("Chọn thể loại", 
                                options=movies_data['genre'].unique(), 
                                default=["Animation", "Horror", "Fantasy", "Romance"])
years = sorted(movies_data['year'].unique())
selected_year = st.sidebar.selectbox("Chọn năm", years, index=years.index(1980) if 1980 in years else 0)

# Lọc dữ liệu dựa trên lựa chọn của người dùng
filtered_data = movies_data[
    (movies_data['year'] == selected_year) &
    (movies_data['genre'].isin(genres)) &
    (movies_data['score'] >= score_range[0]) &
    (movies_data['score'] <= score_range[1])
]

# Main content: Hiển thị bảng dữ liệu đã lọc
st.subheader("Danh sách phim theo năm và thể loại")
st.dataframe(filtered_data[['name', 'genre', 'year', 'score']])

# Tính điểm trung bình theo thể loại và vẽ biểu đồ đường
avg_score = movies_data.groupby('genre')['score'].mean().reset_index()
fig_score, ax = plt.subplots(figsize=(12, 6))
ax.plot(avg_score['genre'], avg_score['score'], marker='o', color='blue')
ax.set_xlabel('Thể loại')
ax.set_ylabel('Điểm trung bình')
ax.set_title('Điểm trung bình của các thể loại phim')
plt.xticks(rotation=45)
st.pyplot(fig_score)

# Tính và hiển thị ngân sách trung bình theo thể loại
st.subheader("Ngân sách trung bình của các bộ phim theo thể loại")
avg_budget = movies_data.groupby('genre')['budget'].mean().round().reset_index()
st.dataframe(avg_budget)

# Vẽ biểu đồ cột cho ngân sách trung bình
fig_budget = plt.figure(figsize=(12, 6))
plt.bar(avg_budget['genre'], avg_budget['budget'], color='maroon')
plt.xlabel('Thể loại')
plt.ylabel('Ngân sách trung bình')
plt.title('Biểu đồ cột hiển thị ngân sách trung bình của phim theo thể loại')
plt.xticks(rotation=45)
st.pyplot(fig_budget)