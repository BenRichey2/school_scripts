-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: mysql    Database: iyse222
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.48-MariaDB-0ubuntu0.18.04.1

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
-- Current Database: `iyse222`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `iyse222` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `iyse222`;

--
-- Table structure for table `accesses`
--

DROP TABLE IF EXISTS `accesses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accesses` (
  `category` varchar(30) NOT NULL,
  `number` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accesses`
--

LOCK TABLES `accesses` WRITE;
/*!40000 ALTER TABLE `accesses` DISABLE KEYS */;
INSERT INTO `accesses` VALUES ('deserts',37),('drinks',71),('for kids',20),('for pets',50),('inedible',31),('mains',67),('poisonous',42),('snacks',108),('takeout',40);
/*!40000 ALTER TABLE `accesses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customerAndBiz`
--

DROP TABLE IF EXISTS `customerAndBiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customerAndBiz` (
  `ID` int(11) NOT NULL,
  `primaryName` varchar(50) NOT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `middleIntial` char(1) DEFAULT NULL,
  `StreetNum` varchar(5) NOT NULL,
  `StreetName` varchar(50) NOT NULL,
  `suiteNum` varchar(50) DEFAULT NULL,
  `building` varchar(50) DEFAULT NULL,
  `IsBusiness` varchar(3) NOT NULL,
  `zipCode` int(11) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` char(2) NOT NULL,
  `telephoneNum` varchar(14) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customerAndBiz`
--

LOCK TABLES `customerAndBiz` WRITE;
/*!40000 ALTER TABLE `customerAndBiz` DISABLE KEYS */;
INSERT INTO `customerAndBiz` VALUES (1,'KROGER',NULL,NULL,'704','EUCLIDE AVENUE','NULL','NULL','YES',40508,'Lexington','KY','859-245-1865'),(2,'RAY','HYATT','L','300','ROSE STREET','ROOM102','Hardyman Building','NO',40506,'Lexington','KY',''),(3,'RAY','HYATT','L','301','Hilltop Avenue','ROOM102',NULL,'NO',40506,'Lexington','KY',''),(4,'John','Wick',NULL,'82','Beaver Street','ROOM1301',NULL,'NO',10005,'New York','NY','555-555-5555'),(5,'John','Williams',NULL,'324','Aylesford place',NULL,NULL,'NO',40506,'lexington','KY',''),(6,'Tony','Stark',NULL,'200','Park Avenue Penthouse',NULL,NULL,'NO',10001,'New York','NY','555-555-3142'),(7,'Stephen','Strange',NULL,'117A','Blecker Street',NULL,NULL,'NO',10001,'New York','NY','(555)555-432'),(8,'BOB','Smith','C','200','Park Avenue',NULL,'Apartment 221','NO',10001,'New York','NY',''),(9,'BOWMAN','WILDCAT','F','#1','Avenue of Champions',NULL,NULL,'NO',40506,'Lexington','KY',''),(10,'BOB','SMITH','C','200','Park Avenue',NULL,NULL,'NO',40507,'Lexington','KY','859-245-0965'),(11,'BOB','PORTER',NULL,'1','Dead End Row','ROOM 200',NULL,'YES',12347,'Lexington','TX','859-245-1265'),(12,'BOB','SYDELL',NULL,'1','Dead End Row','ROOM 200',NULL,'YES',12347,'Lexington','TX','859-245-1165'),(13,'JAKE','RICK',NULL,'666','HELLs Bells rd',NULL,NULL,'NO',43056,'Lexington','OH','859-245-1365'),(14,'McDonalds',NULL,NULL,'357','S Limestone',NULL,NULL,'YEs',40508,'Lexington','Ky','859-245-1865'),(15,'Chick-fil-A',NULL,NULL,'440','Hilltop Avenue',NULL,NULL,'YES',40506,'Lexington','Ky','859-245-1665'),(16,'Walmart',NULL,NULL,'500','W New Circle Rd',NULL,NULL,'YES',40511,'Lexington','Ky','859.233.0222'),(17,'Target',NULL,NULL,'500','S Upper Street',NULL,NULL,'YES',40508,'Lexington','Ky','859-245-1865'),(18,'Dollar General',NULL,NULL,'318','Southland',NULL,NULL,'YES',40508,'Lexington','Ky','859-245-1965'),(19,'Walgreens',NULL,NULL,'878','E High Street',NULL,NULL,'YES',40502,'Lexington','Ky','859-245-1964'),(20,'Walmart',NULL,NULL,'725','Campbell Bypass',NULL,NULL,'YES',42718,'CAMPBEELSVILLE','Ky','895-789-0707'),(21,'Autozone',NULL,NULL,'820','Lane Alled Rd',NULL,NULL,'YES',40504,'Lexington','Ky','214-568-2222'),(22,'McDonalds',NULL,NULL,'1007','Green Gable Drive',NULL,NULL,'YES',40347,'Lexington','Ky','2147483647'),(23,'Arbys',NULL,NULL,'3261','Nicholasville Rd',NULL,NULL,'YES',40508,'Lexington','Ky','859-245-1965'),(24,'Cook Out',NULL,NULL,'855','S Broadway',NULL,NULL,'YES',40504,'Lexington','Ky','2147483647'),(25,'Sam','Morty',NULL,'777','Pure Fiction rd',NULL,NULL,'NO',77066,'SaraSota','FL',''),(26,'Austin','Powers',NULL,'88','Mellow Yellow rd',NULL,NULL,'NO',45123,'Lexington','KY','859-431-1023'),(27,'Real','Rich','E','2','BS rd',NULL,NULL,'NO',40501,'Lexington','Ky','859-431-1022'),(29,'Hoe','Richz','E','1','Limbo rd',NULL,NULL,'NO',40502,'Lexington','Ky','2147483647'),(30,'Rack','Sanchez','E','3','Lost place',NULL,NULL,'NO',40589,'Williamstown','Ky','2147483647'),(31,'Starbucks',NULL,NULL,'808','E High St',NULL,NULL,'YES',40502,'Lexington','Ky','8595369009'),(32,'Walmart',NULL,NULL,'500','W NEW CIRCLE RD',NULL,NULL,'YES',40511,'Lexington','Ky','859.233.0222'),(33,'GoodWill',NULL,NULL,'1441','LEESTOWN RD',NULL,NULL,'YES',40511,'Lexington','Ky','895-789-2312 '),(34,'Naruto','Uzumake',NULL,'231','ROSE St',NULL,NULL,'NO',40517,'Lexington','Ky','859-213-5678'),(35,'Sasuke','Uchilha',NULL,'331','tiktok St',NULL,NULL,'NO',40557,'Lexington','Ky','859-889-9571'),(36,'Gordan FOOD SERVICE STORE',NULL,NULL,'1856','Plaudit Place',NULL,NULL,'YES',40509,'Lexington','Ky','859-007-0571'),(37,'Panda Express',NULL,NULL,'160','Avenue of Champions',NULL,NULL,'YES',40506,'Lexington','Ky','859-218-6726'),(38,'Nikola','Tesla',NULL,'321','Aylesford pl',NULL,NULL,'NO',40506,'Lexington','Ky','859-221-3451'),(39,'Thomas','The-Tank',NULL,'123','Aylesford pl',NULL,NULL,'NO',40504,'Lexington','Ky','859-123-4567'),(40,'Shark','Man',NULL,'10','Rose pl',NULL,NULL,'NO',40508,'Lexington','Ky','859-245-1965');
/*!40000 ALTER TABLE `customerAndBiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `lname` char(20) NOT NULL,
  `fname` char(15) DEFAULT NULL,
  `city` char(18) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `category` varchar(30) NOT NULL,
  `item` text,
  `description` text,
  `price` decimal(4,2) DEFAULT NULL,
  KEY `category` (`category`),
  CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`category`) REFERENCES `accesses` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES ('snacks','olive hash','mashed olives in gravy',2.50),('snacks','smarties','small savory bites',1.00),('snacks','clumpers','chocolate-covered raisins',1.50),('drinks','smoothie ','peach and frog flavored',5.54),('drinks','milk ','fresh from our cow',2.50),('drinks','water','guaranteed mostly pure',0.50),('mains','steak','primal rib',20.50),('mains','fish','whatever we found at the market',25.00),('mains','mac-n-cheese','always a winner!',15.00),('deserts','ice cream','durian or avocado',5.00),('deserts','shave ice','durian or avocado',3.20),('deserts','cake','dark forest',4.00),('for kids','mac-n-cheese','always a winner!',5.00),('for kids','small fry','most likely some fish',5.00),('takeout','empty box','recyclable',0.30),('takeout','pizza slice','vegan, white',1.00),('takeout','ice cream cone','durian or avocado',5.00),('inedible','beer stein','glass',3.00),('inedible','can holder','rubber',2.00),('inedible','napkins','50, recycled',1.00),('poisonous','table cleaner','bottled',10.50);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recieptsTab`
--

DROP TABLE IF EXISTS `recieptsTab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recieptsTab` (
  `businessName` varchar(50) NOT NULL,
  `numItems` int(11) NOT NULL,
  `TotalPrice` double NOT NULL,
  `StreetNum` int(11) NOT NULL,
  `StreetName` varchar(50) NOT NULL,
  `BuyDate` date NOT NULL,
  `blobPic` blob,
  `Buyer` int(11) DEFAULT NULL,
  `Seller` int(11) DEFAULT NULL,
  `City` varchar(50) NOT NULL,
  `State` varchar(50) NOT NULL,
  `zipCode` varchar(50) NOT NULL,
  `telephoneNum` varchar(14) NOT NULL,
  `HighestPrice` double NOT NULL,
  `LowestPrice` double NOT NULL,
  KEY `Buyer` (`Buyer`),
  KEY `Seller` (`Seller`),
  CONSTRAINT `recieptsTab_ibfk_1` FOREIGN KEY (`Buyer`) REFERENCES `customerAndBiz` (`ID`) ON DELETE SET NULL,
  CONSTRAINT `recieptsTab_ibfk_2` FOREIGN KEY (`Seller`) REFERENCES `customerAndBiz` (`ID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recieptsTab`
--

LOCK TABLES `recieptsTab` WRITE;
/*!40000 ALTER TABLE `recieptsTab` DISABLE KEYS */;
INSERT INTO `recieptsTab` VALUES ('KROGER',15,86.34,704,'EUCLID AVENUE','2023-02-07',NULL,34,1,'Lexington','KY','40508','(859) 687-3260',11.99,2.99),('Gordon FOOD SERVICE STORE',2,8.98,1856,'Plaudit Place','2023-02-11',NULL,35,36,'Lexington','KY','40509','859-007-0571',4.49,4.49),('Target',2,10.79,500,'S Upper St.','2023-02-01',NULL,35,17,'Lexington','Ky','40508','895-286-3352',5.69,4.49),('Walmart',11,36.72,725,'CAMPBELLSVILLE BYP','2022-10-26',NULL,35,20,'CAMPBEELSVILLE','Ky','42718','895-789-0707',11.98,1),('Panda Express',1,10.18,160,'Avenue of Champions','2023-01-30',NULL,40,37,'Lexington','Ky','40506','859-218-6726',9.6,9.6),('GoodWill',2,5.99,1441,'LEESTOWN RD','2023-01-29',NULL,39,33,'Lexington','Ky','40511','895-559-2312',2.6,1.6),('Dollar General',10,20.99,318,'Southland','2023-01-28',NULL,38,18,'Lexington','Ky','40503','895-111-2312',6.6,3.6),('Arbys',3,11.99,3261,'Nicholasville Rd','2023-01-27',NULL,38,23,'Lexington','Ky','40503','2147483647',7.78,1.6),('Starbucks',3,9.99,808,'E High St','2023-01-26',NULL,2,31,'Lexington','Ky','40502','895-334-1132',4.78,2.6),('McDonalds',3,11.99,1007,'Green Gable Drive','2023-01-25',NULL,8,22,'Lexington','Ky','40504','859-245-1865',5.78,1.98),('McDonalds',3,10.99,357,'S Limestone','2023-01-25',NULL,7,14,'Lexington','Ky','40504','859-245-1865',5.78,1.98),('Cook Out',7,18.99,855,'S Broadway','2023-01-24',NULL,13,24,'Lexington','Ky','40504','859-245-1665',9.78,2.98),('Chick-fil-A',7,30.99,440,'Hilltop Avenue','2023-01-23',NULL,13,15,'Lexington','Ky','40504','859-245-1665',8.78,1.98),('Walgreens',5,20.99,878,'E High St','2023-01-09',NULL,9,19,'Lexington','Ky','40502','895-789-0707',7.78,2.98),('Autozone',6,99.99,1007,'Lane Alled Rd','2023-02-12',NULL,3,21,'Lexington','Ky','40504','214-568-2222',54.78,7.98);
/*!40000 ALTER TABLE `recieptsTab` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-10 12:24:55
