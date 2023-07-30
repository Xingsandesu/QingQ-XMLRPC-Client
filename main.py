# Copyright (C) 2023 kodesu, Inc. All Rights Reserved
# @Time    : 2023-7
# @Author  : kodesu
# @Blog    : kookoo.top
# ————————————————
import time
import xmlrpc.client
import yaml
import os
import mistune
import sys
from mistune.directives import RSTDirective, TableOfContents
import traceback


class TypechoPublish:
    """
    这里是与XML-PRC交互，Markdown渲染部分
    """

    def publish_to_typecho(markdown_file, url, username, password):
        """
        发布Markdown内容到Typecho
        """
        # 读取Markdown文件内容
        global metadata
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 读取Markdown
        title = os.path.splitext(os.path.basename(markdown_file))[0]

        # 解析YAML头信息
        yaml_end = content.find('---', 3)
        try:
            if yaml_end != -1:
                yaml_str = content[3:yaml_end]
                metadata = yaml.safe_load(yaml_str)
            else:
                metadata = {}
        except yaml.constructor.ConstructorError:
            input("YAML文件头解析错误")
            sys.exit()

        # 连接到Typecho的XML-RPC接口
        server = xmlrpc.client.ServerProxy(url)

        # 登录并获取会话ID
        session_id = server.metaWeblog.getUsersBlogs('', username, password)[0]['blogid']

        # 获取分类

        categories = metadata.get('categories', [])

        # 解析去除 YAML 字段 正文部分Markdown文档
        md_content = content[yaml_end + 3:]
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

        # 文章参数
        post = {
            'title': title,  # 文章标题
            'description': html_content,  # 文章内容
            'categories': categories,  # 文章分类
        }

        # 发布文章
        post_id = server.metaWeblog.newPost(session_id, username, password, post, True)

        if post_id:
            print(f"文章发布成功！文章ID为：{post_id}")
        else:
            print("文章发布失败！")


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
            'Typecho': {
                'url': 'https://YourServerUrl/action/xmlrpc',
                'username': 'YourUser',
                'password': 'Yourpassword'
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
                    print("配置文件为空，将使用默认配置。")
                    config_data = cls.get_default_config()
                else:
                    try:
                        config_data = yaml.safe_load(config_content)
                        if not isinstance(config_data, dict):
                            # 如果配置文件中只有字典名而没有键值对，则使用默认配置
                            print("配置文件内容不正确，将使用默认配置。")
                            config_data = cls.get_default_config()
                        elif 'Typecho' not in config_data:
                            # 如果配置文件中没有Typecho字段，则使用默认配置
                            print("配置文件缺少Typecho字段，将使用默认配置。")
                            config_data['Typecho'] = cls.get_default_config()['Typecho']
                        elif not isinstance(config_data['Typecho'], dict):
                            # 如果Typecho字段的值不是一个字典，则使用默认配置
                            print("Typecho字段内容不正确，将使用默认配置。")
                            config_data['Typecho'] = cls.get_default_config()['Typecho']
                    except yaml.YAMLError:
                        # 如果配置文件内容不正确，打印错误信息，使用默认配置
                        print("配置文件内容不正确，将使用默认配置。")
                        config_data = cls.get_default_config()
        else:
            # 如果配置文件不存在，打印信息，使用默认配置
            print("配置文件不存在，将使用默认配置。")
            config_data = cls.get_default_config()

        # 确保配置文件中包含Typecho字典，并添加缺失的键
        # setdefault函数在config_data字典中查找'Typecho'键
        typecho_config = config_data.setdefault('Typecho')
        # 获取默认配置中的Typecho字典
        default_typecho_config = cls.get_default_config()['Typecho']
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


def get_dragged_file_info():
    """
    拖动文件-Markdown文件指定逻辑
    """
    if len(sys.argv) > 1:
        # 获取第一个命令行参数，即拖动文件的路径
        file_path = sys.argv[1]

        # 获取文件所在的目录路径
        file_directory = os.path.dirname(os.path.abspath(file_path))

        # 获取文件名
        file_name = os.path.basename(file_path)
        if file_name.endswith(".md"):
            print("文件格式正确")
            return file_directory, file_name
        else:
            print("文件格式错误")
    else:
        # 如果没有拖动文件，打印文件路径用于Debug，返回None
        print(f"脚本当前所在目录{os.path.dirname(os.path.abspath(__file__))}")
        return None


def run():
    print('Copyright (C) 2023 kodesu, Inc. All Rights Reserved ')
    print('Date    : 2023-7')
    print('Author  : kodesu')
    print('Blog    : https://kookoo.top')
    print('Github  : https://github.com/Xingsandesu/QingQ-XMLPRC-Client')
    print(f"Ver     : {ver}")
    print('Model   : Normal')
    print('--------------------')
    # Step 1 调用get_dragged_file_info()并存储返回值
    result = get_dragged_file_info()
    if result is not None:
        dragged_file_name: str
        dragged_file_directory, dragged_file_name = result
        print("拖动文件的运行目录：", dragged_file_directory)
        print("拖动文件的文件名：", dragged_file_name)
        # Step 2 设置工作目录环境
        os.chdir(dragged_file_directory)
        # 获取当前工作目录
        current_dir = os.getcwd()
        print(f"当前工作目录:{current_dir}")
        # 拼接配置文件的完整路径
        config_file_path = os.path.join(current_dir, ConfigManager.CONFIG_FILE_NAME)
        print(f"配置文件工作目录:{config_file_path}")
        try:
            # Step3 加载配置文件
            config = ConfigManager.load_config()
            url = config['Typecho']['url']
            username = config['Typecho']['username']
            password = config['Typecho']['password']
            # 打印配置信息
            print(f"Typecho XML-PRC URL:{url}")
            print(f"用户名:{username}")
            print(f"密码:{password}")
            # Step 4 发送内容
            TypechoPublish.publish_to_typecho(dragged_file_name, url, username, password)
            sys.exit()
        except NameError:
            print("请检查配置文件，确认相关信息是否正确，服务器是否能够正常访问，XML-PRC接口是否开启")
            sys.exit()

    else:
        input("没有拖动文件")
        raise NameError('没有拖动文件')


if __name__ == "__main__":
    try:
        ver = '1.0'
        run()
        print("三秒后结束程序")
        time.sleep(3)
        sys.exit()
    except NameError:
        sys.exit()
    except FileNotFoundError:
        input("没有这个文件")
    except Exception:
        # 捕获所有异常，并将Traceback信息写入到文件中
        try:
            timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
            filename = f'error_{timestamp}.txt'
            with open(filename, 'w') as f:
                traceback.print_exc(file=f)
        except Exception:
            input("请检查权限。无法创建错误文件")
