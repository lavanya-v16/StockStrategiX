from flask import Flask, render_template, Blueprint,json,jsonify
from db_manager import DatabaseManager,Insights,StockManager,ProfitlossManager,PortfolioManager
import yfinance as yf
from datetime import datetime

insights_route=Blueprint("insights_route",__name__)

@insights_route.route("/insights/<username>",methods=["GET"])
def insights(username):
    db_manager=DatabaseManager('database.db')
    insights_manager=Insights(db_manager)
    stock_manager=StockManager(db_manager)
    profitloss_manager=ProfitlossManager(db_manager)
    portfolio_manager=PortfolioManager(db_manager)
    rows=portfolio_manager.get_portfolio_user(username)
    if rows!=[]:
        list_of_realized_profit=profitloss_manager.get_highest(username)
        list_of_unrealized_profit=portfolio_manager.get_profit_total(username)
        buy_price_total=portfolio_manager.get_buyprice_total(username)
        percent=(list_of_unrealized_profit[0][0]/buy_price_total[0][0])*100
        if percent>0:
            percent=percent
        else:
            percent=-percent
        total_realised_profit=profitloss_manager.sum_profit(username)
        print(total_realised_profit)




        l=[]
        k=[]
        m=[]
        n=[]
        distr=insights_manager.get_distribution(username)  # percent of different stock based on investment amt
        for sname,distribution in distr:
            l.append(sname)
            k.append(distribution)


        plpercent=insights_manager.pl_percent(username)   # finding profit loss percent , computations done in db manager
        if (list_of_realized_profit) :
            return render_template("app_pages/insights.html", highest=list_of_realized_profit[0], lowest=list_of_realized_profit[-1],
                           sname=l,distribution=k,unrealized=list_of_unrealized_profit[0][0], unrealised_percent=percent,
                             realised_profit=total_realised_profit[0][0],pl=plpercent  )
        else:
            return render_template("app_pages/insights.html" )

        
    
    else:
        return render_template("app_pages/insights.html" )


    # db_manager = DatabaseManager('database.db')
    # insights_manager=Insights(db_manager)
    # stock_manager=StockManager(db_manager)
    # l=[]
    # k=[]
    # m=[]
    # n=[]
    # o=[]
    # p=[]
    # q=[]
    # r=[]
    # s=[]
    # m1=[]
    # n1=[]
    # distr=insights_manager.get_distribution(username)  # percent of different stock based on investment amt
    # for sname,distribution in distr:
    #     l.append(sname)
    #     k.append(distribution)

    # distr=insights_manager.get_top(username)   # list of all stocka in descednign order of profit/loss
    # for sname1,pl in distr:
    #     m.append(sname1)
    #     n.append(pl)

    # m1=m[-3:]      # losers
    # n1=n[-3:]
    # m=m[:3]        #gainers
    # n=n[:3]
    # plpercent=insights_manager.pl_percent(username)   # finding profit loss percent , computations done in db manager
    # print(plpercent)

    # uniquename=stock_manager.get_unique_Stock(username)
    # print(uniquename)
    # print(l)
    # for i in uniquename:
    #     if i[0] not in l:
    #         print("i",i)
    #         s.append(i)       # s contains the list of stocks in transaction log but not on portfolio
    # print("unique",s)

    # for i in l:
    #     stock_name = yf.Ticker(i)
    #     a=stock_name.info["fiftyTwoWeekHigh"]
    #     b=stock_name.info["fiftyTwoWeekLow"]
    #     end_date = datetime.now().strftime('%Y-%m-%d')
    #     stock_name_history = stock_name.history(period="1d")
    #     c=round(stock_name_history.Close[-1], 2)
    #     o.append(a)
    #     p.append(b)
    #     q.append(c)
    #     irow=insights_manager.get_fiftytwo()
    #     if irow==[]:
    #         insights_manager.insert_fiftytwo(i,a,b,c)
    #     else:
    #         entrycount = 0
    #         for j in range(len(irow)):
    #             if irow[j][0] == i:
    #                 entrycount=100
    #                 insights_manager.update_fiftytwo(a,b,c)
    #         if entrycount==0:
    #             insights_manager.insert_fiftytwo(i,a,b,c)
    # for i in range(len(p)):
    #     if ((o[i]+p[i])//2) > q[i]:
    #         r.append(l[i])
    
    
    # return render_template("app_pages/insights.html",sname=l,distribution=k, top_sname=m, top_price=n, last_sname=m1, 
    #                        last_price=n1,pl=plpercent,high=o, low=p, cmp=q,low_cmp=r)