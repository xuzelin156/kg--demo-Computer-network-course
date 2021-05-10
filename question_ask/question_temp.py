# encoding=utf-8

"""

@author: xuzelin

@file: question_temp.py

@time: 2020/12/20

@desc:
设置问题模板，为每个模板设置对应的SPARQL语句。demo提供如下模板：

1. 某实体的兄弟关系有哪些
2. 某阶段之后是哪个阶段
3. 某实体包含了哪些实体
4. 与某实体内涵相同的是
5. 与某实体内涵相反的是
6. 某实体继承自哪个实体
7. 某实体参考自哪里/那本教程
8. 与某实体可以相互变换的实体有哪些
9. 与某实体有因果的实体有哪些？
10.某实体的某属性是什么
11.某实体是正确的吗？

"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
PREFIX : <http://www.semanticweb.org/yan/ontologies/2020/9/untitled-ontology-6#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if len(matches) == 0:
            return None
        else:
            return self.action()


class QuestionSet:
    def __init__(self):
        pass


    @staticmethod
    def has_brother_question(word_objects):
        """
        某实体的兄弟关系有哪些
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :兄弟关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_Successive_question(word_objects):
        """
        某阶段之后是哪个阶段
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :前后继关系 ?z." \
                    u"?z :名称  ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_contain_question(word_objects):
        """
        某实体包含了哪些实体
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :包含关系  ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_same_question(word_objects):
        """
        与某实体内涵相同的是
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :同一关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_opposition_question(word_objects):
        """
        与某实体内涵相反的是
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :对立关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_inherit_question(word_objects):
        """
        某实体继承自哪个实体
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :前后继关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_reference_question(word_objects):
        """
        某实体参考自哪里
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :参考关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_vary_question(word_objects):
        """
        与某实体可以相互变换的实体有哪些
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :变换关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_karma_question(word_objects):
        """
        与某实体有因果的实体有哪些？
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?y :名称 '{disanzhang}'." \
                    u"?y :因果关系 ?z." \
                    u"?z :名称 ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_basic_disanzhang_info_question(word_objects):
        """
        某实体的某属性是什么
        :param word_objects:
        :return:
        """

        keyword = None
        for r in disanzhang_basic_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?s :名称 '{disanzhang}'." \
                    u"?s {keyword} ?x.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'), keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)

                break

        return sparql

    @staticmethod
    def is_ASKattribute_question(word_objects):
        """
        某实体是正确的吗？
        :param word_objects:
        :return:
        """
        sparql = None
        for w in word_objects:
            if w.pos == pos_disanzhang:
                e = u"?s :名称 '{disanzhang}'." \
                    u"?s rdf:type :正确.".format(disanzhang=w.token.encode('utf-8').decode('utf-8'))

                sparql = SPARQL_ASK_TEM.format(prefix=SPARQL_PREXIX, expression=e)
                break

        return sparql

class PropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_dingyi_value():
        return u':定义'

    @staticmethod
    def return_jieshao_value():
        return u':介绍'

    @staticmethod
    def return_youdian_value():
        return u':优点'

    @staticmethod
    def return_quedian_value():
        return u':缺点'

    @staticmethod
    def return_zuoyong_value():
        return u':作用'

    @staticmethod
    def return_juyou_value():
        return u':具有'

    @staticmethod
    def return_neirong_value():
        return u':内容'

    @staticmethod
    def return_biecheng_value():
        return u':别称'

    @staticmethod
    def return_gongneng_value():
        return u':功能'

    @staticmethod
    def return_baokuo_value():
        return u':包括'

    @staticmethod
    def return_hanyi_value():
        return u':含义'

    @staticmethod
    def return_shuyu_value():
        return u':属于'

    @staticmethod
    def return_shuxing_value():
        return u':属性'

    @staticmethod
    def return_xingzhi_value():
        return u':性质'

    @staticmethod
    def return_yiyi_value():
        return u':意义'

    @staticmethod
    def return_shijian_value():
        return u':时间'

    @staticmethod
    def return_tezheng_value():
        return u':特征'

    @staticmethod
    def return_tedian_value():
        return u':特点'

    @staticmethod
    def return_zhuangtai_value():
        return u':状态'

    @staticmethod
    def return_jiancheng_value():
        return u':简称'

    @staticmethod
    def return_leixing_value():
        return u':类型'

    @staticmethod
    def return_jibie_value():
        return u':级别'

    @staticmethod
    def return_zucheng_value():
        return u':组成'

    @staticmethod
    def return_jiegou_value():
        return u':结构'

    @staticmethod
    def return_zhize_value():
        return u':职责'

    @staticmethod
    def return_yingwen_value():
        return u':英文'

    @staticmethod
    def return_biaodashi_value():
        return u':表达式'

    @staticmethod
    def return_yaosu_value():
        return u':要素'

    @staticmethod
    def return_guize_value():
        return u':规则'

    @staticmethod
    def return_xiangjie_value():
        return u':详解'

    @staticmethod
    def return_shiyi_value():
        return u':释义'

    @staticmethod
    def return_lingyu_value():
        return u':领域'

    @staticmethod
    def return_gainian_value():
        return u':概念'


# TODO 定义关键词
pos_disanzhang = "nz"

disanzhang_entity = (W(pos=pos_disanzhang))

dingyi = W("定义")
jieshao = W("介绍")
youdian = W("优点")
quedian = W("缺点")
zuoyong = W("作用")
juyou = W("具有")
neirong = W("内容")
biecheng = W("别称")
gongneng = W("功能")
baokuo = W("包括")
hanyi = W("含义")
shuyu = W("属于")
shuxing = W("属性")
xingzhi = W("性质")
yiyi = W("意义")
shijian = W("时间")
tezheng = W("特征")
tedian = W("特点")
zhuangtai = W("状态")
jiancheng = W("简称")
leixing = W("类型")
jibie = W("级别")
zucheng = W("组成")
jiegou = W("结构")
zhize = W("职责")
yingwen = W("英文")
biaodashi = W("表达式")
yaosu = W("要素")
guize = W("规则")
xiangjie = W("详解")
shiyi = W("释义")
lingyu = W("领域")
gainian = W("概念")
attribute = (dingyi | jieshao | youdian | quedian | zuoyong | juyou
             | neirong | biecheng | gongneng | baokuo | hanyi |
             shuyu | shuxing | xingzhi | yiyi | shijian | tezheng |
             tedian | zhuangtai | jiancheng | leixing | jibie |
             zucheng | jiegou | zhize | yingwen | biaodashi |
             yaosu | guize | xiangjie | shiyi  | lingyu | gainian)

brother = W("兄弟")
Successive = W("阶段")
contain = W("包含")
connotation = W("内涵") | W("意思")
same = (W("相同") | W("一致") | W("一样") )
opposition = (W("相反") | W("对立") )
inherit = W("继承")
reference = W("参考")
vary = W("变换")
karma = W("因果")
zhengque = W("正确")

# TODO 问题模板/匹配规则
"""
1. 某实体的兄弟关系有哪些
2. 某阶段之后是哪个阶段
3. 某实体包含了哪些实体
4. 与某实体内涵相同的是
5. 与某实体内涵相反的是
6. 某实体继承自哪个实体
7. 某实体参考自哪里/那本教程
8. 与某实体可以相互变换的实体有哪些
9. 与某实体有因果的实体有哪些？
10.某实体的某属性是什么
11.某实体是正确的吗？
"""
rules = [
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + brother + Star(Any(), greedy=False), action=QuestionSet.has_brother_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + Successive + Star(Any(), greedy=False), action=QuestionSet.has_Successive_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + contain + Star(Any(), greedy=False), action=QuestionSet.has_contain_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + connotation + Star(Any(), greedy=False) + same + Star(Any(), greedy=False), action=QuestionSet.has_same_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + connotation + Star(Any(), greedy=False) + opposition + Star(Any(), greedy=False), action=QuestionSet.has_opposition_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + inherit + Star(Any(), greedy=False), action=QuestionSet.has_inherit_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + reference + Star(Any(), greedy=False),action=QuestionSet.has_reference_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + vary + Star(Any(), greedy=False), action=QuestionSet.has_vary_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + karma + Star(Any(), greedy=False), action=QuestionSet.has_karma_question),
    Rule(condition_num=2, condition=disanzhang_entity + Star(Any(), greedy=False) + attribute + Star(Any(), greedy=False),action=QuestionSet.has_basic_disanzhang_info_question),
    Rule(condition_num=3, condition=disanzhang_entity + Star(Any(), greedy=False) + zhengque + Star(Any(), greedy=False),action=QuestionSet.is_ASKattribute_question)
]

# TODO 具体的属性词匹配规则
disanzhang_basic_keyword_rules = [
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + dingyi + Star(Any(), greedy=False),action=PropertyValueSet.return_dingyi_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + jieshao + Star(Any(), greedy=False),action=PropertyValueSet.return_jieshao_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + youdian + Star(Any(), greedy=False),action=PropertyValueSet.return_youdian_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + quedian + Star(Any(), greedy=False),action=PropertyValueSet.return_quedian_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + zuoyong + Star(Any(), greedy=False),action=PropertyValueSet.return_zuoyong_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + juyou + Star(Any(), greedy=False),action=PropertyValueSet.return_juyou_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + neirong + Star(Any(), greedy=False),action=PropertyValueSet.return_neirong_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + biecheng + Star(Any(), greedy=False),action=PropertyValueSet.return_biecheng_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + gongneng + Star(Any(), greedy=False),action=PropertyValueSet.return_gongneng_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + baokuo + Star(Any(), greedy=False),action=PropertyValueSet.return_baokuo_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + hanyi + Star(Any(), greedy=False),action=PropertyValueSet.return_hanyi_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + shuyu + Star(Any(), greedy=False),action=PropertyValueSet.return_shuyu_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + shuxing + Star(Any(), greedy=False),action=PropertyValueSet.return_shuxing_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + xingzhi + Star(Any(), greedy=False),action=PropertyValueSet.return_xingzhi_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + yiyi + Star(Any(), greedy=False),action=PropertyValueSet.return_yiyi_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + shijian + Star(Any(), greedy=False),action=PropertyValueSet.return_shijian_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + tezheng + Star(Any(), greedy=False),action=PropertyValueSet.return_tezheng_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + tedian + Star(Any(), greedy=False),action=PropertyValueSet.return_tedian_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + zhuangtai + Star(Any(), greedy=False),action=PropertyValueSet.return_zhuangtai_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + jiancheng + Star(Any(), greedy=False),action=PropertyValueSet.return_jiancheng_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + leixing + Star(Any(), greedy=False),action=PropertyValueSet.return_leixing_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + jibie + Star(Any(), greedy=False),action=PropertyValueSet.return_jibie_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + zucheng + Star(Any(), greedy=False),action=PropertyValueSet.return_zucheng_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + jiegou + Star(Any(), greedy=False),action=PropertyValueSet.return_jiegou_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + zhize + Star(Any(), greedy=False),action=PropertyValueSet.return_zhize_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + yingwen + Star(Any(), greedy=False),action=PropertyValueSet.return_yingwen_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + biaodashi + Star(Any(), greedy=False),action=PropertyValueSet.return_biaodashi_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + yaosu + Star(Any(), greedy=False),action=PropertyValueSet.return_yaosu_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + guize + Star(Any(), greedy=False),action=PropertyValueSet.return_guize_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + xiangjie + Star(Any(), greedy=False),action=PropertyValueSet.return_xiangjie_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + shiyi + Star(Any(), greedy=False),action=PropertyValueSet.return_shiyi_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + lingyu + Star(Any(), greedy=False),action=PropertyValueSet.return_lingyu_value),
    KeywordRule(condition=disanzhang_entity + Star(Any(), greedy=False) + gainian + Star(Any(), greedy=False),action=PropertyValueSet.return_gainian_value),
]
