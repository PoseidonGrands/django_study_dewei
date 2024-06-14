import jieba
from django import template

from msg_test.consts import SENSITIVE_WORDS

register = template.Library()


@register.filter
def word_check(value):
    cut_words = jieba.lcut(value)
    # &符号求集合交集
    res = list(set(SENSITIVE_WORDS) & set(cut_words))
    if not res:
        return value
    return '包含敏感词汇'


@register.filter
def word_check_replace(value):
    cut_words = jieba.lcut(value)
    # &符号求集合交集
    check = list(set(SENSITIVE_WORDS) & set(cut_words))
    res = []
    if not check:
        return value
    # 分词结果出现在交集，则是敏感词
    print("分词是：", cut_words)
    print("交集是：", check)
    for word in cut_words:
        if word in check:
            _len = len(word)
            # 几个字符就替换几个*
            word = '*' * _len
        res.append(word)
    print(res)
    return ''.join(res)
