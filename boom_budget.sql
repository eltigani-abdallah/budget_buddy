-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: boom_budget
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comptes`
--

DROP TABLE IF EXISTS `comptes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comptes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int DEFAULT NULL,
  `solde` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `comptes_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comptes`
--

LOCK TABLES `comptes` WRITE;
/*!40000 ALTER TABLE `comptes` DISABLE KEYS */;
/*!40000 ALTER TABLE `comptes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reference` varchar(255) NOT NULL,
  `description` text,
  `amount` decimal(10,2) NOT NULL,
  `date` datetime NOT NULL,
  `type` varchar(50) NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'depot ','loyer',200.00,'2025-03-19 10:55:00','Dépôt','loyer mois de mars'),(2,'gift ','your winner loto',200000.00,'2025-03-19 10:59:46','Transfert','loto'),(3,'Virement','loyer',134.00,'2025-03-19 11:41:35','Transfert','loyer du mois de mars'),(4,'Virement','loyer',134.00,'2025-03-19 11:42:21','Dépôt','loyer du mois de mars'),(5,'paiement','loyer',150.00,'2025-03-19 11:43:32','Transfert','mois de mars'),(6,'D35354KJ54f5','achat pc gamer',3000.00,'2025-03-19 11:55:58','Transfert','PC'),(7,'D35354KJ54f5','achat pc gamer',3000.00,'2025-03-19 11:56:11','Retrait','PC'),(8,'D35354KJ54f5','achat pc gamer',1600.00,'2025-03-19 11:56:43','Retrait','PC'),(9,'D35354K54f5','ps5',500.00,'2025-03-19 11:57:09','Retrait','playstation'),(10,'mr dupond','loyer du mois de mars',130.00,'2025-03-19 13:57:20','Transfert','loyer'),(11,'mr dupond','loyer du mois de mars',700.00,'2025-03-19 13:59:37','Transfert','loyer'),(12,'dh5353d','achat jeux video',120.00,'2025-03-19 15:40:32','Retrait','loisir');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `date_inscription` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateurs`
--

LOCK TABLES `utilisateurs` WRITE;
/*!40000 ALTER TABLE `utilisateurs` DISABLE KEYS */;
INSERT INTO `utilisateurs` VALUES (1,'Dupont','Jean','jean.dupont@example.com','MotDePasseHashéIci','2025-03-17 10:37:58'),(2,'sdf','fdsd','fdsg','$2b$12$xacQ7TnBJCJM7lGKhCkQdOqITRpAcLcRbmVVpsz0IQtrPqsTxHQxe','2025-03-17 11:02:47'),(3,'abc','def','zbatata484@gmail.com','$2b$12$2A1aCGEIa8HcWpTOWeP33.zeG4QAsP5uhihL3fNWCWhi4rUDa/Jfa','2025-03-17 11:08:44'),(7,'riad','bey','vanessa.sabatier@laplateforme.io','$2b$12$LKjFholbXYSPLQQn.AH7BO0VOvDpcf/PRlrGmkPFjYBJdUalMX/5e','2025-03-17 11:22:37'),(10,'riad','bey','ashdu13015@gmail.com','$2b$12$ExE./aciYkLvKZBJVrFcsOEAhpbQabhLw4aEA70RgcWhIg6iANUba','2025-03-17 11:24:28'),(12,'ufl','opl','riad1313@gmail.com','$2b$12$Q4LjChpjZ//5R/tW0CVATOtHlA/GsKfRf/6UIxV0gTYV6wpJ9aqb.','2025-03-17 11:29:00'),(13,'elti','eltmpm','elti32565@gmail.com','$2b$12$CYnBZInZNwz70Ep2Bw4vk.wnCl3s0Z6P/o7mZsWx10T0iPxLfRhtS','2025-03-17 13:24:53'),(14,'alice','dubois','alice-dubois@gmail.com','$2b$12$yuf7NmGFFlmyBnRQCb7VDuB72I1tCHCr3ZfKBUcAAaILgDjMt0T/S','2025-03-17 14:36:47'),(15,'adv','sfd','adv13@gmail.com','$2b$12$.9dQ/fDrUnuU7Q46UAuqJe/fof2iH6JMxnshYXJsPQYfenzpPDK1.','2025-03-18 07:17:17'),(16,'yuiliia','abc','yuiliia13@gmail.com','$2b$12$dL7ayxciCObZ/gwxn7ZNGuSnOJBt2rjxedR0lQuCQ7dG65Jdk3M.6','2025-03-18 10:15:46'),(17,'vanessa','sabatier','poulet1313@gmail.com','$2b$12$22Sllpt2JXNpxz9aS20vpuG8LfWpP0ARGit8t3IqG5OA6eoL79Tvy','2025-03-18 11:55:01'),(18,'AzRia','Saito','kiritodu13@gmail.com','$2b$12$E7dATLV6/7nd.OREM.z6OeUtBCpLy6NEBa55N9HwkCcm4y7fQcawS','2025-03-19 07:07:25'),(19,'noa','noa ','Noanoa13@gmail.com','$2b$12$5GEvZk9ShTIIbWOvzV6zyO/HHIeQ2k2cT3VP2pM6IZm3Mq35hq/JS','2025-03-19 07:33:48'),(20,'Pablo','Escobar','pablo.escobar@gmail.com','$2b$12$euowX4kkso6rdH6cBVvWc.jeOU3Y/02DtdQRgoL/HjPN/WjVOO/l2','2025-03-20 06:57:02');
/*!40000 ALTER TABLE `utilisateurs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-20 10:00:03
