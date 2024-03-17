import os
import toml
import click

from . import log, cmd, app

BIN_HOME = '/usr/local/bin'
APP_HOME = '/usr/local/app'
APPGET_HOME = '/usr/local/app/appget'
APPGET_BIN = '/usr/local/app/appget/bin'
APPGET_LIB = '/usr/local/app/appget/lib'
APPGET_PLUGINS = '/usr/local/app/appget/plugins'
APPGET_CONFIG = '/usr/local/app/appget/.config/appget.toml'


class AppGet(app.App):
    # metadata 元数据
    name = 'appget'  # 名称
    desc = 'A tool for installing custom software'  # 描述
    homepage = 'https://github.com/lonelypale/appget'  # 主页
    license = 'MIT'  # 许可证

    # 其他属性
    config = {}  # 配置文件字典

    def __init__(self):
        super().__init__()
        self.__load_config()
        print(f'__file__={__file__}')

    def __load_config(self):
        if os.path.exists(APPGET_CONFIG):
            self.config = toml.load(APPGET_CONFIG)
        else:
            log.error(f'config file does not exist: {APPGET_CONFIG}')

    def __load_plugins(self):
        pass

    def install(self):
        log.info("install")

    def uninstall(self):
        log.info("uninstall")

    def update(self):
        log.info("update")

    def upgrade(self):
        log.info("upgrade")

    def list(self):
        log.info("list")

    def info(self):
        log.info("info")

    def search(self):
        log.info("search")


@click.group()
@click.help_option('-h', '--help')
@click.version_option('v0.1.0', '-v', '--version', message='appget version v0.1.0  (剑意无痕，千山飞雪。)')
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj['APPGET'] = AppGet()


@cli.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
@click.pass_context
def install(ctx, name, count):
    """
    asdf 测试 docs
    :param ctx:
    :param name:
    :param count:
    :return:
    """
    ctx.obj['APPGET'].install()
    return
    try:
        statinfo = os.stat(APPGET_HOME)
    except FileNotFoundError:
        try:
            # xattr -d com.apple.provenance ./appget
            os.makedirs(APPGET_HOME)
            statinfo = os.stat(APPGET_HOME)
            log.info(f'created directory: {APPGET_HOME}')
        except PermissionError as err:
            raise Exception(err.__str__())
    except Exception:
        raise
    print(statinfo)


@cli.command()
@click.pass_context
def uninstall(ctx):
    ctx.obj['APPGET'].uninstall()
    return
    cmd.run(f'rm -rf {APPGET_HOME}')


@cli.command()
@click.pass_context
def update(ctx):
    ctx.obj['APPGET'].update()
    return
    cmd.run(f'python3 -m pip install --upgrade --target={APPGET_LIB} appget')


@cli.command()
@click.pass_context
def upgrade(ctx):
    ctx.obj['APPGET'].upgrade()


@cli.command(name='list')
@click.pass_context
def list_alias(ctx):
    ctx.obj['APPGET'].list()


@cli.command()
@click.pass_context
def info(ctx):
    ctx.obj['APPGET'].info()


@cli.command()
@click.pass_context
def search(ctx):
    ctx.obj['APPGET'].search()
