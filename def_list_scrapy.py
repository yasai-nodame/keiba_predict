import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import pprint


#引数に競馬のリンクのリストを取得した関数処理
def txt_r_value(race_link_list): #リンクの入ったリストを引数に取得
    #リンクのページを取得
    url = 'https://db.netkeiba.com'+race_link_list 
    
    response = requests.get(url)
    
    response.encoding = 'UTF-8'
    
    soup = BeautifulSoup(response.content,'html.parser')
    
    
    #for文でスクレイピングしたtdタグのtxt_1データを取得
    txt_r = soup.find_all('td',class_='txt_r')
    
    txt1_name_list = [] #空のリスト
    txt_c_list = []
    txt_r_list = []
    # for element in  txt_1:
    #     s = element.text.replace('[西]','').strip()
    #     txt1_name_list.append(s)
    #     for i in range(len(txt1_name_list)):
    #         if i % 4 == 0:
    #             txt1_name_list.remove(i)
    
    for element in txt_r:
        s = element.text
        
        if s != '':
            txt_r_list.append(s)
    
    print(txt_r_list)
    
    del txt_r_list[4]
    del txt_r_list[8] 
    del txt_r_list[12] 
    del txt_r_list[16] 
    del txt_r_list[20]  
    
    # txt_r_list[64:80] = [] race_link_list[0]でしか適用されないスライド処理
    
    
    
    division = [txt_r_list[i:i+4] for i in range(0, len(txt_r_list),4)] #リストしたtxt_rを4分割にしてカラムの数に合わせる
    
    df = pd.DataFrame(division) #データフレームで表確認
    df.columns = ['in order of arrival','hourse number','time','odds']
    
    df_contact = pd.concat([df,txt_l_value(race_link_list),txt_c_value(race_link_list)],axis=1) #txt_l_value(race_link_list)の戻り値txt_lタグのデータとtxt_rタグのデータを結合して表示
    
    # df_contact.to_csv('KeibaSample.csv')
    
    return df_contact
    #4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79
    
    
    
def txt_l_value(race_link_list):
    #リンクのページを取得
    url = 'https://db.netkeiba.com'+race_link_list 
    
    response = requests.get(url)
    
    response.encoding = 'UTF-8'
    
    soup = BeautifulSoup(response.content,'html.parser')
    
    
    txt_l = soup.find_all('td',class_='txt_l')
    
    #txt_lタグは馬名、騎手、調教師、馬主の枠なのでとりあえず４つのカラムを作り、後で馬名、騎手のカラムの値を数値化に置換。調教師、馬主のカラムはdropで削除する。
    txt_l_list = [] #ここに馬名、騎手、調教師、馬主を追加していく。
    
    for element in txt_l:
        str = element.text.replace('[西]','').strip() #[西]と両端の空文字を削除
        txt_l_list.append(str)
    
    
    division = [txt_l_list[i:i+4] for i in range(0,len(txt_l_list),4)]
    df = pd.DataFrame(division)
    df.columns = ['hourse_name','rider','trainer','hourse_owner']
    
    return df
    
def txt_c_value(race_link_list):
    
    txt_c_list = [] #ここに斤量と性別を入れていく。
    
    #リンクのページを取得
    url = 'https://db.netkeiba.com'+race_link_list 
    
    response = requests.get(url)
    
    response.encoding = 'UTF-8'
    
    soup = BeautifulSoup(response.content,'html.parser')
    
    txt_c = soup.find_all('td',class_='txt_c')
    
    for element in txt_c:
        str = element.text.strip()
        txt_c_list.append(str)
        
    
    #defference_in_raceカラムの最初のレコードが空文字なので0に置換させて数字を揃える
    txt_c_list.insert(2,txt_c_list[2].replace('','0') )
    
    txt_c_list = list(filter(None,txt_c_list)) #filter()を使って空文字を除去する。
    
    division = [txt_c_list[i:i+4] for i in range(0,len(txt_c_list),4)]
    df = pd.DataFrame(division)
    df.columns = ['sex','weight','difference_in_race','climb']
    
    return df

