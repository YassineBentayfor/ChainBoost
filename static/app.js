const displayProjects = (projects) => {
    const projectsList = document.getElementById('projectsList');
    projectsList.innerHTML = '';

    projects.forEach((project, index) => {
        const row = projectsList.insertRow();
        row.innerHTML = `
            <td>${project.title}</td>
            <td>${project.description}</td>
            <td>${project.fundingGoal}</td>
            <td>${project.totalContributions}</td> 
            <td><button onclick="contributeToProject(${index})">Contribute</button></td>
        `;
    });
};


const createProject = async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const fundingGoal = document.getElementById('fundingGoal').value;
    const durationDays = document.getElementById('durationDays').value;

    const response = await fetch('/projects', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title,
            description,
            fundingGoal,
            durationDays
        })
    });

    if (response.status === 201) {
        loadProjects();
    }
};

const loadProjects = async () => {
    const response = await fetch('/projects');
    if (response.ok) {
        const data = await response.json();
        const projects = data.projects || [];
        displayProjects(projects);
    }
};

const contributeToProject = async (index) => {
    const contributeSection = document.getElementById('contributeToProjectSection');
    document.getElementById('projectId').value = index;
    contributeSection.style.display = 'block';

    const createProjectSection = document.getElementById('createProjectSection');
    createProjectSection.style.display = 'none';
};

document.getElementById('projectForm').addEventListener('submit', createProject);
const loadProjectsForContribution = async () => {
    const response = await fetch('/projects');
    if (response.ok) {
        const data = await response.json();
        const projects = data.projects || [];
        const projectIdDropdown = document.getElementById('projectId');

        projects.forEach((project, index) => {
            const option = document.createElement('option');
            option.value = project.id;
            option.textContent = `${project.title} - ${project.id}`;
            projectIdDropdown.appendChild(option);
        });
    }
};



loadProjects();
loadProjectsForContribution();
