from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Function to create the projects table if it doesn't exist
def create_projects_table():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            fundingGoal INTEGER,
            durationDays INTEGER,
            totalContributions INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Endpoint to add a project
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    funding_goal = data.get('fundingGoal')
    duration_days = data.get('durationDays')

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (title, description, fundingGoal, durationDays) VALUES (?, ?, ?, ?)',
                   (title, description, funding_goal, duration_days))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Project added successfully'}), 201

# Endpoint to get all projects
@app.route('/projects', methods=['GET'])
def get_projects():
    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, fundingGoal, durationDays, totalContributions FROM projects')
    projects = cursor.fetchall()
    conn.close()
    
    projects_data = [{'id': row[0], 'title': row[1], 'description': row[2], 'fundingGoal': row[3], 'durationDays': row[4], 'totalContributions': row[5]} for row in projects]
    return jsonify({'projects': projects_data}), 200



@app.route('/contribute/<int:project_id>', methods=['PUT'])
def contribute_to_project(project_id):
    data = request.get_json()
    contribution = data.get('contribution')

    conn = sqlite3.connect('projects.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()

    if project:
        updated_total = project[5] + contribution  # Assuming totalContributions is at index 5
        cursor.execute('UPDATE projects SET totalContributions = ? WHERE id = ?', (updated_total, project_id))
        conn.commit()

        return jsonify({'message': f'Contribution of {contribution} ETH made to Project ID: {project_id}'}), 200
    else:
        return jsonify({'error': f'Project with ID {project_id} does not exist'}), 404


@app.route('/') 
def index():
    return render_template('index.html')

if __name__ == '__main__':
    create_projects_table()
    app.run(debug=True, port=8080)
    





