-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: mysql    Database: lnri226
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
-- Current Database: `lnri226`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `lnri226` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `lnri226`;

--
-- Table structure for table `Address`
--

DROP TABLE IF EXISTS `Address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Address` (
  `id_number` int(11) NOT NULL AUTO_INCREMENT,
  `is_business` bit(1) NOT NULL,
  `name_prefix` varchar(3) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_initial` varchar(1) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `name_suffix` varchar(5) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `street_address` varchar(100) DEFAULT NULL,
  `unit_number` varchar(10) DEFAULT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `zip_code` int(11) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_number`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Address`
--

LOCK TABLES `Address` WRITE;
/*!40000 ALTER TABLE `Address` DISABLE KEYS */;
INSERT INTO `Address` VALUES (1,_binary '\0','Mr','Ray','L','Hyatt','Jr',NULL,'300 Rose Street Hardymon Building','102','Lexington','Kentucky',40506,NULL),(2,_binary '\0','Mr','Ray','L','Hyatt','Jr',NULL,'301 Hilltop Avenue','102','Lexington','Kentucky',40506,NULL),(3,_binary '\0',NULL,'John',NULL,'Wick',NULL,NULL,'82 Beaver St','1301','New York','New York',10005,'5555555555'),(4,_binary '\0',NULL,'Tony',NULL,'Stark',NULL,NULL,'200 Park Avenue Penthouse',NULL,'New York','New York',10001,'5555553142'),(5,_binary '\0','Dr','Stephen',NULL,'Strange',NULL,NULL,'117A Bleecker Street',NULL,'New York','New York',10001,'5555554321'),(6,_binary '\0',NULL,'Bob','C','Smith',NULL,NULL,'200 Park Avenue Apartment','221','New York','New York',10001,NULL),(7,_binary '\0',NULL,'Bowman','F','Wildcat',NULL,NULL,'1 Avenue of Champions',NULL,'Lexington','Kentucky',40506,NULL),(8,_binary '\0',NULL,'Bob','C','Smith',NULL,NULL,'200 Park Avenue',NULL,'Lexington','Kentucky',40507,NULL),(9,_binary '\0',NULL,'Bob',NULL,'Porter',NULL,NULL,'1 Dead End Row','200','Dallas','Texas',12347,NULL),(10,_binary '\0','Mr','Bob',NULL,'Sydell',NULL,NULL,'1 Dead End Row','200','Dallas','Texas',12347,NULL),(11,_binary '\0',NULL,'Art',NULL,'Jones',NULL,NULL,'2500 Alumni Dr','162','Lexington','Kentucky',40517,'8599370921'),(12,_binary '\0',NULL,'Logan',NULL,'Ramsey',NULL,NULL,'1772 Augusta Ct',NULL,'Lexington','Kentucky',40505,'8593749865'),(13,_binary '\0',NULL,'Isaac',NULL,'Abrams',NULL,NULL,'1100 Eldemere Rd',NULL,'Lexington','Kentucky',40502,'8591234567'),(14,_binary '\0',NULL,'Sawyer',NULL,'Allen',NULL,NULL,'2044 Georgian Way','23','Lexington','Kentucky',40504,'8598906542'),(15,_binary '',NULL,NULL,NULL,NULL,NULL,'Walmart','3735 Palomar Center Dr',NULL,'Lexington','Kentucky',40513,NULL),(16,_binary '',NULL,NULL,NULL,NULL,NULL,'Papa John’s Pizza','265a Avenue of Champions',NULL,'Lexington','Kentucky',40508,NULL),(17,_binary '',NULL,NULL,NULL,NULL,NULL,'Meijer','351 Meijer Way','100','Lexington','Kentucky',40503,NULL),(18,_binary '',NULL,NULL,NULL,NULL,NULL,'Walmart','500 W New Circle Rd',NULL,'Lexington','Kentucky',40511,NULL),(19,_binary '',NULL,NULL,NULL,NULL,NULL,'Kroger','704 Euclid Avenue',NULL,'Lexington','Kentucky',40502,NULL),(20,_binary '',NULL,NULL,NULL,NULL,NULL,'Walmart','4051 Nicholasville Rd',NULL,'Lexington','Kentucky',40503,NULL),(21,_binary '',NULL,NULL,NULL,NULL,NULL,'Best Buy','3220 Nicholasville Rd',NULL,'Lexington','Kentucky',40503,NULL),(22,_binary '',NULL,NULL,NULL,NULL,NULL,'Chick-fil-A','2299 Richmond Rd',NULL,'Lexington','Kentucky',40502,'8593359856'),(23,_binary '',NULL,NULL,NULL,NULL,NULL,'Macy’s','3301 Nicholasville Rd',NULL,'Lexington','Kentucky',40503,NULL),(24,_binary '',NULL,NULL,NULL,NULL,NULL,'Costco Wholesale','1500 Fitzgerald Court',NULL,'Lexington','Kentucky',40509,NULL),(25,_binary '',NULL,NULL,NULL,NULL,NULL,'Bandido Taqueria','535 S Upper St',NULL,'Lexington','Kentucky',40508,'8593179721'),(26,_binary '',NULL,NULL,NULL,NULL,NULL,'Cane’s','544 S Upper St',NULL,'Lexington','Kentucky',40508,NULL),(27,_binary '',NULL,NULL,NULL,NULL,NULL,'Chipotle','345 South Limestone',NULL,'Lexington','Kentucky',40508,NULL),(28,_binary '',NULL,NULL,NULL,NULL,NULL,'Blue & Co., LLC','250 W Main St','2900','Lexington','Kentucky',40507,NULL),(29,_binary '',NULL,NULL,NULL,NULL,NULL,'Lexington Financial Center','250 West Main St','1400','Lexington','Kentucky',40507,NULL),(30,_binary '',NULL,NULL,NULL,NULL,NULL,'Marr, Miller & Myers, PSC','500 Summit Drive',NULL,'Corbin','Kentucky',47501,NULL),(31,_binary '',NULL,NULL,NULL,NULL,NULL,'W.R. Ramsey & Associates, Inc','3201 Summit Square Place',NULL,'Lexington','Kentucky',40509,NULL),(32,_binary '',NULL,NULL,NULL,NULL,NULL,'Barbara Baldwin CPA','2957 Four Pines Dr',NULL,'Lexington','Kentucky',40502,'8593211008'),(33,_binary '',NULL,NULL,NULL,NULL,NULL,'Innovative Accounting','710 E Main St',NULL,'Lexington','Kentucky',40502,'8597570535'),(34,_binary '',NULL,NULL,NULL,NULL,NULL,'ATD Solutions LLC','2240 Executive Drive',NULL,'Lexington','Kentucky',40505,NULL),(35,_binary '',NULL,NULL,NULL,NULL,NULL,'Fusioncorp LLC','1406 N Forbes',NULL,'Lexington','Kentucky',40511,NULL),(36,_binary '',NULL,NULL,NULL,NULL,NULL,'Groff Engineering & Consulting PLLC','306 Jonathan Ct',NULL,'Lexington','Kentucky',40353,NULL),(37,_binary '',NULL,NULL,NULL,NULL,NULL,'Sutherland & Associates','331 S Mill St',NULL,'Lexington','Kentucky',40508,NULL),(38,_binary '',NULL,NULL,NULL,NULL,NULL,'Plumber NYC','1696 2nd Ave',NULL,'New York','New York',10128,NULL),(39,_binary '',NULL,NULL,NULL,NULL,NULL,'Central Bank & Trust Co.','300 W Vine Street',NULL,'Lexington','Kentucky',40507,NULL),(40,_binary '',NULL,NULL,NULL,NULL,NULL,'Staples','2081 Harrodsburg Rd',NULL,'Lexington','Kentucky',40504,NULL);
/*!40000 ALTER TABLE `Address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Receipts`
--

DROP TABLE IF EXISTS `Receipts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Receipts` (
  `receipt_number` int(11) NOT NULL AUTO_INCREMENT,
  `receipt_data` date DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `receipt_scan` tinyblob,
  PRIMARY KEY (`receipt_number`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `Receipts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Address` (`id_number`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Receipts`
--

LOCK TABLES `Receipts` WRITE;
/*!40000 ALTER TABLE `Receipts` DISABLE KEYS */;
INSERT INTO `Receipts` VALUES (1,'2023-02-15',11,'Meijer','351 Meijer Way 100 Lexington Kentucky 40503',NULL),(2,'2023-02-14',11,'Costco Wholesale','1500 Fitzgerald Court Lexington Kentucky 40509',NULL),(3,'2023-02-14',11,'Bandido Taqueria','535 S Upper St Lexington Kentucky 40508',NULL),(4,'2023-02-14',11,'Kroger','704 Euclid Avenue Lexington Kentucky 40502',NULL),(5,'2019-11-19',12,'Best Buy','3220 Nicholasville Rd Lexington Kentucky 40503',NULL),(6,'2023-02-16',12,'Chick-fil-A','2299 Richmond Rd Lexington Kentucky 40502',NULL),(7,'2023-02-14',12,'Kroger','704 Euclid Avenue Lexington Kentucky 40502',NULL),(8,'2022-07-22',12,'Macy’s','3301 Nicholasville Rd Lexington Kentucky 40503',NULL),(9,'2023-02-11',13,'Walmart','500 W New Circle Rd Lexington Kentucky 40511',NULL),(10,'2022-11-28',13,'Kroger','704 Euclid Avenue Lexington Kentucky 40502',NULL),(11,'2022-10-24',13,'Walmart','4051 Nicholasville Rd Lexington Kentucky 40503',NULL),(12,'2023-02-05',13,'Walmart','500 W New Circle Rd Lexington Kentucky 40511',NULL),(13,'2023-01-23',14,'Cane’s','544 S Upper St Lexington Kentucky 40508',NULL),(14,'2022-10-15',14,'Chipotle','345 South Limestone Lexington Kentucky 40508',NULL),(15,'2023-02-17',14,'Walmart','3735 Palomar Center Dr Lexington Kentucky 40502',NULL);
/*!40000 ALTER TABLE `Receipts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sale`
--

DROP TABLE IF EXISTS `Sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Sale` (
  `sale_id` int(11) NOT NULL AUTO_INCREMENT,
  `receipt_number` int(11) DEFAULT NULL,
  `items_sold` int(11) DEFAULT NULL,
  `total_sale` decimal(10,2) DEFAULT NULL,
  `highest_price` decimal(10,2) DEFAULT NULL,
  `lowest_price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`sale_id`),
  KEY `receipt_number` (`receipt_number`),
  CONSTRAINT `Sale_ibfk_1` FOREIGN KEY (`receipt_number`) REFERENCES `Receipts` (`receipt_number`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sale`
--

LOCK TABLES `Sale` WRITE;
/*!40000 ALTER TABLE `Sale` DISABLE KEYS */;
INSERT INTO `Sale` VALUES (1,1,1,24.98,24.98,24.98),(2,2,4,41.66,15.99,4.69),(3,3,9,18.56,1.99,1.99),(4,4,5,28.04,10.99,1.79),(5,5,1,17.99,16.99,16.99),(6,6,2,5.87,3.89,1.65),(7,7,5,7.06,2.99,1.32),(8,8,2,32.71,16.93,13.93),(9,9,17,48.47,5.48,0.98),(10,10,1,3.69,3.69,3.69),(11,11,22,45.56,6.04,0.92),(12,12,20,79.31,10.23,1.32),(13,13,1,11.23,10.99,10.99),(14,14,1,8.43,7.95,7.95),(15,15,2,6.56,3.98,2.58);
/*!40000 ALTER TABLE `Sale` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-10 19:40:05
