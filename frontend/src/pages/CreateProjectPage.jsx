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
    fetch('http://127.0.0.1:8000/api/projects/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      if (response.ok) {
        alert('計畫已成功上傳！');
        navigate('/'); // 成功後跳轉回計畫列表頁
      } else {
        alert('上傳失敗！');
      }
    })
    .catch(error => console.error("Error creating project:", error));
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