# Kit Boy Auto Solution
Kit Boy Auto Solution Digitizes and centralizes workshop operations by replacing manual and error-prone processes with a unified digital system.
Improve communication by ensuring timely and automated updates to both customers and workshop staff.
Enhance customer experience by enabling transparency, progress tracking, and service history management.
Support executive decision-making by providing dashboards and reports showing workshop efficiency, job completion rate, and payment records.
Secure and streamline financial records by reducing dependency on Excel and cashbooks, minimize data loss and improve auditability.
Introduce proactive service reminders by reducing missed services or updates through scheduled and automated notifications.
Enable accountability and traceability by logging all actions, mechanics' responsibilities, and customer approvals.

# Aim
Kit Boy is a comprehensive vehicle service management system designed to streamline crash recovery, maintenance tracking, customer communication, and payment processing, while providing real-time updates and performance insights to both customers and workshop executives.

# What Kit Boy will do
1.	Record and manage crash recovery cases by allowing service workers to log incidents and dispatch recovery vehicles.
2.	Track vehicle maintenance activities, from initial diagnosis to task assignment and completion.
3.	Update customers automatically with real-time progress reports via email, or a dashboard interface.
4.	Maintain detailed records for all registered vehicles, mechanics, and customers.
5.	Support payment management by recording transactions, generating invoices, and tracking balances.
6.	Provide role-based access for different users (admins, mechanics, service workers, and executives).
7.	Send scheduled reminders to customers for maintenance follow-ups and to mechanics for pending tasks.
8.	Generate executive reports and dashboards showing workshop performance, revenue, and workload metrics.

# What Kit Boy will not do
1.	Provide live GPS tracking or telematics integration for vehicles in transit or during recovery (not within current scope).
2.	Handle spare parts inventory management in detail (stock levels, suppliers, restocking alerts are outside the current phase).
3.	Include mobile apps (this version is focused on desktop or web-based systems; mobile app may be considered in future iterations).
4.	Integrate with third-party payment gateways or banks (payment is recorded manually in the system, not processed online).
5.	Offer voice or video communication features (all updates are text-based notifications).
6.	Automate complex diagnostic processes — mechanic input is required for all inspections and assessments.

# Tools for Development
1.	Programming Language: Python — used for the back-end logic and desktop GUI (Python Software Foundation, 2024).
2.	Programming Language: PHP and JavaScript, offering cross-platform support and rapid project development (PHP, 2024).
3.	Scripting Language: HTML, CSS, Bootstrap – For designing web site interface for customers (W3schools, 2025).
4.	Database: MySQL — chosen for its reliability, performance, and support for relational data models needed to manage users, vehicles, and maintenance records (DuBois, 2023).
5.	GUI Library: CustomTkinter — enables a modern, user-friendly desktop interface for python GUI building (Schimansky, 2024).
6.	IDE: Visual Studio Code — selected for its extensive plugin support, version control integration, and lightweight performance (Microsoft, 2024).
7.	Design Tools: Star UML for ERD and system diagrams, and Figma for interface prototyping (StarUML, 2024).
8.	Version Control: Git — used to manage codebase revisions, enable team collaboration, and track changes (Git SCM, 2024).

# Hardware requirements
<table>
  <tr>
    <th>Resource</th>
    <th>Specification</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>Developer Workstations</td>
    <td>Minimum: Intel Core i3, 4GB RAM, 128GB SSD</td>
    <td>For development and testing of the system by programmers and UI designers.</td>
  </tr>
  <tr>
    <td>Server Machine (if hosting web version or central DB)</td>
    <td>Minimum: Intel Core i7, 16GB RAM, 1TB HDD/SSD</td>
    <td>Hosts MySQL database and central services for multi-user access in a networked environment.</td>
  </tr>
  <tr>
    <td>Client Machines</td>
    <td>Minimum: Intel Core i3, 4GB RAM, Windows 10+</td>
    <td>For use by mechanics, admins, and service workers to access the system interface.</td>
  </tr>
  <tr>
    <td>Backup Device/External Storage</td>
    <td>500GB+ external drive or NAS</td>
    <td>Regular backups of customer, maintenance, and payment data for data recovery.</td>
  </tr>
  <tr>
    <td>Printer/Scanner</td>
    <td>Any standard model</td>
    <td>To print invoices, maintenance reports, and scan signed customer documents.</td>
  </tr>
</table>

# Functional Requirements
These are the main features that system must be able to do and without them, the system is not fully complete and capable to perform effectively and efficiently.
1.	User Authentication: 
Kit boy must support login/logout of multiple users such as Admin, Mechanic, Receptionist and Customer followed by role-based controls to regulate access.
  - Admins manage users and configurations
  - Mechanics can log vehicle diagnoses, fixes and used resources
2.	Receptionist handles customer check-in/out, communication
3.	Customer Management
Add, edit and delete customer records. Customer Management: 
Add, edit and delete customer records. Link customer to one or more vehicles, Store customer communication preference (SMS or email). Ability to flag VIP or frequent customers.
4.	Vehicle Management: Add
The system must be able to add, edit and delete vehicle records like make, model, year of make, engine type, VIN/Chassis number, license plate. View full maintenance history for vehicle. Store mileage and last service date.
5.	Maintenance & Repair Logging
Mechanics can log: Symptoms described by customer, diagnosis (OBD2 or API), actions taken, fixes performed. Maintenance & Repair Logging: 
Mechanics can log: Symptoms described by customer, diagnosis (OBD2 or API), actions taken, fixes performed. Parts, resources used and their cost. Time takes to complete work. Attachment documents or photos of damaged or purchased parts. Track work status: Pending – In progress – Completed – Picked Up.
6.	Assistive Diagnostics (AI API Integration): )
Accept natural language symptom input, send input to 3rd party API (Hugging Face). (Face, 2025)). Receive and display and display suggested diagnoses to the mechanic. Log both the input and AI-suggested output for reference.
7.	Customer Notification
Notify customer when their vehicle is ready for pickup, upcoming or due maintenance is near. Customer Notification: 
Notify customer when their vehicle is ready for pickup, upcoming or due maintenance is near. Notification channels (Email, SMS)
8.	Reminders and Alerts
System tracks, due maintenance intervals (based on mileage or time), pick-up reminders for completed jobs. Reminders and Alerts: 
System tracks, due maintenance intervals (based on mileage or time), pick-up reminders for completed jobs. System can send internal alerts to staff such as a particular vehicle is overdue by 3 days, it can remind customer that its time to service their car. Dashboard widget showing current reminders.
9.	Reports & Analytics
Daily and Monthly summary of vehicles service, revenue generated, parts used and inventory used. Reports & Analytics:  
Daily and Monthly summary of vehicles service, revenue generated, parts used and inventory used. Customer and vehicle maintenance history reports. Export data to CSV or PDF.
10.	Database & Backup Management
Store all records securely in a relational database (MySQL), routine backups (automated or manual), admin tool to restore from a backup when required. Database & Backup Management: 
Store all records securely in a relational database (MySQL), routine backups (automated or manual), admin tool to restore from a backup when required.
11.	Future features
Customer self-service portal to view maintenance history and book appointments. Future features: 
Customer self-service portal to view maintenance history and book appointments. Inventory and parts managements, KYC compliance for customer such as national ID and profile setup. Integration with OBD scanner via USB/Bluetooth for future automation.
