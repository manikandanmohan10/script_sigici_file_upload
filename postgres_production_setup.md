
# PostgreSQL Setup and Backup Guide

## Installing PostgreSQL

To install PostgreSQL, run the following commands:

```
sudo apt install postgresql
```

## To connect to postgreSQL

Switch to the PostgreSQL user:
```
sudo -i -u postgres
```
Access the PostgreSQL CLI:
```
psql
```
Exit the postgresql
```
\q
```


## Changing the PostgreSQL Password

Access the PostgreSQL CLI and set a new password for the postgres user:
```
ALTER USER postgres PASSWORD 'yourpassword';
```

## Allowing External Database Connections

To allow PostgreSQL connections from external servers, follow these steps:

1. Modify the `postgresql.conf` file to allow external connections:

```
sudo nano /etc/postgresql/<version>/main/postgresql.conf
```

Set `listen_addresses` to:

```
listen_addresses = '*'
```

2.Modify the pg_hba.conf file to accept connections:

```
sudo nano /etc/postgresql/<version>/main/pg_hba.conf
```
Add the following line:

```
host    all             all             146.59.239.166/32          md5
```

3.Restart PostgreSQL to apply changes:

```
sudo systemctl restart postgresql
```

## Creating a Backup

1.Create a directory for the backup:

```
mkdir backup
```

2.Set the appropriate permissions:

```
sudo chown ubuntu:ubuntu /home/ubuntu/backup
sudo chmod 755 /home/ubuntu/backup
```

### Resolving Backup Issues

If you encounter issues with backup permissions, follow these steps:

1. Open the `pg_hba.conf` file:

```
sudo nano /etc/postgresql/<version>/main/pg_hba.conf
```

2. Find the line:

```
local   all   postgres   peer
```

3. Change peer to md5:

```
local   all   postgres   md5
```

4. Restart PostgreSQL:

```
sudo systemctl restart postgresql
```

### Backup cmd:

```
sudo pg_dump -U postgres -W -F c -b -v -f /home/ubuntu/backup/dec-17.backup sigici_data
```



## Share the backup file

1.To share the backup file from the server to your local machine:

```
scp ubuntu@54.37.65.120:/home/ubuntu/backup/dec-17.backup <path>/backup
```

2.To share the backup file from local to server

```
scp /home/ubuntu/backup/dec-17-2.backup ubuntu@135.125.181.152:/home/ubuntu/backup
```

## Restore the backup file

```
pg_restore -U postgres -d sigici_data -v /home/ubuntu/backup/dec-17.backup
```
