-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: elatico
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `accede`
--

DROP TABLE IF EXISTS `accede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accede` (
  `idUsuario` int NOT NULL,
  `idAlmacen` int NOT NULL,
  `idTienda` int NOT NULL,
  PRIMARY KEY (`idAlmacen`,`idUsuario`,`idTienda`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idTienda` (`idTienda`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accede`
--

LOCK TABLES `accede` WRITE;
/*!40000 ALTER TABLE `accede` DISABLE KEYS */;
INSERT INTO `accede` VALUES (2,1,1),(2,1,2),(3,1,3);
/*!40000 ALTER TABLE `accede` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `almacen`
--

DROP TABLE IF EXISTS `almacen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `almacen` (
  `idAlmacen` int NOT NULL AUTO_INCREMENT,
  `latitudAlmacen` decimal(18,15) NOT NULL,
  `longitudAlmacen` decimal(18,15) DEFAULT NULL,
  PRIMARY KEY (`idAlmacen`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `almacen`
--

LOCK TABLES `almacen` WRITE;
/*!40000 ALTER TABLE `almacen` DISABLE KEYS */;
INSERT INTO `almacen` VALUES (1,25.664219486420595,-100.421560887268850);
/*!40000 ALTER TABLE `almacen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contiene`
--

DROP TABLE IF EXISTS `contiene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contiene` (
  `idAlmacen` int NOT NULL DEFAULT '1',
  `idProducto` int NOT NULL,
  `cantidadProducto` int NOT NULL,
  PRIMARY KEY (`idAlmacen`,`idProducto`),
  KEY `idProducto` (`idProducto`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contiene`
--

LOCK TABLES `contiene` WRITE;
/*!40000 ALTER TABLE `contiene` DISABLE KEYS */;
INSERT INTO `contiene` VALUES (1,1,7),(1,2,15),(1,3,3);
/*!40000 ALTER TABLE `contiene` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `idTipo` int NOT NULL,
  `nombreTipo` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`idTipo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'Administrador'),(2,'Almacen'),(3,'Tienda');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idPedido` int NOT NULL AUTO_INCREMENT,
  `idAlmacen` int NOT NULL,
  `idTienda` int NOT NULL,
  `idProducto` int NOT NULL,
  `cantidadPedido` int NOT NULL,
  `fechaPedido` date NOT NULL,
  `fechaEntrega` date DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pendiente',
  PRIMARY KEY (`idPedido`,`idAlmacen`,`idProducto`,`idTienda`),
  KEY `idAlmacen` (`idAlmacen`),
  KEY `idTienda` (`idTienda`),
  KEY `idProducto` (`idProducto`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,1,1,1,4,'2023-04-13','2023-04-20','Entregado'),(2,1,2,2,7,'2023-04-28','2023-05-09','Entregado'),(3,1,3,3,5,'2023-05-12','0000-00-00','Pendiente');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `idProducto` int NOT NULL AUTO_INCREMENT,
  `nombreProducto` varchar(20) NOT NULL,
  PRIMARY KEY (`idProducto`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Tachones'),(2,'Tenis de Correr'),(3,'Tenis de Yoga');
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tienda`
--

DROP TABLE IF EXISTS `tienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tienda` (
  `idTienda` int NOT NULL AUTO_INCREMENT,
  `nombreTienda` varchar(20) NOT NULL,
  `latitudTienda` decimal(18,15) NOT NULL,
  `longitudTienda` decimal(18,15) DEFAULT NULL,
  PRIMARY KEY (`idTienda`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tienda`
--

LOCK TABLES `tienda` WRITE;
/*!40000 ALTER TABLE `tienda` DISABLE KEYS */;
INSERT INTO `tienda` VALUES (1,'Innova Sports',25.656691498716803,-100.336182129680000),(2,'Under Armour',25.725034248203120,-100.359700105779080),(3,'Decathlon',25.658121082808524,-100.353117913679110);
/*!40000 ALTER TABLE `tienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `nombreUsuario` varchar(50) NOT NULL,
  `contrasenaUsuario` char(102) DEFAULT NULL,
  `nombre` varchar(80) DEFAULT NULL,
  `apellidoPaterno` varchar(80) DEFAULT NULL,
  `apellidoMaterno` varchar(80) DEFAULT NULL,
  `idTipo` int NOT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `idTipo` (`idTipo`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'emilioadmin','666','Emilio','Cano','Moreno',1),(2,'juanalmacen','555','Juan','Garza','Garza',2),(3,'pedrotienda','444','Pedro','Garcia','Juarez',3);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valida`
--

DROP TABLE IF EXISTS `valida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valida` (
  `idUsuario` int NOT NULL,
  `idTipo` int NOT NULL,
  PRIMARY KEY (`idTipo`,`idUsuario`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valida`
--

LOCK TABLES `valida` WRITE;
/*!40000 ALTER TABLE `valida` DISABLE KEYS */;
INSERT INTO `valida` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `valida` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-20 20:27:47
