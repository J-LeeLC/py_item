"""
获取翻译参数sign,实现翻译功能
"""

import execjs
import js2py
from flask import Flask, url_for
import pandas as pd
from pandas.core.frame import DataFrame

app = Flask(__name__)


@app.route('/chacun?qStr=<qStr>')
def sign_str(qStr):
    if qStr.find("%@F") != -1:
        q = qStr.replace("%@F", "/")
    else:
        q = qStr
    with open('static/sign.js', 'r', encoding='utf-8') as f:
        content = js2py.EvalJs()  # 实例化解析js对象
        content.execute(f.read())  # js转python代码
        n = content.pro(q)
        sign_c = content.e(n, "320305.131321201")
        return sign_c


with app.test_request_context():
    print(url_for('sign_str', qStr='传感器网络是由大量部署在作用区域内的、具有无线通信与计算能力的微小传感器节点通过自组织方式构成的能根据环境自主完成指定任务的分布式智能化网络系统。'))


if __name__ == '__main__':
    app.debug = True
    app.run()
