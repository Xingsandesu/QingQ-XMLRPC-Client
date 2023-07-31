# 轻传

---

## 简介

本项目使用 Typecho 的 XML-RPC 接口，实现本地 Markdown 文件解析，并且自动上传 Typecho 服务器，实现博客写作本地化与自动化

## 功能列表

| 功能                                 | 描述                                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| XML-RPC 发布                         | 基于 metaWeblog API 实现的发布操作                                                  |
| Markdown 渲染                        | 基于 mistune 实现 Markdown 文件的本地 HTML 渲染                                     |
| 自适应配置检查                       | 自写自纠错自生成逻辑实现 Config 的规范化调用                                        |
| 拖动上传                             | 使用时自动获取 Markdown 文件的路径与文件名拖动即发布，注意，该功能只支持到1.0       |
| TOC 生成支持                         | 基于 mistune 实现支持文档自动生成 TOC                                               |
| YAML 头信息读取                      | 自动读取 Markdown YAML 头信息，实现发布时自动归类，Typecho 打标签与 OBsidian 打标签 |
| 报错抓取                             | 自动抓取Traceback，并保存到error.txt                                                |
| WebDav服务端                         | 集成了一个WebDav服务端，现在可以直接和Obsidian中WebDav插件联动了                    |
| 企业微信推送支持                     | 服务端部署可以直接推送消息到企业微信                                                |
| 基于本地YAML的自动识别上传或修改文章 | 通过本地YAML文件来实现该功能，注意，此文件是隐藏的                                  |
| 异步执行命令                                     | 集成了一个函数，二次开发可以直接调用                                                                                    |

## 快速开始

### 注意，此处可以运用到 1.0 之后的版本

### 1. 下载程序
[Releases · Xingsandesu/QingQ-XMLRPC-Client](https://github.com/Xingsandesu/QingQ-XMLRPC-Client/releases/)

### 2. 准备您的 Markdown 文档

### 3. 企业微信注册（仅 1.2 版本以后需要操作）

1. 到企业微信官网，注册一个企业
2. 登录企业微信后台，创建一个“自建”应用， 获取企业ID、agentid、secret这3个必要的参数
3. 在企业微信的[通讯录](https://so.csdn.net/so/search?q=%E9%80%9A%E8%AE%AF%E5%BD%95&spm=1001.2101.3001.7020)中，创建多个测试账号
4. 在手机端安装“企业微信”APP，使用测试账号登录到企业微信，准备接收消息。

### 4. 准备一个服务器或者主机

- 如果你没有服务器，我推荐使用1.1版本在本机实现一个Hook
- 如果你拥有一个服务器，我推荐使用1.2版本在服务器上运行，通过WebDav更好的与Obsidian联动

### 5. 第一次运行程序

- 第一次运行程序会自动生成 config.yml 配置文件，并且报错，请不用担心，按照配置文件提示去填写他
- 如果你失误填写了错误的配置文件或者格式，重新运行程序或者删除 config.yml ，程序会自动更正配置

### 6.第二次运行程序

- 如果你的配置没有问题，我想现在程序已经开始正常的运行了
- 如果你想在命令行持久运行 在 Linux 上可以创建一个 screen 来运行他
- 或者，见下方进阶配置，把程序注册为服务
- 如果出现了提示报错，请按照提示检查并修改配置文件
- 如果出现了未知错误，请提交 error.txt 到本项目的 issue，并写明复现方法，如果不可复现请直接提交txt内容

### 7. 进阶配置 （可选）

#### 反向代理 

- 在1.2版本后，你可以使用Nginx等软件，反向代理该服务器
- 这里提供一个简单的配置

```
location / {

	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

	proxy_set_header Host $http_host;

	proxy_redirect off;

	proxy_pass http://127.0.0.1:5212;

	# 请将下一行注释符删除，并更改大小为理论最大文件尺寸

	# client_max_body_size 20000m;

}
```


#### 注册为服务，开机自启动

##### Linux
- 首先创建模板

```
# 编辑配置文件
vim /usr/lib/systemd/system/qingq.service
```

- 将下文 `PATH_TO_QINGQ` 更换为程序所在目录：
```
[Unit]

Description=QingQ

Documentation=https://github.com/Xingsandesu/QingQ-XMLRPC-Client

After=network.target

Wants=network.target

[Service]

WorkingDirectory=/PATH_TO_QINGQ

ExecStart=/PATH_TO_QINGQ/QingQ

Restart=on-abnormal

RestartSec=5s

KillMode=mixed

StandardOutput=null

StandardError=syslog

[Install]

WantedBy=multi-user.target

```

- 配置命令

```
# 更新配置
systemctl daemon-reload

# 启动服务
systemctl start qingq

# 设置开机启动
systemctl enable qingq
```

## 快速开始-1.0

### 注意，1.0与此后更新的程序逻辑发生了极大的变更，1.0版本快速开始并不适用与其他版本

1. 下载程序

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
2. 参考`Template模板`来使用这个模板
3. 写作
4. 安装 第三方插件 Remotely Save 
![image.png](https://cdn.jsdelivr.net/gh/Xingsandesu/kookoo-picbed/img/2023%2F07%2F31%2F20230731224333_22-43-34.png)
5. 配置webdav地址与账号密码以及相关设置，账号密码为你的系统账号密码
6. 创建一个保存草稿和发布的文件夹
7. 创建一个文件夹来保存草稿
8. 创建一个文件夹来保存发布
9. 在config.yml填写File_dir为发布文件夹路径
10. 在config.yml填写 Webdav_root_path为你的Obsidian库路径，
> Windows系统 注意这里填C盘的地址，且不要写C:\  ，直接写去掉盘符的路径
> Linux系统则没有限制
11. 填写其他配置，详见快速开始
12. 运行程序
13. 写作完成后，只需把草稿中的markdown复制一份到发布文件夹中，运行同步操作或者等待插件完成自动同步，即可完成发布
14. 如果想要修改，请在草稿文件夹修改文件，同样的复制一份到发布文件夹中，程序会自动生成新的文章覆盖更新。

#### 注意事项

- .slug_cid_mapping.yml 是完成上传后保存的一份特殊的log文件，他是隐藏的，以YAML格式储存，非必要请不要删除他，他记录了所有你使用程序上传的文章信息，根据这些信息才能判断文章是否已经存在，而完成文章发布或更新操作
- print.log 是程序运行的log文件，该文件记录了所有控制台信息，遇到问题你可以查看该文件，注意，log含有重要的身份信息，请不要泄露他
- config.yml 是程序的配置文件，程序需要的参数会在里面填写或更新，更新程序不会删除原有的配置，而是增量写入，每次更新时如果有配置更新，请填写相关配置
- error.txt 是程序遇到未知错误而产生的文件，如果遇到自己解决不了的问题，请附带此文件到issue

### 联动使用方法-1.0

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

- [x] hook 联动
- [x] Obsidian 联动
- [x] 集成WebDav服务器

> 如果有更好的想法，欢迎提交issue

## 更新日志

### 1.1-Server-Hook
- 通过Hook实现获取自定义文件夹内如果有新的markdown文件被创建，程序会自动上传到Typecho
- 提供企业微信消息推送支持，在config.yml中添加自己的企业微信信息，如果markdown文件被正确的上传，则会推送消息到您的企业微信程序中。
- 添加了日志模块，由于是服务端部署模式，将不会使用input()来进行Windows窗口留存，相关所有的输出都会通过print.log保存，如有报错请看log
- 更新了error.txt未知异常报错捕获逻辑
- 提供Linux与Windows两种部署方式，获取请releases中下载


### 1.2

#### BUG FIX
- 重写了文章上传逻辑，现在是基于本地文件.slug_cid_mapping.yml来实现自动识别更新文章或者上传新文章的逻辑，请不要删除这个文件
- 重写了读取YAML头信息的读取方式，修复了之前有可能读取头文件不完全的BUG
- 重写了加载逻辑
- 优化了error.txt的判断点，现在代码更健壮了
- 增加了企业微信应用id的可配置变量，现在可以在配置文件中修改它
- 错别字修正

#### 功能更新
- 集成一个WebDav服务端，在服务器中部署它，或者在电脑中运行他，现在可以直接使用WebDav来配合Obsidian的webdav同步插件来实现无缝上传或者更新文章了
- 支持了XMLRPC上传解析YAML头信息中标签信息，但是这里有一个已知 BUG 详见 typecho/typecho#1607
- 增加异步执行的相关代码

#### 重要公告
- 如果想直接运行在本地运行.py程序，请务必安装requirements.txt中的相关依赖

## 相关依赖


```
见 requirements.txt
```
