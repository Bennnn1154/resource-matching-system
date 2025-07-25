// frontend/src/pages/ProjectListPage.jsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // 1. 引入 Link 元件

function ProjectListPage() {
  const [projects, setProjects] = useState([]);
  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/api/projects/`)
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
            // 2. 用 Link 元件把整張卡片包起來，並設定動態的 to 屬性
            <Link to={`/projects/${project.id}`} key={project.id} style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="project-card">
                <h2>{project.title}</h2>
                <p><strong>主題類別：</strong> {project.subject}</p>
                <p><strong>計畫簡介：</strong> {project.description.substring(0, 100)}...</p> {/* 只顯示部分簡介 */}
                <p><strong>人數限制：</strong> {project.participant_limit} 人</p>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <p>目前沒有任何計畫...</p>
      )}
    </div>
  );
}

export default ProjectListPage;