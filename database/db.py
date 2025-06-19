import sqlite3
from pandas import DataFrame
import streamlit as st
import os
from pathlib import Path


@st.cache_resource
def init_db():
    print(f"init_db")
    db_path = Path(__file__).parent.parent / 'customers.db'
    print(f"dbpath::::: {db_path}")
    conn = sqlite3.connect(db_path,check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='customers'
    """)
    if not c.fetchone():
        c.execute('''CREATE TABLE customers
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name text, 
                     address text, 
                     phone text，
                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
    return conn


def batch_insert(df:DataFrame,conn:sqlite3.Connection):
    # 转换为元组列表（适配 executemany 的参数格式）
    data = [tuple(row) for row in df.itertuples(index=False)]
    c = conn.cursor()
    c.executemany("INSERT INTO customers(name,address,phone) VALUES (?,?,?)", data)
    conn.commit()
    #conn.close()

def delete_customer(name):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE name=?", (name,))
    conn.commit()
    #conn.close()

def update_customer(name, address, phone):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("UPDATE customers SET address = ?, phone = ? WHERE name = ?", (address, phone, name))
    conn.commit()
    #conn.close()

def view_customers(conn:sqlite3.Connection):
    c = conn.cursor()
    c.execute("SELECT id,name,address,phone FROM customers")
    columns = [col[0] for col in c.description]
    data = [dict(zip(columns, row)) for row in c.fetchall()]
    #conn.close()
    return data

def search_customer(name, phone):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE name=? OR phone=?", (name, phone))
    customers = c.fetchall()
    #conn.close()
    return customers


def main():
    st.title("Customer Database App")
    
    
    conn=init_db()

    name = st.text_input("Name")
    address = st.text_input("Address")
    phone = st.text_input("Phone Number")
    st.sidebar.header("Click for operations")
    if st.sidebar.button("Add"):
        add_customer(name, address, phone,conn)

    if st.sidebar.button("Delete"):
        delete_customer(name)

    if st.sidebar.button("Update"):
        update_customer(name, address, phone)


    if st.sidebar.button("Search"):
        customers = search_customer(name, phone)
        st.header("Customers File")
        st.table(customers)   

    if st.sidebar.button("View"):
        customers = view_customers()
        st.header("Customers File")
        st.table(customers)

if __name__ == '__main__':
    main()