
  
# Postgress db

To install postgres sql

```
sudo apt install postgresql
```

```
sudo -i -u postgres
```

```
psql
```

# change password

## Switch to the PostgreSQL user:

```
sudo -i -u postgres
```

## Access the PostgreSQL CLI:
Set a password for the postgres user (or reset it if you already have one):

```
ALTER USER postgres PASSWORD 'yourpassword';
```

## Exit the PostgreSQL CLI:
```
\q
```
Now you should be able to run pg_dump and use the password you just set.

# Create a backup

```
mkdir backup
```

```
sudo chown postgres:postgres /home/ubuntu/backup
sudo chmod 700 /home/ubuntu/backup
```



# Backup cmd:

```
sudo pg_dump -U postgres -W -F c -b -v -f /home/ubuntu/backup/dec-17.backup sigici_data
```

## Issue with backup

1) Open the file
```
sudo nano /etc/postgresql/<version>/main/pg_hba.conf
```

2) Locate the Peer Authentication Entry: Find a line like this:

```
local   all   postgres   peer
```

3) Change peer to md5: Modify the line to:

```
local   all   postgres   md5
```

4) Restart
   
```
sudo systemctl restart postgresql
```

5) Permission

 ```
sudo chown ubuntu:ubuntu /home/ubuntu/backup
sudo chmod 755 /home/ubuntu/backup
 ```

## share the backup file to local

```
scp ubuntu@54.37.65.120:/home/ubuntu/backup/dec-17.backup /home/ss-pr-cpu-37nwe/Desktop/strategy/strategy_prod_official/database/backup
```

## Share the backup file from local to server

```
scp /home/ss-pr-cpu-37nwe/Desktop/strategy/strategy_prod_official/database/backup/dec-17.backup ubuntu@54.37.65.120:/home/ubuntu/backup
```

## Restore the backup file

```
pg_restore -U postgres -d sigici_data -v /home/ubuntu/backup/dec-17.backup
```
