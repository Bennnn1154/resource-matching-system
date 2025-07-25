import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext'; // 引入 AuthContext

function Navbar() {
  // 打開收音機，收聽廣播中的 user 和 logoutUser
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <nav style={{ background: '#eee', padding: '1rem', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between' }}>
      <div>
        <Link to="/" style={{ marginRight: '1rem' }}>計畫列表</Link>
        {/* 如果是大學端使用者，就顯示上傳計畫的連結 */}
        {user && user.user_type === 'university' && (
          <Link to="/create-project">上傳計畫</Link>
        )}
      </div>
      <div>
        {/* 根據 user 是否存在，顯示不同內容 */}
        {user ? (
          <>
            <span style={{ marginRight: '1rem' }}>您好, {user.username}</span>
            <button onClick={logoutUser}>登出</button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ marginRight: '1rem' }}>登入</Link>
            <Link to="/register">註冊</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;