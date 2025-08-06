// frontend/src/pages/CreateProjectPage.jsx

import React, { useState, useContext } from 'react'; // 1. 引入 useContext
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext'; // 2. 引入 AuthContext

function CreateProjectPage() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    participant_limit: 30,
    restrictions: '',
  });

  const navigate = useNavigate();
  // 3. 從廣播系統中，取得通行證 (authTokens)
  const { authTokens } = useContext(AuthContext);
  const API_URL = import.meta.env.VITE_API_URL;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 4. 在 fetch 請求中加入 Authorization 標頭
    fetch(`${API_URL}/api/projects/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // ✅ 核心修正點：附上會員通行證
        // 'Bearer ' 後面有一個空格，這很重要
        'Authorization': `Bearer ${authTokens.access}`
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
        // ... (這裡的錯誤處理邏輯維持不變)
        if (response.ok) {
            return response.json();
        }
        return response.text().then(text => {
            throw new Error(`伺服器錯誤 (狀態碼: ${response.status}): \n${text}`);
        });
    })
    .then(data => {
        alert('計畫已成功上傳！');
        navigate('/');
    })
    .catch(error => {
        console.error("建立專案時發生錯誤:", error);
        alert('上傳失敗！請按 F12 打開開發者工具，查看 Console 中的詳細錯誤訊息。');
    });
  };

  return (
    <div>
      <h1>上傳新計畫</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '500px' }}>
        <input type="text" name="title" value={formData.title} onChange={handleChange} placeholder="計畫標題" required />
        <textarea name="description" value={formData.description} onChange={handleChange} placeholder="計畫簡介" required />
        <input type="text" name="subject" value={formData.subject} onChange={handleChange} placeholder="主題類別 (例如: 科學)" required />
        <input type="number" name="participant_limit" value={formData.participant_limit} onChange={handleChange} placeholder="人數限制" required />
        <textarea name="restrictions" value={formData.restrictions} onChange={handleChange} placeholder="其他限制 (選填)" />
        <button type="submit">送出</button>
      </form>
    </div>
  );
}

export default CreateProjectPage;