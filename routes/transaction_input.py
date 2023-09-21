from flask import Flask, render_template, redirect, url_for, Blueprint, request, flash
import sqlite3
import yfinance as yf
from datetime import datetime
from db_manager import DatabaseManager, StockManager,PortfolioManager,ProfitlossManager

transaction_route = Blueprint("transaction_route", __name__)



@transaction_route.route("/transaction/<username>", methods=[ "GET"])
def transaction_input(username):
    db_manager = DatabaseManager('database.db')
    portfolio_manager = PortfolioManager(db_manager)
    rows=portfolio_manager.get_portfolio_user(username)
    total_investment=portfolio_manager.get_buyprice_total(username)
    if rows!=[]:
        print("inside transaction")
        total_investment=total_investment[0][0]

        total_current_value=portfolio_manager.get_cmp_total(username)
        total_current_value=total_current_value[0][0]
        print(total_current_value)

        return render_template("app_pages/transaction_input.html",rows=rows,total_investment=total_investment,
                           total_current_value=total_current_value)
    else:
        return render_template("app_pages/transaction_input.html",rows=[],total_investment=0,
                           total_current_value=0)



# transaction input to home
# transaction input to portfolio