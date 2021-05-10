# encoding=utf-8

"""

@author: xuzelin

@file: word_tagging.py

@time: 2020/12/20

@desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

"""
import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

        # TODO jieba不能正确切分的词语，我们人工调整其频率。
        jieba.suggest_freq(('兄弟', '关系'), True)
        jieba.suggest_freq(('前后继', '关系'), True)
        jieba.suggest_freq(('包含', '关系'), True)
        jieba.suggest_freq(('同一', '关系'), True)
        jieba.suggest_freq(('对立', '关系'), True)
        jieba.suggest_freq(('继承', '关系'), True)
        jieba.suggest_freq(('参考', '关系'), True)
        jieba.suggest_freq(('变换', '关系'), True)
        jieba.suggest_freq(('因果', '关系'), True)

    @staticmethod
    def get_word_objects(sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        return [Word(word, tag) for word, tag in pseg.cut(sentence)]


# TODO 用于测试
if __name__ == '__main__':
    tagger = Tagger(['./disizhang_object/disanzhang_name.txt', './disizhang_object/disizhang_object.txt'])
    while True:
        s = input('>>')
        for i in tagger.get_word_objects(s):
            print(i.token, i.pos)
