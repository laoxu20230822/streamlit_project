import os
from pathlib import Path
import sqlite3


from pandas import DataFrame
import streamlit as st

from database.customer import CustomerWhereCause
from database.page import Pageable
from database.page import PageResult


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

def view_customers(conn:sqlite3.Connection,filter:CustomerWhereCause,pageable:Pageable) -> PageResult:
    c = conn.cursor()
    sql=f"SELECT id,name,address,phone FROM customers {filter.to_sql()}"
    count_sql=f"select count(1) from ({sql})"
    sql_with_page=f"{sql} {pageable.limit_sql()}"

    c.execute(count_sql)
    total=c.fetchone()[0]
    print(f"total: {total}")

    c.execute(sql_with_page)
    columns = [col[0] for col in c.description]
    data = [dict(zip(columns, row)) for row in c.fetchall()]
    #conn.close()
    total_page=total//pageable.size
    if total%pageable.size>0:
        total_page+=1
    return PageResult(data,total_page,pageable)


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