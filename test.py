import streamlit as st
import pandas as pd
import requests
import urllib.parse
from PIL import Image
import os

# CSVファイルを読み込む
df = pd.read_csv('type2.csv')

st.title('Bizbuddy')
st.write('起業・副業を考える上で大事にしたいことを選択してください')

# ドロップダウンメニューを表示
options = ['多くの人に影響を与えていきたい', '分析や戦略を立てて行動したい', '周囲の人とはぶつかりたくない', '周囲の人や物事を動かしていきたい', '自分の好きを極めていきたい', '社会課題を解決したい']
selected_option = st.selectbox("6つの項目から一つ選択してください", options)

# 選択肢に対応する行を抽出
filtered_df = df[df['マークダウン選択内容'] == selected_option]

# 起業家・経営者画像のサイズを定義
image_width = 220

if not filtered_df.empty:
    st.write('以下はあなたの志向に近い起業家・経営者です：')
    
    # 選択された選択肢に対応する行を表示
    for index, row in filtered_df.iterrows():
        st.write(f"**{row['人物名']}**")
        
        # 画像のパスを取得
        image_path = os.path.join(os.getcwd(), row['人物画像'])
        
        # 画像とテキストを横に配置
        col1, col2 = st.columns([2, 3])
        with col1:
            # 画像を表示
            image = Image.open(image_path)
            st.image(image, width=image_width)
        with col2:
            st.write(f"実績：{row['実績']}")
            st.write(f"特徴：{row['特徴']}")
        
        # 著者名でAPIに書籍を検索する
        author_name = row['人物名']
        query = urllib.parse.urlencode({"author": author_name})
        app_id = "1043474443048754357"
        url = f"https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?{query}&applicationId={app_id}"
        response = requests.get(url)

        try:
            books = response.json()["Items"]
        except KeyError:
            books = []

        # 書籍を表示する
        if books:
            st.write(f"**{author_name} の著書 (上位3件):**")
            top_books = sorted(books, key=lambda x: x["Item"]["reviewCount"], reverse=True)[:3]
            for book in top_books:
                title = book["Item"]["title"]
                link = book["Item"]["itemUrl"]
                image_url = book["Item"]["largeImageUrl"].replace("?_ex=200x200", "")
                
                # リンクと画像を中央に配置
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"[{title}]({link})", unsafe_allow_html=True)
                with col2:
                    st.image(image_url, width=100)
        else:
            st.write(f"**{author_name}** の著書は見つかりませんでした。")
else:
    st.write("該当する起業家・経営者は見つかりませんでした。他の選択肢を試してみてください。")