from sqlalchemy import create_engine

username = 'root'
password = 'password1'
host = 'localhost'
database = 'cds'

def main():
    ''' Database String '''
    # return create_engine('mysql://root:root@localhost/cds?charset=utf8&unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock')
    return create_engine("mysql://" + username + ":" + password + "@" + host + "/" + database + "?charset=utf8&unix_socket=/tmp/mysql.sock")
