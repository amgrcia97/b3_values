from b3_app import db

'''
Password:
>>> mysql -u root
>>> UPDATE mysql.user SET authentication_string=null WHERE User='root';
>>> FLUSH PRIVILEGES;
>>> exit;


Table and Database:
>>> CREATE DATABASE b3_app;
>>> CREATE TABLE users (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(100) NOT NULL, email VARCHAR(30), password VARCHAR(1000), status INT);
>>> CREATE UNIQUE INDEX EMAIL ON users ( email);
>>> CREATE TABLE asset_types (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(100) NOT NULL, description VARCHAR(1000));
>>> CREATE TABLE user_assets (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, user_id int NOT NULL, asset_type int NOT NULL, name VARCHAR(100) NOT NULL, description VARCHAR(1000), qty INT, invested FLOAT(11,7));
>>> ALTER TABLE `b3_app`.`users` ADD COLUMN `logo_url` VARCHAR(1000) NULL AFTER `password`;
'''


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(1000))
    status = db.Column(db.Integer)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class AssetType(db.Model):
    __tablename__ = 'asset_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(80), unique=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class UserAsset(db.Model):
    __tablename__ = 'user_assets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    asset_type = db.Column(db.Integer)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    qty = db.Column(db.Integer)
    invested = db.Column(db.Integer)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
