DROP DATABASE IF EXISTS buyandride;

CREATE DATABASE IF NOT EXISTS buyandride;

USE buyandride;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL, 
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS vehicules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marque VARCHAR(100) NOT NULL,
    modele VARCHAR(100) NOT NULL,
    prix DECIMAL(10,2) NOT NULL,
    km INT NOT NULL,
    energie VARCHAR(50) NOT NULL,
    photo1 VARCHAR(255),
    photo2 VARCHAR(255),
    photo3 VARCHAR(255), 
    photo4 VARCHAR(255),
    photo5 VARCHAR(255),
    type BOOLEAN,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user_vehicule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    id_vehicule INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id),
    FOREIGN KEY (id_vehicule) REFERENCES vehicules(id)
);

CREATE TABLE IF NOT EXISTS pdf (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    pdf VARCHAR(255) NOT NULL,
    id_vehicule INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id),
    FOREIGN KEY (id_vehicule) REFERENCES vehicules(id)
);
