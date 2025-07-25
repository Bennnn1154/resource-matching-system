import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

function RegisterPage() {
    // 收聽 AuthContext 廣播
    const { registerUser } = useContext(AuthContext);

    const handleSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const email = e.target.email.value;
        const password = e.target.password.value;
        const user_type = e.target.user_type.value;
        // 呼叫廣播中的 registerUser 函式
        registerUser(username, email, password, user_type);
    };

    return (
        <div>
            <h1>註冊新帳號</h1>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="請輸入帳號" required />
                <input type="email" name="email" placeholder="請輸入 Email" required />
                <input type="password" name="password" placeholder="請輸入密碼" required autocomplete="new-password" />
                <select name="user_type" required>
                    <option value="">請選擇您的身分</option>
                    <option value="university">我是大學端</option>
                    <option value="school">我是國高中小端</option>
                </select>
                <button type="submit">註冊</button>
            </form>
        </div>
    );
}

export default RegisterPage;