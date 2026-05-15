# --coding:utf-8--
import argparse
import sys

from aomaker.send_msg.wechat import WeChatSend
from aomaker.utils.gen_allure_report import get_allure_results

ENV_NAME = {
    "test": "测试环境"
}


class MyWeChatSend(WeChatSend):
    def __init__(self, webhook_key: str, log_url: str = "", webhook: str = None, **kwargs):
        super(MyWeChatSend, self).__init__(**kwargs)
        self.curl = self.wechat_conf[webhook_key]
        if webhook is not None:
            self.curl = webhook
        self.log_url = log_url

    def send_detail_msg(self, sep="_"):
        """通知中可根据标记分类显示通过率
        sep: 标记分隔符
        """
        reports = get_allure_results(sep=sep)
        if reports:
            markdown_li = []
            for product, result in reports.items():
                format_ = f"<font color=\"info\">🎯「{product}」成功率: {result['passed_rate']}</font>"
                markdown_li.append(format_)
            format_product_rate = "\n".join(markdown_li)
        else:
            format_product_rate = ""
        api_counts = self.total
        text = f"""# 【{self.title}】
 ## 基础信息
🌐测试环境：<font color=\"info\">http://172.31.17.34:30880</font>
📦仓库地址：<font color=\"info\">https://github.com/CloudNativeTools/kse-api-test</font>
👤执行人：<font color=\"comment\">autotest</font>
 ## 执行结果
<font color=\"info\">🎯运行成功率: {self.passed_rate}</font>
{format_product_rate}
❤️用例  总数：<font color=\"info\">{self.total}个</font>
😁成功用例数：<font color=\"info\">{self.passed}个</font>
😭失败用例数：`{self.failed}个`
😡阻塞用例数：`{self.broken}个`
😶跳过用例数：<font color=\"warning\">{self.skipped}个</font>
🕓用例执行时长：<font color=\"warning\">{self.duration}</font>\n
 ## 测试输出
📊测试报告：[click me]({self.report_address})
📄运行日志：[click me]({self.log_url})"""
        self._send_markdown(text)
        self.config_db.close()


def _get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--job_name', default='')
    parser.add_argument('-n', '--build_number', default='')
    parser.add_argument('-u', '--report_url', default='')
    parser.add_argument('--build_user', default='')
    parser.add_argument('-r', '--build_result', default='')
    parser.add_argument('-t', '--build_time', default='')
    parser.add_argument('-k', '--key', default='')
    parser.add_argument('--test_env', default='test')
    parser.add_argument('-c', '--commit_info', default='')
    # utils.yaml中wechat下的key名，即对应群聊的webhook
    parser.add_argument('-g', '--group', default='webhook')
    parser.add_argument('-w', '--webhook', default=None)
    parser.add_argument('--log_url')
    parser.add_argument('--simple', action="store_true")

    return parser


def send_msg(args):
    """发送企业微信通知"""
    parser = _get_parser()
    args, _ = parser.parse_known_args(args)
    test_env = args.test_env
    env = ENV_NAME.get(test_env)
    title = "kse自动化测试-{}".format(env)
    tester = "陆乔时"
    report_address = args.report_url
    webhook_key = args.group
    log_url = args.log_url
    webhook = args.webhook
    wechat = MyWeChatSend(tester=tester, title=title, report_address=report_address, log_url=log_url,
                          webhook_key=webhook_key, webhook=webhook)
    send_func = wechat.send_msg if args.simple else wechat.send_detail_msg
    send_func()


if __name__ == '__main__':
    args = sys.argv[1:]
    send_msg(args)
    # reports = get_allure_results(sep="_")
    # print(reports)
