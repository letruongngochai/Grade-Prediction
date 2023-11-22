import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import math
import os
import pickle

# data_range = {
#     'dtb': [df_raw['dtbhk'].min(), df_raw['dtbhk'].max()],
#     'tc': [df_raw['sotchk'].min(), df_raw['sotchk'].max()], 
#     'tg': [1, df_raw.groupby('mssv').count().hocky.max()]
# }
data_range = {
    'dtb': [0, 10],
    'tc': [0, 32], 
    'tg': [1, 22]
} 

data_address = ["Hà Nội", "Hồ Chí Minh", "Hải Phòng", "Đà Nẵng", "Cần Thơ", "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn",
              "Bạc Liêu", "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau", "Cao Bằng", "Đắk Lắk",
              "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình",
              "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An",
              "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh",
              "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái",
              "Cộng hoà Séc", "Campuchia", "Australia", "Liên Bang Nga"]

data_major = ['khoa_CNPM', 'khoa_HTTT', 'khoa_KHMT', 'khoa_KTMT', 'khoa_KTTT', 'khoa_MMT&TT']

data_mode = ['hedt_CLC', 'hedt_CNTN', 'hedt_CQUI', 'hedt_CTTT', 'hedt_KSTN']

data_dict_sex = {
    'Nam': 1, 
    'Nữ': 0
}

data_dict_address = {'Campuchia': 0.0, 'Australia': 0.0, 'Cộng hoà Séc': 0.0, 'Liên Bang Nga': 0.0, 
                     'Hà Nội': 0.256975698, 'Hồ Chí Minh': 0.092592593, 'Hải Phòng': 0.522727273, 'Đà Nẵng': 0.111111111, 
                     'Hà Giang': 0.75, 'Cao Bằng': 0.75, 'Lai Châu': 0.75, 'Lào Cai': 0.75, 'Tuyên Quang': 0.75, 
                     'Lạng Sơn': 0.75, 'Bắc Kạn': 0.75, 'Thái Nguyên': 0.664473684, 'Yên Bái': 0.75, 'Sơn La': 0.75, 
                     'Phú Thọ': 0.55, 'Vĩnh Phúc': 0.652439244, 'Quảng Ninh': 0.698453682, 'Bắc Giang': 0.716346154, 
                     'Bắc Ninh': 0.444444444, 'Hải Dương': 0.526315789, 'Hưng Yên': 0.458333333, 'Hòa Bình': 0.75, 'Hà Nam': 0.4375, 
                     'Nam Định': 0.477272727, 'Thái Bình': 0.472222222, 'Ninh Bình': 0.684215263, 'Thanh Hóa': 0.734482759, 
                     'Nghệ An': 0.71, 'Hà Tĩnh': 0.671641791, 'Quảng Bình': 0.721428571, 'Quảng Trị': 0.663793134, 
                     'Thừa Thiên Huế': 0.7, 'Quảng Nam': 0.68125, 'Quảng Ngãi': 0.676136364, 'Kon Tum': 0.75, 'Bình Định': 0.7, 
                     'Gia Lai': 0.75, 'Đắk Lắk': 0.75, 'Khánh Hòa': 0.698113275, 'Lâm Đồng': 0.75, 'Bình Phước': 0.6875, 
                     'Bình Dương': 0.361111111, 'Ninh Thuận': 0.745454545, 'Tây Ninh': 0.6125, 'Bình Thuận': 0.616557377, 
                     'Đồng Nai': 0.783333333, 'Long An': 0.6875, 'Đồng Tháp': 0.613636364, 'An Giang': 0.67, 'Bà Rịa - Vũng Tàu': 0.65, 
                     'Tiền Giang': 0.535714286, 'Kiên Giang': 0.715277778, 'Cần Thơ': 0.13125, 'Bến Tre': 0.656976744, 
                     'Vĩnh Long': 0.441176476, 'Trà Vinh': 0.646396396, 'Sóc Trăng': 0.625, 'Bạc Liêu': 0.561851852, 'Cà Mau': 0.646972165, 
                     'Điện Biên': 0.75, 'Đắk Nông': 0.75, 'Hậu Giang': 0.61
}

data_dict_major = {
    'khoa_CNPM': [1, 0, 0, 0, 0, 0], 
    'khoa_HTTT': [0, 1, 0, 0, 0, 0], 
    'khoa_KHMT': [0, 0, 1, 0, 0, 0], 
    'khoa_KTMT': [0, 0, 0, 0, 1, 0], 
    'khoa_KTTT': [0, 0, 0, 0, 0, 1], 
    'khoa_MMT&TT': [0, 0, 0, 1, 0, 0]
}

data_dict_mode = {
    'hedt_CLC': [0, 0, 0, 1, 0], 
    'hedt_CNTN': [0, 0, 1, 0, 0], 
    'hedt_CQUI': [1, 0, 0, 0, 0], 
    'hedt_CTTT': [0, 1, 0, 0, 0], 
    'hedt_KSTN': [0, 0, 0, 0, 1]
}



def minmax_scale(value, min, max):
    return (value - min)/(max - min)

def load_data(data_path, input_dim, output_dim):
    with open(data_path, 'r') as f:
        data_dict = json.load(f)
    X, y = [], []
    for mssv, infos in data_dict.items():
        for i in range(input_dim+1, len(infos)-output_dim+1):
            X.append(np.concatenate((infos[0], np.array(infos[i-input_dim:i]).flatten()), axis=0))
            y.append(np.array(infos[i:i+output_dim])[:, 0])
            
    return np.array(X), np.array(y) 

def find_two_factors(n):
    a = 2
    b = n // 2
    while True:
        if a*b == n:
            while b>a*2 and a%2==0 and b%2==0:
                b //= 2
                a *= 2
            return a, b
        elif a*b > n:
            b -= 1
        else:
            a += 1

def visualize_result(y_prev, y_pred, y_true):
    num_sample = len(y_true)
    num_rows, num_cols = find_two_factors(num_sample)
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(4*num_cols, 2*num_rows))
    for i in range(num_sample): 
        row = i//num_cols 
        col = i%num_cols 
        axes[row][col].plot(np.concatenate((y_prev[i], y_pred[i])), color='red', label='Predicted')
        axes[row][col].plot(np.concatenate((y_prev[i], y_true[i])), color='blue', label='True')
        axes[row][col].legend()
        plt.tight_layout()
    plt.show()

def save_result(file_path, method_name, method_time, mse):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if method_name in df['method'].values:
            df.loc[df['method'] == method_name, ['time', 'mse']] = [method_time, mse]
        else:
            result = {'method': method_name, 'time': method_time, 'mse': mse}
            df = df.append(result, ignore_index=True)
            print(df)
        df.to_csv(file_path, index=False)
    else:
        result = {'method': [method_name], 'time': [method_time], 'mse': [mse]}
        pd.DataFrame(result).to_csv(file_path, index=False)

def convert_infor2input(info): 
    '''
    info = [sex, address, major, mode, sem_info] 
        sem_info = [
            [grade, credit, year, sem]
    ]
    '''
    input = []
    input.append(data_dict_sex[info[0]])
    input.append(data_dict_address[info[1]])
    input = input + data_dict_major[info[2]] + data_dict_mode[info[3]]

    if len(info[4]) > 6:
        for id, sem in enumerate(info[4][-6:]): 
            grade = minmax_scale(sem[0], data_range['dtb'][0], data_range['dtb'][1])
            tc = minmax_scale(sem[1], min=data_range['tc'][0], max=data_range['tc'][1])
            tg = minmax_scale(id + len(info[4]) - 5, data_range['tg'][0], data_range['tg'][1])
            input = input + [grade, tc, tg]
    else: 
        for id, sem in enumerate(info[4][:]): 
            grade = minmax_scale(sem[0], data_range['dtb'][0], data_range['dtb'][1])
            tc = minmax_scale(sem[1], min=data_range['tc'][0], max=data_range['tc'][1])
            tg = minmax_scale(id + 1, data_range['tg'][0], data_range['tg'][1])
            input = input + [grade, tc, tg]
    return input 

def predict(info): 
    input = convert_infor2input(info)
    num_input = 6 if len(info[4])>6 else len(info[4])
    model_path = f'models/rdfr_{num_input}_2'
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model.predict([input])

def predict2(input): 
    num_input = 6 if (len(input)-13)//3 > 6 else (len(input)-13)//3
    model_path = f'models/rdfr_{num_input}_2'
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model.predict([input])

def display_line_chart(points):
    x = points[:, 0]
    y = points[:, 1]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y)
    ax.set_xlabel('Học kỳ')
    ax.set_ylabel('Điểm trung bình')
    ax.set_ylim([0, 11])
    x_ticks = range(len(x))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)

    colors = np.linspace(0, 1, len(y))
    for i in range(len(x)):
        if i > len(points)-3:
            if y[i] < y[i-1]:
                ax.scatter(x[i], y[i], c=[(1, 0, 0, colors[i])], s=50, zorder=3)
            elif y[i] > y[i-1]:
                ax.scatter(x[i], y[i], color='green', s=50, zorder=3)
        else:
            ax.scatter(x[i], y[i], color='blue', s=50, zorder=3)
        ax.annotate(round(y[i], 2), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    ax.grid(alpha=0.3)
    ax.set_title('Điểm trung bình học tập sinh viên các kỳ')
    return fig 

def display_lines_chart(points, points_gt, points_pred):
    x = points[:, 0]
    y = points[:, 1]
    x_gt = points_gt[:, 0]
    y_gt = points_gt[:, 1]
    x_pred = points_pred[:, 0]
    y_pred = points_pred[:, 1]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(np.concatenate((x,x_pred)), np.concatenate((y,y_pred)), color='orange')
    ax.plot(np.concatenate((x,x_gt)), np.concatenate((y,y_gt)), color='blue')
    ax.set_xlabel('Học kỳ')
    ax.set_ylabel('Điểm trung bình')
    ax.set_ylim([0, 11])
    x_ticks = range(len(x)+2)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)

    for i in range(len(x)):
        ax.scatter(x[i], y[i], color='blue', s=50, zorder=3)
        ax.annotate(round(y[i], 2), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
    
    for i in range(len(x_gt)):
        ax.scatter(x_gt[i], y_gt[i], color='blue', s=50, zorder=3)
        ax.annotate(round(y_gt[i], 2), (x_gt[i], y_gt[i]), textcoords="offset points", xytext=(0,10), ha='center')

    if y_pred[0] < y[-1]:
        ax.scatter(x_pred[0], y_pred[0], color='red', s=50, zorder=3)
    else:
        ax.scatter(x_pred[0], y_pred[0], color='green', s=50, zorder=3)
    ax.annotate(round(y_pred[0], 2), (x_pred[0], y_pred[0]), textcoords="offset points", xytext=(0,10), ha='center')
    if y_pred[1] < y_pred[0]:
        ax.scatter(x_pred[1], y_pred[1], color='red', s=50, zorder=3)
    else:
        ax.scatter(x_pred[1], y_pred[1], color='green', s=50, zorder=3)
    ax.annotate(round(y_pred[1], 2), (x_pred[1], y_pred[1]), textcoords="offset points", xytext=(0,10), ha='center')

    ax.grid(alpha=0.3)
    ax.set_title('Điểm trung bình học tập sinh viên các kỳ')
    return fig 

def get_points(info):
    points = []
    if len(info[4]) > 6:
        for id, sem in enumerate(info[4][-6:]): 
            grade = sem[0]
            tg = id + len(info[4]) - 5
            points.append([tg, grade])
    else: 
        for id, sem in enumerate(info[4][:]): 
            grade = sem[0]
            tg = id + 1
            points.append([tg, grade])
    return points

if __name__ == '__main__':
    # file_path = 'data_raw/standardized_diemcongkhuvuc.xlsx'
    # data = pd.read_excel(file_path)

    # output = {}
    # for index, row in data.iterrows():
    #     key = row[0]
    #     value = row[1]
    #     output[key] = value

    # print(output)
    pass







