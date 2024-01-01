-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 01, 2024 at 10:16 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `banking_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `AccountID` int(10) UNSIGNED NOT NULL,
  `ClientID` int(10) UNSIGNED NOT NULL,
  `TypeofAccount` varchar(25) NOT NULL,
  `Balance` decimal(10,2) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`AccountID`, `ClientID`, `TypeofAccount`, `Balance`) VALUES
(2, 3, 'Savings', 12323.00),
(3, 1, 'Savings', 99999999.99),
(4, 90, 'Savings', 1000000.00),
(5, 1, 'Savings', 1123.12),
(6, 11, 'Savings', 1000.00),
(7, 2, 'Savings', 6900.00),
(8, 1, 'Savings', 50000.00),
(9, 2, 'Savings', 1000.00),
(10, 2, 'Savings', 34250.00);

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `ClientID` int(11) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `MiddleName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) NOT NULL,
  `DateOfBirth` date NOT NULL,
  `homeAddress` varchar(100) NOT NULL,
  `Contact` bigint(20) UNSIGNED NOT NULL,
  `EmailAddress` varchar(100) NOT NULL,
  `TypeofID_1` varchar(50) NOT NULL,
  `TypeofID_2` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`ClientID`, `FirstName`, `MiddleName`, `LastName`, `DateOfBirth`, `homeAddress`, `Contact`, `EmailAddress`, `TypeofID_1`, `TypeofID_2`) VALUES
(1, 'RITCHMOND JAMES', 'SAJA', 'TAJARROS', '2002-03-25', 'Buting, Pasig City', 1234567890, 'asdsd@tajarros.edu.ph', 'Philippine Postal ID', 'Barangay Certification'),
(2, 'JHEDDIAH EVAN MHIGUEL', 'DELA CRUZ', 'EMPERADOR', '2010-10-10', 'San Andres, Cainta Rizal', 9939270175, 'jem010@gmail.com', 'School ID (for minors)', NULL),
(6, 'JHUSTIENE CASEY', 'PAULINO', 'DELA CRUZ', '2005-01-23', 'Sta. Lucia, Pasig City', 9939270175, 'jhustienecasey@plpasig.edu.ph', 'Barangay Certification', 'PhilHealth ID'),
(8, 'JHEIZON BRHYLLE ASDAS', 'PAULINO', 'DELA CRUZ', '2002-11-11', 'Sta. Lucia, Pasig Ciy', 9939270175, 'gmjheizs@sad.c', 'Barangay Certification', 'PhilHealth ID'),
(11, 'GM', 'NULL', 'BRHYLLE', '2002-11-11', 'Santa Lucia, Pasig City', 9939270175, 'gmjheizon027@gmail.com', 'Barangay Certification', 'Overseas Filipino Workers (OFW) ID'),
(15, 'JHEIZON', 'BRHYLLE', 'EMPERADOR', '2002-11-11', 'Caloocan City', 9339270175, 'gmjheizon252@gmail.com', 'Barangay Certification', 'PhilHealth ID'),
(33, 'JHACK VON DHAENIEL', 'DELA CRUZ', 'EMPERADOR', '2015-12-18', 'fmfjh@', 9964121267, 'sdasd', 'School ID (for minors)', NULL),
(56, 'JHEKYLL EMP', 'EMPERADOR', 'DELA CRUZ', '2002-11-11', 'Sitio Onse, Caloocan City', 9939270175, 'gmjheizon@gmail.com', 'School ID (for minors)', NULL),
(90, 'NEITO ARISU', 'KUWAKURA', 'KOUTEI', '2002-11-11', 'San Nicholas, Pasig City', 9126411234, 'gmjheizon027@gmail.com', 'School ID (for minors)', NULL),
(123, 'AARON', 'IDK', 'DE LEON', '2002-12-12', 'eyronn12@gmail.com', 1234567890, 'eyronn12@gmail.com', 'School ID (for minors)', NULL),
(543, 'SOOH-KWON', '', 'GWENCHANA', '2002-11-11', 'asdasdasdasd', 9939270175, 'asdasd@gm.com', 'School ID (for minors)', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `listid`
--

CREATE TABLE `listid` (
  `IDType` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `listid`
--

INSERT INTO `listid` (`IDType`) VALUES
('Barangay Certification'),
('Driver\'s License'),
('NBI Clearance'),
('Overseas Filipino Workers (OFW) ID'),
('Overseas Workers Welfare Administration (OWWA) ID'),
('Passport'),
('Person with Disability (PWD) ID'),
('PhilHealth ID'),
('Philippine Identification System (PhilSys) ID'),
('Philippine Postal ID'),
('Professional Regulations Commission (PRC) ID'),
('School ID (for minors)'),
('Senior Citizen ID'),
('Social Security System (SSS) ID'),
('Tax Identification Number (TIN) ID'),
('Unified Multi-purpose ID (UMID)'),
('Voter\'s ID');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`AccountID`),
  ADD KEY `ClientID` (`ClientID`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`ClientID`);

--
-- Indexes for table `listid`
--
ALTER TABLE `listid`
  ADD PRIMARY KEY (`IDType`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
