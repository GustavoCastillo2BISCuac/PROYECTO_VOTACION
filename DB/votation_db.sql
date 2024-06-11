-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: votation_db
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `person_id` varchar(255) NOT NULL,
  `pwd` varchar(255) NOT NULL,
  UNIQUE KEY `person_id` (`person_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('ine','pwd12345');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parties`
--

DROP TABLE IF EXISTS `parties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parties` (
  `party_id` int NOT NULL AUTO_INCREMENT,
  `party_name` varchar(255) NOT NULL,
  `party_candidate_name` varchar(255) DEFAULT NULL,
  UNIQUE KEY `party_id` (`party_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parties`
--

LOCK TABLES `parties` WRITE;
/*!40000 ALTER TABLE `parties` DISABLE KEYS */;
INSERT INTO `parties` VALUES (1,'Morena','Claudia Sheinbaum'),(2,'Movimiento Ciudadano','Jorge Álvarez Máynes'),(3,'PRI','Xóchil Gálvez'),(4,'','Alejandro'),(5,'Verde','Claudia Sheinbaum'),(6,'PT','Claudia Sheinbaum'),(12,'','Alejandra'),(13,'','Goku'),(20,'','PartidoNuevo');
/*!40000 ALTER TABLE `parties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parties_section`
--

DROP TABLE IF EXISTS `parties_section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parties_section` (
  `section_id` int NOT NULL,
  `party_id` int NOT NULL,
  `counter` int DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parties_section`
--

LOCK TABLES `parties_section` WRITE;
/*!40000 ALTER TABLE `parties_section` DISABLE KEYS */;
INSERT INTO `parties_section` VALUES (1,1,2,1),(1,2,3,2),(1,3,1,3),(1,4,2,4),(2,6,2,5),(2,5,1,6),(2,4,2,7),(2,1,1,8),(2,12,1,9),(3,1,2,10),(3,4,1,11),(3,13,1,12),(5,20,1,14);
/*!40000 ALTER TABLE `parties_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `polling_people`
--

DROP TABLE IF EXISTS `polling_people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `polling_people` (
  `person_id` varchar(255) NOT NULL,
  `section_id` int NOT NULL,
  `person_name` varchar(255) DEFAULT NULL,
  `pwd` varchar(255) NOT NULL,
  UNIQUE KEY `person_id` (`person_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polling_people`
--

LOCK TABLES `polling_people` WRITE;
/*!40000 ALTER TABLE `polling_people` DISABLE KEYS */;
INSERT INTO `polling_people` VALUES ('CAM050929',1,'Manuel Hernandez (Cambiado)','pwd123455');
/*!40000 ALTER TABLE `polling_people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sections` (
  `section_id` int NOT NULL,
  `section_description` varchar(255) NOT NULL,
  UNIQUE KEY `section_id` (`section_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (1,'Calle #1 Entre Calle 0 y Calle 2'),(2,'Calle aleatoria 2 entre colonia aleatoria'),(3,'Calle aleatoria 3 en la colonia Santa Ana'),(4,'Calle aleatoria 4'),(5,'Calle aleatoria 5');
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votes`
--

DROP TABLE IF EXISTS `votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `votes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `section_id` int NOT NULL,
  `person_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votes`
--

LOCK TABLES `votes` WRITE;
/*!40000 ALTER TABLE `votes` DISABLE KEYS */;
INSERT INTO `votes` VALUES (1,1,'test1'),(2,1,'test2'),(6,1,'test3'),(7,1,'test4'),(8,1,'test5'),(9,1,'testA'),(10,1,'testB'),(11,1,'testC'),(12,1,'testD'),(13,1,'testE'),(14,1,'testF'),(15,1,'testN'),(16,2,'Yo'),(17,2,'personarandom'),(18,2,'PersonaRandom2'),(19,2,'hola'),(20,2,'curp'),(21,2,'ajsdnh'),(22,2,'jnwjdn'),(23,2,'jshiajsdbinajnsdkajs'),(24,3,'AA'),(25,3,'JKL');
/*!40000 ALTER TABLE `votes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'votation_db'
--

--
-- Dumping routines for database 'votation_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-10 15:25:46
