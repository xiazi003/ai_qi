from flask import render_template, make_response, request
from ... import main
from . import gen_view_data, make_view_response
from flaskr.get_data.db import execute_sql
import matplotlib.pyplot as plt


def layout_resp():
    resp = make_response(render_template('views/layout_overall_bar.html'))
    return resp


@main.route('/views/view_overall_bar', methods=['POST'])
def view_overall_bar():
    type = request.form.get('type')
    return make_view_response(plot_overall_bar, type=type)


def plot_overall_bar(type):
    '''
    绘制 股票交易记录数据 【每日】
    :param name:
    :return:
    '''
    sql = "select count(*) as count,c_name from stock_industry group by c_name order by count desc limit 5"
    df = execute_sql(sql)
    df.cumsum(0)

    plot = df.plot(x='c_name', title="行业公司数量分布", kind='bar')
    fig = plot.get_figure()

    plt.ylabel('公司数量')
    # 由于字体显示太大  导致显示不完全，所以需要重新设置x轴标签字体大小
    # 参考此博文 [https://www.cnblogs.com/Qwells/p/6215280.html]
    plt.xticks(fontsize=7)

    data = gen_view_data(fig)
    return data