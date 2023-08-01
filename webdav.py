import os
import sys
import logging
import time
import traceback
import cherrypy
import yaml
from wsgidav.wsgidav_app import WsgiDAVApp


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


class WebDAVServer:
    """使用cherryPy运行配置创建与启动"""

    def __init__(self, host="localhost", port=8080, webdav_folder=None, verbose=5,
                 webdav_user=None, webdav_password=None):
        self.host = host
        self.port = port
        self.folder = webdav_folder
        self.verbose = verbose
        self.user = webdav_user
        self.password = webdav_password

        self.config = {
            "host": host,
            "port": port,
            "provider_mapping": {"/": {"root": self.folder}},
            "verbose": verbose,
            'logging': {'debug_methods': [],
                        'enable_loggers': [],
                        'logger_date_format': '%Y/%m/%d %X',
                        'logger_format': '%(asctime)s %(levelname)s :%(message)s"'},
            "http_authenticator": {
                "domain_controller": "wsgidav.dc.simple_dc.SimpleDomainController",
                "accept_basic": True,
                "accept_digest": True,
                "default_to_digest": True,
            },
            "simple_dc": {
                "user_mapping": {
                    "*": {
                        self.user: {
                            "password": self.password
                        }
                    }
                },
                "/pub": True
            },
            'dir_browser': {
                "icon": "False",
                "response_trailer": (
                    '<a href="https://github.com/mar10/wsgidav" target="_blank">Power By wsgidav</a><br>'
                    '<a href="https://github.com/Xingsandesu/QingQ-XMLRPC-Client" target="_blank">Work on 轻传</a><br>'
                    '<a href="https://kookoo.top" target="_blank"> Design By KooKoo</a>'
                ),
            },
        }

        wsgidav_app = WsgiDAVApp(self.config)
        cherrypy.tree.graft(wsgidav_app, "/")
        cherrypy.config.update({
            "server.socket_host": self.host,
            "server.socket_port": self.port,
        })
        cherrypy.engine.start()
        print("WebDav服务器启动成功，账号密码为你的Typecho后台账户")
        print("WebDav服务器地址: http://{}:{}/".format(self.config["host"], self.config["port"]))


def webdav_server_start(host, port, root_path, verbose, username, password):
    verbose_value = int(verbose)
    port_value = int(port)
    WebDAVServer(host=host, port=port_value, webdav_folder=root_path, verbose=verbose_value, webdav_user=username,
                 webdav_password=password)


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
                'Username': r'Your_Typecho_User',
                'Password': r'Your_Typecho_Password',
                'Webdav_host': r'0.0.0.0',
                'Webdav_port': r'8080',
                'Webdav_root_path': r'Webdav Server Root File PS: C:\\...\\...',
                'Webdav_verbose': r'0',
            }
        }

    @classmethod
    def load_config(cls):
        """
        这里是 Config.yaml 生成以及检测相关
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


if __name__ == "__main__":
    try:
        logger = Logger()
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
            username = config['QingQ']['Username']
            password = config['QingQ']['Password']
            Webdav_host = config['QingQ']['Webdav_host']
            Webdav_port = config['QingQ']['Webdav_port']
            Webdav_root_path = config['QingQ']['Webdav_root_path']
            Webdav_verbose = config['QingQ']['Webdav_verbose']
        except NameError:
            logger.logger.error("请检查配置文件，确认相关信息是否正确，服务器是否能够正常访问，XML-PRC接口是否开启")

        # 打印配置信息
        try:
            logger.logger.info(f"用户名:{username}")
            logger.logger.info(f"密码:{password}")
            logger.logger.info(f"WebDav服务器监听IP:{Webdav_host}")
            logger.logger.info(f"WebDav服务器监听端口:{Webdav_port}")
            logger.logger.info(f"WebDav服务器工作目录:{Webdav_root_path}")
            logger.logger.info(f"WebDav服务器日志等级:{Webdav_verbose}")
            logger.logger.info(f"注意:Webdav账号密码为您的Typecho账号密码")
            logger.logger.info(f"注意:前服务器日志等级为{Webdav_verbose}，该值可以为0-5.数字越大，日志越详细")
        except NameError:
            logger.logger.error("无法加载配置文件")

        webdav_server_start(Webdav_host, Webdav_port, Webdav_root_path, Webdav_verbose, username, password)
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
