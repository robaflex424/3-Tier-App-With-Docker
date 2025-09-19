To use this mini docker project you have to connect to the MySQL container and run these commands.(expect docker commands)


1. **mysql -u root -p**   # enter password set by you in **docker-compose.yml** or **mysqlpaassword**




2. **USE mysql_db;**

    **CREATE TABLE IF NOT EXISTS users (**
        **id INT AUTO_INCREMENT PRIMARY KEY,**
        **name VARCHAR(100) NOT NULL**
    **);**




3. **INSERT INTO users (name) VALUES ('Ayrton');**


Afterwards you can visit this URL to see if its really working
        **http://localhost:5000/users**
