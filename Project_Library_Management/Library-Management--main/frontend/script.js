const BASE_URL = "http://127.0.0.1:8000";

function showSection(sectionId) {
    document.querySelectorAll(".section").forEach(section => {
        section.classList.remove("active");
    });

    document.getElementById(sectionId).classList.add("active");
}

async function addDepartment() {
    const data = {
        department_id: document.getElementById("deptId").value,
        department_name: document.getElementById("deptName").value
    };

    try {
        const response = await fetch(`${BASE_URL}/departments`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        alert(result.message || result.detail);

        loadDashboard();

    } catch (error) {
        alert(error);
    }
}

async function addMember() {
    const data = {
        member_id: document.getElementById("memberId").value,
        name: document.getElementById("memberName").value,
        email: document.getElementById("memberEmail").value,
        phone: document.getElementById("memberPhone").value,
        department_id: document.getElementById("memberDept").value
    };

    try {
        const response = await fetch(`${BASE_URL}/members`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        alert(result.message || result.detail);

        loadDashboard();

    } catch (error) {
        alert(error);
    }
}

async function addBook() {
    const data = {
        book_id: document.getElementById("bookId").value,
        title: document.getElementById("title").value,
        author: document.getElementById("author").value,
        isbn: document.getElementById("isbn").value,
        available_copies: parseInt(document.getElementById("copies").value),
        department_id: document.getElementById("bookDept").value
    };

    try {
        const response = await fetch(`${BASE_URL}/books`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        alert(result.message || result.detail);

        loadDashboard();

    } catch (error) {
        alert(error);
    }
}

async function addLibrarian() {
    const data = {
        librarian_id: document.getElementById("libId").value,
        name: document.getElementById("libName").value,
        email: document.getElementById("libEmail").value,
        phone: document.getElementById("libPhone").value,
        department_id: document.getElementById("libDept").value
    };

    try {
        const response = await fetch(`${BASE_URL}/librarians`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        alert(result.message || result.detail);

    } catch (error) {
        alert(error);
    }
}

async function issueBook() {
    const data = {
        issue_id: document.getElementById("issueId").value,
        member_id: document.getElementById("issueMember").value,
        book_id: document.getElementById("issueBook").value,
        issue_date: document.getElementById("issueDate").value
    };

    try {
        const response = await fetch(`${BASE_URL}/issues`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        alert(result.message || result.detail);

        loadDashboard();

    } catch (error) {
        alert(error);
    }
}

async function loadDashboard() {
    try {
        const departments = await fetch(`${BASE_URL}/departments`);
        const members = await fetch(`${BASE_URL}/members`);
        const books = await fetch(`${BASE_URL}/books`);

        const departmentData = await departments.json();
        const memberData = await members.json();
        const bookData = await books.json();

        document.getElementById("deptCount").innerText =
            departmentData.length;

        document.getElementById("memberCount").innerText =
            memberData.length;

        document.getElementById("bookCount").innerText =
            bookData.length;

    } catch (error) {
        console.log(error);
    }
}

window.onload = function () {
    loadDashboard();
};