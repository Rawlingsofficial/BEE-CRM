import streamlit as st
import sqlite3
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
from dotenv import load_dotenv
import os
import base64


# Load environment variables from .env file
load_dotenv()  # Load environment variables
load_dotenv()  # Load environment variables

# Access the database path from the .env file
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/database.db')  # Default to 'data/database.db' if not set



# Example: Access environment variables
my_var = os.getenv('MY_VARIABLE', 'default_value')  # Replace with the actual variable you need

# Database Paths
DB_PATH = "data/database.db"
EXCEL_PATH = "data/interactions.xlsx"
SERVICE_ACCOUNT_FILE = "service_account.json"

print(f"MY_VARIABLE is: {my_var}")

# Utility Functions
def create_excel_file_if_not_exists():
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Interactions"
        wb.save(EXCEL_PATH)
    except Exception as e:
        st.error(f"Error initializing Excel file: {e}")

def write_to_excel(data):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Interactions"
        rows = dataframe_to_rows(data, index=False, header=True)
        for row in rows:
            ws.append(row)
        wb.save(EXCEL_PATH)
    except Exception as e:
        st.error(f"Error writing to Excel: {e}")

def fetch_table_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def update_interaction_status(interaction_id, new_status, new_category):
    conn = sqlite3.connect(DB_PATH)
    query = """
    UPDATE interactions
    SET status = ?, category = ?
    WHERE id = ?
    """
    conn.execute(query, (new_status, new_category, interaction_id))
    conn.commit()
    conn.close()




    

def write_to_excel(df):
    df.to_excel(EXCEL_PATH, index=False)

# UI Enhancements with Bootstrap
def include_bootstrap():
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
        <style>
            /* General styles */
            .container { max-width: 1200px; margin: auto; }
            .header { background-color: #f8f9fa; color: #333; padding: 10px 20px; border-radius: 8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); }
            .card { border: 1px solid #dee2e6; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; padding: 20px; }
            .card:hover { box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2); }
            .btn-primary { background-color: #007bff; border-color: #007bff; }
            .text-center { text-align: center; }

            /* AgGrid row hover highlight */
            .ag-theme-alpine .ag-row-hover {
                background-color: #FFD700 !important;  /* Yellow for hover */
            }

            /* AgGrid selected row highlight */
            .ag-theme-alpine .ag-row-selected {
                background-color: #FFD700 !important;  /* Yellow for selection */
                color: #000 !important;               /* Black text for contrast */
            }

            /* Header styling */
            .header {
                border-bottom: 2px solid #FFD700;  /* Yellow underline for headers */
            }

            /* Streamlit tabs customization */
            .stTabs [data-baseweb="tab"] {
                font-weight: bold;
                border: 2px solid transparent;
                padding: 5px 10px;
                border-radius: 10px;
            }

            .stTabs [data-baseweb="tab"]:hover {
                background-color: #FFD700 !important;  /* Yellow on hover */
                color: #000 !important;               /* Black text for hover */
            }

            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #FFD700 !important;  /* Yellow for selected tab */
                color: #000 !important;               /* Black text for selected tab */
                border-color: #FFD700 !important;     /* Yellow border for selected tab */
            }
        </style>
    """, unsafe_allow_html=True)



# Render Knowledge Base Section
def render_knowledge_base():
    st.markdown('<h2 class="header">Knowledge Base</h2>', unsafe_allow_html=True)

    # Fetch data from the database
    knowledge_base_df = fetch_table_data("knowledge_base")

    # Search and Filter Options
    search_query = st.text_input("Search by Question or Answer", placeholder="Type to search...")
    category_filter = st.selectbox("Filter by Category", ["All"] + knowledge_base_df["category"].unique().tolist())

    # Apply Search and Filter
    filtered_df = knowledge_base_df[
        (knowledge_base_df["question"].str.contains(search_query, case=False, na=False) |
         knowledge_base_df["answer"].str.contains(search_query, case=False, na=False))
    ]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["category"] == category_filter]

    # Display Editable Table
    st.markdown("<h4>Edit Knowledge Base</h4>", unsafe_allow_html=True)
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination(enabled=True)
    gb.configure_default_column(editable=True, groupable=True)
    grid_options = gb.build()
    grid_response = AgGrid(filtered_df, grid_options=grid_options, update_mode='value_changed', editable=True)

    # Delete Functionality
    st.markdown("<h4>Delete Question</h4>", unsafe_allow_html=True)
    with st.form("delete_question_form"):
        question_to_delete = st.selectbox(
            "Select Question to Delete",
            knowledge_base_df["question"].tolist()
        )
        delete_submitted = st.form_submit_button("Delete Question")
        if delete_submitted:
            conn = sqlite3.connect(DB_PATH)
            query = "DELETE FROM knowledge_base WHERE question = ?"
            conn.execute(query, (question_to_delete,))
            conn.commit()
            conn.close()
            st.success("Question deleted successfully!")

    # Section to Add New Questions
    st.markdown("<h4>Add New Question</h4>", unsafe_allow_html=True)
    with st.form("add_question_form"):
        new_category = st.selectbox("Select Category", ["Add New Category"] + knowledge_base_df["category"].unique().tolist())
        if new_category == "Add New Category":
            new_category = st.text_input("New Category Name", placeholder="Enter new category")

        new_question = st.text_input("New Question", placeholder="Enter the question")
        new_answer = st.text_area("Answer", placeholder="Provide the answer")
        new_type = st.selectbox("Select Type", ["Add New Type"] + knowledge_base_df["type"].unique().tolist())
        if new_type == "Add New Type":
            new_type = st.text_input("New Type", placeholder="Enter new type")

        submitted = st.form_submit_button("Add Question")
        if submitted:
            if not new_category or not new_question or not new_answer or not new_type:
                st.error("All fields are required to add a new question.")
            else:
                conn = sqlite3.connect(DB_PATH)
                query = """
                INSERT INTO knowledge_base (category, question, answer, type)
                VALUES (?, ?, ?, ?)
                """
                conn.execute(query, (new_category, new_question, new_answer, new_type))
                conn.commit()
                conn.close()
                st.success("New question added successfully!")




# Initialize a global DataFrame to store interactions
# Initialize a global DataFrame to store interactions
if 'interactions' not in st.session_state:
    st.session_state.interactions = pd.DataFrame(columns=["Customer Name", "Contact Info", "Query", "Resolution", "Status", "Category"])

def render_interactions():
    st.markdown('<h2 class="header">Log Interactions</h2>', unsafe_allow_html=True)

    # Create a Bootstrap container
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Input Fields with Bootstrap styling
    customer_name = st.text_input("Customer Name", placeholder="Enter customer's name", key="customer_name")
    contact_info = st.text_input("Contact Info", placeholder="Enter contact information", key="contact_info")
    customer_query = st.text_input("Query", placeholder="Enter customer query", key="customer_query")
    
    # Match Query in Knowledge Base
    knowledge_base = fetch_table_data("knowledge_base")  # Ensure this returns a DataFrame with 'question' and 'answer'
    resolution = None
    category = None

    if customer_query:  # Search for matching queries
        match = knowledge_base[knowledge_base["question"].str.contains(customer_query, case=False, na=False)]
        if not match.empty:
            resolution = match.iloc[0]["answer"]  # Get the resolution
            category = match.iloc[0]["category"]  # Get the category

    # Suggest Resolution
    if resolution:
        st.success(f"Suggested Resolution: {resolution}")
    else:
        st.warning("No matching resolution found. Please log manually if required.")

    # Manual Inputs
    category = st.selectbox(
        "Category",
        ["Select Category"] + knowledge_base["category"].unique().tolist(),
        index=0 if not category else knowledge_base["category"].tolist().index(category) + 1,
    )
    resolution_input = st.text_area("Resolution", value=resolution if resolution else "", height=100)
    status = st.selectbox("Status", ["Pending", "Resolved", "Escalated"])

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Log Interaction Button with Bootstrap styling
    if st.button("Log Interaction", key="log_interaction", help="Click to log the interaction"):
        if not customer_name or not contact_info or not customer_query or not category:
            st.error("All fields are required to log a new interaction.")
        else:
            # Log the interaction
            new_interaction = {
                "Customer Name": customer_name,
                "Contact Info": contact_info,
                "Query": customer_query,
                "Resolution": resolution_input,  # Use the resolution input field
                "Status": status,
                "Category": category
            }
            # Append the new interaction to the session state DataFrame
            st.session_state.interactions = pd.concat([st.session_state.interactions, pd.DataFrame([new_interaction])], ignore_index=True)
            st.success("Interaction logged successfully!")

    # Display all logged interactions
    if not st.session_state.interactions.empty:
        st.markdown("<h3>Logged Interactions</h3>", unsafe_allow_html=True)
        st.dataframe(st.session_state.interactions)

    # Debug Data (for developer view, optional)
    if st.checkbox("Show Debug Data"):  # Hidden unless checked
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Debug Data:")
        st.write("Customer Name:", customer_name)
        st.write("Contact Info:", contact_info)
        st.write("Query:", customer_query)
        st.write("Resolution:", resolution)
        st.write("Status:", status)
        st.write("Category:", category)

    # Close the Bootstrap container
    st.markdown('</div>', unsafe_allow_html=True)
    
    

def log_interaction(customer_name, contact_info, customer_query, resolution, status, category):
    # Debug: Print the values being logged
    print("Logging Interaction:")
    print("Customer Name:", customer_name)
    print("Contact Info:", contact_info)
    print("Query:", customer_query)
    print("Resolution:", resolution)
    print("Status:", status)
    print("Category:", category)

    try:
        conn = sqlite3.connect(DB_PATH)
        sql = """
        INSERT INTO interactions (customer_name, contact_info, query, resolution, status, category, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        # Execute the SQL command with the actual values
        conn.execute(sql, (customer_name, contact_info, customer_query, resolution, status, category, datetime.now()))
        conn.commit()
        st.success("Interaction logged successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")  # Print the error for debugging
    finally:
        conn.close()



            
            
# Render Interactions Section
# Render Manage Interactions Section
def render_manage_interactions():
    st.markdown('<h2 class="header">Manage Interactions</h2>', unsafe_allow_html=True)

    # Fetch data from Interactions Table
    interactions_df = fetch_table_data("interactions")

    if interactions_df.empty:
        st.warning("No data found in the interactions table.")
        return  # Exit if no data

    # Step 1: Filters
    st.markdown("### Filters")
    with st.container():
        driver_name_filter = st.text_input("Filter by Customer Name", placeholder="Type customer name...")
        driver_number_filter = st.text_input("Filter by Contact Info", placeholder="Type contact info...")
        status_filter = st.multiselect(
            "Filter by Status",
            options=["Pending", "Resolved", "Escalated"],
            default=["Pending", "Resolved", "Escalated"]
        )

        # Apply Filters
        filtered_df = interactions_df.copy()
        if driver_name_filter:
            filtered_df = filtered_df[filtered_df["customer_name"].str.contains(driver_name_filter, case=False, na=False)]
        if driver_number_filter:
            filtered_df = filtered_df[filtered_df["contact_info"].str.contains(driver_number_filter, case=False, na=False)]
        if status_filter:
            filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]

    # Display Filtered Table
    st.markdown("### Filtered Interactions")
    if not filtered_df.empty:
        st.dataframe(
            filtered_df[["id", "customer_name", "contact_info", "query", "status", "category"]],
            use_container_width=True
        )
    else:
        st.info("No interactions found matching the current filters.")
        return  # Exit if no interactions match

    # Step 2: Edit Interaction
    st.markdown("### Edit Interaction")
    interaction_id = st.selectbox(
        "Select Interaction ID to Edit",
        filtered_df["id"].tolist(),
        format_func=lambda x: f"ID {x}: {filtered_df.loc[filtered_df['id'] == x, 'query'].values[0][:50]}..."
    )

    selected_row = filtered_df[filtered_df["id"] == interaction_id].iloc[0]

    # Interaction Details (Read-only)
    st.markdown(f"#### Interaction Details (ID: {interaction_id})")
    with st.container():
        cols = st.columns([1, 2])
        with cols[0]:
            st.markdown(f"**Customer Name:** {selected_row['customer_name']}")
            st.markdown(f"**Contact Info:** {selected_row['contact_info']}")
            st.markdown(f"**Query:** {selected_row['query']}")
            st.markdown(f"**Current Resolution:** {selected_row['resolution']}")

    # Editable Section
    st.markdown("##### Update Fields")
    with st.form(f"edit_interaction_form_{interaction_id}"):
        cols = st.columns(2)
        with cols[0]:
            new_status = st.selectbox(
                "Update Status",
                ["Pending", "Resolved", "Escalated"],
                index=["Pending", "Resolved", "Escalated"].index(selected_row["status"]),
            )
        with cols[1]:
            new_category = st.text_input("Update Category", value=selected_row["category"])

        # Submit Button
        submitted = st.form_submit_button("Save Changes", type="primary")

        if submitted:
            update_interaction_status(
                interaction_id=interaction_id,
                new_status=new_status,
                new_category=new_category,
            )
            st.success(f"Interaction ID {interaction_id} updated successfully!")

            # Refresh data
            st.rerun()









# Function to render the analytics dashboard
def render_analytics():
    st.markdown("""
        <style>
            .metric-card {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                text-align: center;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.2);
            }
            .metric-title {
                font-size: 18px;
                font-weight: bold;
                color: #6c757d;
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #FFD700;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='text-center'>Analytics Dashboard</h2>", unsafe_allow_html=True)

    # Fetch interactions data
    interactions_df = fetch_table_data("interactions")

    # Calculate metrics
    resolved_count = len(interactions_df[interactions_df["status"] == "Resolved"])
    escalated_count = len(interactions_df[interactions_df["status"] == "Escalated"])
    pending_count = len(interactions_df[interactions_df["status"] == "Pending"])
    
    # Category breakdown
    category_counts = interactions_df["category"].value_counts()
    mobility_count = category_counts.get("Mobility Complaints", 0)
    financing_count = category_counts.get("Financing Issues", 0)
    incident_count = category_counts.get("Incident Records", 0)
    general_count = len(interactions_df)

    # Dashboard Metrics
    st.markdown("<h3>Status Metrics</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="row">
            <div class="col-md-4">
                <div class="metric-card">
                    <div class="metric-title">Resolved</div>
                    <div class="metric-value">{resolved_count}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="metric-card">
                    <div class="metric-title">Escalated</div>
                    <div class="metric-value">{escalated_count}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="metric-card">
                    <div class="metric-title">Pending</div>
                    <div class="metric-value">{pending_count}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Category Breakdown
    st.markdown("<h3>Category Breakdown</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="row">
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-title">Mobility Complaints</div>
                    <div class="metric-value">{mobility_count}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-title">Financing Issues</div>
                    <div class="metric-value">{financing_count}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-title">Incident Records</div>
                    <div class="metric-value">{incident_count}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <div class="metric-title">General Queries (Total)</div>
                    <div class="metric-value">{general_count}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Export Data Section
    st.markdown("<h3>Export and Sync Data</h3>", unsafe_allow_html=True)
    
    # Export and Sync Buttons Side by Side
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export Interactions Data", key="export_button"):
            # Get user's Downloads folder
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            file_path = os.path.join(downloads_path, "BeeMobility_Interactions.xlsx")

            # Export to Excel
            interactions_df.to_excel(file_path, index=False)
            st.success(f"Data exported successfully to {file_path}!")

    
       

        
        



def get_image_base64(image_path):
    """Convert an image to base64 for embedding in HTML."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set the favicon and page configuration
favicon_path = "assets/favicon-32x32.png"  # Adjust the path as necessary
favicon_base64 = get_image_base64(favicon_path)

st.set_page_config(
    page_title="BEE CRM",
    page_icon=f"data:image/png;base64,{favicon_base64}",  # Use the base64 string for the favicon
    layout="wide"  # Use "wide" for desktop layout
)

def render_title_with_logo():
    # Ensure the correct relative path to the image
    logo_path = "beeUntitled.jpg"  # Adjust to the correct logo file in your assets folder

    # HTML to display the logo and title side by side
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="data:image/jpeg;base64,{get_image_base64(logo_path)}" alt="Logo" style="width: 50px; height: 50px;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold; color: #333;">CRM System</h1>
        </div>
    """, unsafe_allow_html=True)

# Main Function
def main():
    # Call the function to render the title and logo only once
    render_title_with_logo()

    include_bootstrap()
    create_excel_file_if_not_exists()

    # Initialize tabs
    tabs = st.tabs(["Knowledge Base", "Interactions", "Manage Interactions", "Analytics"])

    # Render content for each tab
    with tabs[0]:
        render_knowledge_base()

    with tabs[1]:
        render_interactions()

    with tabs[2]:
        render_manage_interactions()

    with tabs[3]:
        render_analytics()

if __name__ == "__main__":
    main()
