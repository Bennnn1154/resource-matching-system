// frontend/src/main.jsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.jsx';
import ProjectListPage from './pages/ProjectListPage.jsx';
import CreateProjectPage from './pages/CreateProjectPage.jsx';
// --- 以下是我們新增的 ---
import LoginPage from './pages/LoginPage.jsx'; // 引入登入頁面
import RegisterPage from './pages/RegisterPage.jsx'; // 引入註冊頁面
import { AuthProvider } from './context/AuthContext.jsx'; // 引入廣播發射器
import './index.css';

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            { index: true, element: <ProjectListPage /> },
            { path: "create-project", element: <CreateProjectPage /> },
            // --- 為新頁面新增路由 ---
            { path: "login", element: <LoginPage /> },
            { path: "register", element: <RegisterPage /> },
        ],
    },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        {/* 用 AuthProvider 將整個 App 包起來，這樣 App 內所有元件都能收到廣播 */}
        <AuthProvider>
            <RouterProvider router={router} />
        </AuthProvider>
    </React.StrictMode>,
);