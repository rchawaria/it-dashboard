from flask import Flask
import psycopg2
from flask import render_template_string


app = Flask(__name__)

# Reusable DB connection


def get_conn():
    return psycopg2.connect(
        dbname="dashboard",
        user="admin",
        password="password123",
        host="db"
    )

# Home route


@app.route('/')
def home():
    return "IT Dashboard Running in Docker"

# Health check route (DevOps standard)


@app.route('/health')
def health():
    try:
        conn = get_conn()
        conn.close()
        return "OK - DB Connected"
    except Exception as e:
        return f"ERROR: {e}"

# Initialize database + insert sample data


@app.route('/init')
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            message TEXT
        )
    """)

    cur.execute("INSERT INTO logs (message) VALUES ('System started')")
    conn.commit()

    cur.close()
    conn.close()

    return "Database Initialized"

# Fetch logs from database


@app.route('/logs')
def logs():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    html = """
    <html>
    <head>
        <title>IT Dashboard Logs</title>
        <style>
            body { font-family: Arial; background: #f4f4f4; padding: 20px; }
            h1 { color: #333; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            th { background: #333; color: white; }
            tr:nth-child(even) { background: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>📊 IT Dashboard Logs</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Message</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html, rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
