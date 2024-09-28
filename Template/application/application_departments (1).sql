-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 21, 2024 at 05:16 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rit_phd_admission`
--

-- --------------------------------------------------------

--
-- Table structure for table `application_departments`
--

CREATE TABLE `applications_departments` (
  `dept_code` varchar(200) NOT NULL,
  `department` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `application_departments`
--

INSERT INTO `applications_departments` (`dept_code`, `department`) VALUES
('AD', 'ARTIFICIAL INTELLIGENCE AND DATA SCIENCE'),
('CB', 'COMPUTER SCIENCE AND BUSINESS SYSTEM'),
('CE', 'CIVIL ENGINEERING'),
('CHEMISTRY', 'CHEMISTRY'),
('COC', 'CO-CURRICULAR'),
('CSE', 'COMPUTER SCIENCE AND ENGINEERING'),
('ECE', 'ELECTRONICS AND COMMUNICATION ENGINEERING'),
('EEE', 'ELECRICAL AND ELECTRONICS ENGINEERING'),
('ENGLISH', 'ENGLISH'),
('EXC', 'Extra-curricular'),
('HOSTEL', 'HOSTEL'),
('IT', 'INFORMATION TECHNOLOGY'),
('MATHEMATICS', 'MATHEMATICS'),
('MECH', 'MECHANICAL ENGINEERING'),
('NCC', 'NCC'),
('NSS', 'NSS'),
('OFFICE', 'OFFICE'),
('PED', 'PHYSICAL EDUCATION'),
('PH', 'POWER HOUSE'),
('PHYSICS', 'PHYSICS'),
('R&D', 'RESEARCH AND DEVELOPMENT'),
('TRANSPORT', 'TRANSPORT');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `application_departments`
--
ALTER TABLE `applications_departments`
  ADD PRIMARY KEY (`dept_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
