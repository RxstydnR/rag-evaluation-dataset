import re
import requests
from typing import List

ZEN = "".join(chr(0xff01 + i) for i in range(94))  # 全角文字列一覧
HAN = "".join(chr(0x21 + i) for i in range(94))  # 半角文字列一覧
ZEN2HAN = str.maketrans(ZEN, HAN)
HAN2ZEN = str.maketrans(HAN, ZEN)
ALL=re.sub(r'[a-zA-Zａ-ｚＡ-Ｚ\d]+','',ZEN+HAN) + '【】'
code_regex = re.compile('['+'〜'+'、'+'。'+'~'+'*'+'＊'+ALL+'「'+'」'+']')
def preprocessing(text):
    """小文字化、記号・丸囲い数字除去、全角を半角など前処理関数"""
    text = text.lower() # 小文字化
    text = re.sub('\r\n','',text) # \r\nを削除
    # text = re.sub(r'\d+','',text) # 数字列をdelete
    text = code_regex.sub(' ', text) # 記号を消す
    text = text.translate(ZEN2HAN) # 全角を半角に
    return text

    # テスト
    # preprocessing("HELLO WORLD") # => 'hello world'
    # preprocessing("Hello\r\nWorld\n") # => 'helloworld\n'
    # preprocessing("Hello! 〜 World * ＊ [ ] 【 】") # => 'hello    world         '
    # preprocessing("ＡＢＣＤ１２３４５６７８９０") # => 'abcd1234567890'
    # preprocessing("こんにちは！THIS IS A TEST。123４５６７８９０") # => 'こんにちは this is a test 1234567890'
    # preprocessing("") # => ""
    # preprocessing("〜、。~*＊「」") # => "      "
    # preprocessing("ひらがなカタカナ") # => "ひらがなカタカナ"


def remove_space_between_japanese(text):
    """日本語の文字と日本語の文字の間にあるスペースを削除する"""
    
    # 日本語の文字間とスペース、そして再び日本語の文字のパターンを検索します。
    pattern = r'([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF])\s+([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF])'
    
    # 再帰的にスペースを削除するためのループ
    while re.search(pattern, text):
        text = re.sub(pattern, r'\1\2', text)
    
    return text


# 日本語ストップワード辞書
url = "https://raw.githubusercontent.com/stopwords-iso/stopwords-ja/master/stopwords-ja.txt"
stopwords_jp = requests.get(url).text.split("\n")

def remove_stopwords(tokens: List[str]) -> List[str]:
    """指定した単語リストからストップワードを除去した結果を返す"""
    tokens = [token for token in tokens if token not in stopwords_jp]
    return tokens