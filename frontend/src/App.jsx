import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        {/* Outlet 會根據目前的 URL，顯示對應的頁面元件 */}
        <Outlet />
      </main>
    </div>
  );
}

export default App;