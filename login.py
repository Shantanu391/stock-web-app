# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 00:00:34 2022

@author: 91956
"""

import streamlit as st
import pandas as pd
import smtplib
import yfinance as yf


# Security
#passlib,hashlib,bcrypt,scrypt

# DB Management
import sqlite3 
conn = sqlite3.connect('stock.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(name TEXT,email TEXT)')


def add_userdata(name,email):
	c.execute('INSERT INTO userstable(name,email) VALUES (?,?)',(name,email))
	conn.commit()


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def send_email(all_email):
    for dest in all_email:
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()
      s.login("sparrowjohn390@gmail.com", "9561836477")
      message = "Good noon.... Major Project Test email"
      s.sendmail("sparrowjohn390@gmail.com", dest, message)
      s.quit()
      
def get_input():
  start_date = st.sidebar.text_input("Start Date","2020-01-02")
  end_date = st.sidebar.text_input("End Date","2020-08-02")
  stock_symbol = st.sidebar.text_input("Stock Symbol","AMZN")
  return start_date, end_date, stock_symbol

    
def get_data(symbol, start, end):
  data = yf.download(symbol, start=start, end=end)
  return data

def main():
    st.title("Simple Login App")
    menu = ["Stock","Home","Subscription"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Stock":
      start, end, symbol = get_input()
      df = get_data(symbol, start, end)
      st.header(symbol+" Close Price\n")
      st.line_chart(df['Close'])
    
    elif choice == "Home":
        st.subheader("Home")
        user_result = view_all_users()
        clean_db = pd.DataFrame(user_result,columns=["name","email"])
        all_email = clean_db['email'].tolist()
        st.dataframe(clean_db)
        if st.button("Send Email") :
          send_email(all_email)
        
    elif choice == "Subscription":
        st.subheader("Subscription Section")
        name = st.text_input("Name")
        email = st.text_input("Email") 
        if st.button("Subscribe") :
            create_usertable()
            add_userdata(name, email)
            st.success("successfull")
            st.info("Go to Home Screen")
        

if __name__ == '__main__':
	main()