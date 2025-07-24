import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.jsx';
import ProjectListPage from './pages/ProjectListPage.jsx';
import CreateProjectPage from './pages/CreateProjectPage.jsx';
import './index.css';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // App 元件作為所有頁面的外殼 (包含 Navbar)
    children: [
      {
        index: true, // index: true 表示這個是根路徑 (/) 對應的元件
        element: <ProjectListPage />,
      },
      {
        path: "create-project",
        element: <CreateProjectPage />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);