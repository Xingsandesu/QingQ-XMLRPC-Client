# 轻传

---

## 简介

本项目使用 Typecho 的 XML-RPC 接口，实现本地 Markdown 文件解析，并且自动上传 Typecho 服务器，实现博客写作本地化与自动化

## 功能列表

| 功能            | 描述                                                              |
| --------------- | ----------------------------------------------------------------- |
| XML-RPC 发布    | 基于 metaWeblog API 实现的发布操作                                |
| Markdown 渲染   | 基于 mistune 实现 Markdown 文件的本地 HTML 渲染                   |
| 自适应配置检查  | 自写自纠错自生成逻辑实现 Config 的规范化调用                      |
| 拖动上传        | 使用时自动获取 Markdown 文件的路径与文件名拖动即发布              |
| TOC 生成支持    | 基于 mistune 实现支持文档自动生成 TOC                             |
| YAML 头信息读取 | 自动读取 Markdown YAML 头信息，实现发布时自动归类与 OBsidian 归档 |
| 报错抓取                | 自动抓取Traceback，并保存到error.txt                                                              |

## 快速开始

1. 下载程序
[轻传 By GIthub](https://github.com/Xingsandesu/QingQ-XMLPRC-Client/blob/main/QingQ.exe)
[轻传 By KooKoo](https://download.kookoo.top/exe/QingQ.exe)

2. 准备您的 Markdown 文档

3. 拖动文档到轻传，第一次生成配置文件并按照内容修改

4. 再次拖动文档到轻传

5. Done！

## 与 Obsidian 基础联动

首先，您需要了解 Obsidian 的基础概念 - Template 模板与 Markdown YAML 头信息。

### Template模板

模板插件能让你在当前笔记中快速插入预设的文本段。和其他软件的模板不同，Obsidian 的模板和普通笔记一样，都是 Markdown 文件，模板的作用仅仅是保存预设文本段，方便 Obsidian 识别与插入。

#### 设置模板文件夹

使用模板前，你需要指定模板文件夹，这样 Obsidian 才知道模板存放在什么地方。启用模板插件后，你需要在 `设置` -> `模板` -> `模板文件夹位置` 中指定模板文件夹的路径。

#### 在当前笔记中插入模板

设置好了模板文件夹后，你就可以在当前笔记中插入模板了。插入模板的方法很简单， 你可以在左边栏中点击 `插入模板` 按钮，也可以使用相应的快捷键（需要设置），也可以使用命令面板来完成操作。

当你执行这个命令时，模板中的文本段会立刻插入到当前笔记中光标所在的位置。

#### 插入当前笔记标题

如果你想让模板自动生成当前笔记的标题，则可以使用`{{title}}`占位符。

#### 插入日期与时间

Obsidian 允许你在模板中使用占位符 `{{date}}` 和 `{{time}}` 来代表日期和时间。当模板插入到笔记中时，Obsidian 会自动地将这些占位符替换成当下的日期值和时间值。

当然，替换的日期值和时间值的格式也是可以自行设定的。你可以在模板插件的设置页进行格式的设定，具体的格式语法请看[这里](https://momentjs.com/docs/#/displaying/format/)。

_一个小技巧：如果你想在模板中使用两个日期占位符，你可以通过相应的格式把时间占位符变成日期占位符。想使用两个日期占位符也是同理。_

#### 另一种指定格式的方法

除了在设置页中指定日期值和时间值的格式外，你还可以使用 `{{date:YYYY-MM-DD}}`、`{{time:HH:mm}}` 这样的占位符来直接指定格式——冒号 `:` 后的部分都会被识别为格式语法。需要注意的是，这种写法会覆盖设置页中对于占位符的格式设置，因此它仅对于当前模板有效，对其他模板是不起作用的（如果你有多个模板的话）。

#### 在其他地方使用格式语法

目前，这种格式语法也可以在[日记](https://publish.obsidian.md/help-zh/%E6%8F%92%E4%BB%B6/%E6%97%A5%E8%AE%B0)和 [ZK 卡片](https://publish.obsidian.md/help-zh/%E6%8F%92%E4%BB%B6/ZK+%E5%8D%A1%E7%89%87)的模板设置里使用。但是，`{{date}}` 和 `{{time}}` 占位符并不能使用。

### Markdown YAML 头信息

在 Obsidian 中写文档，通常需要在头部写一些关于文章的信息，这些都是需要使用 YAML 语言来写的，例如

```
---
title: 
date: 
tags: 
- 1
- 2

---
```

提醒此部分一般叫做 `Front-matter` 。

文章内部的 YAML 配置都是以 `---` 开始和结束的，而且，结束之后通常还要再有一行的空行，用以区分 Markdown 语法。

#### 基本语法

YAML 使用键值对的形式记录信息，标准格式是

```
key: value
键: 值
```

#### 基本规则

1. 大小写敏感
2. **使用缩进表示层级关系**
3. 禁止使用 tab 缩进，只能使用空格键
4. 缩进长度没有限制，只要元素对齐就表示这些元素属于一个层级
5. 使用 `#` 表示注释
6. 字符串可以不用引号标注（但是建议你最好还是加上引号）

### 联动使用方法

#### 教程

1. 下载我提供的[Template.md](https://github.com/Xingsandesu/QingQ-XMLPRC-Client/blob/main/Template.md)
![image.png](https://cdn.jsdelivr.net/gh/Xingsandesu/kookoo-picbed/img/2023%2F07%2F30%2F20230730151803_15-18-05.png)

2. 参考`Template模板`来使用这个模板
3. 写作
4. 拖动文件到程序，完成发布。

#### 模板YAML字段内容注释

```
---
# 时间日期，Obsidian 模板可以自动识别，此处无需更改
日期: {{date: YYYY年 MM 日 DD 日}}
时间: {{time: HH 点 mm 分}}
Tags:
- 折腾 # Obsidian 可以识别的键值对，作为 Obsidian 本地归档分类使用
categories:
- 折腾 # 本程序上传Typecho时的分类键值对，作为 Typecho 分类时调用，此处填写后文章自动把上传内容划分到您输入的分类中
---
# 此处是自动生成TOC的Tag，写作时，如果仅作为 Obsidian 本地笔记使用，或者不想生成TOC可以删除
.. toc:: 
```



## 常见问题及解决方案

### 1. 如何在 Linux / macOS 中使用它 ?

```
- 下载源码，自行用 Pyinstaller 来构建 Linux 的可运行程序
- 或者直接下载源码，打开命令行，输入 python main. py <您的Markdown文件路径>
```


### 2. 使用上遇到了不能上传的问题 ?

```
- 提交 Issue
- 发送邮件到 fushinn888@gmail.com
```

### 3. 为什么在Typecho后台编辑文章是HTML格式 ?

```
这是因为 Typecho 的一个BUG，直接使用 XML-PRC 来发布 Markdown 格式的文档内容时，Typecho无法自动识别 Markdown 格式，因此，本程序通过在本地直接渲染 Markdown 文件，直接向 Typecho 提交 HTML 文本，曲线解决了这一问题，并且通过这一手段，实现了自动生成 TOC 目录的功能，当然，您也可以自己开发相应的渲染器。
```

### 4. 在其他的CMS上可以使用该程序吗 ?

```
当然！本程序是基于 metaWeblog API 实现的，您也可以部署到其他平台上，包括但不限于WordPress，CSDN，cnblog等，您也可以使用 metaWeblog API 来为本程序添加其他的功能
```

## 效果展示

### Markdown 渲染效果展示

[test - 糊涂涂博客](https://kookoo.top/2023/07/29/82.html)

## 二次开发

欢迎各位

## 异常排错

### 已知异常

- 程序过程中会自动提醒

### 未知异常

- 请提交生成的error.txt到[Issues · Xingsandesu/QingQ-XMLPRC-Client · GitHub](https://github.com/Xingsandesu/QingQ-XMLPRC-Client/issues)

## TODO LIST

- hook 联动
- Obsidian 插件联动

## 相关依赖


```
见 requirements.txt
```

