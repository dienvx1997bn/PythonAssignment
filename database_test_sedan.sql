-- --------------------------------------------------------
-- Host:                         sql12.freesqldatabase.com
-- Server version:               5.5.62-0ubuntu0.14.04.1 - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for sql12532759
CREATE DATABASE IF NOT EXISTS `sql12532759` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `sql12532759`;

-- Dumping structure for table sql12532759.assemblyLines
CREATE TABLE IF NOT EXISTS `assemblyLines` (
  `id` varchar(50) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `productId` varchar(50) DEFAULT NULL,
  `workerId` varchar(50) DEFAULT NULL,
  `status` varchar(10) DEFAULT 'STOPPED',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql12532759.assemblyLines: ~7 rows (approximately)
DELETE FROM `assemblyLines`;
INSERT INTO `assemblyLines` (`id`, `category`, `productId`, `workerId`, `status`) VALUES
	('102924c3', 'SUV', NULL, NULL, 'STOPPED'),
	('2228fa79', 'SEDAN', NULL, NULL, 'STOPPED'),
	('3ff4006a', 'SEDAN', NULL, NULL, 'STOPPED'),
	('8bd9c72d', 'SEDAN', NULL, NULL, 'STOPPED'),
	('8f92215e', 'MINIVAN', NULL, NULL, 'STOPPED'),
	('98ebeaed', 'SEDAN', NULL, NULL, 'STOPPED'),
	('b7500564', 'SUV', NULL, NULL, 'STOPPED');

-- Dumping structure for table sql12532759.materials
CREATE TABLE IF NOT EXISTS `materials` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `cost` int(11) NOT NULL,
  `vendor` varchar(50) NOT NULL,
  `amount` int(11) NOT NULL,
  `quantityPerUnit` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql12532759.materials: ~6 rows (approximately)
DELETE FROM `materials`;
INSERT INTO `materials` (`id`, `name`, `cost`, `vendor`, `amount`, `quantityPerUnit`) VALUES
	('10882e26', 'khung xe Sedan new', 90, 'BMW', 20, 1),
	('49e89a26', 'banh xe Sedan', 200, 'BMW', 180, 4),
	('62a4ead4', 'khung xe Sedan', 120, 'BMW', 15, 1),
	('7738d992', 'dong co Sedan new', 100, 'BMW', 15, 1),
	('9ba1e07a', 'dong co Sedan', 80, 'BMW', 20, 1),
	('cffb27ee', 'banh xe Sedan new', 50, 'BMW', 50, 4);

-- Dumping structure for table sql12532759.products
CREATE TABLE IF NOT EXISTS `products` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `materials` varchar(2048) NOT NULL,
  `category` varchar(50) NOT NULL,
  `cost` int(11) NOT NULL,
  `produceTime` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `progress` varchar(10) NOT NULL COMMENT 'WAITING/PROCESSING/FINISHED',
  `qcStatus` varchar(10) NOT NULL COMMENT 'PASS/FAIL',
  `assemblyId` varchar(50) NOT NULL,
  `workerId` varchar(50) NOT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql12532759.products: ~0 rows (approximately)
DELETE FROM `products`;

-- Dumping structure for table sql12532759.requirements
CREATE TABLE IF NOT EXISTS `requirements` (
  `id` varchar(50) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `materials` varchar(50) DEFAULT NULL,
  `workerSpecialation` varchar(50) DEFAULT NULL,
  `timeNedded` int(11) DEFAULT NULL COMMENT 'in seconds',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Nguyen lieu dau vao cho san xuat';

-- Dumping data for table sql12532759.requirements: ~3 rows (approximately)
DELETE FROM `requirements`;
INSERT INTO `requirements` (`id`, `category`, `name`, `materials`, `workerSpecialation`, `timeNedded`) VALUES
	('6bebf867', 'SEDAN', 'BMW X7', '{ "cffb27ee": 4, "10882e26": 1, "7738d992": 1 }', 'SEDAN', 7),
	('d4ab9592', 'SEDAN', 'Vinfast Lux', '{ "49e89a26": 4, "62a4ead4": 1, "9ba1e07a": 1 }', 'SEDAN', 9),
	('ec77eb31', 'SEDAN', 'Marda CX 3', '{ "49e89a26": 4, "10882e26": 1, "9ba1e07a": 1 }', 'SEDAN', 8);

-- Dumping structure for table sql12532759.workers
CREATE TABLE IF NOT EXISTS `workers` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `specialization` varchar(50) NOT NULL,
  `workingShift` varchar(10) NOT NULL DEFAULT 'ON_SHIFT',
  `workingTime` int(11) NOT NULL DEFAULT '0',
  `assemblyId` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql12532759.workers: ~7 rows (approximately)
DELETE FROM `workers`;
INSERT INTO `workers` (`id`, `name`, `specialization`, `workingShift`, `workingTime`, `assemblyId`) VALUES
	('10ae1c21', 'Nguyen Van Tien', 'SUV', 'ON_SHIFT', 0, NULL),
	('308c17f3', 'Nguyen Van Dien', 'SUV', 'ON_SHIFT', 0, NULL),
	('46b18b05', 'Nguyen Van Tung', 'MINIVAN', 'ON_SHIFT', 0, NULL),
	('5c793637', 'Nguyen Van Toan', 'SEDAN', 'ON_SHIFT', 0, NULL),
	('5e3498c5', 'To Thi Minh Hang', 'SEDAN', 'ON_SHIFT', 0, NULL),
	('74290310', 'Nguyen Minh Duy', 'SUV', 'OUT_SHIFT', 0, NULL),
	('8feb5a75', 'Nguyen Thi Hoai An', 'SEDAN', 'ON_SHIFT', 0, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
