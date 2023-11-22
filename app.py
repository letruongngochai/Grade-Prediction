import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from utils import *


st.set_page_config(page_title='CS313')
if __name__=='__main__':
    st.title("GRADES PREDICTION - GROUP 1")

    st.header("Thông tin sinh viên cần dự đoán:")
    # Nhập thông tin cơ bản {Tên, Giới tính, Nơi sinh, Chuyên ngành, Hệ đào tạo}
    name = st.text_input("Họ và Tên")
    cols = st.columns(2)
    sex = cols[0].selectbox('Giới tính', options=['Nam', 'Nữ'])
    address = cols[1].selectbox('Nơi sinh', options=data_address)
    cols = st.columns(2)
    major = cols[0].selectbox('Khoa', options=data_major)
    mode = cols[1].selectbox('Hệ đào tạo', options=data_mode)
    
    # Nhập thông tin các học kỳ đã học {[[năm học, học kỳ, số tín chỉ, điểm trung bình], ...]}
    num_semester = st.number_input("Số học kỳ đã học", min_value=1, max_value=22)
    sem_info = []
    for i in range(num_semester):
        cols = st.columns(4)
        year = cols[0].number_input("Năm học", min_value=2013, format="%d", key=f"se_{i+1}_1")
        semester = cols[1].number_input("Học kỳ", min_value=1, max_value=3, format="%d", key=f"se_{i+1}_2")
        credit = cols[2].number_input("Số tín chỉ", min_value=0, max_value=32, format="%d", key=f"se_{i+1}_3")
        grade = cols[3].number_input("Điểm trung bình", key=f"se_{i+1}_4") 
        sem_info.append([grade, credit, year, semester])

    # Test khi nhập thông tin sinh viên    
    cols = st.columns(5)
    if cols[2].button('Predict'):
        info = [sex, address, major, mode, sem_info]
        output = predict(info)

        points = get_points(info)
        points = np.array(points + [[len(points)+1, output[0][0]], [len(points)+2, output[0][1]]])
        points[:, 1] *= 10
        fig = display_line_chart(points)
        st.pyplot(fig)

    # Chọn sinh viên có sẵn
    st.sidebar.header('Chọn sinh viên có sẵn')
    file_path = 'data/13_19_info/final_train_dict.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    students = list(data.keys())
    student = st.sidebar.selectbox('MSSV', options=students)
    student_info = data[student]

    # Chọn học kỳ của sinh viên có sẵn
    cols = st.sidebar.columns(4)
    student_selectbox = []
    student_input = student_info[0]
    student_points = []
    student_points_min = 0 
    for i in range(0, len(student_info)-3):
        student_selectbox.append(cols[i%4].checkbox(f'Kỳ thứ {i+1}'))
        if student_selectbox[i]: 
            student_input = student_input + student_info[i+1]
            student_points.append([i+1, student_info[i+1][1]*10])
            student_points_min = i + 1
    student_points_gt = []
    student_points_gt.append([student_points_min+1, student_info[student_points_min+1][1]*10])
    student_points_gt.append([student_points_min+2, student_info[student_points_min+2][1]*10])

    # Test khi chọn sinh viên có sẵn 
    cols = st.sidebar.columns(5)
    if cols[2].button('Predict', key='b_predict') and len(student_input)>13:
        output = predict2(student_input)
        student_points_pred = []
        student_points_pred.append([student_points_min+1, output[0][0]*10])
        student_points_pred.append([student_points_min+2, output[0][1]*10])

        fig = display_lines_chart(np.array(student_points), np.array(student_points_gt), np.array(student_points_pred))
        st.pyplot(fig)

    