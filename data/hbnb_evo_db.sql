-- MySQL dump 10.13  Distrib 8.0.36, for Linux (aarch64)
--
-- Host: localhost    Database: hbnb_evo_db
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.20.04.1

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

-- Create and use the specified database
CREATE DATABASE IF NOT EXISTS hbnb_evo_db;
USE hbnb_evo_db;

--
-- Table structure for table `amenities`
--

DROP TABLE IF EXISTS `amenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenities` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenities`
--

/*!40000 ALTER TABLE `amenities` DISABLE KEYS */;
INSERT INTO `amenities` VALUES ('036bc824-74ed-44dc-a183-1ab6c4878fc2','2024-06-02 15:32:16','2024-06-02 15:32:16','TV'),('2ec8cf22-e5ea-4a1f-aedd-89f15fcc60e9','2024-06-02 15:32:16','2024-06-02 15:32:16','Toilet'),('3ca936e3-8a1e-4313-8308-9c94d5918437','2024-06-02 15:32:16','2024-06-02 15:32:16','Wi-fi'),('544cd593-7475-494d-ba3a-b5ec66b3945d','2024-06-02 15:32:16','2024-06-02 15:32:16','Mini-fridge'),('83874c62-1902-4572-b76a-5cffb7a08a91','2024-06-02 15:32:16','2024-06-02 15:32:16','Air-con');
/*!40000 ALTER TABLE `amenities` ENABLE KEYS */;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cities` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  `country_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `cities_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
INSERT INTO `cities` VALUES ('1f3039cb-9d17-434f-9e79-695be766e6b5','2024-05-24 14:51:39','2024-05-24 14:51:39','Auckland','3d12e1a8-cc92-4162-ba13-ecc4eb4b9877'),('68c06ef5-bf33-46df-a894-9ac54f728f43','2024-05-24 14:50:07','2024-05-24 14:50:07','Kuala Lumpur','db63e499-f604-41a3-b97a-ee4bf9331f75'),('b07598bb-1e0f-4bc5-a04a-f3810f8fa635','2024-05-24 14:51:02','2024-05-24 14:51:02','Vancouver','2875d5d9-a06c-49a2-b791-fb2ab9744fdf'),('b24877a7-8f3f-4acc-bbb4-9e9787d190ef','2024-05-20 13:52:36','2024-05-20 13:52:36','Sydney','c612b95d-cf60-4dce-b53d-4d7c9f57753e'),('b74d8f59-b6a1-4e7e-8cbe-606f01c69395','2024-05-20 13:52:36','2024-05-20 13:52:36','Melbourne','c612b95d-cf60-4dce-b53d-4d7c9f57753e'),('ca2e4f68-96b5-494d-9664-9546ae0becbc','2024-05-24 14:50:07','2024-05-24 14:50:07','Penang','db63e499-f604-41a3-b97a-ee4bf9331f75'),('d47e1de7-b955-4f22-89ab-120a7cee9c36','2024-05-24 14:51:02','2024-05-24 14:51:02','Montreal','2875d5d9-a06c-49a2-b791-fb2ab9744fdf'),('dc8f131f-1148-498a-a99f-7c7c6c12b643','2024-05-24 14:49:05','2024-05-24 14:49:05','Singapore','8df5a778-b6f8-409a-a14b-a172a96b8676');
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `countries` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  `code` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES ('2875d5d9-a06c-49a2-b791-fb2ab9744fdf','2024-05-20 13:35:09','2024-05-20 13:35:09','Canada','CA'),('3d12e1a8-cc92-4162-ba13-ecc4eb4b9877','2024-05-20 14:46:50','2024-05-20 15:17:10','New Zealand','NZ'),('8df5a778-b6f8-409a-a14b-a172a96b8676','2024-05-20 13:35:09','2024-05-20 13:35:09','Singapore','SG'),('c612b95d-cf60-4dce-b53d-4d7c9f57753e','2024-05-20 13:35:09','2024-05-20 13:35:09','Australia','AU'),('db63e499-f604-41a3-b97a-ee4bf9331f75','2024-05-20 13:35:09','2024-05-20 13:35:09','Malaysia','MY');
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;

--
-- Table structure for table `place_amenity`
--

DROP TABLE IF EXISTS `place_amenity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `place_amenity` (
  `place_id` varchar(60) NOT NULL,
  `amenity_id` varchar(60) NOT NULL,
  PRIMARY KEY (`place_id`,`amenity_id`),
  KEY `amenity_id` (`amenity_id`),
  CONSTRAINT `place_amenity_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `place_amenity_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `place_amenity`
--

/*!40000 ALTER TABLE `place_amenity` DISABLE KEYS */;
INSERT INTO `place_amenity` VALUES ('71bebd9b-481b-4bf0-bb83-4e30ea66bdaa','036bc824-74ed-44dc-a183-1ab6c4878fc2'),('821d0c3e-d08a-407b-b8bc-813eaf619595','036bc824-74ed-44dc-a183-1ab6c4878fc2'),('71bebd9b-481b-4bf0-bb83-4e30ea66bdaa','2ec8cf22-e5ea-4a1f-aedd-89f15fcc60e9'),('7b214bfd-923e-42c6-ae00-a985cb6ecfd9','2ec8cf22-e5ea-4a1f-aedd-89f15fcc60e9'),('821d0c3e-d08a-407b-b8bc-813eaf619595','2ec8cf22-e5ea-4a1f-aedd-89f15fcc60e9'),('47236378-e16a-4a2b-91b4-5dab12ec98e7','3ca936e3-8a1e-4313-8308-9c94d5918437'),('71bebd9b-481b-4bf0-bb83-4e30ea66bdaa','3ca936e3-8a1e-4313-8308-9c94d5918437'),('71bebd9b-481b-4bf0-bb83-4e30ea66bdaa','544cd593-7475-494d-ba3a-b5ec66b3945d'),('7b214bfd-923e-42c6-ae00-a985cb6ecfd9','544cd593-7475-494d-ba3a-b5ec66b3945d'),('71bebd9b-481b-4bf0-bb83-4e30ea66bdaa','83874c62-1902-4572-b76a-5cffb7a08a91'),('821d0c3e-d08a-407b-b8bc-813eaf619595','83874c62-1902-4572-b76a-5cffb7a08a91');
/*!40000 ALTER TABLE `place_amenity` ENABLE KEYS */;

--
-- Table structure for table `places`
--

DROP TABLE IF EXISTS `places`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `places` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `city_id` varchar(60) NOT NULL,
  `host_id` varchar(60) NOT NULL,
  `name` varchar(128) NOT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `address` varchar(1024) DEFAULT NULL,
  `number_of_rooms` int NOT NULL,
  `number_of_bathrooms` int NOT NULL,
  `max_guests` int NOT NULL,
  `price_per_night` int NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city_id` (`city_id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `places_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`),
  CONSTRAINT `places_ibfk_2` FOREIGN KEY (`host_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `places`
--

/*!40000 ALTER TABLE `places` DISABLE KEYS */;
INSERT INTO `places` VALUES ('47236378-e16a-4a2b-91b4-5dab12ec98e7','2024-06-12 12:24:47','2024-06-12 12:24:47','ca2e4f68-96b5-494d-9664-9546ae0becbc','573454ff-0dac-4be6-ba23-60c74a395ba0','Motel Goreng Pisang','The one with the giant banana signage.','11, Jalan Adams, George Town, 10450 George Town, Pulau Pinang, Malaysia',5,0,1,50,5.42038,100.314),('71bebd9b-481b-4bf0-bb83-4e30ea66bdaa','2024-06-12 11:30:31','2024-06-12 11:30:31','68c06ef5-bf33-46df-a894-9ac54f728f43','d2999942-2363-4334-9c0b-5b2bbdb65f4d','Motel Bagus','The best motel you will ever stay in... within KL. Trust me on this.','Kuala Lumpur, 50088 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia',8,1,1,150,3.15394,101.715),('7b214bfd-923e-42c6-ae00-a985cb6ecfd9','2024-06-12 11:30:31','2024-06-12 11:30:31','68c06ef5-bf33-46df-a894-9ac54f728f43','ce0f76f2-3dd2-4e81-8006-9e5d537f1b93','Hotel Pontianak','Next to the Petronas Twin Towers','Kuala Lumpur City Centre, 50088 Kuala Lumpur, Federal Territory of Kuala Lumpur, Malaysia',100,1,2,280,3.15567,101.712),('821d0c3e-d08a-407b-b8bc-813eaf619595','2024-06-04 13:59:55','2024-06-04 13:59:55','dc8f131f-1148-498a-a99f-7c7c6c12b643','2dd927b2-9503-4918-a48e-2608859cc49f','Six Storey Hotel','The famous Six Storey Hotel','5 Lorong 6 Geylang, Singapore 399167',50,1,3,150,NULL,NULL),('c1c3518b-2545-4b44-83ae-d99bc9f37d5e','2024-06-04 13:59:55','2024-06-04 13:59:55','dc8f131f-1148-498a-a99f-7c7c6c12b643','573454ff-0dac-4be6-ba23-60c74a395ba0','Bugis Motel','Right next to the shopping centre','390 Victoria Street Singapore 188061 ',12,0,2,65,NULL,NULL);
/*!40000 ALTER TABLE `places` ENABLE KEYS */;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `place_id` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `rating` int NOT NULL,
  `comment` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `place_id` (`place_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('2dd927b2-9503-4918-a48e-2608859cc49f','2024-05-24 14:56:34','2024-05-24 14:56:34','b.wayne@wayne-enterprises.biz','iamthenight','Bruce','Wayne'),('368257a6-9c31-4056-81ef-24977b017c86','2024-05-24 14:56:34','2024-05-24 14:56:34','diana.prince@wowo.email','password','Diana','Prince'),('573454ff-0dac-4be6-ba23-60c74a395ba0','2024-05-19 14:44:35','2024-05-19 14:44:35','p.parker@daily-bugle.net','123456','Peter','Parker'),('77935183-e063-49fa-8504-0223d80197a2','2024-05-24 14:56:34','2024-05-24 14:56:34','clark.kent@daily-planet.news','smallville','Clark','Kent'),('99b9825a-e448-436e-891b-f29acb7d6d3b','2024-05-19 11:31:57','2024-05-19 15:56:29','r.r@ff.com','f4forever','Reed','Richards'),('ce0f76f2-3dd2-4e81-8006-9e5d537f1b93','2024-05-19 11:31:57','2024-05-19 11:31:57','s.summers@xmen.com','profxsuxx','Scott','Summers'),('d2999942-2363-4334-9c0b-5b2bbdb65f4d','2024-05-19 11:31:57','2024-05-19 11:31:57','dr.strange@strange-academy.edu.ny','666666','Stephen','Strange');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

--
-- Dumping routines for database 'hbnb_evo_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-12 16:04:39
