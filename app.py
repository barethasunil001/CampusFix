from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "campusfix.db"


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>CampusFix</title>

<style>
*{
    box-sizing:border-box;
    margin:0;
    padding:0;
}

body{
    font-family:Arial,sans-serif;
    background:#f1f5f9;
    color:#172033;
}

header{
    background:#172554;
    color:white;
    padding:18px 35px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo{
    font-size:25px;
    font-weight:bold;
}

nav button{
    background:none;
    border:none;
    color:white;
    padding:10px 14px;
    cursor:pointer;
    font-size:15px;
}

.container{
    max-width:1400px;
    margin:auto;
    padding:25px;
}

.page{
    display:none;
}

.page.active{
    display:block;
}

.cards{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:18px;
    margin:20px 0;
}

.card{
    background:white;
    padding:22px;
    border-radius:15px;
    box-shadow:0 3px 12px #0001;
}

.card h3{
    color:#64748b;
    font-size:15px;
}

.card p{
    font-size:32px;
    font-weight:bold;
    margin-top:12px;
}

.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
}

.panel{
    background:white;
    padding:22px;
    border-radius:15px;
    box-shadow:0 3px 12px #0001;
    margin-bottom:20px;
}

.panel h2{
    margin-bottom:18px;
}

input,select,textarea{
    width:100%;
    padding:12px;
    margin:7px 0 15px;
    border:1px solid #cbd5e1;
    border-radius:8px;
    font-size:14px;
}

textarea{
    height:100px;
    resize:vertical;
}

label{
    font-weight:bold;
}

.btn{
    background:#2563eb;
    color:white;
    border:none;
    padding:11px 18px;
    border-radius:8px;
    cursor:pointer;
}

.btn:hover{
    opacity:.9;
}

table{
    width:100%;
    border-collapse:collapse;
}

th,td{
    padding:12px;
    border-bottom:1px solid #e2e8f0;
    text-align:left;
}

th{
    background:#f8fafc;
}

.badge{
    padding:5px 10px;
    border-radius:20px;
    font-size:12px;
    font-weight:bold;
}

.pending{
    background:#fef3c7;
    color:#92400e;
}

.progress{
    background:#dbeafe;
    color:#1d4ed8;
}

.resolved{
    background:#dcfce7;
    color:#166534;
}

.bar{
    height:28px;
    background:#2563eb;
    color:white;
    padding:5px 10px;
    margin:7px 0 15px;
    border-radius:5px;
    min-width:35px;
}

.workflow p{
    padding:10px;
    background:#f8fafc;
    margin:8px 0;
    border-radius:8px;
}

.toast{
    position:fixed;
    right:20px;
    bottom:20px;
    background:#172554;
    color:white;
    padding:15px 20px;
    border-radius:10px;
    display:none;
}

@media(max-width:900px){
    .cards{
        grid-template-columns:repeat(2,1fr);
    }

    .grid{
        grid-template-columns:1fr;
    }
}

@media(max-width:600px){
    header{
        flex-direction:column;
        gap:15px;
    }

    .cards{
        grid-template-columns:1fr;
    }

    table{
        font-size:12px;
    }
}
</style>
</head>

<body>

<header>

<div class="logo">
🛠 CampusFix
</div>

<nav>
<button onclick="showPage('dashboard')">Dashboard</button>
<button onclick="showPage('register')">Register Complaint</button>
<button onclick="showPage('tickets')">All Tickets</button>
<button onclick="showPage('reports')">Reports</button>
</nav>

</header>


<div class="container">


<!-- DASHBOARD -->

<section id="dashboard" class="page active">

<h2>Campus Maintenance Dashboard</h2>

<div class="cards">

<div class="card">
<h3>Total Complaints</h3>
<p id="total">0</p>
</div>

<div class="card">
<h3>Pending</h3>
<p id="pending">0</p>
</div>

<div class="card">
<h3>In Progress</h3>
<p id="progress">0</p>
</div>

<div class="card">
<h3>Resolved</h3>
<p id="resolved">0</p>
</div>

</div>


<div class="grid">

<div class="panel">

<h2>Recent Complaints</h2>

<div id="recent">
No complaints yet.
</div>

</div>


<div class="panel workflow">

<h2>CampusFix Workflow</h2>

<p>📝 Student registers complaint</p>
<p>💾 Complaint stored in database</p>
<p>👨‍🔧 Maintenance team handles issue</p>
<p>🔄 Complaint status is updated</p>
<p>✅ Complaint gets resolved</p>
<p>📊 Data appears in reports</p>

</div>

</div>

</section>



<!-- REGISTER -->

<section id="register" class="page">

<div class="panel">

<h2>Register New Complaint</h2>

<form onsubmit="registerComplaint(event)">

<label>Student Name</label>

<input id="name" required>


<label>Department</label>

<select id="department">

<option>Artificial Intelligence</option>
<option>Computer Science</option>
<option>Information Technology</option>
<option>Electronics</option>
<option>Mechanical</option>
<option>Civil</option>
<option>Management</option>

</select>


<label>Building</label>

<select id="building">

<option>Main Building</option>
<option>Engineering Block</option>
<option>AI & CSE Block</option>
<option>Library</option>
<option>Hostel</option>
<option>Administrative Block</option>

</select>


<label>Room Number</label>

<input id="room">


<label>Complaint Category</label>

<select id="category">

<option>Electrical</option>
<option>Furniture</option>
<option>Plumbing</option>
<option>IT</option>
<option>Internet</option>
<option>Cleaning</option>
<option>AC/Cooling</option>
<option>Other</option>

</select>


<label>Priority</label>

<select id="priority">

<option>Low</option>
<option>Medium</option>
<option>High</option>

</select>


<label>Problem Description</label>

<textarea id="problem" required></textarea>


<button class="btn" type="submit">
Register Complaint
</button>

</form>

</div>

</section>



<!-- TICKETS -->

<section id="tickets" class="page">

<div class="panel">

<h2>All Complaints</h2>

<input
id="search"
placeholder="Search complaint..."
onkeyup="loadTickets()"
>


<table>

<thead>

<tr>

<th>ID</th>
<th>Student</th>
<th>Category</th>
<th>Location</th>
<th>Priority</th>
<th>Status</th>
<th>Action</th>

</tr>

</thead>

<tbody id="ticketTable">

</tbody>

</table>

</div>

</section>



<!-- REPORTS -->

<section id="reports" class="page">

<div class="cards">

<div class="card">
<h3>Total</h3>
<p id="rTotal">0</p>
</div>

<div class="card">
<h3>Resolved</h3>
<p id="rResolved">0</p>
</div>

<div class="card">
<h3>Resolution Rate</h3>
<p id="rate">0%</p>
</div>

<div class="card">
<h3>Maintenance Cost</h3>
<p>₹<span id="cost">0</span></p>
</div>

</div>


<div class="grid">

<div class="panel">

<h2>Complaints by Category</h2>

<div id="categoryChart"></div>

</div>


<div class="panel">

<h2>Complaints by Department</h2>

<div id="departmentChart"></div>

</div>

</div>

</section>

</div>


<div id="toast" class="toast"></div>


<script>

function showPage(page){

    document.querySelectorAll(".page").forEach(function(x){
        x.classList.remove("active");
    });

    document.getElementById(page).classList.add("active");

    if(page === "dashboard"){
        loadDashboard();
    }

    if(page === "tickets"){
        loadTickets();
    }

    if(page === "reports"){
        loadReports();
    }
}


function toast(message){

    const box = document.getElementById("toast");

    box.innerText = message;
    box.style.display = "block";

    setTimeout(function(){
        box.style.display = "none";
    },2500);
}


async function registerComplaint(event){

    event.preventDefault();

    const data = {

        student_name:
            document.getElementById("name").value,

        department:
            document.getElementById("department").value,

        building:
            document.getElementById("building").value,

        room_no:
            document.getElementById("room").value,

        category:
            document.getElementById("category").value,

        priority:
            document.getElementById("priority").value,

        problem:
            document.getElementById("problem").value
    };


    try{

        const response = await fetch("/api/tickets",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(data)

        });


        if(response.ok){

            toast("Complaint registered successfully!");

            document.querySelector("form").reset();

            showPage("dashboard");

        }else{

            toast("Something went wrong!");

        }

    }catch(error){

        toast("Server connection error!");

    }
}



async function loadDashboard(){

    try{

        const response =
            await fetch("/api/analytics");

        const data =
            await response.json();


        document.getElementById("total").innerText =
            data.total;

        document.getElementById("pending").innerText =
            data.pending;

        document.getElementById("progress").innerText =
            data.in_progress;

        document.getElementById("resolved").innerText =
            data.resolved;


        const ticketResponse =
            await fetch("/api/tickets");

        const tickets =
            await ticketResponse.json();


        const recent =
            document.getElementById("recent");


        if(tickets.length === 0){

            recent.innerHTML =
                "<p>No complaints yet.</p>";

            return;
        }


        recent.innerHTML =
            tickets.slice(0,5).map(function(ticket){

                let cls = "pending";

                if(ticket.status === "In Progress"){
                    cls = "progress";
                }

                if(ticket.status === "Resolved"){
                    cls = "resolved";
                }

                return `
                <p>
                <b>#${ticket.id}</b>
                ${ticket.category}
                - ${ticket.problem}

                <br>

                <span class="badge ${cls}">
                ${ticket.status}
                </span>

                </p>
                `;

            }).join("");


    }catch(error){

        console.log(error);

    }
}



async function loadTickets(){

    try{

        const response =
            await fetch("/api/tickets");

        let tickets =
            await response.json();


        const search =
            document.getElementById("search")
            .value
            .toLowerCase();


        tickets =
            tickets.filter(function(ticket){

                return JSON.stringify(ticket)
                    .toLowerCase()
                    .includes(search);

            });


        const table =
            document.getElementById("ticketTable");


        table.innerHTML =
            tickets.map(function(ticket){

                let cls = "pending";

                if(ticket.status === "In Progress"){
                    cls = "progress";
                }

                if(ticket.status === "Resolved"){
                    cls = "resolved";
                }


                return `

                <tr>

                <td>${ticket.id}</td>

                <td>${ticket.student_name}</td>

                <td>${ticket.category}</td>

                <td>
                ${ticket.building}
                ${ticket.room_no}
                </td>

                <td>${ticket.priority}</td>

                <td>

                <span class="badge ${cls}">
                ${ticket.status}
                </span>

                </td>

                <td>

                <button
                class="btn"
                onclick="changeStatus(${ticket.id})">

                Update

                </button>

                </td>

                </tr>

                `;

            }).join("");


    }catch(error){

        console.log(error);

    }
}



async function changeStatus(id){

    const status =
        prompt(
            "Enter status:\nPending\nIn Progress\nResolved"
        );


    if(
        status !== "Pending" &&
        status !== "In Progress" &&
        status !== "Resolved"
    ){

        alert("Please enter a valid status.");

        return;
    }


    await fetch("/api/tickets/"+id+"/status",{

        method:"PATCH",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            status:status
        })

    });


    toast("Status updated successfully!");

    loadTickets();

    loadDashboard();
}



async function loadReports(){

    try{

        const response =
            await fetch("/api/analytics");

        const data =
            await response.json();


        document.getElementById("rTotal").innerText =
            data.total;

        document.getElementById("rResolved").innerText =
            data.resolved;


        const rate =
            data.total === 0
            ? 0
            : Math.round(
                data.resolved /
                data.total *
                100
            );


        document.getElementById("rate").innerText =
            rate + "%";


        document.getElementById("cost").innerText =
            data.cost;


        const categories =
            data.categories;


        const categoryValues =
            Object.values(categories);


        const maxCategory =
            Math.max(...categoryValues,1);


        document.getElementById("categoryChart").innerHTML =

            Object.entries(categories)
            .map(function(item){

                const name = item[0];
                const value = item[1];

                const width =
                    value /
                    maxCategory *
                    100;


                return `
                <p>${name} (${value})</p>

                <div
                class="bar"
                style="width:${width}%">

                ${value}

                </div>
                `;

            }).join("");


        const departments =
            data.departments;


        const departmentValues =
            Object.values(departments);


        const maxDepartment =
            Math.max(...departmentValues,1);


        document.getElementById("departmentChart").innerHTML =

            Object.entries(departments)
            .map(function(item){

                const name = item[0];
                const value = item[1];

                const width =
                    value /
                    maxDepartment *
                    100;


                return `
                <p>${name} (${value})</p>

                <div
                class="bar"
                style="width:${width}%">

                ${value}

                </div>
                `;

            }).join("");


    }catch(error){

        console.log(error);

    }
}


loadDashboard();

</script>

</body>
</html>
"""


def get_db():

    connection = sqlite3.connect(DB)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():

    connection = get_db()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS tickets(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_name TEXT NOT NULL,

        department TEXT NOT NULL,

        building TEXT NOT NULL,

        room_no TEXT,

        category TEXT NOT NULL,

        problem TEXT NOT NULL,

        priority TEXT NOT NULL,

        status TEXT DEFAULT 'Pending',

        date TEXT NOT NULL,

        cost REAL DEFAULT 0

    )
    """)

    connection.commit()

    connection.close()


@app.route("/")
def home():

    return render_template_string(HTML)


@app.route("/api/tickets", methods=["GET"])
def get_tickets():

    connection = get_db()

    rows = connection.execute(
        "SELECT * FROM tickets ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return jsonify([
        dict(row)
        for row in rows
    ])


@app.route("/api/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json()

    required = [
        "student_name",
        "department",
        "building",
        "category",
        "problem",
        "priority"
    ]

    for field in required:

        if not data.get(field):

            return jsonify({
                "error": field + " is required"
            }), 400


    connection = get_db()

    connection.execute("""
    INSERT INTO tickets(

        student_name,
        department,
        building,
        room_no,
        category,
        problem,
        priority,
        status,
        date

    )

    VALUES(?,?,?,?,?,?,?,?,?)
    """,(

        data["student_name"],
        data["department"],
        data["building"],
        data.get("room_no",""),
        data["category"],
        data["problem"],
        data["priority"],
        "Pending",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    ))

    connection.commit()

    connection.close()

    return jsonify({
        "success":True
    })


@app.route(
    "/api/tickets/<int:ticket_id>/status",
    methods=["PATCH"]
)
def update_status(ticket_id):

    data = request.get_json()

    status = data.get("status")

    allowed = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if status not in allowed:

        return jsonify({
            "error":"Invalid status"
        }),400


    connection = get_db()

    cursor = connection.execute("""
    UPDATE tickets
    SET status=?
    WHERE id=?
    """,(status,ticket_id))

    connection.commit()

    connection.close()


    if cursor.rowcount == 0:

        return jsonify({
            "error":"Ticket not found"
        }),404


    return jsonify({
        "success":True
    })


@app.route("/api/analytics")
def analytics():

    connection = get_db()


    total = connection.execute(
        "SELECT COUNT(*) FROM tickets"
    ).fetchone()[0]


    pending = connection.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Pending'
        """
    ).fetchone()[0]


    in_progress = connection.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE status='In Progress'
        """
    ).fetchone()[0]


    resolved = connection.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Resolved'
        """
    ).fetchone()[0]


    cost = connection.execute(
        """
        SELECT COALESCE(SUM(cost),0)
        FROM tickets
        """
    ).fetchone()[0]


    category_rows = connection.execute(
        """
        SELECT category, COUNT(*) AS count
        FROM tickets
        GROUP BY category
        """
    ).fetchall()


    department_rows = connection.execute(
        """
        SELECT department, COUNT(*) AS count
        FROM tickets
        GROUP BY department
        """
    ).fetchall()


    connection.close()


    categories = {
        row["category"]:row["count"]
        for row in category_rows
    }
    


    departments = {
        row["department"]:row["count"]
        for row in department_rows
    }


    return jsonify({

        "total":total,

        "pending":pending,

        "in_progress":in_progress,

        "resolved":resolved,

        "cost":cost,

        "categories":categories,

        "departments":departments

    })


if __name__ == "__main__":

    init_db()

    print("")
    print("=" * 50)
    print("        CAMPUSFIX STARTED")
    print("=" * 50)
    print("")
    print("Open in browser:")
    print("http://127.0.0.1:5000")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=False
    )