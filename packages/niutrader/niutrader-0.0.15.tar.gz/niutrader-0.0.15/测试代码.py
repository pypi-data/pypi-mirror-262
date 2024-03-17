from niutrader.niutrader import connect_ths
import pandas as pd
import time
pd.set_option('display.max_columns', 20)
pd.set_option('expand_frame_repr', False)

# 连接同花顺
user = connect_ths()


"""01 获取资金信息"""
print(user.balance)  # 不需要验证码  ，0.4s

# 测试时间开始
start_time = time.time()

"""02 获取持仓信息"""
print(user.position)  # 需要验证码，2.5s左右。没有验证码的话，1.9s左右

# 测试时间结束
elastic_time = time.time() - start_time
print("运行花费时间 %.6fs" % elastic_time)


"""03 买入股票"""
# 限价买入  # 无需验证码，1.1s左右
# buy_msg = user.buy(security='000667', price=1.20, amount=100)  # 限价单，不能低于跌停价
# print(buy_msg)

# 市价买入  # 无需验证码 0.8s左右
# buy_msg = user.market_buy(security='000667', amount=100)
# print(buy_msg)

"""04 卖出股票"""
# 限价卖出
# sell_msg = user.sell(security='000667', price=1.55, amount=100)
# print(sell_msg)

# 市价卖出
# sell_msg = user.market_sell(security='000667', amount=100)
# print(sell_msg)

"""05 撤单"""
# 全部撤单 无需验证码，0.5s左右
# user.cancel_all_entrusts()
# print('全部撤单完毕')

# # 查看可撤单的数据
# can_cancel_msg = user.cancel_entrusts
# df1 = pd.DataFrame(can_cancel_msg)
# print(df1)
# time.sleep(2)
# 只撤单一个（需要订单编号）
# entrust_no = '2527112995'
# cancel_msg = user.cancel_entrust(entrust_no)  # 撤单，注意分辨率缩放为100%，否则报错
# print(cancel_msg)

"""06 查询当日成交"""
# print(user.today_trades)

"""07 查询当日委托"""  # 需要验证码，有验证码2.5s左右，无验证码1.6s
# today_entrusts = user.today_entrusts
# df = pd.DataFrame(today_entrusts)
# print(df)

"""08 刷新数据"""
# user.refresh()

"""09 退出客户端"""
# user.exit()



