import { useState, useEffect } from 'react';
import api from '../api/client';

export default function Templates() {
  const [templates, setTemplates] = useState([]);
  const [exercises, setExercises] = useState([]); // справочник упражнений
  const [selectedId, setSelectedId] = useState(null);
  const [selected, setSelected] = useState(null);
  const [newName, setNewName] = useState('');

  // Для добавления упражнения в шаблон
  const [newExerciseId, setNewExerciseId] = useState('');

  useEffect(() => {
    loadTemplates();
    loadExercises();
  }, []);

  const loadTemplates = async () => {
    const res = await api.get('/api/templates/');
    setTemplates(res.data.results || res.data);
  };

  const loadExercises = async () => {
    const res = await api.get('/api/exercises/');
    setExercises(res.data.results || res.data);
  };

  const loadSelected = async (id) => {
    const res = await api.get(`/api/templates/${id}/`);
    setSelected(res.data);
    setSelectedId(id);
  };

  const createTemplate = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    const res = await api.post('/api/templates/', { name: newName });
    setNewName('');
    await loadTemplates();
    await loadSelected(res.data.id);
  };

  const deleteTemplate = async (id) => {
    if (!confirm('Удалить шаблон?')) return;
    await api.delete(`/api/templates/${id}/`);
    if (selectedId === id) {
      setSelected(null);
      setSelectedId(null);
    }
    await loadTemplates();
  };

  const addExerciseToTemplate = async (e) => {
    e.preventDefault();
    if (!newExerciseId || !selectedId) return;
    await api.post(`/api/templates/${selectedId}/exercises/`, {
      exercise: Number(newExerciseId),
    });
    setNewExerciseId('');
    await loadSelected(selectedId);
  };

  const removeExerciseFromTemplate = async (exId) => {
    if (!selectedId) return;
    await api.delete(`/api/templates/${selectedId}/exercises/${exId}/`);
    await loadSelected(selectedId);
  };

  return (
    <div className="templates-page">
      <div className="templates-sidebar">
        <h2>Мои программы</h2>
        <form onSubmit={createTemplate} className="inline-form">
          <input
            type="text"
            placeholder="Название программы"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
          <button type="submit" className="primary">+</button>
        </form>
        <ul className="list">
          {templates.map((t) => (
            <li
              key={t.id}
              className={selectedId === t.id ? 'active' : ''}
              onClick={() => loadSelected(t.id)}
            >
              <span>{t.name}</span>
              <button
                className="danger small"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteTemplate(t.id);
                }}
              >
                ✕
              </button>
            </li>
          ))}
          {templates.length === 0 && <li className="muted">Пока нет программ</li>}
        </ul>
      </div>

      <div className="templates-editor">
        {selected ? (
          <>
            <h2>{selected.name}</h2>
            <h3>Упражнения</h3>
            <ul className="list">
              {selected.exercises.map((ex) => (
                <li key={ex.id}>
                  <span>
                    <b>#{ex.order}</b> {ex.exercise_name}
                  </span>
                  <button
                    className="danger small"
                    onClick={() => removeExerciseFromTemplate(ex.id)}
                  >
                    ✕
                  </button>
                </li>
              ))}
              {selected.exercises.length === 0 && (
                <li className="muted">Добавьте упражнения</li>
              )}
            </ul>

            <form onSubmit={addExerciseToTemplate} className="inline-form">
              <select
                value={newExerciseId}
                onChange={(e) => setNewExerciseId(e.target.value)}
              >
                <option value="">— выберите упражнение —</option>
                {exercises.map((ex) => (
                  <option key={ex.id} value={ex.id}>
                    {ex.name} ({ex.muscle_group_name})
                  </option>
                ))}
              </select>
              <button type="submit" className="primary">Добавить</button>
            </form>
          </>
        ) : (
          <div className="muted">Выберите или создайте программу слева</div>
        )}
      </div>
    </div>
  );
}