from flask import Flask, jsonify, request, render_template_string
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# In-memory data store
students = {}
student_id_counter = 1

# GCSE grade boundaries and calculations
GRADE_BOUNDARIES = {
    9: 90, 8: 80, 7: 70, 6: 60, 5: 50, 4: 40, 3: 30, 2: 20, 1: 10
}

def calculate_predicted_grade(mock_scores, coursework_score, teacher_assessment):
    """Calculate predicted GCSE grade based on multiple factors"""
    # Weight the different components
    mock_avg = sum(mock_scores) / len(mock_scores) if mock_scores else 0
    
    # Adjust weights if coursework is not provided
    if coursework_score is not None:
        weighted_score = (mock_avg * 0.5) + (coursework_score * 0.3) + (teacher_assessment * 0.2)
    else:
        # Redistribute weight: 60% mocks, 40% teacher assessment
        weighted_score = (mock_avg * 0.6) + (teacher_assessment * 0.4)
    
    # Determine grade based on boundaries
    for grade, boundary in GRADE_BOUNDARIES.items():
        if weighted_score >= boundary:
            return grade
    return 'U'  # Ungraded

def calculate_progress(current_score, target_grade):
    """Calculate how much progress is needed"""
    target_score = GRADE_BOUNDARIES.get(target_grade, 0)
    gap = target_score - current_score
    return {
        'gap': round(gap, 2),
        'on_track': gap <= 0,
        'percentage_complete': min(100, round((current_score / target_score) * 100, 2)) if target_score > 0 else 0
    }

# Error handler
def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except KeyError as e:
            return jsonify({'error': f'Student not found'}), 404
        except Exception as e:
            return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    return wrapper

# HTML Template for the GUI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GCSE Predicted Grades Calculator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        .mock-scores {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .results {
            display: none;
        }
        .results.show {
            display: block;
        }
        .grade-display {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .grade-number {
            font-size: 5em;
            font-weight: bold;
            margin: 20px 0;
        }
        .progress-bar {
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-top: 10px;
        }
        .badge.on-track {
            background: #d4edda;
            color: #155724;
        }
        .badge.needs-improvement {
            background: #fff3cd;
            color: #856404;
        }
        .students-list {
            margin-top: 20px;
        }
        .student-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 GCSE Predicted Grades Calculator</h1>
        
        <div class="card">
            <h2>Student Information</h2>
            <form id="gradeForm">
                <div class="form-group">
                    <label for="studentName">Student Name:</label>
                    <input type="text" id="studentName" required>
                </div>
                
                <div class="form-group">
                    <label for="subject">Subject:</label>
                    <input type="text" id="subject" required placeholder="e.g., Mathematics, English, Science">
                </div>
                
                <div class="form-group">
                    <label for="targetGrade">Target Grade (1-9):</label>
                    <select id="targetGrade" required>
                        <option value="">Select target grade</option>
                        <option value="9">Grade 9</option>
                        <option value="8">Grade 8</option>
                        <option value="7">Grade 7</option>
                        <option value="6">Grade 6</option>
                        <option value="5">Grade 5</option>
                        <option value="4">Grade 4</option>
                        <option value="3">Grade 3</option>
                        <option value="2">Grade 2</option>
                        <option value="1">Grade 1</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Mock Exam Scores (%):</label>
                    <div class="mock-scores">
                        <input type="number" id="mock1" min="0" max="100" placeholder="Mock 1" required>
                        <input type="number" id="mock2" min="0" max="100" placeholder="Mock 2" required>
                        <input type="number" id="mock3" min="0" max="100" placeholder="Mock 3">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="coursework">Coursework Score (%) <em style="color: #999;">(optional)</em>:</label>
                    <input type="number" id="coursework" min="0" max="100">
                </div>
                
                <div class="form-group">
                    <label for="teacherAssessment">Teacher Assessment (%):</label>
                    <input type="number" id="teacherAssessment" min="0" max="100" required>
                </div>
                
                <button type="submit">Calculate Predicted Grade</button>
            </form>
        </div>
        
        <div class="card results" id="results">
            <h2>Results</h2>
            <div class="grade-display">
                <h3>Predicted Grade</h3>
                <div class="grade-number" id="predictedGrade">-</div>
                <span class="badge" id="trackingBadge">-</span>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Current Performance</div>
                    <div class="stat-value" id="currentScore">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Target Score</div>
                    <div class="stat-value" id="targetScore">-</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Gap to Target</div>
                    <div class="stat-value" id="gapScore">-</div>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <label>Progress to Target:</label>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressBar">0%</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>All Students</h2>
            <div class="students-list" id="studentsList">
                <p style="text-align: center; color: #999;">No students added yet</p>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('gradeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const mockScores = [
                parseFloat(document.getElementById('mock1').value),
                parseFloat(document.getElementById('mock2').value),
            ];
            
            const mock3 = document.getElementById('mock3').value;
            if (mock3) mockScores.push(parseFloat(mock3));
            
            const data = {
                name: document.getElementById('studentName').value,
                subject: document.getElementById('subject').value,
                target_grade: parseInt(document.getElementById('targetGrade').value),
                mock_scores: mockScores,
                coursework_score: document.getElementById('coursework').value ? 
                    parseFloat(document.getElementById('coursework').value) : null,
                teacher_assessment: parseFloat(document.getElementById('teacherAssessment').value)
            };
            
            try {
                const response = await fetch('/api/students', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                displayResults(result);
                loadStudents();
            } catch (error) {
                alert('Error calculating grade: ' + error.message);
            }
        });
        
        function displayResults(data) {
            document.getElementById('predictedGrade').textContent = data.predicted_grade;
            document.getElementById('currentScore').textContent = data.weighted_score.toFixed(1) + '%';
            document.getElementById('targetScore').textContent = data.progress.gap <= 0 ? '✓' : data.target_grade;
            document.getElementById('gapScore').textContent = Math.abs(data.progress.gap).toFixed(1);
            
            const progressBar = document.getElementById('progressBar');
            progressBar.style.width = data.progress.percentage_complete + '%';
            progressBar.textContent = data.progress.percentage_complete + '%';
            
            const badge = document.getElementById('trackingBadge');
            if (data.progress.on_track) {
                badge.textContent = 'On Track ✓';
                badge.className = 'badge on-track';
            } else {
                badge.textContent = 'Needs Improvement';
                badge.className = 'badge needs-improvement';
            }
            
            document.getElementById('results').classList.add('show');
        }
        
        async function loadStudents() {
            try {
                const response = await fetch('/api/students');
                const data = await response.json();
                
                const list = document.getElementById('studentsList');
                if (data.students.length === 0) {
                    list.innerHTML = '<p style="text-align: center; color: #999;">No students added yet</p>';
                    return;
                }
                
                list.innerHTML = data.students.map(s => `
                    <div class="student-item">
                        <div>
                            <strong>${s.name}</strong> - ${s.subject}<br>
                            <small>Predicted: Grade ${s.predicted_grade} | Target: Grade ${s.target_grade}</small>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.5em; font-weight: bold; color: #667eea;">${s.predicted_grade}</div>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading students:', error);
            }
        }
        
        loadStudents();
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/students', methods=['GET'])
@handle_errors
def get_students():
    return jsonify({
        'students': list(students.values()),
        'count': len(students)
    }), 200

@app.route('/api/students/<int:student_id>', methods=['GET'])
@handle_errors
def get_student(student_id):
    if student_id not in students:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(students[student_id]), 200

@app.route('/api/students', methods=['POST'])
@handle_errors
def create_student():
    global student_id_counter
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'subject', 'target_grade', 'mock_scores', 'teacher_assessment']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Calculate predicted grade
    mock_scores = data['mock_scores']
    coursework = data.get('coursework_score')  # Optional field
    teacher_assessment = data['teacher_assessment']
    
    predicted_grade = calculate_predicted_grade(mock_scores, coursework, teacher_assessment)
    
    # Calculate weighted score for display
    mock_avg = sum(mock_scores) / len(mock_scores)
    if coursework is not None:
        weighted_score = (mock_avg * 0.5) + (coursework * 0.3) + (teacher_assessment * 0.2)
    else:
        weighted_score = (mock_avg * 0.6) + (teacher_assessment * 0.4)
    
    # Calculate progress
    progress = calculate_progress(weighted_score, data['target_grade'])
    
    student = {
        'id': student_id_counter,
        'name': data['name'],
        'subject': data['subject'],
        'target_grade': data['target_grade'],
        'mock_scores': mock_scores,
        'coursework_score': coursework,
        'teacher_assessment': teacher_assessment,
        'predicted_grade': predicted_grade,
        'weighted_score': weighted_score,
        'progress': progress,
        'created_at': datetime.utcnow().isoformat()
    }
    
    students[student_id_counter] = student
    student_id_counter += 1
    
    return jsonify(student), 201

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@handle_errors
def delete_student(student_id):
    if student_id not in students:
        return jsonify({'error': 'Student not found'}), 404
    
    deleted = students.pop(student_id)
    return jsonify({'message': 'Student deleted', 'student': deleted}), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'students_count': len(students)}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)