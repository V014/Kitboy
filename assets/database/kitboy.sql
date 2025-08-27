-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 27, 2025 at 10:12 PM
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
(1, 1, 1, 1, 86112, '2025-01-01', '2025-06-01', 'Suspension system', 'A diagnosis is showing a p0776, the vehicle is sticking to gear 1 and at a limited speed of about 60km/h', NULL, 'Okay, P0776 on a Nissan Dualis (Qashqai in some markets) with a stuck-in-first-gear issue at a 60km/h speed limit points strongly towards a problem within the automatic transmission\'s shift solenoids or the related valve body.  The code specifically indicates a problem with the shift solenoid \'B\' circuit.  This solenoid is responsible for controlling the shifting between gears.\n\nHere\'s my diagnostic and repair plan:\n\n**Phase 1: Verification and Further Diagnosis**\n\n1. **Confirm the Code:** First, I\'ll need to independently verify the P0776 code using my own diagnostic scanner.  Sometimes codes can be misread or there might be a secondary code lurking that offers more insight.\n2. **Transmission Fluid Check:** I\'ll check the transmission fluid level and condition. Low fluid, burnt fluid (smells burnt or looks dark brown), or contaminated fluid all point to internal transmission damage, which is a serious issue.  I\'ll note the colour and consistency.\n3. **Fluid Temperature Check:**  A high transmission fluid temperature can also contribute to shifting problems. I\'ll check this with a specialized thermometer or using the diagnostic scanner if that capability is available.\n4. **Road Test (carefully):** A short, controlled road test will be necessary to confirm the symptoms. I’ll pay close attention to the transmission\'s behaviour, including any unusual noises (whining, clunking) or vibrations.\n5. **Electrical Checks:**  I\'ll inspect the wiring harness and connectors associated with the transmission shift solenoids for any signs of damage, corrosion, or loose connections.  A visual inspection, followed by a continuity test with a multimeter, will be done.\n\n**Phase 2: Potential Repairs (based on Phase 1 findings)**\n\nDepending on the findings from Phase 1, the repair could range from simple to complex:\n\n* **Solenoid Replacement (Most Likely):**  If the wiring is good and the fluid is okay, the most probable cause is a faulty shift solenoid B.  Replacing this solenoid is relatively straightforward, though it may require some specialized tools to access it within the transmission valve body.\n* **Valve Body Repair/Replacement:**  If multiple solenoids are faulty or there are other issues within the valve body (internal leaks, wear), a valve body repair or replacement might be necessary. This is a more involved repair.\n* **Transmission Fluid Change:** A complete transmission fluid and filter change is advisable regardless of the primary issue, as contaminated fluid can exacerbate problems.\n* **Internal Transmission Damage:** In the worst-case scenario, internal damage to the transmission (worn clutches, planetary gear problems) could be the root cause.  This would require a full transmission rebuild or replacement, which is a significant undertaking and costly.\n\n\n**Important Note:**  I need to carefully consider the mileage and age of the vehicle before recommending a full transmission rebuild.  The cost of that repair may outweigh the vehicle\'s value.  I will discuss the various repair options and their associated costs with the owner before proceeding.\n\nThis is my preliminary assessment.  Further investigation is needed to pinpoint the exact cause and determine the most appropriate and cost-effective repair.', 3, 0, 1100000.00, '2025-08-27 09:08:24'),
(2, 2, 2, 1, 92345, '2025-03-01', '2025-09-01', '', 'Schedule general service', 'New break pads, 15w-40 oil', NULL, 6, 50, 200000.00, '2025-02-05 10:29:10'),
(3, 3, 3, 1, 113456, '2025-04-01', '2025-10-01', '', 'Due to misalignment, front tires have worn out and need replacement. ', 'Two size 16 tires', 'Alright, let\'s get this Belta sorted.  113,456 miles is a decent amount of driving, and with the front tire wear due to misalignment, it\'s time for some attention.\n\n**Here\'s my plan of action:**\n\n1. **Wheel Alignment Check and Adjustment:** Before ordering new tires, we absolutely *must* get a proper wheel alignment.  The misalignment is the root cause of the premature tire wear, and replacing the tires without fixing this will just lead to the same problem repeating.  I\'ll need to check the caster, camber, and toe angles and adjust them to the manufacturer\'s specifications using the alignment machine.\n\n2. **Tire Selection & Installation:** Once the alignment is perfect, we can proceed with selecting and installing replacement front tires. I\'ll need to know the customer\'s preference on tire brand, type (all-season, summer, winter, etc.), and speed rating.  I\'ll also ensure the correct tire size is used, matching the specifications found on the driver\'s side door jamb or the owner\'s manual.  After installation, we\'ll perform a final balance check on each tire to eliminate vibrations.\n\n3. **Tire Rotation (if needed):**  Depending on the customer\'s tire history and preference, rotating the rear tires to the front might be recommended.  This will even out tire wear. However, given the front tires are worn out due to misalignment, and assuming the rears are in good condition, a full rotation might not be the most cost-effective option right now, but I\'ll discuss this with the customer.\n\n4. **Inspection of Suspension Components:** While I\'m at it, I\'ll also perform a visual inspection of the suspension components – ball joints, tie rod ends, etc. – to check for any signs of wear or damage that could have contributed to the misalignment.  Any significant issues will need to be reported and addressed before the car leaves the workshop.\n\n5. **Post-Alignment Test Drive:** After the alignment and tire replacement, a short test drive is essential to ensure the alignment is correct and that the vehicle handles properly.\n\n**Parts Needed:**\n\n* Two new front tires (size to be determined based on vehicle specifications and customer preference)\n* Wheel balancing weights (as needed)\n\n\nThis should get the Toyota Belta back on the road safely and efficiently.  I\'ll keep you updated on the progress.', 4, 50, 400000.00, '2025-08-25 13:05:27'),
(4, 4, 4, 1, 60334, '2025-01-01', '2025-06-01', 'Engine service', 'Requires OBD-II engine scan to identify issue. The car keeps showing the check engine light and fails to pull on up hills', 'OBD-II Diagnostics device', 'Okay, I\'ve got a Volkswagen Tiguan in the bay with a check engine light and hill climbing issues.  Mileage is 60,334, last serviced on January 1st, 2025.  Since we need an OBD-II scan to identify the problem, let\'s get that done first.\n\n**Procedure:**\n\n1. **Connect OBD-II Scanner:** Plug the OBD-II scanner into the Tiguan\'s diagnostic port (usually located under the dashboard).  Make sure to select the correct vehicle make, model, and year in the scanner\'s settings.\n2. **Retrieve Diagnostic Trouble Codes (DTCs):**  Run a full scan and record all DTCs. Note any freeze frame data associated with each code.  This data provides a snapshot of the engine\'s conditions when the code was set.\n3. **Interpret DTCs:**  Look up the DTCs using a reliable database or repair manual specific to the Volkswagen Tiguan.  This will give us a description of the potential problem.\n4. **Visual Inspection:** Based on the DTCs, we may need to visually inspect specific components.  This might include checking:\n    * **Spark plugs and ignition coils:**  Misfires are a common cause of poor hill climbing ability and can trigger a check engine light.\n    * **Air filter:** A clogged air filter restricts airflow, reducing engine power.\n    * **Mass airflow sensor (MAF sensor):** A faulty MAF sensor can lead to incorrect fuel metering, impacting performance.\n    * **Fuel filter:** A clogged fuel filter can restrict fuel flow, causing poor performance.\n    * **Exhaust system:**  Check for leaks or blockages which could restrict exhaust flow.\n    * **Vacuum hoses:** Inspect vacuum hoses for cracks or leaks.\n5. **Further Diagnostic Tests:**  Depending on the DTCs and visual inspection, we might need to perform additional tests, such as:\n    * **Fuel pressure test:** To check fuel delivery.\n    * **Compression test:** To assess engine cylinder health.\n    * **Sensor testing:** To check the functionality of various sensors (e.g., oxygen sensor, camshaft sensor).\n6. **Report Findings & Recommendation:** Once the root cause is identified, I will prepare a report detailing the diagnostic findings, the likely cause of the problem, and a repair recommendation, including parts and labor costs.\n\n**Preliminary Thoughts (based on limited information):**\n\nThe combination of a check engine light and difficulty climbing hills suggests a potential problem with engine performance.  Possible causes could include issues with the ignition system, fuel delivery system, air intake system, or a more serious engine problem. The OBD-II scan is crucial to narrow down the possibilities.', 6, 10, 380000.00, '2025-08-14 13:02:22'),
(5, 5, 5, 1, 100345, '2025-01-01', '2025-06-01', '', 'Pulling reduced due to lack of fuel being sent to the combustion chamber', 'Oil filter, battery N70', 'Okay, a Mercedes E250 with reduced power due to insufficient fuel reaching the combustion chamber.  100,345 miles isn\'t excessively high, but it\'s time for a thorough investigation.  Since the last service was fairly recent,  it\'s less likely to be a simple maintenance issue, though we should rule that out first.\n\nHere\'s my diagnostic plan:\n\n**Phase 1:  Quick Checks (under 30 minutes)**\n\n1. **Fuel Level:**  Sounds obvious, but let\'s confirm the fuel tank isn\'t simply empty.\n2. **Fuel Pressure:**  We need to check the fuel rail pressure. Low pressure points to a problem in the fuel pump, filter, pressure regulator, or even a leak in the fuel lines.  This requires a fuel pressure gauge.\n3. **Fuel Pump Relay:**  A quick check to see if the pump is even receiving power.  We can do this with a multimeter.\n4. **Visual Inspection:**  A quick look around the fuel system for any obvious leaks or damage.\n\n\n**Phase 2:  More In-Depth Diagnostics (1-2 hours)**\n\n1. **Fuel Filter:**  Even if the service was recent, a clogged fuel filter can significantly restrict fuel flow. Replacement is relatively straightforward.\n2. **Fuel Pump:**  If the pressure is low, we\'ll need to test the fuel pump itself. This might involve testing its output directly or listening for its operation.  A faulty pump is a common cause.\n3. **Mass Airflow Sensor (MAF):**  A faulty MAF sensor can give incorrect readings, leading the engine to receive less fuel than needed.  Cleaning or replacing this sensor is a possibility.\n4. **Throttle Position Sensor (TPS):**  Similar to the MAF, a faulty TPS can affect fuel delivery.\n5. **Fuel Injectors:**  Low fuel delivery to the combustion chamber could indicate faulty injectors that aren\'t spraying fuel properly.  This requires a more specialized test, possibly using an injector tester.\n\n\n**Phase 3:  Advanced Diagnostics (if needed)**\n\n1. **Computer Diagnostics:**  A full scan of the engine control unit (ECU) using a Mercedes-Benz diagnostic tool is essential.  This will reveal any stored trouble codes (DTCs) which can pinpoint the problem area.\n2. **Fuel Pressure Regulator:**  A faulty regulator can cause inconsistent fuel pressure.\n3. **Fuel Lines & Connections:**  A thorough inspection for leaks or blockages in the fuel lines.\n\n\n**Possible Causes (in order of likelihood based on the description):**\n\n1. **Clogged Fuel Filter:**  Most likely if the car is otherwise running normally.\n2. **Faulty Fuel Pump:**  A common issue causing low fuel pressure.\n3. **Faulty Fuel Injectors:**  Less likely, but possible.\n4. **Sensor Issues (MAF, TPS):**  Could contribute but usually lead to other symptoms.\n5. **Fuel Pressure Regulator:**  Less common, but still possible.\n\n\nI\'ll begin with Phase 1.  Let me know if you have any specific tools or diagnostic equipment available.  Once we\'ve completed Phase 1, I\'ll advise on the next steps.', 4, 25, 500000.00, '2025-08-25 13:12:03'),
(6, 6, 6, 3, 87990, NULL, NULL, 'Breaking system', 'Vehicle making sqeeking noise when stopping', NULL, NULL, 4, 0, 150000.00, '2025-07-23 13:14:44'),
(7, 7, 7, 3, 87654, NULL, NULL, 'Body service', 'Paint needs refresh', NULL, NULL, 6, 0, 500000.00, '2025-07-23 19:20:33'),
(8, 8, 8, 4, 65968, NULL, NULL, 'General service', 'Radio needs replacement to Android car play', NULL, 'Okay, got it.  We need to replace the factory radio in a Mazda Demio with a new unit that supports Android Auto.  Before we order parts, we need to gather some more information:\n\n1. **Year of Manufacture:**  Knowing the year will help determine the correct radio size and wiring harness compatibility.  A quick VIN check should help establish this.\n\n2. **Existing Radio Model:**  If possible, finding the model number of the current radio will help identify the correct replacement size and ensure compatibility with the existing wiring.  This info might be on a sticker on the radio itself.\n\n3. **Specific Android Auto Requirements:** Do they want a specific brand or features (e.g., screen size, navigation, etc.)?  This will influence the price and availability of options.\n\n4. **Steering Wheel Controls:** Do they want to retain the use of steering wheel controls? If so, we\'ll need a harness to integrate the new radio.\n\n5. **Budget:**  Knowing their budget will allow me to suggest appropriate units.  There\'s a vast price range for Android Auto radios.\n\nOnce I have this information, I can:\n\n* **Source a compatible replacement radio:** I\'ll check for reputable brands and compatibility.\n* **Identify the necessary installation components:** This may include a wiring harness, antenna adapter, and potentially a fascia panel (depending on the new radio\'s size and design).\n* **Provide a time estimate for the job:**  This will depend on the complexity of the installation and any unforeseen issues.\n* **Provide a total cost estimate:**  This will include the cost of parts and labor.\n\nLet\'s get that VIN number and some more detail on their preferences.', 4, 0, 350000.00, '2025-08-14 08:22:32');

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
(1, 1, 'Payment', 'The customer might be alarmed by the price for the job, make sure they will commit and send the money', '2025-08-22 06:12:01', 1, '2025-06-30', 'incomplete'),
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
(1, 1, 'Dualis', 'Nissan', '2010', 'BT3321', '89DDJVH49GTY', 'automatic', 'Beige', '2025-08-18 19:59:07'),
(2, 2, 'Hulux', 'Toyota', '2010', 'MN2345', '', 'manual', 'White', '2025-06-15 22:05:19'),
(3, 3, 'Belta', 'Toyota', '2012', 'TH3456', '', 'automatic', 'Brown', '2025-06-15 22:05:19'),
(4, 4, 'Tiguan', 'Volkswagen', '2016', 'MG4432', '', 'automatic', 'Silver', '2025-06-15 22:05:19'),
(5, 5, 'E250', 'Mercedes', '2012', 'SC213H', '', 'automatic', 'Black', '2025-06-15 22:05:19'),
(6, 6, 'Note', 'Nissan', '2012', 'RC0023', '84URYT47EYRU', 'automatic', 'Black', '2025-07-21 11:51:23'),
(7, 7, 'Axio', 'Toyota', '2012', 'TH8876', 'RYT4857TYEU5', 'manual', 'Silver', '2025-07-23 19:19:25'),
(8, 8, 'Demio', 'Mazda', '2012', 'MW3943', 'FG3746RTY738', 'automatic', 'Blue', '2025-07-25 18:36:32'),
(10, 1, 'Dualis', 'Nissan', '2010', 'BT3321', '89DDJVH49GJX', 'automatic', 'Beige', '2025-08-18 19:51:27'),
(11, 1, 'Dualis', 'Nissan', '2010', 'BT3321', '89DDJVH49GTY', 'automatic', 'Beige', '2025-08-18 19:51:41');

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
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

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
