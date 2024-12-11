# Bee Mobility CRM System - Official Codebase

## Overview

The Bee Mobility CRM system is designed to handle customer interactions, maintain a knowledge base, and provide insightful analytics for customer service teams. This system allows customer service staff to log and manage customer queries, track resolutions, and update statuses while ensuring the knowledge base is always up-to-date.

This `README.md` provides an overview of the **code structure**, **function definitions**, and **purpose** of each section in the CRM system code.

## Main Code Overview

The CRM system is built using **Streamlit**, **SQLite3**, **Pandas**, and **openpyxl**. It leverages **AgGrid** for managing data tables and includes an interactive UI with **Bootstrap** for a responsive design.

Below is a breakdown of the key functions and their purpose within the codebase:

---

### **1. Utility Functions**

#### `create_excel_file_if_not_exists()`

- **Purpose**: Initializes the Excel file (`interactions.xlsx`) if it does not exist. This is important for storing logs of interactions if they are not stored in the SQLite database.
- **Description**: If the Excel file does not exist, it creates one with a sheet titled "Interactions".

#### `write_to_excel(df)`

- **Purpose**: Writes the customer interactions DataFrame (`df`) to the Excel file (`interactions.xlsx`).
- **Description**: This function allows for exporting customer interaction data to Excel, useful for offline access or backup.

#### `fetch_table_data(table_name)`

- **Purpose**: Fetches data from a specified SQLite table and returns it as a Pandas DataFrame.
- **Description**: This function is used to retrieve the knowledge base and interaction data stored in the SQLite database, making it accessible for manipulation and display within the CRM.

#### `update_interaction_status(interaction_id, new_status, new_category)`

- **Purpose**: Updates the status and category of a specific interaction.
- **Description**: This function is called when a customer interaction is edited (for example, changing its status from "Pending" to "Resolved").

#### `log_interaction(customer_name, contact_info, customer_query, resolution, status, category)`

- **Purpose**: Logs a new customer interaction to the SQLite database.
- **Description**: This function inserts a new record into the "interactions" table, storing information about the customer, their query, resolution, status, and category.

---

### **2. UI and Rendering Functions**

#### `include_bootstrap()`

- **Purpose**: Includes the Bootstrap framework in the Streamlit app for responsive and modern UI design.
- **Description**: This function integrates Bootstrap styles to ensure that the app layout is mobile-friendly and visually appealing, providing a professional user interface for the CRM.

#### `render_knowledge_base()`

- **Purpose**: Displays and manages the knowledge base section of the CRM.
- **Description**: This function allows users to search and filter the knowledge base, edit entries, delete questions, and add new ones. It uses **AgGrid** to create an editable table of knowledge base entries (questions and answers).

#### `render_interactions()`

- **Purpose**: Renders the interaction logging interface.
- **Description**: This function provides fields for logging customer interactions, such as customer name, contact info, query, resolution, and status. It also provides suggested resolutions from the knowledge base and handles the logging process when the user clicks "Log Interaction".

#### `render_manage_interactions()`

- **Purpose**: Displays and manages customer interactions that have been logged.
- **Description**: This function allows customer service teams to filter interactions by customer name, contact info, or status. It also provides an option to edit the status or category of logged interactions.

#### `render_analytics()`

- **Purpose**: Renders the analytics dashboard.
- **Description**: This function provides insight into the CRM system’s data, including metrics such as the number of resolved, escalated, and pending interactions, as well as category breakdowns (e.g., Mobility Complaints, Financing Issues). It also includes functionality to export the data to an Excel file.

#### `render_title_with_logo()`

- **Purpose**: Displays the title of the CRM system along with the logo.
- **Description**: This function renders a visually appealing header for the CRM app, showing the company logo and the title "CRM System".

---

### **3. Streamlit Configuration and Main Function**

#### `get_image_base64(image_path)`

- **Purpose**: Converts an image to a base64-encoded string.
- **Description**: This utility function is used to embed images (like the logo and favicon) directly into the Streamlit app without needing external image files.

#### `main()`

- **Purpose**: The main entry point for the Streamlit app.
- **Description**: This function initializes the app, renders the logo and title, includes Bootstrap, and sets up tabs for navigating between different sections: Knowledge Base, Interactions, Manage Interactions, and Analytics.

---

## Database Schema

The CRM uses an **SQLite** database to store interaction data and knowledge base entries. Below is the structure of the two primary tables:

### 1. **interactions**

- `id`: (INTEGER, Primary Key) Unique identifier for each interaction.
- `customer_name`: (TEXT) The name of the customer.
- `contact_info`: (TEXT) Contact details for the customer.
- `query`: (TEXT) The customer’s query or issue.
- `resolution`: (TEXT) The resolution provided to the customer.
- `status`: (TEXT) The current status of the interaction (e.g., Pending, Resolved, Escalated).
- `category`: (TEXT) The category of the interaction (e.g., Mobility Complaints, Financing Issues).
- `timestamp`: (DATETIME) The time when the interaction was logged.

### 2. **knowledge_base**

- `id`: (INTEGER, Primary Key) Unique identifier for each knowledge base entry.
- `category`: (TEXT) The category of the knowledge base entry (e.g., Mobility Complaints).
- `question`: (TEXT) The question or query in the knowledge base.
- `answer`: (TEXT) The answer or resolution provided in the knowledge base.
- `type`: (TEXT) The type of entry (e.g., FAQ, Procedure, Troubleshooting).

---

## Running the CRM

1. Clone or download the repository to your local machine.
2. Make sure you have **Streamlit**, **SQLite3**, **Pandas**, and **openpyxl** installed.
3. Run the following command to start the CRM:

```bash
streamlit run app.py

