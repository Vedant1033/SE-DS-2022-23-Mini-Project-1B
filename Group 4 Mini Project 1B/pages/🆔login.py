import mysql.connector
import streamlit as st
import streamlit.components.v1 as components
from streamlit.runtime.credentials import check_credentials
import pandas as pd


# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vedant@1033",
    database="used_car_price"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Streamlit app code
def main():
    st.set_page_config(page_title="Login and Registration")

    # Create a menu with options for login and registration
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Show the login form
    if choice == "Login":
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Check if the username and password match a record in the database
            mycursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = mycursor.fetchone()
            if result:
                st.success("Logged in!")
            else:
                st.error("Invalid username or password")

    # Show the registration form
    elif choice == "Register":
        st.title("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            # Check if the username already exists in the database
            mycursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            result = mycursor.fetchone()
            if result:
                st.error("Username already taken")
            else:
                # Add the new user to the database
                mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                mydb.commit()
                st.success("Registration successful")

                st.experimental_set_query_params(logged_in=True)


                # Define the JavaScript code to redirect to the main page
                redirect_js = """
                    <script>
                        window.location.replace(window.location.href.split('?')[0] + '?logged_in=True');
                    </script>
                """

                # Display the login form
                if st.button("Login"):
                    # Check the username and password
                    if check_credentials(username, password):
                        # Redirect to the main page
                        components.html(redirect_js)




if __name__ == '__main__':
    main()




