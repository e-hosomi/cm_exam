# %%
import datetime
import requests
import os

# 現在の日付
current_date = datetime.date.today()

# ケアマネ試験日
exam_date = datetime.date(2024, 10, 13)

# 二つの日付の差を計算
diff = exam_date - current_date

daycount_txt = '''
{}/{}/{}

ケアマネ試験日：
2024年10月13日（日）

ケアマネ試験日まで
あと{}日!'''.format(current_date.year, current_date.month, current_date.day, diff.days)

# Format the current date to match the file names
formatted_date = current_date.strftime("%Y-%m-%d")

#アクセストークンを以下に設定（LINE Notifyのwebサイトで発行したトークンを貼り付け）
acc_token = 'Jo7Hdbdhay7UuqKcQbEBeaxt9eTeTuhyOJYqRmfBoSd'

def send_line(msg):
    # サーバーに送るパラメータを用意
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + acc_token}
    payload = {'message': msg}
    requests.post(url, headers=headers, params=payload)


# %%
# 問題作成
#htmlを解析しデータを抽出するためのライブラリ
from bs4 import BeautifulSoup

#httpリクエストを行うためのライブラリ
#webページの情報を取得する
import requests

#すべて表示するプリント
from pprint import pprint

#問題を日数に割り当てるためのライブラリ
from datetime import datetime, timedelta

# %%
def get_soup(url):
    # requestsを使ってURLからHTMLコンテンツを取得
    response = requests.get(url)

    # 取得したHTMLコンテンツ
    html_content = response.text

    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

def get_find_a(soup,url):
    #配列を宣言
    links = []
    # 特定の条件にマッチするすべてのリンクを検索し、表示
    for link in soup.find_all('a', href=True):
        href = link['href']
        # 'https://kakomonn.com/keamane/list1/'で始まるURLに限定
        if href.startswith(url):
            links.append(href)
    return links

# %%
#メインページのsoup
soup_main = get_soup('https://kakomonn.com/keamane')
home_links = get_find_a(soup_main,'https://kakomonn.com/keamane/list1/')

# %%
ques_ini_num = []
for link in home_links:
    soup_sub = get_soup(link)
    ques_links = get_find_a(soup_sub, 'https://kakomonn.com/keamane/questions/')
    url = str(ques_links[0])
    ques_ini_num.append(url[-5:])

# %%
# リスト内包表記を用いて文字列のリストを整数のリストに変換
ques_ini_num = [int(item) for item in ques_ini_num]

# 開始日付を定義
start_date = datetime(2024, 4, 3)

# 各問題番号とその日付を格納するリスト
dates_for_questions = []

# 各セットとその中の各問題に対して処理
for i, start_number in enumerate(ques_ini_num):
    for offset in range(60):  # 各セットは60問を含む
        question_date = start_date + timedelta(days=i*60 + offset)  # 日付を計算
        question_number = start_number + offset  # 問題番号を計算
        dates_for_questions.append((question_number, question_date.strftime('%Y-%m-%d')))

# %%
# 現在の日付に対応する問題番号を再検索
question_number_for_today = [qn for qn, qd in dates_for_questions if qd == current_date.strftime('%Y-%m-%d')]

if question_number_for_today:
    # リストから最初の要素を取り出し、文字列に変換
    question_number_str = str(question_number_for_today[0])
else:
    question_number_str = "該当する問題番号がありません。"


# %%

url = 'https://kakomonn.com/keamane/questions/' + question_number_str
print(url)
soup = get_soup(url)

txt = ""
# タイトルを取得
title = soup.find("h1", class_="ctr_h1").text
txt += "\n\n" + title + "\n\n"

# 質問文を取得
question = soup.find("div", class_="centerbody01_24").text
txt += question + "\n\n"

# 選択肢を取得
options = [option.text.strip() for option in soup.find_all("div", class_="centerbody01_26")]
for i, option in enumerate(options, 1):
    txt += f"{i}. {option}" + "\n\n"

txt += url + "\n"

daycount_txt += txt

# メッセージを送信
if __name__ == '__main__':
    send_line(daycount_txt)