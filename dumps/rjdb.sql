-- MySQL dump 10.13  Distrib 5.7.12, for Win32 (AMD64)
--
-- Host: localhost    Database: rjdb
-- ------------------------------------------------------
-- Server version	5.6.32-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `disciplines`
--

DROP TABLE IF EXISTS `disciplines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `disciplines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `feature` varchar(255) NOT NULL,
  `cycle` varchar(85) NOT NULL,
  `code` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disciplines`
--

LOCK TABLES `disciplines` WRITE;
/*!40000 ALTER TABLE `disciplines` DISABLE KEYS */;
/*!40000 ALTER TABLE `disciplines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(85) NOT NULL,
  `specialty` varchar(124) NOT NULL,
  `study_form` varchar(1) NOT NULL DEFAULT 'Д',
  `university` varchar(85) NOT NULL DEFAULT 'ДТК ДДТУ',
  `qualification` varchar(85) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journal_hours`
--

DROP TABLE IF EXISTS `journal_hours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `journal_hours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `load_id` int(11) NOT NULL,
  `modules` tinyint(4) NOT NULL,
  `lecture` int(11) NOT NULL DEFAULT '0',
  `practice` int(11) NOT NULL DEFAULT '0',
  `labor` int(11) NOT NULL DEFAULT '0',
  `seminar` int(11) NOT NULL DEFAULT '0',
  `self_lecture` int(11) NOT NULL DEFAULT '0',
  `self_practice` int(11) NOT NULL DEFAULT '0',
  `self_labor` int(11) NOT NULL DEFAULT '0',
  `self_seminar` int(11) NOT NULL DEFAULT '0',
  `AKR` int(11) NOT NULL DEFAULT '0',
  `DKR` int(11) NOT NULL DEFAULT '0',
  `MK` int(11) NOT NULL DEFAULT '0',
  `lecture2` int(11) NOT NULL DEFAULT '0',
  `practice2` int(11) NOT NULL DEFAULT '0',
  `labor2` int(11) NOT NULL DEFAULT '0',
  `seminar2` int(11) NOT NULL DEFAULT '0',
  `self_lecture2` int(11) NOT NULL DEFAULT '0',
  `self_practice2` int(11) NOT NULL DEFAULT '0',
  `self_labor2` int(11) NOT NULL DEFAULT '0',
  `self_seminar2` int(11) NOT NULL DEFAULT '0',
  `AKR2` int(11) NOT NULL DEFAULT '0',
  `DKR2` int(11) NOT NULL DEFAULT '0',
  `MK2` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `load_id` (`load_id`),
  CONSTRAINT `journal_hours_loads_fk` FOREIGN KEY (`load_id`) REFERENCES `loads` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal_hours`
--

LOCK TABLES `journal_hours` WRITE;
/*!40000 ALTER TABLE `journal_hours` DISABLE KEYS */;
/*!40000 ALTER TABLE `journal_hours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journal_marks`
--

DROP TABLE IF EXISTS `journal_marks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `journal_marks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `load_id` int(11) NOT NULL,
  `wc1` int(11) NOT NULL DEFAULT '1',
  `wc2` int(11) NOT NULL DEFAULT '0',
  `visit` int(11) NOT NULL DEFAULT '0',
  `lecture` int(11) NOT NULL DEFAULT '0',
  `practice` int(11) NOT NULL DEFAULT '0',
  `labor` int(11) NOT NULL DEFAULT '0',
  `seminar` int(11) NOT NULL DEFAULT '0',
  `AKR` int(11) NOT NULL DEFAULT '0',
  `DKR` int(11) NOT NULL DEFAULT '0',
  `module` int(11) NOT NULL DEFAULT '0',
  `visit2` int(11) NOT NULL DEFAULT '0',
  `lecture2` int(11) NOT NULL DEFAULT '0',
  `practice2` int(11) NOT NULL DEFAULT '0',
  `labor2` int(11) NOT NULL DEFAULT '0',
  `seminar2` int(11) NOT NULL DEFAULT '0',
  `AKR2` int(11) NOT NULL DEFAULT '0',
  `DKR2` int(11) NOT NULL DEFAULT '0',
  `module2` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `load_id` (`load_id`),
  CONSTRAINT `journal_marks_loads_fk` FOREIGN KEY (`load_id`) REFERENCES `loads` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal_marks`
--

LOCK TABLES `journal_marks` WRITE;
/*!40000 ALTER TABLE `journal_marks` DISABLE KEYS */;
/*!40000 ALTER TABLE `journal_marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loads`
--

DROP TABLE IF EXISTS `loads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `discipline_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `semester` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `lecture` int(11) NOT NULL DEFAULT '0',
  `practice` int(11) NOT NULL DEFAULT '0',
  `labor` int(11) NOT NULL DEFAULT '0',
  `seminar` int(11) NOT NULL DEFAULT '0',
  `self_lecture` int(11) NOT NULL DEFAULT '0',
  `self_practice` int(11) NOT NULL DEFAULT '0',
  `self_labor` int(11) NOT NULL DEFAULT '0',
  `self_seminar` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `loads_discipline_fk_idx` (`discipline_id`),
  KEY `loads_teachers_fk_idx` (`teacher_id`),
  KEY `loads_groups_fk_idx` (`group_id`),
  CONSTRAINT `loads_disciplines_fk` FOREIGN KEY (`discipline_id`) REFERENCES `disciplines` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `loads_groups_fk` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `loads_teachers_fk` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loads`
--

LOCK TABLES `loads` WRITE;
/*!40000 ALTER TABLE `loads` DISABLE KEYS */;
/*!40000 ALTER TABLE `loads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `first` varchar(85) NOT NULL,
  `middle` varchar(85) DEFAULT NULL,
  `last` varchar(85) NOT NULL,
  `sex` varchar(1) NOT NULL,
  `privilege` varchar(85) NOT NULL,
  `finance_form` varchar(1) NOT NULL DEFAULT 'Б',
  PRIMARY KEY (`id`),
  KEY `group_fk_idx` (`group_id`),
  CONSTRAINT `students_groups_fk` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  CONSTRAINT `teachers_users_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(85) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first` varchar(85) NOT NULL,
  `middle` varchar(85) DEFAULT NULL,
  `last` varchar(85) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `sex` varchar(1) NOT NULL DEFAULT 'M',
  `access` varchar(10) NOT NULL DEFAULT '1',
  `pristine` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','58acb7acccce58ffa8b953b12b5a7702bd42dae441c1ad85057fa70b','Ronald','Sterling','Everdone','creategoolemail@gmail.com','M','34',0),(3,'woman','a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057','Валерія','Шмітцівна','Жінка','woman@gmugle.com','F','1',0),(5,'Bob','a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057','Другий','Номер','Боб','second@gamuil.com','M','2',0),(10,'Sally','a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057','Микола','Дмитрович','Сальний','nikola@gmugle.com','M','12',0),(11,'allinc','a7470858e79c282bc2f6adfd831b132672dfd1224c1e78cbf5bcd057','Иван','Иванович','Инклусивец','kkk@kkk.ua','M','1234',0);
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

-- Dump completed on 2017-07-28 16:02:44
