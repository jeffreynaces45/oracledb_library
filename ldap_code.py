import ldap3
import ssl
from ldap3 import Tls #https://ldap3.readthedocs.io/en/latest/
from ldap3 import Server, Connection, ALL, NTLM
import sqlite3 #https://inloop.github.io/sqlite-viewer/
import pandas as pd # pip install pandas https://www.youtube.com/watch?v=UZIhVmkrAEs&ab_channel=JieJenn
import csv #https://www.pythontutorial.net/python-basics/python-write-csv-file/
import datetime
import oracledb
import time
from datetime import *

# READ_CSV_FILE - read content of csv file
def read_file(FILE_NAME):    
    with open(FILE_NAME, 'r') as csv_file:                    #leggiamo dentro il file csv e leggiamo il suo contenuto
        content = csv_file.read()
    return content

# Find_update - find uid not present in csv file
def find_update(result, lista, FILE_NAME):
    data_sql = []
    for i in result:
        data = [str(i.givenName), str(i.uid), str(i.CodFiscale), str(i.sn), str(i.cn), str(i.mail), str(i.employeeNumber), str(i.shadowFlag), str(i.shadowLastChange)]
        data_confronto = [str(i.givenName), str(i.uid), str(i.CodFiscale)]
        if str(i.uid) in lista:
        #    print(f'{i.uid} è presente nel file csv')
            pass
        else:                                           #se non è presente allora lo inserisco dentro il file ed eseguo la query di import sulla tabella
            with open(FILE_NAME, 'a', encoding='utf-8') as f:
                header = ['givenName', 'uid', 'CodFiscale', 'sn', 'cn', 'mail', 'employeeNumber','shadowFlag','shadowLastChange'] 
                dict = {"givenName": str(i.givenName), "uid": str(i.uid), "CodFiscale": str(i.CodFiscale), "sn": str(i.sn), "cn": str(i.cn), "mail": str(i.mail), "employeeNumber": str(i.employeeNumber), "shadowFlag" : str(i.shadowFlag), "shadowLastChange": str(i.shadowLastChange)}
                dict_obj = csv.DictWriter(f, fieldnames=header)
                dict_obj.writerow(dict)
            f.close()
            data_sql.append((str(i.givenName), str(i.uid), str(i.CodFiscale), str(i.sn), str(i.cn), str(i.mail), str(i.employeeNumber), str(i.shadowFlag), str(i.shadowLastChange)))
            data_singolo=[str(i.givenName), str(i.uid), str(i.CodFiscale), str(i.sn), str(i.cn), str(i.mail), str(i.employeeNumber), str(i.shadowFlag), str(i.shadowLastChange)]
    #if len(data_sql) == 1:
    #    print("adesso eseguo query singola")
    #    data_sql=data_singolo
    #print(data_sql)
    return data_sql

#ORACLE_CONNECTION - Import only ldap_entry not in ldap_csv file into oracle database with query
def oracle_connessione(data):
    # Connessione ORACLE
    oracledb.init_oracle_client()          #necessario per la libreria oracledb
    BATCH_SIZE = 10000
    connection = oracledb.connect(user='MIDPOINT',                          #puntamenti al server oracle
                 password='pswd', dsn='ldap-dns/SERVICE_NAME')
    with connection.cursor() as cursor:
        cursor.setinputsizes(None, 25)
        cursor = connection.cursor()
        sql = "insert into LDAP_SERVICE_USERS (GIVEN_NAME, LDAP_UID, COD_FISCALE, SN, CN, MAIL, EMPLOYEE_NUMBER, SHADOW_FLAG, SHADOW_LAST_CHANGE) values (:1, :2, :3, :4, :5, :6, :7, :8, :9)"
        #print(data)
        now = datetime.now()
        today = date.today()
        current_time = now.strftime("%H:%M")
        #print(len(data))
        if len(data) > 1 and len(data) != 9:
        #    print('adesso carico i dati dentro la tabella LDAP perchè ci sono dati nuovi')
            cursor.executemany(sql, data)
        #    print('account caricati')
            f = open("/tmp/ldap.log", "a")
            f.write(f"data: {today} alle ore: {current_time} abbiamo caricato gli account {data} \n")
            f.close()

        # carico solamente 1 account
        if len(data) == 9:
            cursor.execute(sql, [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
        #    print("account caricato")
            f = open("/tmp/ldap.log", "a")
            f.write(f"data: {today} alle ore: {current_time} abbiamo caricato l' account {data} \n")
            f.close()

        connection.commit()
    return data

#LDAP_CONNECTION - connection ldap e retrieve attributes
def ldap_connessione(): #Stringa di connessione
    server = Server('ldap-server', use_ssl=False, get_info=ALL)
    conn = Connection(server, 'ldap_dn_administrator', 'password_ldap', auto_bind=True)
    #cerchiamo gli account per mailboxTipo e ci prendiamo tutti gli attributi necessari ecc... (&(objectclass=person)(|(codFiscale=XXX)(codFiscale=ZZZ)))
    conn.search('dn_ldap', '(&(objectclass=person)(|(mailboxtipo=s)(mailboxtipo=g)))', attributes=['givenName', 'uid', 'CodFiscale', 'sn', 'cn', 'mail', 'employeeNumber', 'shadowLastChange', 'shadowFlag'])
    result=conn.entries
    return result

#REMOVE_BLANK - metodo per rimuovere spazi bianchi
def remove_blank(FILE_NAME):
    df = pd.read_csv(FILE_NAME, encoding='latin-1')
    df.to_csv(FILE_NAME, index=False)



contenuto =read_file('/tmp/ldap-entry.csv')                          #legge il file csv
result = ldap_connessione()                                 # connessione ldap per ricavare gli attributi e gli account
risultato =find_update(result, contenuto, '/tmp/ldap-entry.csv')     # trova nuovi  account in base al uid (se non trova uid aggiunge l'account) 
oracle_connessione(risultato)                        #si collega sulla tabella e fa l'import di quegli account 
remove_blank('/tmp/ldap-entry.csv')                              # rimuovere gli spazi bianchi sul file csv

