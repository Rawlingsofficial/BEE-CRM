# Bee Mobility CRM Project

## Comprehensive Overview
The Bee Mobility CRM is an interactive, user-friendly platform designed to streamline customer service operations, manage knowledge base content, and track customer interactions efficiently. Hosted without the need for user login credentials, anyone with the access link can use the CRM system, ensuring quick, easy access for the customer service team. This platform is built with **Streamlit** for a responsive web-based interface, with **Bootstrap** styling for a sleek, modern design.

The CRM provides multiple sections for managing customer interactions, editing the knowledge base, and reviewing important metrics, all within a centralized dashboard. By offering real-time data updates, editable knowledge base entries, and an intuitive interface, the Bee Mobility CRM improves team efficiency and enhances the overall customer support experience.

---

## Key Features

### 1. Knowledge Base Management
- **Search and Filter**: Staff can search and filter knowledge base entries using keywords from the question or answer fields. Filters allow categorization of the entries, which makes it easier to find relevant responses.
- **Editable Knowledge Base**: Authorized staff can add new questions and answers to the knowledge base or edit existing entries. This functionality ensures that customer service responses remain up-to-date and relevant.
- **Delete Questions**: Staff members can delete outdated or irrelevant questions from the knowledge base. A simple form-based interface allows for easy deletion.

### 2. Logging Customer Interactions
- **Interaction Logging**: Customer service staff can log customer interactions by inputting details such as customer name, contact information, query, and resolution status.
- **Suggested Resolution**: The CRM system automatically suggests resolutions based on keywords from the query entered, providing a faster response for common inquiries.
- **Manual Resolution Entry**: If no suggested resolution is found, staff can manually enter a resolution. Interaction logs include a 'status' field to track the progress of each case (e.g., 'Pending', 'Resolved', 'Escalated').
- **Display of Logged Interactions**: All logged interactions are displayed in a table format within the CRM, giving staff visibility into previous customer interactions and case statuses.

### 3. Managing Interactions
- **Interaction Filters**: Customer service staff can filter interactions based on customer name, contact information, and status, making it easier to find specific cases or track unresolved interactions.
- **Edit Existing Interactions**: Staff can edit interaction details, including status and category. This feature allows for easy updates to logged interactions, ensuring that customer records remain accurate and up-to-date.
- **Track Interaction Status**: The CRM offers a real-time view of customer interactions, showing their status (e.g., 'Pending', 'Resolved', 'Escalated'), helping staff prioritize tasks effectively.

### 4. Analytics Dashboard
- **Status Metrics**: The dashboard provides an overview of the number of interactions in each status (e.g., 'Resolved', 'Escalated', 'Pending'), helping management monitor the performance of customer service teams.
- **Category Breakdown**: Analytics break down interactions by category (e.g., 'Mobility Complaints', 'Financing Issues', 'Incident Records'), providing insights into the most frequent types of customer inquiries.
- **Export Data**: Admin users can export interaction data to an Excel file for further analysis or record-keeping, making it easy to analyze CRM data outside of the platform.

### 5. Excel Integration
- **Data Export**: The CRM system allows for exporting logged interactions to an Excel file, which can be used for reporting or further analysis.
- **Excel File Creation**: If the interactions data does not already exist in an Excel file, the system will automatically create the file, ensuring data persistence in an accessible format.
- **Writing to Excel**: Data from interactions is saved to an Excel file, making it easy to track customer service activity over time and maintain a record of past queries and resolutions.

### 6. User Interface
- **Responsive Design**: The CRM system is built using Streamlit with Bootstrap integration, ensuring that the interface is responsive and accessible on all devices, including desktops, tablets, and smartphones.
- **Clean Layout**: The CRM is designed with a user-friendly layout that minimizes complexity and enhances user experience. Important sections such as 'Knowledge Base', 'Interactions', and 'Analytics' are clearly labeled and easy to navigate.

### 7. Security and Access Control
- While the CRM does not require login credentials, access to sensitive administrative functions, such as editing the knowledge base or exporting data, is limited to authorized users.
- The system ensures that only designated users can make changes to the knowledge base, preventing unauthorized edits and ensuring content accuracy.

### 8. Real-Time Updates
- The CRM updates in real-time, meaning any changes made to interactions or the knowledge base are immediately visible to all users accessing the platform. This feature ensures that all team members are on the same page and can access the most current information at all times.

### 9. Data Protection
- **Data Encryption**: The CRM uses secure connections to ensure that all customer data entered into the system is protected.
- **Privacy**: Sensitive customer information is handled with care, and the system ensures compliance with best practices for data privacy and protection.

---

## Project Context
This CRM system was developed as part of a real-world project at Bee Mobility, where I was tasked with creating an efficient, scalable, and user-friendly tool for the customer service team. The project was implemented to solve the challenges of managing customer interactions, maintaining an up-to-date knowledge base, and ensuring fast, accurate responses to customer inquiries. This simplified version of the CRM reflects the core features and functionalities implemented during the project.

---

## Why This Project is Special
This was one of my favorite projects so far. It provided me with an opportunity to work on a real-world problem and deliver a solution that had a direct, positive impact on the business. Seeing the CRM in use by the Bee Mobility customer service team and knowing that it was solving problems for both the team and the customers made the effort truly rewarding.

---

## Conclusion
The Bee Mobility CRM is an essential tool for managing customer inquiries and interactions. It offers real-time updates, an editable knowledge base, and a comprehensive analytics dashboard, all while providing a responsive and user-friendly interface. It was designed with scalability in mind, ensuring that it can grow as Bee Mobility's customer service needs evolve.

---

## Technologies Used
The CRM system was developed using a combination of modern technologies to ensure scalability, ease of use, and efficient data management:

- **Streamlit**: Used for creating the web-based user interface. It allows for easy integration of Python code into an interactive web application, making it ideal for rapid development and deployment.
- **SQLite**: Chosen for local data storage. SQLite is a lightweight, serverless database engine that simplifies the deployment process, while still providing robust capabilities for storing interactions and knowledge base entries.
- **Bootstrap**: Integrated to handle styling and ensure the interface is responsive. Bootstrap makes the web app user-friendly and accessible across different devices, including desktops, tablets, and smartphones.
- **Pandas**: Utilized for managing data and exporting interaction logs to Excel. Pandas is ideal for data manipulation and is widely used for data analysis and reporting in Python.
- **Python**: The core programming language, ensuring all business logic, data manipulation, and backend functionality are handled efficiently.

The integration of these technologies allowed for seamless data flow, user interaction, and responsive design, all while maintaining performance and scalability. Together, they made this CRM solution both practical for everyday use and adaptable for future growth.

---

## How to Use
1. Clone this repository to your local machine.
2. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```
3. Run the Streamlit app using the following command:
    ```
    streamlit run app.py
    ```
4. The CRM interface will be accessible via the generated link. Navigate through the various tabs to manage interactions, edit the knowledge base, and review analytics.

