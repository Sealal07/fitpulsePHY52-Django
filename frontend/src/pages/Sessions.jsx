import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

export default function Sessions() {
  const [sessions, setSessions] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [newName, setNewName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadSessions();
    api.get('/api/templates/').then((res) =>
      setTemplates(res.data.results || res.data)
    );
  }, []);

  const loadSessions = async () => {
    const res = await api.get('/api/sessions/');
    setSessions(res.data.results || res.data);
  };

  const startSession = async (e) => {
    e.preventDefault();
    const name = newName.trim() || (selectedTemplate
      ? templates.find((t) => t.id === Number(selectedTemplate))?.name
      : 'Тренировка');
    const payload = { name };
    if (selectedTemplate) payload.template = Number(selectedTemplate);
    const res = await api.post('/api/sessions/', payload);
    navigate(`/sessions/${res.data.id}`);
  };

  const deleteSession = async (id) => {
    if (!confirm('Удалить тренировку?')) return;
    await api.delete(`/api/sessions/${id}/`);
    await loadSessions();
  };

  const formatDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleString('ru-RU', { dateStyle: 'short', timeStyle: 'short' });
  };

  return (
    <div className="sessions-page">
      <h2>Мои тренировки</h2>

      <form onSubmit={startSession} className="start-form">
        <input
          type="text"
          placeholder="Название (необязательно)"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <select
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
        >
          <option value="">— без шаблона —</option>
          {templates.map((t) => (
            <option key={t.id} value={t.id}>{t.name}</option>
          ))}
        </select>
        <button type="submit" className="primary">Начать тренировку</button>
      </form>

      <ul className="list">
        {sessions.map((s) => (
          <li key={s.id} onClick={() => navigate(`/sessions/${s.id}`)}>
            <div>
              <b>{s.name}</b>
              <div className="muted small">{formatDate(s.date)}</div>
              {s.template_name && (
                <div className="muted small">по шаблону: {s.template_name}</div>
              )}
            </div>
            <button
              className="danger small"
              onClick={(e) => {
                e.stopPropagation();
                deleteSession(s.id);
              }}
            >
              ✕
            </button>
          </li>
        ))}
        {sessions.length === 0 && <li className="muted">Пока нет тренировок</li>}
      </ul>
    </div>
  );
}