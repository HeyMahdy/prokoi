Hello from GitHub
# Method 1: Specify database in command
sudo /opt/lampp/bin/mysql -u root testdb < myapp/schema/user.sql

# Method 2: Use -e flag with commands
sudo /opt/lampp/bin/mysql -u root -e "USE testdb; SOURCE /path/to/file.sql;"

# Method 3: Interactive mode
sudo /opt/lampp/bin/mysql -u root
> CREATE DATABASE IF NOT EXISTS testdb;
> USE testdb;
> SOURCE /path/to/file.sql;