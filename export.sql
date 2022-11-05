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
  `category` varchar(50) NOT NULL,
  `productId` varchar(50) DEFAULT NULL,
  `workerId` int(10) unsigned NOT NULL DEFAULT '0',
  `hasProduct` int(10) unsigned NOT NULL DEFAULT '0',
  `status` varchar(10) NOT NULL DEFAULT 'STOPPED',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql12532759.assemblyLines: ~6 rows (approximately)
DELETE FROM `assemblyLines`;
INSERT INTO `assemblyLines` (`id`, `category`, `productId`, `workerId`, `hasProduct`, `status`) VALUES
	('102924c3', 'SUV', NULL, 0, 0, 'STOPPED'),
	('2228fa79', 'SEDAN', NULL, 0, 0, 'STOPPED'),
	('3ff4006a', 'SEDAN', NULL, 0, 0, 'STOPPED'),
	('8f92215e', 'MINIVAN', NULL, 0, 0, 'STOPPED'),
	('98ebeaed', 'SEDAN', NULL, 0, 0, 'STOPPED'),
	('b7500564', 'SUV', NULL, 0, 0, 'STOPPED');

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

-- Dumping data for table sql12532759.materials: ~8 rows (approximately)
DELETE FROM `materials`;
INSERT INTO `materials` (`id`, `name`, `cost`, `vendor`, `amount`, `quantityPerUnit`) VALUES
	('1e652f53', 'banh xe SUV', 110, 'Toyota', 80, 4),
	('49e89a26', 'banh xe Sedan', 200, 'BMW', 100, 4),
	('62a4ead4', 'khung xe Sedan', 120, 'BMW', 50, 1),
	('7738d992', 'dong co Sedan new', 100, 'BMW', 15, 1),
	('9ba1e07a', 'dong co Sedan', 80, 'BMW', 10, 1),
	('b680b709', 'khung xe MiniVan', 55, 'Thaco', 8, 1),
	('e2adcdd3', 'banh xe MiniVan', 30, 'Thaco', 16, 4),
	('f0df3099', 'khung xe SUV', 65, 'Toyota', 5, 1);

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Nguyen lieu dau vao cho san xuat';

-- Dumping data for table sql12532759.requirements: ~4 rows (approximately)
DELETE FROM `requirements`;
INSERT INTO `requirements` (`id`, `category`, `name`, `materials`, `workerSpecialation`) VALUES
	('1', 'SUV', 'Ford Ranger', '{ "f0df3099": 1, "1e652f53": 4 }', 'SUV'),
	('2', 'SEDAN', 'Vinfast Lux', '{ "49e89a26": 4, "62a4ead4": 1, "9ba1e07a": 1 }', 'SEDAN'),
	('3', 'SEDAN', 'Mecedes X7', '{ "49e89a26": 4, "62a4ead4": 1, "7738d992": 1 }', 'SEDAN'),
	('4', 'MINIVAN', 'Inova', '{ "b680b709": 1, "e2adcdd3": 4 }', 'MINIVAN');

-- Dumping structure for table sql12532759.workers
CREATE TABLE IF NOT EXISTS `workers` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `specialization` varchar(50) NOT NULL,
  `workingShift` varchar(10) NOT NULL DEFAULT 'ON_SHIFT',
  `workingTime` int(11) NOT NULL DEFAULT '0',
  `assemblyId` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table sql12532759.workers: ~5 rows (approximately)
DELETE FROM `workers`;
INSERT INTO `workers` (`id`, `name`, `specialization`, `workingShift`, `workingTime`, `assemblyId`) VALUES
	('1', 'Nguyen Van Dien', 'SUV', 'ON_SHIFT', 0, 'None'),
	('2', 'Nguyen Minh Duy', 'SUV', 'OUT_SHIFT', 0, 'None'),
	('3', 'Nguyen Van Tien', 'SUV', 'ON_SHIFT', 0, 'None'),
	('4', 'Nguyen Van Tung', 'SUV', 'ON_SHIFT', 0, 'None'),
	('5', 'To Thi Minh Hang', 'SEDAN', 'ON_SHIFT', 0, 'None');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
