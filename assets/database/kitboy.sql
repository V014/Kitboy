-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 07, 2025 at 05:51 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kitboy`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(7) NOT NULL,
  `user_id` int(7) DEFAULT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `payment_status` enum('complete','pending','incomplete') DEFAULT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `user_id`, `firstname`, `lastname`, `email`, `address`, `contact`, `payment_status`, `date_registered`) VALUES
(1, NULL, 'Wanga', 'Kanjala', 'wangakanjala@gmail.com', 'box 1738, Blantyre, Chilomoni Fargo, Dulamoyo Rd', '0996335639', 'complete', '2025-08-06 19:33:30'),
(2, NULL, 'Emmanuel', 'Chinyanja', 'emkach@gmail.com', 'Box 1234, Blantyre, Chilobwe', '0987425369', 'complete', '2025-02-08 12:31:17'),
(3, NULL, 'Michael ', 'Golden', 'michaelgolden@gmail.com', 'Box 2234, Blantyre, Namiwawa', '0993485763', 'pending', '2025-02-27 08:46:36'),
(4, NULL, 'Emily', 'Golden', 'emilygolden@gmail.com', 'box 2233, Blantyre, Nyambadwe', '09934567847', 'pending', '2025-03-27 08:46:36'),
(5, NULL, 'Benson', 'Clark', 'bensonclark@gmail.com', 'Box 4321, Blantyre, Chinyonga', '0998485748', 'pending', '2025-04-27 08:46:36'),
(6, NULL, 'Richie', 'Chiwaula', 'rc@gmail.com', 'Zomba, Chikupira, Box 1234', '0885112269', 'pending', '2025-05-08 12:25:37'),
(7, NULL, 'Watson', 'Manda', 'wmanda20@gmail.com', 'BOX 2025 Chilobwe Blantyre', '09939485421', NULL, '2025-07-19 19:34:49'),
(8, NULL, 'Wilson', 'Gondwe', 'willgondwe@gmail.com', 'P.O. Box 8374', '09948572634', NULL, '2025-07-21 06:05:22');

-- --------------------------------------------------------

--
-- Table structure for table `customer_payments`
--

CREATE TABLE `customer_payments` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) NOT NULL,
  `vehicle_id` int(7) NOT NULL,
  `maintenance_id` int(7) NOT NULL,
  `payment_type` enum('airtel money','tnm mpamba','cash','national bank','standard bank','FDH bank') NOT NULL,
  `amount` decimal(20,2) NOT NULL,
  `recipt_number` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_payments`
--

INSERT INTO `customer_payments` (`id`, `customer_id`, `vehicle_id`, `maintenance_id`, `payment_type`, `amount`, `recipt_number`, `date`) VALUES
(1, 1, 1, 1, 'cash', 1100000.00, 'bt2345', '2025-01-08 12:26:57'),
(2, 2, 2, 2, 'national bank', 200000.00, 'cj2345', '2025-02-08 12:30:58'),
(3, 3, 3, 3, 'cash', 400000.00, 'mj8890', '2025-03-01 12:52:14'),
(4, 4, 4, 4, 'national bank', 80000.00, 'er7654', '2025-04-01 12:54:04'),
(5, 6, 6, 6, 'standard bank', 500000.00, 'RC7654', '2025-07-25 17:12:26'),
(6, 8, 8, 8, 'national bank', 300000.00, 'FT2323CDRX\\BNK', '2025-07-25 19:06:25');

-- --------------------------------------------------------

--
-- Table structure for table `error_logs`
--

CREATE TABLE `error_logs` (
  `id` int(7) NOT NULL,
  `event` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `maintenances`
--

CREATE TABLE `maintenances` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) NOT NULL,
  `vehicle_id` int(7) NOT NULL,
  `mechanic_id` int(7) NOT NULL,
  `mileage` int(7) DEFAULT NULL,
  `last_service` date DEFAULT NULL,
  `next_service` date DEFAULT NULL,
  `service_type` enum('Breaking system','Engine service','General service','Body service','Suspension system') NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `parts_used` varchar(255) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `labor_hours` int(3) DEFAULT NULL,
  `completion` int(3) NOT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maintenances`
--

INSERT INTO `maintenances` (`id`, `customer_id`, `vehicle_id`, `mechanic_id`, `mileage`, `last_service`, `next_service`, `service_type`, `description`, `parts_used`, `notes`, `labor_hours`, `completion`, `cost`, `date`) VALUES
(1, 1, 1, 1, 86112, '2025-01-01', '2025-06-01', 'Suspension system', 'Steering wobbling erratically during drive, Tyres worn out due to suspension issues.', NULL, NULL, 3, 0, 1100000.00, '2025-08-06 08:29:37'),
(2, 2, 2, 1, 92345, '2025-03-01', '2025-09-01', '', 'Schedule general service', 'New break pads, 15w-40 oil', NULL, 6, 50, 200000.00, '2025-02-05 10:29:10'),
(3, 3, 3, 1, 113456, '2025-04-01', '2025-10-01', '', 'Due to misalignment, front tires have worn out and need replacement. ', 'Two size 16 tires', NULL, 4, 50, 400000.00, '2025-02-05 10:29:10'),
(4, 4, 4, 1, 60334, '2025-01-01', '2025-06-01', '', 'Requires OBD-II engine scan to identify issue.', 'OBD-II Diagnostics device', NULL, 2, 10, 80000.00, '2025-04-05 10:29:10'),
(5, 5, 5, 1, 100345, '2025-01-01', '2025-06-01', '', 'Pulling reduced due to lack of fuel being sent to the combustion chamber', 'Oil filter, battery N70', NULL, 4, 25, 500000.00, '2025-05-05 10:29:10'),
(6, 6, 6, 3, 87990, NULL, NULL, 'Breaking system', 'Vehicle making sqeeking noise when stopping', NULL, NULL, 4, 0, 150000.00, '2025-07-23 13:14:44'),
(7, 7, 7, 3, 87654, NULL, NULL, 'Body service', 'Paint needs refresh', NULL, NULL, 6, 0, 500000.00, '2025-07-23 19:20:33'),
(8, 8, 8, 4, 65968, NULL, NULL, 'General service', 'Radio needs replacement to Android car play', NULL, NULL, 4, 0, 350000.00, '2025-07-25 18:38:56');

-- --------------------------------------------------------

--
-- Table structure for table `mechanics`
--

CREATE TABLE `mechanics` (
  `id` int(7) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `identification` varchar(255) NOT NULL,
  `certification` varchar(255) NOT NULL,
  `certified_on` date DEFAULT NULL,
  `institute` varchar(255) DEFAULT NULL,
  `skills` varchar(255) NOT NULL,
  `specification` varchar(255) DEFAULT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mechanics`
--

INSERT INTO `mechanics` (`id`, `firstname`, `lastname`, `identification`, `certification`, `certified_on`, `institute`, `skills`, `specification`, `date_registered`) VALUES
(1, 'George', 'Banda', 'VXY1234', 'German Auto Mobiles', '2023-01-06', 'Carl Benz School of Engineering', 'General service on German makes.', 'OBD-II engine diagnostics', '2025-07-17 07:25:38'),
(2, 'Isaac', 'knox', 'BTER34', 'Bachelor in Mechanical Engineering', '2020-01-01', 'Polytechnic Malawi', 'Vehicle repairs', 'Engine Maintenance', '2025-07-17 07:24:50'),
(3, 'Bill', 'Phiri', 'OIDU67', 'Master\'s in engineering', '1999-01-01', 'Polytechnic Malawi', 'General Vehicle repairs', 'Engine repairs', '2025-07-17 07:27:44'),
(4, 'Ongani', 'Banda', 'IUR495', 'Bachelors in Electrical Engineering', '1998-01-01', 'Polytechnic Malawi', 'General Electric repairs', 'Vehicle electric repairs', '2025-07-17 07:30:33'),
(5, 'Kingsley', 'Mponda', 'TT573Y', 'Bachlors in Electric Engineering', '1998-01-01', 'Polytechnic Malawi', 'General Car Electrics', 'OBD2 Scanning', '2025-07-21 10:54:12');

-- --------------------------------------------------------

--
-- Table structure for table `reminders`
--

CREATE TABLE `reminders` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) DEFAULT NULL,
  `reminder_type` enum('Payment','Service','Retreival','Recovery','Maintenance') NOT NULL,
  `description` text DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `vehicle_id` int(7) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `status` enum('incomplete','complete') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reminders`
--

INSERT INTO `reminders` (`id`, `customer_id`, `reminder_type`, `description`, `date`, `vehicle_id`, `due_date`, `status`) VALUES
(1, 1, 'Retreival', 'The customer might be alarmed by the price for the job, make sure they will commit.', '2025-07-05 20:44:10', 1, '2025-06-30', 'incomplete'),
(2, 2, 'Maintenance', 'Remind mechanics to get started with repairs', '2025-06-16 21:00:55', 2, '2025-06-18', 'incomplete'),
(3, 3, 'Maintenance', 'Reminder to mechanics to get started', '2025-06-16 21:02:33', 3, '2025-06-18', 'incomplete'),
(4, 5, 'Payment', 'Customer needs to make downpayment', '2025-07-25 17:04:19', 5, '2025-08-29', 'incomplete'),
(5, 7, 'Payment', 'Customer needs to make down payment', '2025-07-25 17:05:12', 7, '2025-08-29', 'incomplete');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(7) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `date`) VALUES
(1, 'void', '1234', 'admin', '2025-05-15 11:36:37');

-- --------------------------------------------------------

--
-- Table structure for table `user_sessions`
--

CREATE TABLE `user_sessions` (
  `id` int(7) NOT NULL,
  `user_id` int(7) NOT NULL,
  `status` enum('online','offline') DEFAULT NULL,
  `login` time NOT NULL DEFAULT current_timestamp(),
  `logout` time DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) NOT NULL,
  `model` varchar(255) NOT NULL,
  `make` varchar(255) NOT NULL,
  `year` year(4) NOT NULL,
  `reg_number` varchar(255) NOT NULL,
  `vin_number` varchar(255) NOT NULL,
  `transmission` enum('manual','automatic','','') NOT NULL,
  `color` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `customer_id`, `model`, `make`, `year`, `reg_number`, `vin_number`, `transmission`, `color`, `date`) VALUES
(1, 1, 'Dualis', 'Nissan', '2010', 'BT3321', '', 'automatic', 'Beige', '2025-06-15 22:05:19'),
(2, 2, 'Hulux', 'Toyota', '2010', 'MN2345', '', 'manual', 'White', '2025-06-15 22:05:19'),
(3, 3, 'Belta', 'Toyota', '2012', 'TH3456', '', 'automatic', 'Brown', '2025-06-15 22:05:19'),
(4, 4, 'Tiguan', 'Volkswagen', '2016', 'MG4432', '', 'automatic', 'Silver', '2025-06-15 22:05:19'),
(5, 5, 'E250', 'Mercedes', '2012', 'SC213H', '', 'automatic', 'Black', '2025-06-15 22:05:19'),
(6, 6, 'Note', 'Nissan', '2012', 'RC0023', '84URYT47EYRU', 'automatic', 'Black', '2025-07-21 11:51:23'),
(7, 7, 'Axio', 'Toyota', '2012', 'TH8876', 'RYT4857TYEU5', 'manual', 'Silver', '2025-07-23 19:19:25'),
(8, 8, 'Demio', 'Mazda', '2012', 'MW3943', 'FG3746RTY738', 'automatic', 'Blue', '2025-07-25 18:36:32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `customer_payments`
--
ALTER TABLE `customer_payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `maintenance_id` (`maintenance_id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `error_logs`
--
ALTER TABLE `error_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `maintenances`
--
ALTER TABLE `maintenances`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customers_id` (`customer_id`),
  ADD KEY `vehicle_id` (`vehicle_id`),
  ADD KEY `mechanic_id` (`mechanic_id`);

--
-- Indexes for table `mechanics`
--
ALTER TABLE `mechanics`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reminders`
--
ALTER TABLE `reminders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `fk_vehicle_id` (`vehicle_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_sessions`
--
ALTER TABLE `user_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `customer_payments`
--
ALTER TABLE `customer_payments`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `error_logs`
--
ALTER TABLE `error_logs`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `maintenances`
--
ALTER TABLE `maintenances`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `mechanics`
--
ALTER TABLE `mechanics`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reminders`
--
ALTER TABLE `reminders`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user_sessions`
--
ALTER TABLE `user_sessions`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customers`
--
ALTER TABLE `customers`
  ADD CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `customer_payments`
--
ALTER TABLE `customer_payments`
  ADD CONSTRAINT `customer_payments_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `customer_payments_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`),
  ADD CONSTRAINT `customer_payments_ibfk_3` FOREIGN KEY (`maintenance_id`) REFERENCES `maintenances` (`id`),
  ADD CONSTRAINT `customer_payments_ibfk_4` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`);

--
-- Constraints for table `maintenances`
--
ALTER TABLE `maintenances`
  ADD CONSTRAINT `maintenances_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `maintenances_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`),
  ADD CONSTRAINT `maintenances_ibfk_3` FOREIGN KEY (`mechanic_id`) REFERENCES `mechanics` (`id`);

--
-- Constraints for table `reminders`
--
ALTER TABLE `reminders`
  ADD CONSTRAINT `fk_vehicle_id` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`),
  ADD CONSTRAINT `reminders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);

--
-- Constraints for table `user_sessions`
--
ALTER TABLE `user_sessions`
  ADD CONSTRAINT `user_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
