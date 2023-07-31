# Copyright (C) 2023 kodesu, Inc. All Rights Reserved
# @Time    : 2023-7
# @Author  : kodesu
# @Blog    : kookoo.top
# ————————————————
import xmlrpc.client
import yaml
import os
import mistune
import sys
from mistune.directives import RSTDirective, TableOfContents
import traceback
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import requests
import json
import platform
import subprocess
import threading


# 运行命令部分
def run_command_with_output(command):
    webdav_logger = WebDavLogger()
    try:
        # 执行命令并捕获输出
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # 实时输出标准输出和错误输出，使用临时日志记录器
        for line in process.stdout:
            webdav_logger.logger.info(line.rstrip())

        for line in process.stderr:
            webdav_logger.logger.error(line.rstrip())

        # 等待子进程完成
        process.wait()

    except Exception as e:
        logger.logger.error(f"执行命令时出错：{e}")


# Webdav 构建命令运行服务器部分
class WebDAVServer:
    def __init__(self, webdav_host="0.0.0.0", webdav_port=80, webdav_root_path="/tmp", webdav_auth_type="nt"):
        self.host = webdav_host
        self.port = webdav_port
        self.root_path = webdav_root_path

    def start_server(self):
        system_type = platform.system()
        try:

            if system_type == "Windows":
                command = f"wsgidav --host={self.host} --port={self.port} --root={self.root_path} --auth=nt"
            elif system_type == "Linux":
                command = f"wsgidav --host={self.host} --port={self.port} --root={self.root_path} --auth=pam-login"
            elif system_type == "Darwin":
                command = f"wsgidav --host={self.host} --port={self.port} --root={self.root_path} --auth=pam-login"
            else:
                logger.logger.error("不支持的操作系统类型。")

            command_to_run = command
            command_thread = threading.Thread(target=run_command_with_output, args=(command_to_run,))
            command_thread.start()

        except:
            timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
            filename = f'error_{timestamp}.txt'
            with open(filename, 'w') as f:
                traceback.print_exc(file=f)
            logger.logger.error(f"未知错误，报错已保存到{filename}")


# 企业微信推送部分
class WeChatPush:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self.get_access_token()

    def send_text_message(self, message):
        send_text_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(self.access_token)
        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": message
            },
            "safe": 0,
        }
        text_message_res = requests.post(url=send_text_url, data=json.dumps(data)).json()
        return text_message_res

    def get_media_id(self, filetype, path):
        upload_file_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}".format(
            self.access_token, filetype)
        files = {filetype: open(path, 'rb')}
        file_upload_result = requests.post(upload_file_url, files=files).json()
        return file_upload_result["media_id"]

    def send_picture_message(self, media_id):
        send_picture_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(self.access_token)
        data = {
            "touser": "@all",
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": media_id
            },
            "safe": 0,
        }
        picture_message_res = requests.post(url=send_picture_url, data=json.dumps(data)).json()
        return picture_message_res

    def get_access_token(self):
        get_act_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(
            self.corpid, self.corpsecret)
        act_res = requests.get(url=get_act_url).json()
        access_token = act_res["access_token"]
        return access_token


# 日志系统部分

class Logger:
    def __init__(self):
        # 创建一个日志器
        self.logger = logging.getLogger("logger")

        # 设置日志输出的最低等级,低于当前等级则会被忽略
        self.logger.setLevel(logging.INFO)

        # 创建处理器：sh为控制台处理器，fh为文件处理器
        sh = logging.StreamHandler()

        # 创建处理器：sh为控制台处理器，fh为文件处理器,log_file为日志存放的文件夹
        log_file = os.path.join("print.log")
        fh = logging.FileHandler(log_file, mode="a", encoding="UTF-8")

        # 创建格式器,并将sh，fh设置对应的格式
        formator = logging.Formatter(fmt="%(asctime)s %(levelname)s :%(message)s",
                                     datefmt="%Y/%m/%d %X")
        sh.setFormatter(formator)
        fh.setFormatter(formator)

        # 将处理器，添加至日志器中
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


class WebDavLogger:
    def __init__(self):
        # 创建一个日志器
        self.logger = logging.getLogger("webdav_logger")

        # 设置日志输出的最低等级,低于当前等级则会被忽略
        self.logger.setLevel(logging.INFO)

        # 创建处理器：sh为控制台处理器，fh为文件处理器
        sh = logging.StreamHandler()

        # 创建处理器：sh为控制台处理器，fh为文件处理器,log_file为日志存放的文件夹
        log_file = os.path.join("print.log")
        fh = logging.FileHandler(log_file, mode="a", encoding="UTF-8")

        # 创建格式器,并将sh，fh设置对应的格式
        formator = logging.Formatter('')
        sh.setFormatter(formator)
        fh.setFormatter(formator)

        # 将处理器，添加至日志器中
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


# 文件夹 Hook 部分
class FolderWatcher:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.observer = Observer()  # 创建一个观察者对象

    def start(self):
        event_handler = EventHandler()  # 创建一个事件处理器对象
        self.observer.schedule(event_handler, self.folder_path, recursive=False)  # 将事件处理器与观察者关联
        self.observer.start()  # 启动观察者
        logger.logger.info(f"正在监听{file}")

        try:
            while True:
                time.sleep(1)  # 持续运行，每隔1秒检查一次事件
        except KeyboardInterrupt:
            logger.logger.warning("轻传-Server 服务被中断")
            wechat_push.send_text_message("轻传-Server 服务被中断")
            self.observer.stop()  # 捕获键盘中断信号，停止观察者

        self.observer.join()  # 等待观察者线程结束


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        当有文件或文件夹创建时触发该事件
        """
        if not event.is_directory:  # 判断是否为文件
            filepath = event.src_path  # 获取新创建的文件的路径
            if filepath.endswith('.md'):  # 判断文件是否为.md文件
                self.process_md_file(filepath)  # 调用处理.md文件的方法

    def process_md_file(self, filename):  # 处理.md文件的方法
        try:
            logger.logger.info(f"Hook 文件夹新增了一个Markdown文件: {filename}")
            TypechoPublish.publish_to_typecho(filename, url, username, password)
        except:
            # 捕获所有异常，并将Traceback信息写入到文件中
            try:
                timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
                filename = f'error_{timestamp}.txt'
                with open(filename, 'w') as f:
                    traceback.print_exc(file=f)
                logger.logger.error(f"XMLRPC 认证失败，请检查配置文件，报错已保存到{filename}")
            except:
                logger.logger.error("请检查权限。无法创建错误文件")


# 文档 Publish 部分
class TypechoPublish:
    """
    这里是与XML-RPC交互，Markdown渲染部分
    """

    def publish_to_typecho(markdown_file, url, username, password):
        """
        发布Markdown内容到Typecho
        """
        # 读取Markdown文件内容
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 读取Markdown文件名
        title = os.path.splitext(os.path.basename(markdown_file))[0]

        # 解析YAML头信息
        yaml_lines = []
        content_lines = content.splitlines()
        yaml_start = None
        for idx, line in enumerate(content_lines):
            if line.strip() == '---':
                if yaml_start is not None:
                    yaml_end = idx
                    break
                else:
                    yaml_start = idx + 1
            elif yaml_start is not None:
                yaml_lines.append(line)

        if yaml_start is not None:
            yaml_str = "\n".join(yaml_lines)
            try:
                metadata = yaml.safe_load(yaml_str)
            except yaml.constructor.ConstructorError:
                print("YAML头信息解析错误，请检查YAML头信息内容和格式是否正确")
                return
        else:
            metadata = {}



        # 连接到Typecho的XML-RPC接口
        server = xmlrpc.client.ServerProxy(url)

        # 解析去除 YAML 字段 正文部分Markdown文档
        md_content = "\n".join(content_lines[yaml_end + 1:])  # 连接YAML头之后的内容行
        # 创建 Mistune 实例，解析 Markdown 正文文档，并添加TOC Table Strikethrough删除线
        markdown = mistune.create_markdown(
            plugins=[
                'strikethrough',
                'table',
                'task_lists',
                RSTDirective([TableOfContents()]),
            ]
        )
        html_content = markdown(md_content)

        # 从 .slug_cid_mapping.yml 中加载已保存的文章信息
        try:
            with open(".slug_cid_mapping.yml", "r") as file:
                slug_cid_mapping = yaml.safe_load(file)
        except FileNotFoundError:
            slug_cid_mapping = {}

        # 检查是否有对应标题的文章已经发布
        if title in slug_cid_mapping:
            post_id = slug_cid_mapping[title]['post_id']
            # 使用已有的文章ID进行更新
            post = {
                'title': title,  # 文章标题
                'description': html_content,  # 文章内容
                'categories': metadata.get('categories', []),  # 文章分类
                'mt_keywords': metadata.get('mt_keywords', [])  # 文章Tag
            }
            server.metaWeblog.editPost(post_id, username, password, post, True)
            logger.logger.info(f"标题:{title},id:{post_id}文章更新成功！")
            wechat_push.send_text_message(f"标题:{title},id:{post_id}文章更新成功！")
        else:
            # 如果文章是新的，使用 XML-RPC API 进行发布
            # 登录并获取会话ID
            session_id = server.metaWeblog.getUsersBlogs('', username, password)[0]['blogid']
            # 文章参数
            post = {
                'title': title,  # 文章标题
                'description': html_content,  # 文章内容
                'categories': metadata.get('categories', []),  # 文章分类
                'mt_keywords': metadata.get('mt_keywords', [])  # 文章Tag
            }
            # 发布文章
            post_id = server.metaWeblog.newPost(session_id, username, password, post, True)
            if post_id:
                logger.logger.info(f"标题:{title},id:{post_id}文章发布成功！")
                wechat_push.send_text_message(f"标题:{title},id:{post_id}文章发布成功！")
                # 将新文章的信息保存到 .slug_cid_mapping 中
                slug_cid_mapping[title] = {
                    'post_id': post_id,
                    'categories': metadata.get('categories', []),
                    'mt_keywords': metadata.get('mt_keywords', [])
                }
                # 保存更新后的 .slug_cid_mapping.yml 文件，使用追加模式 'a'
                with open(".slug_cid_mapping.yml", "a") as file:
                    file.write(f"\n{title}:\n")
                    file.write(f"  post_id: {post_id}\n")
                    file.write(f"  categories: {metadata.get('categories', [])}\n")
                    file.write(f"  mt_keywords: {metadata.get('mt_keywords', [])}\n")
            else:
                print("文章发布失败！")


# 配置文件部分
class ConfigManager:
    """
    配置文件检查
    """
    CONFIG_FILE_NAME = 'config.yaml'

    @staticmethod
    def get_default_config():
        """
        默认的配置信息，如果配置文件缺失或配置项缺失，则会使用这里定义的默认值
        """
        return {
            'QingQ': {
                'Corp_id': 'Wechat Corp_id',
                'Corp_secret': 'Wechat Corp_secret',
                'Agentid': 'Wechat App Agentid',
                'File_dir': 'Hook File PS: C:\...\...',
                'Url': 'https://Your_Server_Url/action/xmlrpc',
                'Username': 'Your_Typecho_User',
                'Password': 'Your_Typecho_Password',
                'Webdav_host': '0.0.0.0',
                'Webdav_port': '8080',
                'Webdav_root_path': 'Webdav Server Root File PS: /.../... '
            }
        }

    @classmethod
    def load_config(cls):
        """
        这里是 Config.yml 生成以及检测相关
        """
        # 检查配置文件是否存在
        if os.path.exists(cls.CONFIG_FILE_NAME):
            # 如果配置文件存在，尝试加载配置数据
            with open(cls.CONFIG_FILE_NAME, 'r') as config_file:
                config_content = config_file.read()
                # 如果配置文件内容为空，则使用默认配置
                if not config_content.strip():
                    logger.logger.error("配置文件为空，将使用默认配置。")
                    config_data = cls.get_default_config()
                else:
                    try:
                        config_data = yaml.safe_load(config_content)
                        if not isinstance(config_data, dict):
                            # 如果配置文件中只有字典名而没有键值对，则使用默认配置
                            logger.logger.error("配置文件内容不正确，将使用默认配置。")
                            config_data = cls.get_default_config()
                        elif 'QingQ' not in config_data:
                            # 如果配置文件中没有QingQ字段，则使用默认配置
                            logger.logger.error("配置文件缺少QingQ字段，将使用默认配置。")
                            config_data['QingQ'] = cls.get_default_config()['QingQ']
                        elif not isinstance(config_data['QingQ'], dict):
                            # 如果QingQ字段的值不是一个字典，则使用默认配置
                            logger.logger.error("QingQ字段内容不正确，将使用默认配置。")
                            config_data['QingQ'] = cls.get_default_config()['QingQ']
                    except yaml.YAMLError:
                        # 如果配置文件内容不正确，打印错误信息，使用默认配置
                        logger.logger.error("配置文件内容不正确，将使用默认配置。")
                        config_data = cls.get_default_config()
        else:
            # 如果配置文件不存在，打印信息，使用默认配置
            config_data = cls.get_default_config()
            logger.logger.error("配置文件不存在，将使用默认配置。")

        # 确保配置文件中包含QingQ字典，并添加缺失的键
        # setdefault函数在config_data字典中查找'QingQ'键
        typecho_config = config_data.setdefault('QingQ')
        # 获取默认配置中的Typecho字典
        default_typecho_config = cls.get_default_config()['QingQ']
        for key, value in default_typecho_config.items():
            # 对于默认配置中的每个键值对，检查是否在配置文件中，如果不存在，则添加该键值对
            typecho_config.setdefault(key, value)

        # 保存配置数据，以确保缺失的键值对得到添加或更新
        cls.save_config(config_data)

        # 返回配置数据
        return config_data

    @classmethod
    def save_config(cls, config_data):
        """
        将配置数据保存到配置文件
        """
        with open(cls.CONFIG_FILE_NAME, 'w') as config_file:
            yaml.dump(config_data, config_file)


def ver():
    ver = '1.2 - Server'
    logger.logger.info('--------------------')
    logger.logger.info('Copyright (C) 2023 kodesu, Inc. All Rights Reserved ')
    logger.logger.info('Date    : 2023-7')
    logger.logger.info('Author  : kodesu')
    logger.logger.info('Blog    : https://kookoo.top')
    logger.logger.info('Github  : https://github.com/Xingsandesu/QingQ-XMLRPC-Client')
    logger.logger.info(f"Ver     : {ver}")
    logger.logger.info('Model   : Server hook')
    logger.logger.info('--------------------')


if __name__ == "__main__":
    # 版本显示
    try:
        # 初始化日志系统
        logger = Logger()

        # 显示版本信息
        ver()

        # 获取当前脚本所在的文件夹路径
        # 检查是否已经打包成可执行文件
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件，使用sys.executable获取可执行文件的路径
            current_path = os.path.dirname(sys.executable)
        else:
            # 如果是脚本文件，使用os.path.abspath(__file__)获取脚本文件的路径
            current_path = os.path.dirname(os.path.abspath(__file__))

        # 将当前路径设置为工作路径
        os.chdir(current_path)

        # 获取当前工作目录
        current_dir = os.getcwd()
        logger.logger.info(f"当前工作目录:{current_dir}")

        # 拼接配置文件的完整路径
        config_file_path = os.path.join(current_dir, ConfigManager.CONFIG_FILE_NAME)
        logger.logger.info(f"配置文件工作目录:{config_file_path}")

        try:
            # 尝试加载配置文件
            config = ConfigManager.load_config()
            url = config['QingQ']['Url']
            username = config['QingQ']['Username']
            password = config['QingQ']['Password']
            file = config['QingQ']['File_dir']
            corpid = config['QingQ']['Corp_id']
            agentid = config['QingQ']['Agentid']
            corpsecret = config['QingQ']['Corp_secret']
            Webdav_host = config['QingQ']['Webdav_host']
            Webdav_port = config['QingQ']['Webdav_port']
            Webdav_root_path = config['QingQ']['Webdav_root_path']
        except NameError:
            logger.logger.error("请检查配置文件，确认相关信息是否正确，服务器是否能够正常访问，XML-PRC接口是否开启")

        # 打印配置信息
        try:
            logger.logger.info(f"Typecho XML-PRC URL:{url}")
            logger.logger.info(f"用户名:{username}")
            logger.logger.info(f"密码:{password}")
            logger.logger.info(f"监视文件夹路径:{file}")
            logger.logger.info(f"企业微信企业id值:{corpid}")
            logger.logger.info(f"企业微信应用secret值:{corpsecret}")
            logger.logger.info(f"企业微信应用Agentid值:{agentid}")
            logger.logger.info(f"WebDav服务器监听IP:{Webdav_host}")
            logger.logger.info(f"WebDav服务器监听端口:{Webdav_port}")
            logger.logger.info(f"WebDav服务器工作目录:{Webdav_root_path}")
        except NameError:
            logger.logger.error("无法加载配置文件")

        # 加载微信推送 Class
        try:
            wechat_push = WeChatPush(corpid, corpsecret, agentid)
        except KeyError:
            logger.logger.error("企业微信配置错误，请检查企业微信相关配置")
        except NameError:
            logger.logger.error("企业微信配置错误，请检查企业微信相关配置")

        # 加载Webdav Server
        webdav_server = WebDAVServer(webdav_host=Webdav_host, webdav_port=Webdav_port,
                                     webdav_root_path=Webdav_root_path)
        webdav_server.start_server()

        # 加载 文件Hook Class
        try:
            watcher = FolderWatcher(file)
            watcher.start()
        except FileNotFoundError:
            logger.logger.error("监视文件路径配置错误，请检查监视文件路径是否正确")
        except NameError:
            logger.logger.error("监视文件路径配置错误，请检查监视文件路径是否正确")
        except OSError:
            logger.logger.error("监视文件路径配置错误，请检查监视文件路径是否正确")





    except Exception:
        # 捕获所有异常，并将Traceback信息写入到文件中
        try:
            timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
            filename = f'error_{timestamp}.txt'
            with open(filename, 'w') as f:
                traceback.print_exc(file=f)
            logger.logger.error(f"未知错误，报错已保存到{filename}")
        except Exception:
            logger.logger.error("请检查权限。无法创建错误文件")
