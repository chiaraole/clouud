const alumnosUrl = 'http://lb-prodpro-1434514222.us-east-1.elb.amazonaws.com:8000/students';
const profesoresUrl = 'http://lb-prodpro-1434514222.us-east-1.elb.amazonaws.com:8080/professors';
const clasesUrl = 'http://lb-prodpro-1434514222.us-east-1.elb.amazonaws.com:8081/classes';

function loadStudents() {
    fetch(alumnosUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerHTML = createTable(data.students, 'alumnos');
        })
        .catch(error => console.error('Error:', error));
}

function loadProfessors() {
    fetch(profesoresUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerHTML = createTable(data.professors, 'profesores');
        })
        .catch(error => console.error('Error:', error));
}

function loadClasses() {
    fetch(clasesUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerHTML = createTable(data.classes, 'clases');
        })
        .catch(error => console.error('Error:', error));
}

function createTable(data, type) {
    let table = `<table><tr>`;
    const keys = Object.keys(data[0]);
    keys.forEach(key => {
        table += `<th>${key}</th>`;
    });
    table += `<th>Actions</th></tr>`;
    data.forEach(item => {
        table += `<tr>`;
        keys.forEach(key => {
            table += `<td>${item[key]}</td>`;
        });
        table += `
            <td>
                <button onclick="editItem('${type}', ${item.id})">Edit</button>
                <button onclick="deleteItem('${type}', ${item.id})">Delete</button>
            </td>
        </tr>`;
    });
    table += `</table>`;
    table += `<button onclick="showCreateForm('${type}')">Add New ${type.slice(0, -1)}</button>`;
    return table;
}

function showCreateForm(type) {
    const formHtml = `
        <h2>Add New ${type.slice(0, -1)}</h2>
        <form onsubmit="createItem(event, '${type}')">
            ${generateFormFields(type)}
            <button type="submit">Submit</button>
        </form>
    `;
    document.getElementById('result').innerHTML = formHtml;
}

function generateFormFields(type) {
    let fields = '';
    switch(type) {
        case 'alumnos':
            fields = `
                <label>Name: <input type="text" name="name" required></label><br>
                <label>Lastname: <input type="text" name="lastname" required></label><br>
                <label>Degree: <input type="number" name="degree" required></label><br>
            `;
            break;
        case 'profesores':
            fields = `
                <label>Name: <input type="text" name="name" required></label><br>
                <label>Lastname: <input type="text" name="lastname" required></label><br>
                <label>Email: <input type="email" name="email" required></label><br>
            `;
            break;
        case 'clases':
            fields = `
                <label>Name: <input type="text" name="name" required></label><br>
                <label>Student ID: <input type="number" name="id_alumno" required></label><br>
                <label>Professor ID: <input type="number" name="id_profesor" required></label><br>
                <label>Degree: <input type="number" name="degree" required></label><br>
            `;
            break;
    }
    return fields;
}

function createItem(event, type) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => data[key] = value);
    let url = '';

    switch(type) {
        case 'alumnos':
            url = alumnosUrl;
            break;
        case 'profesores':
            url = profesoresUrl;
            break;
        case 'clases':
            url = clasesUrl;
            break;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        alert(`${type.slice(0, -1)} added successfully`);
        loadContent(type);
    })
    .catch(error => console.error('Error:', error));
}

function editItem(type, id) {
    if (id === undefined) {
        console.error("Undefined ID");
        return;
    }
    let url = '';
    switch(type) {
        case 'alumnos':
            url = `${alumnosUrl}/${id}`;
            break;
        case 'profesores':
            url = `${profesoresUrl}/${id}`;
            break;
        case 'clases':
            url = `${clasesUrl}/${id}`;
            break;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const formHtml = `
                <h2>Edit ${type.slice(0, -1)}</h2>
                <form onsubmit="updateItem(event, '${type}', ${id})">
                    ${generateEditFormFields(type, data)}
                    <button type="submit">Submit</button>
                </form>
            `;
            document.getElementById('result').innerHTML = formHtml;
        })
        .catch(error => console.error('Error:', error));
}

function generateEditFormFields(type, data) {
    let fields = '';
    switch(type) {
        case 'alumnos':
            fields = `
                <label>Name: <input type="text" name="name" value="${data.student[1]}" required></label><br>
                <label>Lastname: <input type="text" name="lastname" value="${data.student[2]}" required></label><br>
                <label>Degree: <input type="number" name="degree" value="${data.student[3]}" required></label><br>
            `;
            break;
        case 'profesores':
            fields = `
                <label>Name: <input type="text" name="name" value="${data.professor[1]}" required></label><br>
                <label>Lastname: <input type="text" name="lastname" value="${data.professor[2]}" required></label><br>
                <label>Email: <input type="email" name="email" value="${data.professor[3]}" required></label><br>
            `;
            break;
        case 'clases':
            fields = `
                <label>Name: <input type="text" name="name" value="${data.class[1]}" required></label><br>
                <label>Student ID: <input type="number" name="id_alumno" value="${data.class[2]}" required></label><br>
                <label>Professor ID: <input type="number" name="id_profesor" value="${data.class[3]}" required></label><br>
                <label>Degree: <input type="number" name="degree" value="${data.class[4]}" required></label><br>
            `;
            break;
    }
    return fields;
}

function updateItem(event, type, id) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => data[key] = value);
    let url = '';

    switch(type) {
        case 'alumnos':
            url = `${alumnosUrl}/${id}`;
            break;
        case 'profesores':
            url = `${profesoresUrl}/${id}`;
            break;
        case 'clases':
            url = `${clasesUrl}/${id}`;
            break;
    }

    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        alert(`${type.slice(0, -1)} updated successfully`);
        loadContent(type);
    })
    .catch(error => console.error('Error:', error));
}

function deleteItem(type, id) {
    if (confirm(`Are you sure you want to delete this ${type.slice(0, -1)}?`)) {
        let url = '';

        switch(type) {
            case 'alumnos':
                url = `${alumnosUrl}/${id}`;
                break;
            case 'profesores':
                url = `${profesoresUrl}/${id}`;
                break;
            case 'clases':
                url = `${clasesUrl}/${id}`;
                break;
        }

        fetch(url, {
            method: 'DELETE'
        })
        .then(() => {
            alert(`${type.slice(0, -1)} deleted successfully`);
            loadContent(type);
        })
        .catch(error => console.error('Error:', error));
    }
}

function loadContent(type) {
    switch(type) {
        case 'alumnos':
            loadStudents();
            break;
        case 'profesores':
            loadProfessors();
            break;
        case 'clases':
            loadClasses();
            break;
    }
}
