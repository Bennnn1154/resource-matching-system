import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ background: '#eee', padding: '1rem', marginBottom: '1rem' }}>
      <Link to="/" style={{ marginRight: '1rem' }}>計畫列表</Link>
      <Link to="/create-project">上傳計畫</Link>
    </nav>
  );
}

export default Navbar;