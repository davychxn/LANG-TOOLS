# LANG-TOOLS / Python - 英语音节提取工具

[English](./README.md) | [中文](./README_CN.md)

一个基于 [CMU 发音词典](http://www.speech.at.cs.cmu.edu/cgi-bin/cmudict) 提取和归类所有英语音节模式的 Python 工具包。

## 概述

本工具解析 CMU 词典中的 ARPAbet 音标序列，使用基于规则的算法将其拆分为音节单元。核心设计原则是 **"双重用途"（double usage）**——某些音素（鼻音 M/N/NG、流音 R/L、滑音 Y）同时充当前一个音节的韵尾和下一个音节的声母，这反映了这些音素在自然英语语音中的实际表现。

## 项目结构

```
py/
  libs/
    EngParser.py         # 核心音节提取引擎
  scan_syllables2.py     # 批量扫描器 - 处理整本 CMU 词典
  example.py             # 单词用法示例
  syllables_data.json    # 输出结果 - 所有提取的音节模式
```

## 音素分类

算法将 ARPAbet 音素分为三组：

| 分组 | 音素 | 在音节中的角色 |
|------|------|---------------|
| **元音** (15个) | AH, EY, ER, AO, UW, IH, AA, IY, EH, AE, OW, AW, AY, UH, OY | 音节核心 |
| **辅音** (18个) | W, Z, F, T, P, B, G, K, S, TH, D, V, SH, ZH, HH, JH, CH, DH | 仅作音节声母 |
| **双重用途** (6个) | M, N, NG, R, L, Y | 既可作声母也可作韵尾 |

此外，辅音组合 **TR**、**DR**、**TS**、**DS** 被视为有效的复合声母。

## 算法

1. 从左到右遍历音素序列
2. 当元音后紧跟普通辅音时，该辅音开始一个**新**音节（最大声母原则）
3. 当元音后紧跟双重用途音素（M、N、NG、R、L）时，该音素附加到**当前**音节作为韵尾，同时也作为**下一个**音节的声母
4. 元音到元音的特殊过渡处理：
   - UW/OW/AW + 元音：插入桥接辅音 **W**（如 "swear"）
   - ER + 元音：插入桥接辅音 **R**（如 "history"）
   - 其他元音对：直接分割

## 输出格式

`syllables_data.json` 包含：

```json
{
  "syllables_all": {
    "K_AE": ["K", "AE"],
    "T_R_IY": ["T", "R", "IY"],
    "R_AH_N": ["R", "AH", "N"],
    ...
  },
  "syllables_maps_list": [
    { /* 单音素音节 (34个) */ },
    { /* 双音素音节 (436个) */ },
    { /* 三音素音节 (1387个) */ },
    { /* 四音素音节 (213个) */ },
    {}, {}, {}
  ]
}
```

唯一音节模式总数：**2,070**

## 用法

### 单个单词

```python
from libs.EngParser import EngParser

eng_parser = EngParser()
syllables_map, sound_map = eng_parser.extract_syllables("K AH0 M Y UW2 N AH0 K EY1 SH AH0 N")

print(sound_map.keys())
# dict_keys(['K_AH', 'M', 'Y_UW', 'N_AH', 'K_EY', 'SH_AH', 'N'])
```

### 批量扫描（完整词典）

```bash
python scan_syllables2.py
```

读取 CMU 词典文件，提取所有音节模式，导出 `syllables_data.json`。

**运行结果：**

```
D:\...\LANG-TOOLS\py>python scan_syllables2.py
2070
Json exported.
```

## 环境要求

- Python 3.8+
- CMU 发音词典文件（`cmudict-0.7b`）
- 无需外部依赖
