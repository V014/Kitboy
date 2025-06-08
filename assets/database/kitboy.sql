-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 08, 2025 at 02:37 PM
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
-- Table structure for table `company_payments`
--

CREATE TABLE `company_payments` (
  `id` int(7) NOT NULL,
  `description` varchar(255) NOT NULL,
  `to` varchar(255) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(7) NOT NULL,
  `user_id` int(7) DEFAULT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `payment_status` enum('complete','pending','incomplete') NOT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `user_id`, `firstname`, `lastname`, `email`, `address`, `contact`, `payment_status`, `date_registered`) VALUES
(1, NULL, 'Wanga', 'Kanjala', 'wangakanjala@gmail.com', 'box 1738, Blantyre, Chilomoni Fargo', '0996335639', 'complete', '2025-06-08 12:28:52'),
(2, NULL, 'Emmanuel', 'Chinyanja', 'emkach@gmail.com', 'Box 1234, Blantyre, Chilobwe', '0987425369', 'complete', '2025-06-08 12:31:17'),
(3, NULL, 'Michael ', 'Golden', 'michaelgolden@gmail.com', 'Box 2234, Blantyre, Namiwawa', '0993485763', 'pending', '2025-05-27 08:46:36'),
(4, NULL, 'Emily', 'Golden', 'emilygolden@gmail.com', 'box 2233, Blantyre, Nyambadwe', '09934567847', 'pending', '2025-05-27 08:46:36'),
(5, NULL, 'Benson', 'Clark', 'bensonclark@gmail.com', 'Box 4321, Blantyre, Chinyonga', '0998485748', 'pending', '2025-05-27 08:46:36'),
(6, NULL, 'Richie', 'Chiwaula', 'rc@gmail.com', 'Zomba, Chikupira, Box 1234', '0885112269', 'pending', '2025-06-08 12:25:37');

-- --------------------------------------------------------

--
-- Table structure for table `customer_payments`
--

CREATE TABLE `customer_payments` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) NOT NULL,
  `vehicle_id` int(7) NOT NULL,
  `maintenance_id` int(7) NOT NULL,
  `method` enum('airtel money','tnm mpamba','cash','national bank','standard bank') NOT NULL,
  `amount` decimal(20,2) NOT NULL,
  `recipt_number` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer_payments`
--

INSERT INTO `customer_payments` (`id`, `customer_id`, `vehicle_id`, `maintenance_id`, `method`, `amount`, `recipt_number`, `date`) VALUES
(1, 1, 1, 1, 'cash', 1100000.00, 'bt2345', '2025-06-08 12:26:57'),
(2, 2, 2, 2, 'national bank', 200000.00, 'cj2345', '2025-06-08 12:30:58');

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
  `customers_id` int(7) NOT NULL,
  `vehicle_id` int(7) NOT NULL,
  `mechanic_id` int(7) NOT NULL,
  `reg_number` varchar(255) NOT NULL,
  `mileage` int(7) NOT NULL,
  `last_service` date DEFAULT NULL,
  `next_service` date DEFAULT NULL,
  `service_type` varchar(255) NOT NULL,
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

INSERT INTO `maintenances` (`id`, `customers_id`, `vehicle_id`, `mechanic_id`, `reg_number`, `mileage`, `last_service`, `next_service`, `service_type`, `description`, `parts_used`, `notes`, `labor_hours`, `completion`, `cost`, `date`) VALUES
(1, 1, 1, 1, 'BT3321', 86112, '2025-01-01', '2025-06-01', 'Suspension over hall, wheel alignment', 'Steering wobbling erratically during drive, Tyres worn out due to suspension issues.', NULL, NULL, NULL, 0, 1100000.00, '2025-06-05 10:29:10'),
(2, 2, 2, 1, 'MN2345', 92345, '2025-03-01', '2025-09-01', 'Oil change, break change, wheel alignment', 'Schedule general service', 'New break pads, 15w-40 oil', NULL, 6, 50, 200000.00, '2025-06-05 10:29:10'),
(3, 3, 3, 1, 'TH3456', 113456, '2025-04-01', '2025-10-01', 'Wheel alignment, tire replacement', 'Due to misalignment, front tires have worn out and need replacement. ', 'Two size 16 tires', NULL, 4, 50, 400000.00, '2025-06-05 10:29:10'),
(4, 4, 4, 1, 'MG 4432', 60334, '2025-01-01', '2025-06-01', 'Engine Misfire', 'Requires OBD-II engine scan to identify issue.', 'OBD-II Diagnostics device', NULL, 2, 10, 80000.00, '2025-06-05 10:29:10'),
(5, 5, 5, 1, 'SC 213H', 100345, '2025-01-01', '2025-06-01', 'Battery change and oil pump change', 'Pulling reduced due to lack of fuel being sent to the combustion chamber', 'Oil filter, battery N70', NULL, 4, 25, 500000.00, '2025-06-05 10:29:10');

-- --------------------------------------------------------

--
-- Table structure for table `mechanics`
--

CREATE TABLE `mechanics` (
  `id` int(7) NOT NULL,
  `fisrtname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `identification` varchar(255) NOT NULL,
  `certification` varchar(255) NOT NULL,
  `certified_on` date DEFAULT NULL,
  `certification_institute` varchar(255) DEFAULT NULL,
  `skills` varchar(255) NOT NULL,
  `specification` varchar(255) DEFAULT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mechanics`
--

INSERT INTO `mechanics` (`id`, `fisrtname`, `lastname`, `identification`, `certification`, `certified_on`, `certification_institute`, `skills`, `specification`, `date_registered`) VALUES
(1, 'George', 'Banda', 'VXY1234', 'German Auto Mobiles', '2023-01-06', 'Carl Benz School of Engineering', 'General service on German brands such as: Audi, BMW, Mercedes-Benz, Porsche, Volkswagen. OBD-II engine diagnostics and error code handling. Suspension and head gasket repair.', 'OBD-II engine diagnostics and error code handling.', '2025-05-18 16:35:06');

-- --------------------------------------------------------

--
-- Table structure for table `reminders`
--

CREATE TABLE `reminders` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `vehicle_id` int(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reminders`
--

INSERT INTO `reminders` (`id`, `customer_id`, `title`, `description`, `date`, `vehicle_id`) VALUES
(1, 1, 'Communicate with client to accept job.', 'The customer might be alarmed by the price for the job, make sure they will commit.', '2025-05-20 13:34:17', 1);

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
  `login_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `logout_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int(7) NOT NULL,
  `customer_id` int(7) NOT NULL,
  `name` varchar(255) NOT NULL,
  `brand` varchar(255) NOT NULL,
  `year_of_make` int(4) NOT NULL,
  `transmission` enum('manual','automatic','','') NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `customer_id`, `name`, `brand`, `year_of_make`, `transmission`, `date`) VALUES
(1, 1, 'Dualis', 'Nissan', 2010, 'automatic', '2025-05-18 16:43:38'),
(2, 2, 'Hulux', 'Toyota', 2010, 'manual', '2025-05-20 08:37:16'),
(3, 3, 'Belta', 'Toyota', 2012, 'automatic', '2025-05-20 08:37:58'),
(4, 4, 'Tiguan', 'Volkswagen', 2016, 'automatic', '2025-05-20 08:39:04'),
(5, 5, 'E250', 'Mercedes', 2012, 'automatic', '2025-05-20 08:39:37');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `company_payments`
--
ALTER TABLE `company_payments`
  ADD PRIMARY KEY (`id`);

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
  ADD KEY `customers_id` (`customers_id`),
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
-- AUTO_INCREMENT for table `company_payments`
--
ALTER TABLE `company_payments`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `customer_payments`
--
ALTER TABLE `customer_payments`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `error_logs`
--
ALTER TABLE `error_logs`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `maintenances`
--
ALTER TABLE `maintenances`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `mechanics`
--
ALTER TABLE `mechanics`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reminders`
--
ALTER TABLE `reminders`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
  ADD CONSTRAINT `maintenances_ibfk_1` FOREIGN KEY (`customers_id`) REFERENCES `customers` (`id`),
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
