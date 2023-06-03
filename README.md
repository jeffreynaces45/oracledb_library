# oracledb_library <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />

> ℹ️ Info
> lo script viene usato per importare delle entry da ldap, dopo averli comporato con i dati all'interno del file csv
> in questo modo possiamo estrarre e importare solo i nuovi account.

# Overview
il programma è diviso in più funzioni, ognuna di questa funzione ha un compito specifico, lo script viene eseguito in ordine:
1. Function Read_file
2. Function Ldap_connessione
3. Function Find_update
4. Function Oracle_connection
5. Function Remove_blank

## Prerequisiti
Installare il pacchetto oracledb tramite il packages manager pip sulla macchina linux lanciando il comando:
```python 
python -m pip install oracledb
```
Installare le librerie di Oracle Client sulla macchina linux, pacchetto rpm.
[instant_client](https://www.oracle.com/database/technologies/instant-client.html)
da quel sito si prende il pacchetto che vogliamo e lo mettiamo dentro una directory della macchina tramite wget
per comodità l’abbiamo lasciato nella directory /opt/oracle
abbiamo lanciato a questo punto il comando rpm -ivh xxx.xxx.rpm per installare il pacchetto.
![image](https://github.com/jeffreynaces45/oracledb_library/assets/68586091/cb57089d-5be6-4880-9a1d-98cd2fcb0961)
Questo documento descrive la procedura per esportare delle utenze di ldap ed importarle poi successivamente su una tabella di un database Oracle.
Impostiamo la variabile d’ambiente per permettere allo script di andare a cercare la libreria oracle quando andremo a eseguire il codice.
export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_10
tramite il commando ENV o PRINTENV possiamo verificare la variabile.
Adesso basterà richiamare  per attivare la modalità python-oracledb in Thick mode cosi da sfruttare tutte le funzionalità della libreria Oracledb. 
```python 
oracledb.init_oracle_client()
```
### <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
Per consultare la libreria andare nel sito, per linux:
[oracledb-on_linux](https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#installing-python-oracledb-on-linux)
### <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
in windows è necessario che imposti la variabile d'ambiente e la richiami nel codice:
```python 
oracledb.init_oracle_client(lib_dir=r"C:\instantclient_21_10") 
```  
## Configurazione
## Read_file
leggo il contenuto del file csv che abbiamo preventivamente creato con tutti gli account che abbiamo importato all'interno del database Oracle.
Questi account sono tutti gli account già caricato sulla tabella, con questo script andremo ad aggiungere nuovi entry_ldap sulla tabella tenendo aggiornata la lista.
## Ldap_connessione
Mi collego al server ldap e filtro per tutti gli object_class='person' per mailboxtipo=s o mailboxtipo=g, estrapolo tutti gli attributi e salvo il contenuto di tutte queste entry.
## Find_update
In questa funzione passo i risultati della ricerca di ldap e la lista del file csv, con questo possiamo:
- per ogni entry nella ricerca_ldap estrapolo i dati
- se l'uid della ricerca_ldap  è presente nel file_csv allora
  -  l'entry è gia presente nella tabella di Oracle
  - altrimenti inserisco la entry di ldap all'interno del file csv, inoltre salvo il contenuto della entry nelle variabili data_sql e data_singolo.
## Oracle_connection
in questa funzione estrapolo le entry_ldap nuove che abbiamo estrapolato con la funzione precente, ci collegghiamo sulla tabella oracle passando le credenziali da admin.
- se la lunghezza dei dati è diverso da 1 e diverso da 9 carichiamo i dati usando lo statement executemany
- altrimenti se la lunghezza dei dati == 9 allora carichiamo il dato (1 singolo account da aggiungere) tramite lo statement execute.
## Remove_blank
questa funzione semplicemente va a eliminare le righe vuote all'interno del file csv.

