import psycopg2
import hashlib
import re
###
# TODO : pip install psycopg2
###
###
# TODO : first step you sould create your user and database to read, write and remove data from it.
###
conn = psycopg2.connect(
    database="maktab",
    user="maktab",
    password="maktab",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
try:
    cur.execute(
        "create table users (username varchar(200) primary key,password varchar(200))")
    cur.execute(
        "create table admin (username varchar(200) primary key,password varchar(200))")
except psycopg2.errors.DuplicateTable:
    pass
conn.commit()

# this moudle hash any password in login ,register and update password
def hashing(password: str):
    # TODO : this regex just accept when password has 8 or more lenth and have lower case upper case caracters and symols like [!@#$%^&*]
    if re.match(r"([a-zA-Z0-9!@#$%^&*()-=+,<>.?:;|~]{8,})", password):
        text = hashlib.sha1(password.encode())
        return text.hexdigest()

# this moudle for register user and create contact table with name contact_USERNAME to save contacts ther
def register(username, password):
    insert_user_query = f"insert into users values ('{username}','{
        hashing(password)}')"
    create_user_contact_table_query = f"create table contact_{
        username} (name varchar(200) not null,email varchar(200),mobile varchar(200) not null,phone varchar(200),address varchar(200))"
    cur.execute(insert_user_query)
    cur.execute(create_user_contact_table_query)
    conn.commit()


def login(username, password):
    qurery_login = f"select password from users where username = '{username}'"
    cur.execute(qurery_login)
    if cur.fetchone()[0] == hashing(password):
        conn.commit()
        return True
    return False


def change_password(username, old_password, new_password):
    if login(username, old_password):
        change_password_query = f"update users set password = '{
            hashing(new_password)}' where username = '{username}'"
        cur.execute(change_password_query)
        conn.commit()
        return True
    return False


def admin_register(admin_username, admin_password):
    insert_admin_query = f"insert into admin values ('{admin_username}','{
        hashing(hashing(admin_password))}')"
    cur.execute(insert_admin_query)
    conn.commit()


def admin_login(admin_username, admin_password):
    qurery_login = f"select password from password where username = '{
        username}'"
    cur.execute(qurery_login)
    if cur.fetchone()[0] == hashing(admin_password):
        conn.commit()
        return True
    return False


def admin_change_password(admin_username, admin_old_password, admin_new_password):
    if login(admin_username, admin_old_password):
        change_password_query = f"update users set password = '{
            hashing(admin_new_password)}' where username = '{admin_username}'"
        cur.execute(change_password_query)
        conn.commit()
        return True
    return False


def add_user_contact(username, name, email, mobile, phone, address):
    add_contact_query = f"insert into contact_{
        username} values('{name}','{email}','{mobile}','{phone}','{address}')"
    cur.execute(add_contact_query)
    conn.commit()


def get_contact_user(username):
    get_contact_user_query=f"select * from conatct_{username}"
    cur.execute(get_contact_user_query)
    rows = cur.fetchall()
    contact_dict = {}
    for row in rows:
        contact_dict[row[0]] = {"email":[1],"mobile":[2],"phone":3,"address":4}
    conn.commit()
    return contact_dict

def edit_user_contact(username,name,email,mobile,phone,address):
    edit_user_contact_query=f"update contact_{username} set name = '{name}' email = '{email}' mobile = '{mobile}',phone = '{phone}',address = '{address}' where name = {self.name}"
    cur.execute(edit_user_contact_query)
    conn.commit()

