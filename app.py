import os
import subprocess
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Compile the C code automatically if the binary doesn't exist
if not os.path.exists("./lost_found"):
    subprocess.run(["gcc", "lost_found.c", "-o", "lost_found"], check=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Campus Lost & Found | FoCP (CSE-1003)</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 30px auto; padding: 0 15px; background: #f9f9fb; }
        .header { background: #1e293b; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .header h1 { margin: 0 0 8px 0; font-size: 22px; }
        .header p { margin: 0; color: #cbd5e1; font-size: 15px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }
        input, select, button { padding: 8px 12px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #2563eb; color: white; border: none; cursor: pointer; }
        button:hover { background: #1d4ed8; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }
        .badge-LOST { background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
        .badge-FOUND { background: #dcfce7; color: #166534; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Campus Lost & Found Directory</h1>
        <p><strong>Name:</strong> Vansh Sehgal | <strong>Scholar No:</strong> 26U020158 | <strong>Course:</strong> FoCP (CSE-1003)</p>
    </div>

    <div class="card">
        <h3>Report a Lost or Found Item</h3>
        <form method="POST" action="/add">
            <select name="status" required>
                <option value="LOST">LOST</option>
                <option value="FOUND">FOUND</option>
            </select>
            <input type="text" name="name" placeholder="Item Name (e.g., Blue Bottle)" required>
            <input type="text" name="location" placeholder="Location (e.g., Library)" required>
            <input type="text" name="contact" placeholder="Phone / Room No." required>
            <button type="submit">Submit Entry</button>
        </form>
    </div>

    <div class="card">
        <h3>Search Directory</h3>
        <form method="GET" action="/">
            <input type="text" name="q" value="{{ query }}" placeholder="Search by item or location...">
            <button type="submit">Search</button>
            <a href="/" style="margin-left:10px; font-size:14px;">Reset</a>
        </form>

        <table>
            <tr><th>ID</th><th>Status</th><th>Item</th><th>Location</th><th>Contact</th></tr>
            {% for row in items %}
            <tr>
                <td>#{{ row[0] }}</td>
                <td><span class="badge-{{ row[1] }}">{{ row[1] }}</span></td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
            </tr>
            {% else %}
            <tr><td colspan="5">No matching items found.</td></tr>
            {% endfor %}
        </table>
    </div>
    <!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "49404520bdfd498384bb6c177577b484"}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("q", "").strip()
    cmd = ["./lost_found", "search", query] if query else ["./lost_found", "list"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    items = []
    for line in result.stdout.strip().split("\n"):
        if line and line != "EMPTY":
            items.append(line.split("|"))
            
    return render_template_string(HTML_TEMPLATE, items=items, query=query)

@app.route("/add", methods=["POST"])
def add():
    status = request.form.get("status", "LOST")
    name = request.form.get("name", "").strip()
    location = request.form.get("location", "").strip()
    contact = request.form.get("contact", "").strip()
    
    if name and location and contact:
        subprocess.run(["./lost_found", "add", status, name, location, contact])
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
