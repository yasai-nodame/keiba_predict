import streamlit as st
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt
import time

#タイトル
st.title("競馬予測アプリ")

#以下をサイドバーに表示
st.sidebar.markdown('### 予測に使う競馬データを入力してください')

#ファイルアップロード
uploaded_file = st.sidebar.file_uploader('### ファイルを入力してください',type='csv')


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,encoding='SHIFT-JIS',index_col=0)
    
    
    #相関の確認
    if st.button('相関関係を確認'):
        comment = st.empty()
        comment.write('### 相関確認を確認しています。少々お待ち下さい。')
        time.sleep(2)
        
        my_bar = st.progress(0)
        
        for percent_compleate in range(100):
            time.sleep(0.02)     
        
            my_bar.progress(percent_compleate + 1)
        
        df1 = df.corr()
        st.dataframe(df1)
    
    
    
    
    #目的変数と説明変数を選択制にする。
    df_columns = df.columns
    
    #説明変数は複数選択可
    x = st.multiselect('説明変数を選択してください(複数選択可)',df_columns)
    
    #目的変数は一つ選択可
    y = st.selectbox('目的変数を選択してください',df_columns)
    
    #重回帰分析を行う
    st.markdown('機械学習を実行します。')
    
    execute = st.button('実行')
    
    
    #実行ボタンが押された後の処理
    if execute:
        X = df[x] #説明変数
        Y = df[y] #目的変数
        
        x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3)
        
        my_bar = st.progress(0)
        
        #プログレスバーを用意
        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1)
            
        
        model = LinearRegression()      
        model.fit(x_train,y_train)
        model.score(x_test,y_test)
        
        Y_pred = model.predict(X)
        A1 = model.score(x_test,y_test)
        A1 = str(math.ceil(A1*100))
        
        Y_pred = Y_pred.tolist()
        Y_pred = [round(Y_pred[n],2) for n in range(len(Y_pred))]
        
        X['Predict'] = Y_pred
        X = X.style.set_properties(subset=['Predict'])
        
        name = '精度は'+ A1 +'%です。'
        st.dataframe(X)
        
        com = st.empty()
        com.write(name)
        
    
