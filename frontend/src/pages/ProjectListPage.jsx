import React, { useState, useEffect } from 'react';

function ProjectListPage() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/projects/')
      .then(response => response.json())
      .then(data => setProjects(data))
      .catch(error => console.error("Error fetching projects:", error));
  }, []);

  return (
    <div>
      <h1>進行中的計畫</h1>
      {projects.length > 0 ? (
        <div className="project-list-container">
          {projects.map(project => (
            <div key={project.id} className="project-card">
              <h2>{project.title}</h2>
              <p><strong>主題類別：</strong> {project.subject}</p>
              <p><strong>計畫簡介：</strong> {project.description}</p>
              <p><strong>人數限制：</strong> {project.participant_limit} 人</p>
              <p><strong>其他限制：</strong> {project.restrictions || '無'}</p>
              <p><strong>狀態：</strong> {project.status}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>目前沒有任何計畫...</p>
      )}
    </div>
  );
}

export default ProjectListPage;