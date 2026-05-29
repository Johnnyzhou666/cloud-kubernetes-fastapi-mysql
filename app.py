import os
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

# Fetch database connection information from Kubernetes environment variables
# Provide default values for local testing outside of K8s
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin123')
DB_NAME = os.environ.get('DB_NAME', 'cloud_db')

def get_db_connection():
    """Establish a connection to the MySQL database"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/')
def index():
    """Core functionality: Read data from the database and display it on the webpage"""
    conn = get_db_connection()
    
    if not conn:
        return "<h1>Error: Cannot connect to database!</h1><p>Check if the database pod is running and the DB_HOST is correct.</p>", 500

    try:
        with conn.cursor() as cursor:
            # Execute basic read operations (satisfies the project's "basic read operations" requirement)
            cursor.execute("SELECT * FROM students")
            records = cursor.fetchall()
            
            # Construct a simple HTML table to return to the frontend
            html = "<h2>Cloud Computing Project - Student Roster</h2>"
            html += "<table border='1' cellpadding='10'><tr><th>ID</th><th>Name</th><th>Program</th></tr>"
            for row in records:
                html += f"<tr><td>{row['id']}</td><td>{row['name']}</td><td>{row['program']}</td></tr>"
            html += "</table>"
            
            return html
    except Exception as e:
        return f"<h1>Error reading from database: {e}</h1>", 500
    finally:
        conn.close()

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes Liveness/Readiness probes"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Listen on port 80, corresponding to the containerPort in app-deployment.yaml
    app.run(host='0.0.0.0', port=80)
