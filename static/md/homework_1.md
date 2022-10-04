# homework_1

### 2022.9
### 王义成 19122330

## 1. 安装 pyhanlp

![](.\res\install_pyhanlp.png)

## 2. 编写正向、逆向、双向匹配算法，对比测试结果

![来源：课程PPT](.\res\segment_flowchart.png "切分算法流程图")

### 2.1 词典加载
参考课本配套的源代码，如下：
```python
from pyhanlp import *


def load_dictionary():
    """
    加载HanLP中的mini词库
    :return: 一个set形式的词库
    """
    IOUtil = JClass('com.hankcs.hanlp.corpus.io.IOUtil')
    path = HanLP.Config.CoreDictionaryPath.replace('.txt', '.mini.txt')
    dic = IOUtil.loadDictionary([path])
    return set(dic.keySet())
```

### 2.2 正向匹配算法
* 代码实现
```python
def forward_segment(text, dic):
    words = []
    i = 0
    while i < len(text):
        longest_word = text[i]
        for j in range(i + 1, len(text) + 1):
            word_cache = text[i:j]
            if word_cache in dic:
                longest_word = word_cache
        words.append(longest_word)
        i += len(longest_word)

    return words
```
* 运行结果
```
['项目', '的', '研究']
['商品', '和服', '务']
['研究生', '命', '起源']
['当下', '雨天', '地面', '积水']
['结婚', '的', '和尚', '未', '结婚', '的']
['欢迎', '新', '老师', '生前', '来', '就餐']
```
通过对切分结果的分析可以看出，正向匹配算法的正确率仅有 1/6，仅有 '项目的研究' 一段文本切分正确，切分效果不理想。

### 2.3 逆向匹配算法
* 代码实现
```python
def backward_segment(text, dic):
    words = []
    i = len(text) - 1
    while i >= 0:
        longest_word = text[i]
        for j in range(0, i):
            word_cache = text[j: i + 1]
            if word_cache in dic:
                longest_word = word_cache
        words.append(longest_word)
        i -= len(longest_word)
    words.reverse()

    return words
```
* 运行结果
```
['项', '目的', '研究']
['商品', '和', '服务']
['研究', '生命', '起源']
['当下', '雨天', '地面', '积水']
['结婚', '的', '和', '尚未', '结婚', '的']
['欢', '迎新', '老', '师生', '前来', '就餐']
```
与课件对比可以发现，'当下雨天地面积水' 一段的切分结果与课件中的有出入，并非是代码中出现错误，而是我使用的mini词典中并未收录”下雨天“一词，自然无法正确匹配。

通过对切分结果的分析可以看出，逆向匹配算法的正确率为 1/2，在测试数据集上的表现优于正向匹配，但仍然不够理想。

### 2.4 双向匹配算法
* 代码实现
```python
def count_single_char(words):  # 统计单字成词的个数
    num = 0
    for word in words:
        if len(word) == 1:
            num += 1

    return num


def bidirectional_segment(text, dic):
    f = forward_segment(text, dic)
    b = backward_segment(text, dic)
    if len(f) < len(b):                                  # 词数更少优先级更高
        return f
    elif len(f) > len(b):
        return b
    else:
        if count_single_char(f) < count_single_char(b):  # 单字更少优先级更高
            return f
        else:
            return b                                     # 都相等时逆向匹配优先级更高
```
* 运行结果
```
['项', '目的', '研究']
['商品', '和', '服务']
['研究', '生命', '起源']
['当下', '雨天', '地面', '积水']
['结婚', '的', '和', '尚未', '结婚', '的']
['欢', '迎新', '老', '师生', '前来', '就餐']
```
通过对切分结果的分析可以看出，双向匹配算法的正确率为 1/2，未能达到预期中结合正向、逆向两种算法优点的效果。

### 2.5 速度对比
![](.\res\benchmark.png)

从上图可知，正向、逆向匹配算法的运行速度相当，均快于双向匹配算法，大约是双向匹配算法的两倍。
