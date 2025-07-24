import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function CreateProjectPage() {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    participant_limit: 30,
    restrictions: '',
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
      e.preventDefault();

      fetch(`${import.meta.env.VITE_API_URL}/api/projects/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
      })
      .then(response => {
          // 如果回應的狀態碼是成功的 (例如 201 Created)
          if (response.ok) {
              // 我們才把它當作 JSON 來解析
              return response.json();
          }
          // 如果回應是失敗的 (例如 400 Bad Request)
          // 我們把它當作純文字來讀取，這樣才能看到 HTML 錯誤頁面的內容
          return response.text().then(text => {
              // 拋出一個包含伺服器回應內容的錯誤
              throw new Error(`伺服器錯誤 (狀態碼: ${response.status}): \n${text}`);
          });
      })
      .then(data => {
          // 這個 .then 只會在 response.ok 為 true 時執行
          alert('計畫已成功上傳！');
          navigate('/');
      })
      .catch(error => {
          // 這裡可以捕捉到上面拋出的錯誤
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