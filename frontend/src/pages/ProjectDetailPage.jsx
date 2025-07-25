// frontend/src/pages/ProjectDetailPage.jsx

import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

function ProjectDetailPage() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [showForm, setShowForm] = useState(false);
    const [applicationData, setApplicationData] = useState({
        contact_person: '',
        contact_email: '',
        contact_phone: '',
        notes: '',
    });

    const { user, authTokens } = useContext(AuthContext);
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

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
    }, [id]);

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setApplicationData(prevState => ({ ...prevState, [name]: value }));
    };

    const handleApplicationSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch(`${API_URL}/api/applications/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authTokens.access}`
            },
            body: JSON.stringify({
                project: id,
                ...applicationData
            })
        });

        if (response.status === 201) {
            alert('申請已成功送出！');
            setShowForm(false);
            // --- 變更點 1: 申請成功後，重新抓取一次計畫資料來更新畫面 ---
            const updatedResponse = await fetch(`${API_URL}/api/projects/${id}/`);
            const updatedData = await updatedResponse.json();
            setProject(updatedData);
        } else {
            alert('申請送出失敗，請稍後再試。');
            console.error(await response.json());
        }
    };

    if (!project) {
        return <div>Loading...</div>;
    }

    // --- 變更點 2: 將判斷邏輯移到 return 陳述式之前 ---
    // 確保在 project 資料載入完成後才進行判斷，避免錯誤
    const hasApplied = user && project.applicants.includes(user.user_id);
    const isFull = project.application_count >= project.participant_limit;

    return (
        <div>
            <h1>{project.title}</h1>
            <div className="project-card" style={{ textAlign: 'left', marginBottom: '2rem' }}>
                <p><strong>主題類別：</strong> {project.subject}</p>
                <p><strong>計畫簡介：</strong> {project.description}</p>
                <p><strong>人數限制：</strong> {project.participant_limit} 人</p>
                {/* --- 變更點 3: 顯示目前報名人數與是否額滿 --- */}
                <p><strong>目前報名/人數上限：</strong> {project.application_count} / {project.participant_limit} {isFull ? <span style={{color: 'red'}}>(已額滿)</span> : ''}</p>
                <p><strong>其他限制：</strong> {project.restrictions || '無'}</p>
                <p><strong>狀態：</strong> {project.status}</p>
            </div>

            {/* --- 變更點 4: 升級條件式渲染，加入已報名和已額滿的判斷 --- */}
            {user && user.user_type === 'school' && (
                <div>
                    {hasApplied ? (
                        <p style={{ color: 'green', fontWeight: 'bold', fontSize: '1.2rem' }}>您已報名成功！</p>
                    ) : isFull ? (
                        <p style={{ color: 'red', fontWeight: 'bold', fontSize: '1.2rem' }}>此活動報名已額滿。</p>
                    ) : !showForm ? (
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