// frontend/src/pages/ProjectDetailPage.jsx

import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

function ProjectDetailPage() {
    const { id } = useParams(); // 從 URL 中讀取計畫的 ID
    const [project, setProject] = useState(null);
    const [showForm, setShowForm] = useState(false); // 控制申請表單是否顯示
    const [applicationData, setApplicationData] = useState({
        contact_person: '',
        contact_email: '',
        contact_phone: '',
        notes: '',
    });

    const { user, authTokens } = useContext(AuthContext); // 從廣播系統取得使用者資訊和 token
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    // 當元件載入時，根據 ID 抓取計畫資料
    useEffect(() => {
        const fetchProject = async () => {
            const response = await fetch(`${API_URL}/api/projects/${id}/`);
            if (response.ok) {
                const data = await response.json();
                setProject(data);
            } else {
                console.error("Failed to fetch project details");
            }
        };
        fetchProject();
    }, [id]); // 當 id 改變時，重新抓取資料

    // 處理表單欄位變動
    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setApplicationData(prevState => ({ ...prevState, [name]: value }));
    };

    // 處理申請表單提交
    const handleApplicationSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch(`${API_URL}/api/applications/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 這是關鍵！提交申請時，必須附上使用者的通行證 (Token)
                'Authorization': `Bearer ${authTokens.access}`
            },
            body: JSON.stringify({
                project: id, // 告訴後端要申請哪個計畫
                ...applicationData
            })
        });

        if (response.status === 201) {
            alert('申請已成功送出！');
            setShowForm(false); // 隱藏表單
        } else {
            alert('申請送出失敗，請稍後再試。');
            console.error(await response.json());
        }
    };

    // 如果計畫資料還在載入中，顯示讀取訊息
    if (!project) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{project.title}</h1>
            <div className="project-card" style={{ textAlign: 'left', marginBottom: '2rem' }}>
                <p><strong>主題類別：</strong> {project.subject}</p>
                <p><strong>計畫簡介：</strong> {project.description}</p>
                <p><strong>人數限制：</strong> {project.participant_limit} 人</p>
                <p><strong>其他限制：</strong> {project.restrictions || '無'}</p>
                <p><strong>狀態：</strong> {project.status}</p>
            </div>

            {/* 這是條件式渲染：只有當使用者已登入且身分為 school 時，才顯示按鈕 */}
            {user && user.user_type === 'school' && (
                <div>
                    {!showForm ? (
                        <button onClick={() => setShowForm(true)}>我要報名</button>
                    ) : (
                        <form onSubmit={handleApplicationSubmit}>
                            <h3>填寫申請資料</h3>
                            <input type="text" name="contact_person" placeholder="學校聯絡人姓名" onChange={handleFormChange} required />
                            <input type="email" name="contact_email" placeholder="聯絡 Email" onChange={handleFormChange} required />
                            <input type="text" name="contact_phone" placeholder="聯絡電話" onChange={handleFormChange} required />
                            <textarea name="notes" placeholder="備註事項 (選填)" onChange={handleFormChange} />
                            <button type="submit">確認送出申請</button>
                            <button type="button" onClick={() => setShowForm(false)} style={{ marginLeft: '10px', background: '#6c757d' }}>取消</button>
                        </form>
                    )}
                </div>
            )}
        </div>
    );
}

export default ProjectDetailPage;