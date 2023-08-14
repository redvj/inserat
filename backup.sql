-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: inserat
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.4

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
-- Table structure for table `advertisement`
--

DROP TABLE IF EXISTS `advertisement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advertisement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb3_bin NOT NULL,
  `description` text COLLATE utf8mb3_bin NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `price` float DEFAULT NULL,
  `contact_info` varchar(255) COLLATE utf8mb3_bin DEFAULT NULL,
  `city_id` int NOT NULL,
  `zip_code` int NOT NULL,
  `category_id` int NOT NULL,
  `subcategory_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `image_filename` varchar(100) COLLATE utf8mb3_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `city_id` (`city_id`),
  KEY `subcategory_id` (`subcategory_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_advertisement_zip_code` (`zip_code`),
  CONSTRAINT `advertisement_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `advertisement_ibfk_2` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
  CONSTRAINT `advertisement_ibfk_3` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`id`),
  CONSTRAINT `advertisement_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement`
--

LOCK TABLES `advertisement` WRITE;
/*!40000 ALTER TABLE `advertisement` DISABLE KEYS */;
INSERT INTO `advertisement` VALUES (1,'Apple watch 7, mit Garantie 9 Monate, Apple watch','Apple watch 7 Alu. 45cm mit Garantie 9 Monate.\r\nEinwandfrei. Norm. Gebrauchsspuren\r\n\r\nVersand möglich plus Porto\r\nAbholen in ','2023-08-13 01:04:53',300.5,'',22,8005,2,6,1,'8025706782_3.jpg'),(3,'Lenovo Yoga Duet 7 13ITL6 Laptop/Tablet neuw. i7, 16GB, 1TB','All-in-One Laptop/Tablet: kann als Tablet oder als Laptop verwendet werden (inklusive Tastatur und Stift), mit Touchscreen. Neupreis 1244 Franken, gekauft am 24. Juni 2021.\r\n\r\nDer Laptop hat einen modernen und leistungsfähigen Intel i7 Prozessor und 16GB Ram. Zudem eine 1TB SSD Festplatte für schnellen Zugriff auf die Daten.\r\n\r\nDer Zustand dieses Laptops ist sehr gut. Bei Fragen gebe ich gerne Auskunft.\r\n\r\nAnbei der Originalbeschrieb:\r\n\r\nEin Modus für jede Stimmung\r\nMit nur 1,16 kg ist das Yoga Duet 7 leicht und vielseitig genug, um überall eingesetzt werden zu können. Mit dem verstellbaren Klappständer können Sie bequemer und effizienter im Laptop-Modus oder in stumpferen Winkeln arbeiten, skizzieren oder Notizen machen. Die abnehmbare Bluetooth®-Tastatur sorgt für ein entspannteres, alternatives Tipp- und Anzeigeerlebnis.\r\n\r\nImmer in Verbindung bleiben\r\nMit Intel® Wi-Fi 6 können Sie dreimal schneller eine Verbindung zum Internet herstellen als mit Standard-WLAN. Und dank modernem Standby erhalten Sie auch dann Benachrichtigungen, wenn sich Ihr Yoga Duet 7 im Bereitschaftsmodus befindet.\r\n\r\nSchau mal, ohne Hände!\r\nMit seinen smarten Funktionen spart Ihnen das Yoga Duet 7 Zeit und Mühe. Sie können sich einfach mit einem Lächeln anmelden und werden automatisch abgemeldet, wenn Sie weggehen. Sie erhalten Benachrichtigungen, wenn jemand Ihnen über die Schulter schaut, um sicherzustellen, dass Ihre Arbeit privat bleibt. Sie können sogar über den Sperrbildschirm mit Ihrer digitalen Sprachassistentin Alexa sprechen.\r\n\r\nMobile Unterhaltung wie zu Hause\r\nGeniessen Sie überall kristallklare Bilder ? dank einem 33 cm (13\") 2K-Touchscreen-Display mit 100 % sRGB-Farbgenauigkeit, 400 cd/m² Helligkeit und breitem Betrachtungswinkel. Zusammen mit Dolby Audio?-Lautsprechern und einem smarten Verstärker für einen besseren Klang sorgt Ihr Yoga Duet 7 so auch unterwegs für Unterhaltung.','2023-08-13 13:18:17',799,'',4,3114,1,1,2,'2023-08-13_15-16.png');
/*!40000 ALTER TABLE `advertisement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advertisement_image`
--

DROP TABLE IF EXISTS `advertisement_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advertisement_image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(100) COLLATE utf8mb3_bin NOT NULL,
  `advertisement_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `advertisement_id` (`advertisement_id`),
  CONSTRAINT `advertisement_image_ibfk_1` FOREIGN KEY (`advertisement_id`) REFERENCES `advertisement` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_image`
--

LOCK TABLES `advertisement_image` WRITE;
/*!40000 ALTER TABLE `advertisement_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `advertisement_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('4781e5260070');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (2,'Apple'),(1,'Computers & Accessories');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (1,'Aargau'),(2,'Appenzell'),(3,'Basel'),(4,'Bern'),(5,'Freiburg'),(6,'Genf'),(7,'Glarus'),(8,'Graubuenden'),(9,'Jura'),(23,'Liechtenstein'),(10,'Luzern'),(11,'Neuenburg'),(12,'Nid- & Obwalden'),(13,'Schwyz'),(14,'Solothurn'),(15,'St.Gallen'),(17,'Tessin'),(16,'Thurgau'),(18,'Uri'),(19,'Waadt'),(20,'Wallis'),(22,'Zuerich'),(21,'Zug');
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `recipient_id` int NOT NULL,
  `content` text COLLATE utf8mb3_bin NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `recipient_id` (`recipient_id`),
  KEY `sender_id` (`sender_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`recipient_id`) REFERENCES `user` (`id`),
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategory`
--

DROP TABLE IF EXISTS `subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `subcategory_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategory`
--

LOCK TABLES `subcategory` WRITE;
/*!40000 ALTER TABLE `subcategory` DISABLE KEYS */;
INSERT INTO `subcategory` VALUES (1,'Computer',1),(2,'Accessories',1),(3,'Software',1),(4,'Tablets',1),(5,'Iphone',2),(6,'Watch',2),(7,'Mac',2);
/*!40000 ALTER TABLE `subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  `last_name` varchar(50) COLLATE utf8mb3_bin NOT NULL,
  `username` varchar(255) COLLATE utf8mb3_bin NOT NULL,
  `email` varchar(120) COLLATE utf8mb3_bin NOT NULL,
  `password_hash` varchar(128) COLLATE utf8mb3_bin NOT NULL,
  `user_adedd` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_blocked` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Administrator','admin','root','blazer-sonst0k@icloud.com','pbkdf2:sha256:260000$7R4euwcHdNm6qRjx$366daa0bedd628b8a496eb0aae7876c8f0a35b7a9df307754cfc2eb3df5b857b','2023-08-13 00:31:56','2023-08-14 12:13:07',1,0),(2,'Hans','Müller','hans','hans@mueller.ch','pbkdf2:sha256:260000$fVYr6XXqFQmuN170$23825c0043b139124cc20d04c2e8b22c292ddbc41891c6db492d16ac23826140','2023-08-13 02:10:14','2023-08-13 18:42:47',0,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-14 14:18:09
