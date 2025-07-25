// frontend/src/App.jsx

import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar';
import { AuthProvider } from './context/AuthContext'; // <-- 在這裡引入
import './App.css';

function App() {
  return (
    // 將 AuthProvider 包裹在所有頁面內容的外層
    // 因為 App 元件本身已經在 RouterProvider 的內部了，所以這裡的 AuthProvider 也可以取用到路由功能
    <AuthProvider>
      <div className="App">
        <Navbar />
        <main>
          <Outlet />
        </main>
      </div>
    </AuthProvider>
  );
}

export default App;