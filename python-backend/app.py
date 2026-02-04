"""
Portfolio Backend API
Flask REST API for portfolio management.

This API provides endpoints for:
- Health check
- Skills CRUD operations
- Projects management
- Contact form handling
- Learning log
- Analytics

Run with: python app.py
API will be available at: http://localhost:5000
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime
from typing import Tuple, Any
import json
import mysql.connector
from mysql.connector import pooling
import os

# app.py
app = Flask(__name__)
CORS(app)

# Import our portfolio manager
from portfolio_manager import PortfolioManager


# ==================== APP INITIALIZATION ====================

app = Flask(__name__)

# Enable CORS for all routes (allows frontend to connect)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:*", "http://127.0.0.1:*", "null"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize portfolio manager
portfolio = PortfolioManager()


# ==================== HELPER FUNCTIONS ====================

def success_response(
    data: Any = None,
    message: str = None,
    status_code: int = 200
) -> Tuple[Response, int]:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Tuple of (JSON response, status code)
    """
    response = {"success": True}
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    return jsonify(response), status_code


def error_response(
    error: str,
    status_code: int = 400,
    details: Any = None
) -> Tuple[Response, int]:
    """
    Create a standardized error response.
    
    Args:
        error: Error message
        status_code: HTTP status code
        details: Additional error details
        
    Returns:
        Tuple of (JSON response, status code)
    """
    response = {
        "success": False,
        "error": error
    }
    
    if details is not None:
        response["details"] = details
    
    return jsonify(response), status_code


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email appears valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic check: contains @ and at least one . after @
    if '@' not in email:
        return False
    
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local, domain = parts
    if not local or not domain or '.' not in domain:
        return False
    
    return True


# ==================== ROOT ENDPOINT ====================

@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint - API documentation.
    
    Returns:
        JSON with API information and available endpoints
    """
    return success_response(
        data={
            "name": "Portfolio Backend API",
            "version": "1.0.0",
            "description": "REST API for portfolio management",
            "documentation": {
                "health": {
                    "endpoint": "/api/health",
                    "method": "GET",
                    "description": "Check API health status"
                },
                "skills": {
                    "list": {"endpoint": "/api/skills", "method": "GET"},
                    "get": {"endpoint": "/api/skills/<name>", "method": "GET"},
                    "update": {"endpoint": "/api/skills/<name>", "method": "PUT"},
                    "by_category": {"endpoint": "/api/skills/category/<category>", "method": "GET"},
                    "by_status": {"endpoint": "/api/skills/status/<status>", "method": "GET"}
                },
                "projects": {
                    "list": {"endpoint": "/api/projects", "method": "GET"},
                    "create": {"endpoint": "/api/projects", "method": "POST"}
                },
                "contact": {
                    "submit": {"endpoint": "/api/contact", "method": "POST"}
                },
                "analytics": {
                    "progress": {"endpoint": "/api/analytics/progress", "method": "GET"}
                },
                "learning_log": {
                    "list": {"endpoint": "/api/learning-log", "method": "GET"},
                    "create": {"endpoint": "/api/learning-log", "method": "POST"}
                }
            }
        },
        message="Welcome to the Portfolio API! See documentation for available endpoints."
    )


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Check if API is running.
    
    Returns:
        JSON with health status and timestamp
    """
    return success_response(
        data={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": "API is running normally"
        },
        message="Portfolio API is healthy"
    )


# ==================== SKILLS ENDPOINTS ====================

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """
    Get all skills.
    
    Returns:
        JSON with list of all skills
    """
    try:
        skills = portfolio.get_all_skills()
        return success_response(
            data=skills,
            message=f"Retrieved {len(skills)} skills"
        )
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/skills/<skill_name>', methods=['GET'])
def get_skill(skill_name: str):
    """
    Get a specific skill by name.
    
    Args:
        skill_name: Name of the skill (URL parameter)
        
    Returns:
        JSON with skill data or error if not found
    """
    try:
        skill = portfolio.get_skill(skill_name)
        
        if skill:
            return success_response(data=skill)
        else:
            return error_response(
                f"Skill '{skill_name}' not found",
                404,
                {"available_skills": [s["name"] for s in portfolio.get_all_skills()]}
            )
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/skills/<skill_name>', methods=['PUT'])
def update_skill(skill_name: str):
    """
    Update a skill's progress level.
    
    Args:
        skill_name: Name of the skill (URL parameter)
        
    Request Body:
        {"level": int} - New level between 0-100
        
    Returns:
        JSON with updated skill data or error
    """
    try:
        # Get and validate request data
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        if 'level' not in data:
            return error_response(
                "Missing 'level' in request body",
                400,
                {"expected": {"level": "integer between 0 and 100"}}
            )
        
        new_level = data['level']
        
        # Validate level
        if not isinstance(new_level, int):
            return error_response(
                "Level must be an integer",
                400,
                {"received": type(new_level).__name__, "expected": "integer"}
            )
        
        if not 0 <= new_level <= 100:
            return error_response(
                "Level must be between 0 and 100",
                400,
                {"received": new_level, "valid_range": "0-100"}
            )
        
        # Update skill
        success = portfolio.update_skill_progress(skill_name, new_level)
        
        if success:
            updated_skill = portfolio.get_skill(skill_name)
            return success_response(
                data=updated_skill,
                message=f"Updated {skill_name} to {new_level}%"
            )
        else:
            return error_response(
                f"Skill '{skill_name}' not found",
                404,
                {"available_skills": [s["name"] for s in portfolio.get_all_skills()]}
            )
            
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/skills/category/<category>', methods=['GET'])
def get_skills_by_category(category: str):
    """
    Get skills filtered by category.
    
    Args:
        category: Category name (URL parameter)
        
    Returns:
        JSON with skills in the specified category
    """
    try:
        all_categories = portfolio.get_skills_by_category()
        
        # Case-insensitive search
        matching_category = None
        for cat_name in all_categories.keys():
            if cat_name.lower() == category.lower():
                matching_category = cat_name
                break
        
        if matching_category:
            skills = all_categories[matching_category]
            return success_response(
                data={
                    "category": matching_category,
                    "skills": skills,
                    "count": len(skills)
                }
            )
        else:
            return error_response(
                f"Category '{category}' not found",
                404,
                {"available_categories": list(all_categories.keys())}
            )
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/skills/status/<status>', methods=['GET'])
def get_skills_by_status(status: str):
    """
    Get skills filtered by status.
    
    Args:
        status: Status name (URL parameter) - Completed, Learning, or Upcoming
        
    Returns:
        JSON with skills matching the status
    """
    try:
        valid_statuses = ["Completed", "Learning", "Upcoming"]
        
        # Case-insensitive matching
        matching_status = None
        for valid in valid_statuses:
            if valid.lower() == status.lower():
                matching_status = valid
                break
        
        if not matching_status:
            return error_response(
                f"Invalid status '{status}'",
                400,
                {"valid_statuses": valid_statuses}
            )
        
        skills = portfolio.get_skills_by_status(matching_status)
        return success_response(
            data={
                "status": matching_status,
                "skills": skills,
                "count": len(skills)
            }
        )
    except Exception as e:
        return error_response(str(e), 500)


# ==================== PROJECTS ENDPOINTS ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """
    Get all projects.
    
    Returns:
        JSON with list of all projects
    """
    try:
        projects = portfolio.get_all_projects()
        return success_response(
            data=projects,
            message=f"Retrieved {len(projects)} projects"
        )
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/projects', methods=['POST'])
def add_project():
    """
    Add a new project.
    
    Request Body:
        {
            "name": str,
            "description": str,
            "technologies": list[str],
            "status": str (optional)
        }
        
    Returns:
        JSON with created project data
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        # Validate required fields
        required_fields = ['name', 'description', 'technologies']
        missing = [f for f in required_fields if f not in data or not data[f]]
        
        if missing:
            return error_response(
                f"Missing required fields: {', '.join(missing)}",
                400,
                {"required_fields": required_fields}
            )
        
        # Validate technologies is a list
        if not isinstance(data['technologies'], list):
            return error_response(
                "Technologies must be a list",
                400,
                {"expected": ["HTML", "CSS", "JavaScript"]}
            )
        
        # Create project
        project = portfolio.add_project(
            name=data['name'],
            description=data['description'],
            technologies=data['technologies'],
            status=data.get('status', 'In Progress')
        )
        
        return success_response(
            data=project,
            message="Project added successfully",
            status_code=201
        )
        
    except Exception as e:
        return error_response(str(e), 500)


# ==================== CONTACT ENDPOINT ====================

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """
    Handle contact form submissions.
    
    Request Body:
        {
            "name": str,
            "email": str,
            "message": str,
            "subject": str (optional)
        }
        
    Returns:
        JSON with confirmation message
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        missing = [f for f in required_fields if not data.get(f)]
        
        if missing:
            return error_response(
                f"Missing required fields: {', '.join(missing)}",
                400,
                {"required_fields": required_fields}
            )
        
        # Validate email
        if not validate_email(data['email']):
            return error_response(
                "Invalid email address",
                400,
                {"received": data['email']}
            )
        
        # Validate message length
        if len(data['message'].strip()) < 10:
            return error_response(
                "Message must be at least 10 characters",
                400,
                {"received_length": len(data['message'].strip())}
            )
        
        # Save contact message
        contact = portfolio.save_contact_message(
            name=data['name'].strip(),
            email=data['email'].strip(),
            message=data['message'].strip(),
            subject=data.get('subject', '').strip() or None
        )
        
        # Log to console (in production, you'd send an email)
        print("\n" + "=" * 50)
        print("📧 NEW CONTACT MESSAGE")
        print("=" * 50)
        print(f"From: {contact['name']} ({contact['email']})")
        if contact.get('subject'):
            print(f"Subject: {contact['subject']}")
        print(f"Message: {contact['message']}")
        print(f"Time: {contact['timestamp']}")
        print("=" * 50 + "\n")
        
        return success_response(
            data={
                "id": contact['id'],
                "timestamp": contact['timestamp']
            },
            message=f"Thank you, {data['name']}! Your message has been received."
        )
        
    except Exception as e:
        return error_response(str(e), 500)


# ==================== ANALYTICS ENDPOINT ====================

@app.route('/api/analytics/progress', methods=['GET'])
def get_progress_report():
    """
    Get progress analytics.
    
    Returns:
        JSON with comprehensive progress report
    """
    try:
        report = portfolio.generate_progress_report()
        return success_response(
            data=report,
            message="Progress report generated"
        )
    except Exception as e:
        return error_response(str(e), 500)


# ==================== LEARNING LOG ENDPOINTS ====================

@app.route('/api/learning-log', methods=['GET'])
def get_learning_log():
    """
    Get learning log entries.
    
    Query Parameters:
        limit (int, optional): Maximum number of entries to return
        
    Returns:
        JSON with learning log entries
    """
    try:
        limit = request.args.get('limit', type=int)
        logs = portfolio.get_learning_log(limit)
        
        return success_response(
            data=logs,
            message=f"Retrieved {len(logs)} log entries"
        )
    except Exception as e:
        return error_response(str(e), 500)


@app.route('/api/learning-log', methods=['POST'])
def add_learning_log():
    """
    Add a learning log entry.
    
    Request Body:
        {
            "entry": str,
            "topic": str (optional),
            "day": int (optional)
        }
        
    Returns:
        JSON with created log entry
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        if 'entry' not in data or not data['entry'].strip():
            return error_response(
                "Missing 'entry' in request body",
                400,
                {"expected": {"entry": "string", "topic": "string (optional)", "day": "integer (optional)"}}
            )
        
        log = portfolio.add_learning_log(
            entry=data['entry'].strip(),
            topic=data.get('topic'),
            day=data.get('day')
        )
        
        return success_response(
            data=log,
            message="Learning log entry added",
            status_code=201
        )
        
    except Exception as e:
        return error_response(str(e), 500)


# ==================== PERSONAL INFO ENDPOINT ====================

@app.route('/api/personal-info', methods=['GET'])
def get_personal_info():
    """
    Get personal information.
    
    Returns:
        JSON with personal info
    """
    try:
        info = portfolio.get_personal_info()
        return success_response(data=info)
    except Exception as e:
        return error_response(str(e), 500)


# ==================== COST CALCULATOR ENDPOINT ====================

@app.route('/api/calculate-cost', methods=['POST'])
def calculate_aws_cost():
    """
    Calculate estimated AWS monthly costs.
    
    Request Body:
        {
            "storageGB": int,
            "hours": int (optional, default 730)
        }
        
    Returns:
        JSON with cost breakdown
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is required", 400)
        
        storage_gb = data.get('storageGB', 0)
        hours = data.get('hours', 730)
        
        if not isinstance(storage_gb, (int, float)) or storage_gb < 0:
            return error_response(
                "storageGB must be a non-negative number",
                400
            )
        
        # AWS pricing (example rates)
        ec2_rate = 0.0116  # per hour
        db_rate = 0.034     # per hour
        storage_rate = 0.023  # per GB per month
        
        # Calculate costs (y = mx + c pattern from Day 2!)
        ec2_cost = ec2_rate * hours
        db_cost = db_rate * hours
        storage_cost = storage_rate * storage_gb
        total_cost = ec2_cost + db_cost + storage_cost
        
        return success_response(
            data={
                "breakdown": {
                    "ec2": round(ec2_cost, 2),
                    "database": round(db_cost, 2),
                    "storage": round(storage_cost, 2)
                },
                "totalCost": round(total_cost, 2),
                "parameters": {
                    "storageGB": storage_gb,
                    "hours": hours
                }
            },
            message=f"Estimated monthly cost: ${round(total_cost, 2)}"
        )
        
    except Exception as e:
        return error_response(str(e), 500)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return error_response(
        "Endpoint not found. Visit / for API documentation.",
        404
    )


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    return error_response(
        f"Method not allowed for this endpoint",
        405
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    return error_response(
        "Internal server error. Please try again later.",
        500
    )


# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 PORTFOLIO BACKEND API")
    print("=" * 60)
    print()
    print("📍 Server URL:     http://localhost:5000")
    print()
    print("📚 Available Endpoints:")
    print("   GET  /                      - API documentation")
    print("   GET  /api/health            - Health check")
    print("   GET  /api/skills            - Get all skills")
    print("   GET  /api/skills/<name>     - Get specific skill")
    print("   PUT  /api/skills/<name>     - Update skill progress")
    print("   GET  /api/projects          - Get all projects")
    print("   POST /api/projects          - Add new project")
    print("   POST /api/contact           - Submit contact form")
    print("   GET  /api/analytics/progress - Get progress report")
    print("   POST /api/calculate-cost    - Calculate AWS costs")
    print()
    print("🔧 Running in DEBUG mode")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Database connection pool
db_config = {
    'host': 'localhost',
    'user': 'portfolio_app',
    'password': os.environ.get('DB_PASSWORD', 'your_secure_password'),
    'database': 'portfolio_db',
    'pool_name': 'portfolio_pool',
    'pool_size': 5
}

connection_pool = pooling.MySQLConnectionPool(**db_config)

def get_db_connection():
    return connection_pool.get_connection()

# Contact form endpoint
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        
        # Validate required fields
        if not all(key in data for key in ['name', 'email', 'message']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO contacts (name, email, subject, message, ip_address)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['name'],
            data['email'],
            data.get('subject', ''),
            data['message'],
            request.remote_addr
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Thank you! Your message has been received.'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all contacts (admin only - add authentication in production!)
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, name, email, subject, message, created_at, is_read
            FROM contacts
            ORDER BY created_at DESC
            LIMIT 50
        """)
        
        contacts = cursor.fetchall()
        
        # Convert datetime to string for JSON
        for contact in contacts:
            contact['created_at'] = contact['created_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(contacts)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Track page view
@app.route('/api/pageview', methods=['POST'])
def track_pageview():
    try:
        data = request.json
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO page_views (page_path, referrer, user_agent, ip_address)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('path', '/'),
            data.get('referrer', ''),
            request.headers.get('User-Agent', ''),
            request.remote_addr
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analytics endpoint
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Total views last 7 days
        cursor.execute("""
            SELECT 
                DATE(viewed_at) AS date,
                COUNT(*) AS views
            FROM page_views
            WHERE viewed_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY DATE(viewed_at)
            ORDER BY date
        """)
        daily_views = cursor.fetchall()
        
        # Top pages
        cursor.execute("""
            SELECT page_path, COUNT(*) AS views
            FROM page_views
            WHERE viewed_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY page_path
            ORDER BY views DESC
            LIMIT 10
        """)
        top_pages = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convert dates for JSON
        for row in daily_views:
            row['date'] = row['date'].isoformat()
        
        return jsonify({
            'daily_views': daily_views,
            'top_pages': top_pages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)