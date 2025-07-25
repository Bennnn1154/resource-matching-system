// frontend/src/context/AuthContext.jsx

import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode"; // 我們需要一個套件來解碼 JWT token
import { useNavigate } from 'react-router-dom';

// 建立我們的廣播頻道
const AuthContext = createContext();

export default AuthContext;

// 建立廣播電台的發射器 (Provider)，它會管理所有認證相關的狀態和邏輯
export const AuthProvider = ({ children }) => {
    // 從 localStorage 讀取 token，這樣使用者重新整理頁面後，登入狀態還會在
    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
    
    // 從 token 中解碼出使用者資訊
    const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);
    
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    // 登入函式
    const loginUser = async (username, password) => {
        const response = await fetch(`${API_URL}/api/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();

        if (response.status === 200) {
            setAuthTokens(data);
            setUser(jwtDecode(data.access));
            // 將 token 存入 localStorage
            localStorage.setItem('authTokens', JSON.stringify(data));
            navigate('/'); // 登入成功後，跳轉到首頁
        } else {
            alert('登入失敗！請檢查帳號或密碼。');
        }
    };

    // 註冊函式
    const registerUser = async (username, email, password, user_type) => {
        const response = await fetch(`${API_URL}/api/register/`, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({username, email, password, user_type})
        });
        if(response.status === 201){
            alert('註冊成功！現在您可以登入了。');
            navigate('/login'); // 註冊成功後，跳轉到登入頁
        } else {
            const data = await response.json();
            // 這裡可以做得更細緻，例如顯示具體哪個欄位錯誤
            alert(`註冊失敗: ${JSON.stringify(data)}`);
        }
    };

    // 登出函式
    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        // 清除 localStorage 中的 token
        localStorage.removeItem('authTokens');
        navigate('/login');
    };

    // 我們要廣播出去的內容
    const contextData = {
        user,
        authTokens,
        loginUser,
        registerUser,
        logoutUser,
    };

    // useEffect 會在 authTokens 改變時執行，未來可以用來刷新 token
    useEffect(() => {
        // 這部分未來可以加入 token 刷新邏輯
    }, [authTokens]);

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    );
};