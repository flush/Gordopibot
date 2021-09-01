-- MariaDB dump 10.19  Distrib 10.5.10-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: gordopibot_db
-- ------------------------------------------------------
-- Server version	10.5.10-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aperturas_local`
--

DROP TABLE IF EXISTS `aperturas_local`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aperturas_local` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `fechaApertura` datetime DEFAULT NULL,
  `fechaCierre` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aperturas_local`
--

LOCK TABLES `aperturas_local` WRITE;
/*!40000 ALTER TABLE `aperturas_local` DISABLE KEYS */;
INSERT INTO `aperturas_local` VALUES (6,'2021-06-14 08:30:00','2021-06-14 13:00:00'),(7,'2021-06-17 18:30:00','2021-06-17 21:00:00'),(8,'2021-06-19 22:00:00','2021-06-19 23:30:00'),(9,'2021-06-20 18:00:00','2021-06-20 22:00:00'),(10,'2021-06-23 18:45:00','2021-06-23 23:45:00'),(11,'2021-06-30 18:30:00','2021-06-30 22:30:00'),(13,'2021-07-04 17:00:00','2021-07-04 20:00:00'),(14,'2021-07-07 19:00:00','2021-07-07 21:00:00'),(15,'2021-07-21 17:00:00','2021-07-21 20:30:00'),(16,'2021-08-09 18:00:00','2021-08-09 21:00:00'),(17,'2021-08-18 17:00:00','2021-08-18 21:00:00');
/*!40000 ALTER TABLE `aperturas_local` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_usuario`
--

DROP TABLE IF EXISTS `categorias_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categorias_usuario` (
  `codigo` char(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_usuario`
--

LOCK TABLES `categorias_usuario` WRITE;
/*!40000 ALTER TABLE `categorias_usuario` DISABLE KEYS */;
INSERT INTO `categorias_usuario` VALUES ('AD','Administrador'),('JU','Jugón'),('SJ','Socio junior'),('SP','Socio de Pago');
/*!40000 ALTER TABLE `categorias_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partidas`
--

DROP TABLE IF EXISTS `partidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partidas` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `nombreJuego` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `idJuego` int(10) unsigned DEFAULT NULL,
  `idApertura` bigint(20) unsigned DEFAULT NULL,
  `idCreador` int(10) unsigned DEFAULT NULL,
  `plazas` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `partidas_usuario_fk` (`idCreador`),
  KEY `partidas_apertura_fk` (`idApertura`),
  CONSTRAINT `partidas_apertura_fk` FOREIGN KEY (`idApertura`) REFERENCES `aperturas_local` (`id`),
  CONSTRAINT `partidas_usuario_fk` FOREIGN KEY (`idCreador`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partidas`
--

LOCK TABLES `partidas` WRITE;
/*!40000 ALTER TABLE `partidas` DISABLE KEYS */;
INSERT INTO `partidas` VALUES (11,'2021-06-17 18:30:00','Aliens: Hadley\'s Hope',257313,7,709463079,5),(12,'2021-06-19 22:00:00','Herocults',98734,8,709463079,5),(13,'2021-06-19 22:00:00','Haunted Village',104952,8,709463079,4),(14,'2021-06-20 19:00:00','นักบุกเบิกแห่ง Catan',13,9,4609792,4),(15,'2021-06-20 20:30:00','Merv: La route de la soie',306040,9,4609792,4),(16,'2021-06-23 18:45:00','Merv: La route de la soie',306040,10,4609792,4),(17,'2021-06-30 18:30:00','Alta Tensione',2651,11,4609792,5),(19,'2021-07-04 17:00:00','Bonfire',304420,13,4609792,4),(20,'2021-07-07 19:00:00','Tiny Epic Pirates',309430,14,44289874,4),(21,'2021-07-21 17:00:00','Arkham Horror (Third Edition)',257499,15,1149034943,4),(22,'2021-08-09 18:00:00','Doom: Le Jeu de Plateau',205317,16,709463079,4),(23,'2021-08-18 17:00:00','Runebound',9829,17,709463079,3);
/*!40000 ALTER TABLE `partidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(10) unsigned NOT NULL,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `categoria` char(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuarios_categoria_fk` (`categoria`),
  CONSTRAINT `usuarios_categoria_fk` FOREIGN KEY (`categoria`) REFERENCES `categorias_usuario` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (4609792,'Tafh15','SP'),(7281595,'Abaldea','JU'),(12040738,'TheYuriGagarin','SP'),(15117258,'Sergio','SP'),(33605231,'Alteon','SJ'),(44289874,'Pabtulkas','JU'),(78485716,'Cristina','SJ'),(155682333,'Senefelder','SP'),(252231615,'Isa','SJ'),(286872521,'Bgmraul','JU'),(391593077,'Victormania','SJ'),(412210367,'Sergio PC','JU'),(487384307,'pgarciab84','SP'),(602605430,'Alex5casas','SP'),(709463079,'Alfredo','SP'),(715134915,'Juli','SP'),(733905290,'VenganZalando','SP'),(769205187,'Exdezh (Joaquin)','JU'),(854746973,'Pizorra40','JU'),(989833157,'sshadowman','JU'),(1020918543,'Lorena','SP'),(1058579500,'Rafael Gomez','SP'),(1149034943,'Alberto Álvarez','SP'),(1187090192,'Moyoglo','JU'),(1191490864,'M, Ángeles','SP'),(1236697738,'Paco Fdez','SP'),(1265325114,'Ani','JU'),(1419004892,'Valenzuelo','JU'),(1435233215,'angel m','JU'),(1742594637,'Isabel','SJ'),(1837553630,'Joaquin','JU'),(1883271023,'Antonio_EdCo','JU');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_aperturas`
--

DROP TABLE IF EXISTS `usuarios_aperturas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_aperturas` (
  `idUsuario` int(10) unsigned DEFAULT NULL,
  `idApertura` bigint(20) unsigned DEFAULT NULL,
  KEY `usuario_apertura_usuario_fk` (`idUsuario`),
  KEY `usuario_apertura_apertura_fk` (`idApertura`),
  CONSTRAINT `usuario_apertura_apertura_fk` FOREIGN KEY (`idApertura`) REFERENCES `aperturas_local` (`id`),
  CONSTRAINT `usuario_apertura_usuario_fk` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_aperturas`
--

LOCK TABLES `usuarios_aperturas` WRITE;
/*!40000 ALTER TABLE `usuarios_aperturas` DISABLE KEYS */;
INSERT INTO `usuarios_aperturas` VALUES (709463079,6),(709463079,7),(733905290,7),(15117258,7),(709463079,8),(4609792,8),(4609792,9),(12040738,9),(4609792,10),(709463079,10),(1191490864,10),(15117258,10),(4609792,11),(1191490864,11),(709463079,11),(854746973,11),(4609792,13),(1236697738,13),(1837553630,13),(391593077,13),(709463079,14),(44289874,14),(733905290,14),(1149034943,15),(709463079,16),(1149034943,16),(709463079,17),(1149034943,17),(733905290,17);
/*!40000 ALTER TABLE `usuarios_aperturas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_partidas`
--

DROP TABLE IF EXISTS `usuarios_partidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_partidas` (
  `idUsuario` int(10) unsigned DEFAULT NULL,
  `idPartida` bigint(20) unsigned DEFAULT NULL,
  KEY `usuario_partidas_usuario_fk` (`idUsuario`),
  KEY `usuario_partidas_partidas_fk` (`idPartida`),
  CONSTRAINT `usuario_partidas_partidas_fk` FOREIGN KEY (`idPartida`) REFERENCES `partidas` (`id`),
  CONSTRAINT `usuario_partidas_usuario_fk` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_partidas`
--

LOCK TABLES `usuarios_partidas` WRITE;
/*!40000 ALTER TABLE `usuarios_partidas` DISABLE KEYS */;
INSERT INTO `usuarios_partidas` VALUES (709463079,11),(1149034943,11),(12040738,11),(733905290,11),(15117258,11),(709463079,12),(709463079,13),(4609792,12),(4609792,14),(4609792,13),(4609792,15),(12040738,15),(4609792,16),(709463079,16),(1191490864,16),(15117258,16),(4609792,17),(1191490864,17),(709463079,17),(854746973,17),(4609792,19),(1236697738,19),(1837553630,19),(44289874,20),(709463079,20),(733905290,20),(1149034943,21),(709463079,22),(1149034943,22),(709463079,23),(1149034943,23),(733905290,23);
/*!40000 ALTER TABLE `usuarios_partidas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-20 18:42:23
