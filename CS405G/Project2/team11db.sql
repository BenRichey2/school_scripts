-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: mysql    Database: bbri226
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
-- Current Database: `bbri226`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `bbri226` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `bbri226`;

--
-- Table structure for table `CONTACT`
--

DROP TABLE IF EXISTS `CONTACT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CONTACT` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_name` varchar(100) NOT NULL DEFAULT '000000',
  `business_name` varchar(100) NOT NULL DEFAULT '000000',
  `address` varchar(250) NOT NULL,
  `street_address` varchar(150) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zip` varchar(15) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONTACT`
--

LOCK TABLES `CONTACT` WRITE;
/*!40000 ALTER TABLE `CONTACT` DISABLE KEYS */;
INSERT INTO `CONTACT` VALUES (1,'Mr. Ray L. Hyatt Jr','000000','300 Rose Street Room 102 Hardymon Building Lexington, Kentucky 40506','300 Rose Street Room 102 Hardymon Building','Lexington','KY','40506',NULL),(2,'Mr. Ray L. Hyatt Jr','000000','301 Hilltop Avenue, Room 102 Lexington, Ky 40506','301 Hilltop Avenue Room 102','Lexington','KY','40506',NULL),(3,'John Wick','000000','82 Beaver St Room 1301 New York, New York 10005','82 Beaver St Room 1301','New York','NY','10005','555-555-5555'),(4,'Tony Stark','000000','200 Park Avenue Penthouse New York, New York 10001','200 Park Avenue','New York','NY','10001','555-555-3142'),(5,'Dr. Stephen Strange','000000','117A Bleecker Street New York, New York 10001','117A Bleecker Street','New York','NY','10001','(555)555-4321'),(6,'Bob Porter','Intech','1 Dead End Row Room 200 Dallas, TX 12347','1 Dead End Row Room 200','Dallas','TX','12347',NULL),(7,'Bob C. Smith','000000','200 Park Avenue Apartment 221 New York, NY 10001','200 Park Avenue Apartment 221','New York','NY','10001',NULL),(8,'Bowman F. Wildcat','000000','#1 Avenue of Champions Lexington, Ky 40506','#1 Avenue of Champions','Lexington','KY','40506',NULL),(9,'Bob C. Smith','000000','200 Park Avenue Lexington, KY 40507','200 Park Avenue','Lexington','KY','40507',NULL),(10,'Mr. Bob Sydell','Intech','1 Dead End Row Room 200 Dallas, TX 12347','1 Dead End Row Room 200','Dallas','TX','12347',NULL),(11,'000000','Kroger','106 Market Place Circle, Georgetown, KY 40324','106 Market Place Circle','Georgetown','KY','40324','859-420-6969'),(12,'Ben Richey','000000','123 New Circle Rd, Lexington, KY 40508','123 New Circle Rd','Lexington','KY','40508','859-676-4969'),(13,'000000','Kroger','704 Euclid Ave, Lexington, KY 40502','704 Euclid Ave','Lexington','KY','40502','859-678-7564'),(14,'000000','Dollar Tree','3101 Clays Mill Road, Lexington, KY 40503','3101 Clays Mill Road','Lexington','KY','40503','859-098-2435'),(15,'000000','Target','500 S Upper St, Lexington, KY 40508','500 S Upper St','Lexington','KY','40508','859-490-5867'),(16,'000000','Target','131 West Reynolds Rd, Lexington, KY 40503','131 West Reynolds Rd','Lexington','KY','40503','859-345-6789'),(17,'000000','McDonalds','3765 Palomar Centre Dr, Lexington, KY 40513','3765 Palomar Centre Dr','Lexington','KY','40513','859-223-8811'),(18,'000000','Slainte Public House','320 E Main St, Georgetown, KY 40324','320 E Main St','Georgetown','KY','40324','502-642-4631'),(19,'000000','Shaker Village of Pleasant Hill','3501 Lexington Road, Harrodsburg, KY 40330','3501 Lexington Road','Harrodsburg','KY','40330','859-123-0987'),(20,'000000','Schwabs Pipes N Stuff','245 Southland Dr, Lexington, KY 40503','245 Southland Dr','Lexington','KY','40503','859-266-1011'),(21,'000000','Nike by Lexington','4084 Finn Way, Lexington, KY 40517','4084 Finn Way','Lexington','KY','40517','859-309-6346'),(22,'000000','Kroger','3040 Dolphin Dr, Elizabethtown, KY 42701','3040 Dolphin Dr','Elizabethtown','KY','42701','859-102-9384'),(23,'000000','Buffalo Wild Wings','1511 Ring Rd Ste 106, Elizabethtown, KY 42701','1511 Ring Rd Ste 106','Elizabethtown','KY','42701','859-453-6271'),(24,'000000','Chipotle','345 S Limestone, Lexington, KY 40508','345 S Limestone','Lexington','KY','40508','859-389-6643'),(25,'000000','Subway','Margaret I King Library, 410 Administration Dr., Lexington, KY 40506','Margaret I King Library, 410 Administration Dr.','Lexington','KY','40506','859-079-8365'),(26,'000000','Chick-fil-A','239 Student Ctr, UK Student Center, Lexington, KY 40508','239 Student Ctr, UK Student Center','Lexington','KY','40508','859-218-6726'),(27,'000000','Ticketmaster','9348 Civic Center Drive, Beverly Hills, CA, 90210','9348 Civic Center Drive','Beverly Hills','CA','90210','859-666-0666'),(28,'000000','Crocs','3401 Nicholasville Rd, Lexington, Ky 40503','3401 Nicholasville Rd','Lexington','KY','40503','859-752-0398'),(29,'000000','McDonalds','357 S Limestone, Lexington, KY 40508','357 S Limestone','Lexington','KY','40508','859-567-9624'),(31,'Gavin','000000','521 S Broadway, The Lex Apartments, Lexington, Kentucky, 40508','521 S Broadway, The Lex Apartments','Lexington','KY','40508','859-253-5936'),(32,'000000','Coliseum Liquors','379 Rose Street, Lexington, KY 40508','379 Rose Street','Lexington','KY','40508','859-252-8831'),(33,'000000','Bodega','140 Mason Street, San Francisco, CA 94102','140 Mason Street','San Francisco','CA','94102','415-655-9341'),(34,'000000','Marti & Liz','150 West Lowry Lane, Lexington, KY 40503','150 West Lowry Lane','Lexington','KY','40503','859-523-6477'),(35,'000000','Sephora','3401 Nicholasville Road, Lexington, KY 40503','3401 Nicholasville Road','Lexington','KY','40503','859-245-0601'),(36,'000000','The Fresh Market','3387 Tates Creek Road, Lexington, KY 40517','3387 Tates Creek Road','Lexington','KY','40517','859-266-0150'),(37,'Adam Smith','000000','1603 East New Circle Road, Lexington, KY 40505','1603 East New Circle Road','Lexington','KY','40505','777-888-9999'),(38,'Layla Bell','000000','413 West Vine Street, Lexington, KY 40507','413 West Vine Street','Lexington','KY','40507','444-555-6666'),(39,'Samantha Wells','000000','2121 Nicholasville Road, Lexington, KY 40503','2121 Nicholasville Road','Lexington','KY','40503','111-222-3333'),(40,'Brandon Sims','000000','168 West Main Street, Lexington, KY 40508','168 West Main Street','Lexington','KY','40508','555-444-3333'),(41,'Tofunmi Oyetan','000000','320 North Martin Luther King Boulevard, Lexington, KY 40506','320 South Martin Luther King Boulevard','Lexington','KY','40506','485-998-2395'),(42,'John C. Na','000000','203 Whoischamp Lexington, KY 40502','203 Whoischamp','Lexington','KY','40502','000-372-6897'),(43,'Chris P. Bacon','000000','100 Real Pork Ave. Lexington, KY 40502','100 Real Pork Ave.','Lexington','KY','40502','234-001-0003'),(44,'Dwayne Johnson','000000','454 Underock Lexington, KY 40506','454 Underock','Lexington','KY','40506','696-969-6969'),(45,'Saitama','000000','671 Not Japan Lexington, KY 40503','454 Underock','Lexington','KY','40503','777-777-5555'),(46,'Bruce Wayne','Wayne Tech','343 Crime Ave., Gotham, KY 40523','343 Crime Ave.','Gotham','KY','40523','371-444-2948');
/*!40000 ALTER TABLE `CONTACT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RECEIPT`
--

DROP TABLE IF EXISTS `RECEIPT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RECEIPT` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `supplier_id` int(11) DEFAULT NULL,
  `consumer_id` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `quantity` float(14,3) NOT NULL,
  `total_sale` float(14,2) NOT NULL,
  `receipt_image` blob,
  `highest` float(14,2) DEFAULT NULL,
  `lowest` float(14,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `supplier_id` (`supplier_id`),
  KEY `consumer_id` (`consumer_id`),
  CONSTRAINT `RECEIPT_ibfk_1` FOREIGN KEY (`supplier_id`) REFERENCES `CONTACT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `RECEIPT_ibfk_2` FOREIGN KEY (`consumer_id`) REFERENCES `CONTACT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RECEIPT`
--

LOCK TABLES `RECEIPT` WRITE;
/*!40000 ALTER TABLE `RECEIPT` DISABLE KEYS */;
INSERT INTO `RECEIPT` VALUES (1,6,2,'2023-02-17',4.000,15000000.00,NULL,14999999.00,0.03),(2,11,12,'2022-11-16',4.000,28.39,NULL,18.00,2.00),(3,11,12,'2022-10-25',1.000,27.55,NULL,27.55,27.55),(4,13,12,'2022-08-29',11.000,39.90,NULL,9.00,4.00),(5,14,12,'2022-08-27',4.000,5.30,NULL,1.00,0.75),(6,20,12,'2022-07-01',1.000,11.13,NULL,11.13,11.13),(7,19,12,'2022-07-04',5.000,32.33,NULL,8.00,6.00),(8,18,12,'2022-07-11',2.000,13.76,NULL,6.88,6.88),(10,21,31,'2023-02-17',4.000,112.79,NULL,65.99,4.00),(11,23,31,'2023-02-09',3.000,15.02,NULL,4.00,1.00),(12,28,31,'2023-02-17',4.000,96.98,NULL,85.21,1.00),(13,26,31,'2023-01-31',5.000,21.63,NULL,13.00,7.00),(14,21,31,'2023-02-17',2.000,-189.08,NULL,172.00,17.00),(15,46,4,'2023-02-17',5.000,69000000.00,NULL,67000000.00,500000.00),(16,34,41,'2022-09-15',3.000,84.77,NULL,52.71,7.03),(17,35,38,'2022-09-13',2.000,38.16,NULL,14.08,14.08),(18,32,40,'2023-01-28',1.000,13.77,NULL,13.77,13.77),(19,33,37,'2023-01-16',3.000,38.03,NULL,17.00,5.73);
/*!40000 ALTER TABLE `RECEIPT` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-10 15:41:21
