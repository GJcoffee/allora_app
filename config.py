mysql_config = {
    'host': '192.168.50.20',
    'user': 'root',
    'port': 3306,
    'password': '123456',
    'database': 'haxi',
}  # 本地测试

db_uri = f'mysql://{mysql_config.get("user")}:{mysql_config["password"]}@{mysql_config["host"]}:3306/{mysql_config["database"]}'
