import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

function LoginPage() {
  // 打開收音機，收聽 AuthContext 廣播
  const { loginUser } = useContext(AuthContext);

  const handleSubmit = (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    // 呼叫廣播中的 loginUser 函式
    loginUser(username, password);
  };

  return (
    <div>
      <h1>登入</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="請輸入帳號" required />
        <input type="password" name="password" placeholder="請輸入密碼" required autocomplete="new-password" />
        <button type="submit">登入</button>
      </form>
    </div>
  );
}

export default LoginPage;