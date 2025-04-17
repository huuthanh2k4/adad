# Comment thông tin nhóm và link website
# Thành viên nhóm: Phạm Hữu Thành
# Link website: https://2221060786-phamhuuthanh.streamlit.app/

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Đọc và làm sạch dữ liệu
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")
print(movies_data.info())
movies_data = movies_data.dropna()
print(movies_data.describe())

# Tiêu đề ứng dụng
st.title("Phân Tích Dữ Liệu Phim")

# Hiển thị thông tin cơ bản về dữ liệu
st.write('Thông tin cơ bản về dữ liệu')
st.write('Dữ liệu chứa các cột như: tên phim, thể loại, năm phát hành, điểm số, ngân sách, doanh thu, v.v.')
st.write('Tổng số phim:',len(movies_data))


st.sidebar.header("Bộ lọc dữ liệu")
score_range = st.sidebar.slider("Chọn khoảng điểm", 
                                min_value=1.0, max_value=10.0, value=(3.0, 6.0), step=0.1)
genres = st.sidebar.multiselect("Chọn thể loại", 
                                options=movies_data['genre'].unique(), 
                                default=["Animation", "Horror", "Fantasy", "Romance"])
selected_year = st.sidebar.selectbox("Chọn năm", 
                                     options=sorted(movies_data['year'].unique()), 
                                     index=0)
 

if not genres:
    genres = movies_data['genre'].unique()

if not selected_year:
    selected_year = movies_data['year'].unique()

filtered_data = movies_data[
    (movies_data['year'] == selected_year) &
    (movies_data['genre'].isin(genres)) &
    (movies_data['score'] >= score_range[0]) &
    (movies_data['score'] <= score_range[1])
]


st.subheader("Danh sách phim đã lọc")
st.dataframe(filtered_data[['name', 'genre', 'year', 'score']])

avg_score = movies_data.groupby('genre')['score'].mean().reset_index()
fig, ax = plt.subplots()
ax.plot(avg_score['genre'], avg_score['score'], marker='o', color='blue')
ax.set_xlabel('Thể loại')
ax.set_ylabel('Điểm trung bình')
ax.set_title('Điểm trung bình của các thể loại phim')
plt.xticks(rotation=45)
st.pyplot(fig)



avg_budget = movies_data.groupby('genre')['budget'].mean().reset_index()    
fig, ax = plt.subplots()
ax.bar(avg_budget['genre'], avg_budget['budget'], color='r')
ax.set_xlabel('Thể loại')
ax.set_ylabel('Ngân sách trung bình')
ax.set_title('Ngân sách trung bình của các thể loại phim')
plt.xticks(rotation=45)
st.pyplot(fig)
