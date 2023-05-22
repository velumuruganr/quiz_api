-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: one_decision_quiz
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.2

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
-- Table structure for table `answers`
--

DROP TABLE IF EXISTS `answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `total_choices` int DEFAULT NULL,
  `correctly_answered` int DEFAULT NULL,
  `mark` float DEFAULT NULL,
  `result_id` int DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `result_id` (`result_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`result_id`) REFERENCES `results` (`id`),
  CONSTRAINT `answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answers`
--

LOCK TABLES `answers` WRITE;
/*!40000 ALTER TABLE `answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choices`
--

DROP TABLE IF EXISTS `choices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `choices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `choice_text` text,
  `is_correct` tinyint(1) DEFAULT NULL,
  `question_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `choices_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choices`
--

LOCK TABLES `choices` WRITE;
/*!40000 ALTER TABLE `choices` DISABLE KEYS */;
INSERT INTO `choices` VALUES (29,'eat good food',1,29),(30,'drink cooldrinks',0,29),(31,'eat fresh food',1,29),(32,'new',0,30),(33,'new 2',1,30),(37,'Too much exposure to the sun',1,32),(38,'Hidden water currents',1,32),(39,'Listening to the radio',0,32),(40,'Taking a lift from someone we do not know or trust',1,32),(41,'Falling from a window or ledge, high up from the ground',1,32),(42,'Running around with our shoelaces untied',1,32),(43,'Playing in an old and disused building',1,32),(44,'Drawing a picture',0,32),(45,'School teachers',1,33),(46,'Paramedics',1,33),(47,'Police',1,33),(48,'People who start fires intended to harm',0,33),(49,'Doctors',1,33),(50,'Car drivers who drive over the speed limit',0,33),(51,'Firefighters',1,33),(52,'People who leave broken glass in the parks',0,33),(53,'By listening to our trusted adults ',1,34),(54,'Viewing inappropriate content online',0,34),(55,'Viewing age-appropriate content online',0,34),(56,'By taking notice of warning signs',1,34),(57,'Reporting something if we believe it is dangerous or unsafe',1,34),(58,'By using crossings, underpasses and bridges to crossroads when possible',1,34),(59,'By playing with matches',0,34);
/*!40000 ALTER TABLE `choices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personal_development_areas`
--

DROP TABLE IF EXISTS `personal_development_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal_development_areas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_development_areas`
--

LOCK TABLES `personal_development_areas` WRITE;
/*!40000 ALTER TABLE `personal_development_areas` DISABLE KEYS */;
INSERT INTO `personal_development_areas` VALUES (7,'Managing Feelings and Emotions'),(8,'Our World'),(9,'Understanding Hazards'),(10,'Computer Safety'),(11,'Growing and Changing'),(12,'Fire Safety'),(13,'First Aid'),(23,'Managing Relationships'),(33,'Being Responsible'),(34,'Keeping/Staying Healthy'),(35,'Transition');
/*!40000 ALTER TABLE `personal_development_areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_text` text,
  `test_id` int DEFAULT NULL,
  `pda_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pda_id` (`pda_id`),
  KEY `test_id` (`test_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`pda_id`) REFERENCES `personal_development_areas` (`id`),
  CONSTRAINT `questions_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (29,'keep healthy',58,34),(30,'new',58,7),(32,' Which of the following could be dangerous?',65,34),(33,'Who keeps us safe in the community? ',65,34),(34,'How can we keep ourselves and others safe?',65,34);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `total_questions` int DEFAULT NULL,
  `correctly_answered` int DEFAULT NULL,
  `test_id` int DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `test_id` (`test_id`),
  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  CONSTRAINT `results_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schools`
--

DROP TABLE IF EXISTS `schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schools`
--

LOCK TABLES `schools` WRITE;
/*!40000 ALTER TABLE `schools` DISABLE KEYS */;
INSERT INTO `schools` VALUES (2,'Trotts Hill School','Wisden Rd, Stevenage SG1 5JD'),(3,'Nobel School','Mobbsbury Way, Stevenage SG2 0HS'),(5,'Howe Dell School','Hatfield'),(6,'Southfield School','Hatfield'),(7,'Oak View Primary','Hatfield'),(8,'Birchwood Nursery School','Hatfield');
/*!40000 ALTER TABLE `schools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `year_group` varchar(50) DEFAULT NULL,
  `school_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `school_id` (`school_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (17,'Om','9',3),(18,'OM','5',3),(19,'Danny','5',3),(20,'Case','5',3),(21,'Case','5',3),(22,'Om','5',3),(23,'Hayley','5',3),(24,'Nani','5',3),(25,'Nani','9',3),(26,'John','9',3),(27,'John','5',3),(28,'Stacy','5',3),(29,'Jack','5',3),(30,'Amit','5',3),(31,'amit','5',3),(32,'amit','5',3),(33,'Amit','5',3),(34,'Amit','5',3),(35,'Amit','5',3),(36,'Amit','5',3),(37,'Amit','5',3),(38,'Amit','5',3),(39,'Amit','5',3),(40,'Amit','5',3),(41,'Amit','5',3),(42,'Amit','5',3),(43,'Amit','5',3),(44,'Amit','5',3),(45,'Amit','5',3),(46,'Amit','5',3),(47,'Amit','5',3),(48,'','5',3),(49,'Amit','5',3),(50,'Amit','5',3),(51,'Amit','5',3),(52,'amir','5',3),(53,'amit','5',3),(54,'amit','5',3),(55,'amit','5',3);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `school_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `school_id` (`school_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`),
  CONSTRAINT `teachers_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (3,2,9),(4,2,12),(5,5,15),(6,5,18),(7,5,19);
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_schools`
--

DROP TABLE IF EXISTS `test_schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_schools` (
  `id` int NOT NULL AUTO_INCREMENT,
  `test_id` int NOT NULL,
  `school_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `test_id` (`test_id`,`school_id`),
  KEY `school_id` (`school_id`),
  CONSTRAINT `test_schools_ibfk_1` FOREIGN KEY (`test_id`) REFERENCES `tests` (`id`) ON DELETE CASCADE,
  CONSTRAINT `test_schools_ibfk_2` FOREIGN KEY (`school_id`) REFERENCES `schools` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_schools`
--

LOCK TABLES `test_schools` WRITE;
/*!40000 ALTER TABLE `test_schools` DISABLE KEYS */;
INSERT INTO `test_schools` VALUES (66,65,2),(67,65,3);
/*!40000 ALTER TABLE `test_schools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tests`
--

DROP TABLE IF EXISTS `tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
INSERT INTO `tests` VALUES (58,'Keeping safe'),(65,'Keeping/staying safe');
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role` enum('admin','teacher') NOT NULL DEFAULT 'teacher',
  `password_reset_token` varchar(255) DEFAULT NULL,
  `password_reset_token_created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@gmail.com','$2b$12$RBSXk5S6bNtLzstSpKrOQuk9wbUcEWYUhOnixkMMY9Mdtj15zF/y6','admin',NULL,NULL),(2,'string','string','$2b$12$S5g84CfQb/464sOFn1mpU.8qN762OJyBjfTuJhRGO5SQKZeclpLcW','admin',NULL,NULL),(3,'hayley','hayley@1decision.co.uk','$2b$12$2wV7KfWsTv4krluZJWYor.TlodWJQsCTBGQ3o1Ib6UQzqUMjcg2AW','teacher',NULL,NULL),(9,'Morgan','Morgan@1decision.co.uk','$2b$12$WAW/l0YmoKBYH8LpEHw6N.2g.ptPHWMZRJ2ylyNcXDYj20jQczNmq','teacher',NULL,NULL),(10,'Libby','Libby@1decision.co.uk','$2b$12$M0ni/YW2/HVGpRKivjr1euffyTi..GDhoygtP5HtIeITepn0.j.oC','teacher',NULL,NULL),(11,'Sofia','Sofia@1decision.co.uk','$2b$12$DVo3uGxAxkXQPDdQSL1QFOm2NI.ueQ6RDDSKZQBtgrbE1d4MLJnn6','teacher',NULL,NULL),(12,'Casey','Casey@1decision.co.uk','$2b$12$n1Ld9hla7cxt5MiRobnfeuGzOo1OFq51W5bDtMC5BOCUd.uslrrSy','teacher',NULL,NULL),(13,'velu','velu@gmail.com','$2b$12$.6fUkx1.TNfldTsfMqM7AOxDA2pJlVFhdp89hMBjg9gzcHYlJmizi','admin','40c71ef0a9489c05c8e99b5bb86448b7d55a62efa82604dc1fc01d4fdf56b055','2023-04-28 11:06:35'),(14,'Tommy','Tommy@gmail.com','$2b$12$cUStbpUW8lKxnb0GP9VQuerKCtyCcmqQ.Cem0GXURmFE7hboVAU6y','teacher',NULL,NULL),(15,'Om','omprakash@1decision.co.uk','$2b$12$Js8gIZkhX74Z8Cvc2kZyYeSD45GsrTZTvHm34uYje5D0Hxp3bnsnO','teacher',NULL,NULL),(16,'Tommy123','Tommy@1decision.co.uk','$2b$12$wAHnCZrVlYJHjKeJZAPiTuQyHNENDYoZo5rSX567xpTbChw8Tvjf2','teacher',NULL,NULL),(17,'Tommy1','tommy@1decision.co.uk','$2b$12$HTte8iWA24rb1NCNJTWbkuFsO9uKQMbbLNMW.1WK1hV5iR/q7Tq0i','teacher',NULL,NULL),(18,'TommyGodbear','Tommy@1decision.co.uk','$2b$12$gNfpy/OtXshDR/AWgf20zuygWosMl9q7hv42RQXUSx1fPIAfFB/vi','teacher',NULL,NULL),(19,'Danny','Danny@gmail.com','$2b$12$aXeBdmGeWt8vvNmRAiawee.T2iJCP9tRoSXZnOCVPdSH1KomlAY86','teacher',NULL,NULL),(20,'velmurugan','velmuruganr165@gmail.com','$2b$12$V8IwqzXR5OzHEv7Lnyz73OSdNM.BbaeKupsiCRKraDUvKjL.oMSCe','admin',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-19 10:54:00
