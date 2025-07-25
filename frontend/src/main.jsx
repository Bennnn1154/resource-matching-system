// frontend/src/main.jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.jsx';
import ProjectListPage from './pages/ProjectListPage.jsx';
import CreateProjectPage from './pages/CreateProjectPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
// 我們不再需要從這裡引入 AuthProvider
import './index.css';
import ProjectDetailPage from './pages/ProjectDetailPage.jsx'; // 1. 引入我們即將建立的新頁面

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            { index: true, element: <ProjectListPage /> },
            { path: "create-project", element: <CreateProjectPage /> },
            { path: "login", element: <LoginPage /> },
            { path: "register", element: <RegisterPage /> },
            // 2. 新增這一條動態路由規則
            { path: "projects/:id", element: <ProjectDetailPage /> },
        ],
    },
]);


ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        {/* 這裡只留下 RouterProvider，讓它成為最外層 */}
        <RouterProvider router={router} />
    </React.StrictMode>,
);