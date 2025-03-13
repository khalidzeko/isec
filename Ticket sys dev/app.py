from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import sqlite3
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to initialize the database and create the table if not exists
def init_db():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            username TEXT NOT NULL,
            project TEXT NOT NULL,
            issue TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

# Function to generate random ticket ID
def generate_ticket_id():
    """Generate a random alphanumeric ticket ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Function to insert a ticket into the database
def insert_ticket(username, project, issue, description):
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    ticket_id = generate_ticket_id()
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO tickets (ticket_id, username, project, issue, description, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (ticket_id, username, project, issue, description, 'Pending', created_at))
    conn.commit()
    conn.close()
    return ticket_id  # Return the generated ticket ID

# Route to submit a ticket
@app.route('/', methods=['GET', 'POST'])
def index():
    ticket_id = None  # Default value for ticket_id

    if request.method == 'POST':
        username = request.form['username']
        project = request.form['project']
        issue = request.form['issue']
        description = request.form['description']
        
        # Insert the ticket and get the ticket_id
        ticket_id = insert_ticket(username, project, issue, description)
        
        # Store the ticket ID in the session for display
        session['ticket_id'] = ticket_id
        
        # After inserting, pass the ticket_id to the template
        return render_template('index.html', ticket_id=ticket_id)

    theme = session.get('theme', 'light')

    # Check if the ticket_id exists in the session and display it if so
    ticket_id = session.get('ticket_id')

    # If the page is refreshed, remove the ticket_id from the session
    if ticket_id:
        session.pop('ticket_id', None)
    
    return render_template('index.html', theme=theme, ticket_id=ticket_id)

# Route for Admin Page - View All Tickets and Change Status
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()

    # Fetch tickets where the status is not 'Completed'
    c.execute("SELECT * FROM tickets WHERE status != 'Completed'")
    tickets = c.fetchall()
    conn.close()

    return render_template('admin.html', tickets=tickets)

@app.route('/admin/<ticket_id>', methods=['POST'])
def update_ticket_status(ticket_id):
    new_status = request.form['status']  # Get the new status from the form
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()

    # Update the status of the ticket
    c.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()

    # Redirect to the admin page to see the updated ticket list
    return redirect('/admin')

# Route for Track Page - Track Ticket by Ticket ID or User ID
@app.route('/track', methods=['GET', 'POST'])
def track():
    ticket_info = None  # Default value for ticket_info
    tickets_info = None  # Default value for multiple tickets info

    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        user_id = request.form.get('user_id')  # New input field for user ID

        conn = sqlite3.connect('tickets.db')
        c = conn.cursor()

        if ticket_id:
            # Fetch ticket information based on ticket_id
            c.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
            ticket_info = c.fetchone()
        elif user_id:
            # Fetch all tickets related to the user_id
            c.execute("SELECT * FROM tickets WHERE username = ?", (user_id,))
            tickets_info = c.fetchall()

        conn.close()
    
    return render_template('track.html', ticket_info=ticket_info, tickets_info=tickets_info)

# Route for Completed Tickets
@app.route('/completed_tickets')
def completed():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tickets WHERE status = 'Completed'")
    completed_tickets = c.fetchall()
    conn.close()
    return render_template('completed_tickets.html', tickets=completed_tickets)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
