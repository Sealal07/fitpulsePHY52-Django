import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/client';

export default function SessionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [exercises, setExercises] = useState([]);
  const [selectedExercise, setSelectedExercise] = useState('');
  const [weight, setWeight] = useState('');
  const [reps, setReps] = useState('');
  const [lastIsPr, setLastIsPr] = useState(false);
  const [lastPrName, setLastPrName] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadSession();
    api.get('/api/exercises/').then((res) =>
      setExercises(res.data.results || res.data)
    );
  }, [id]);

  const loadSession = async () => {
    const res = await api.get(`/api/sessions/${id}/`);
    setSession(res.data);
  };

  const addSet = async (e) => {
    e.preventDefault();
    setError('');
    setLastIsPr(false);
    if (!selectedExercise || !weight || !reps) {
      setError('Заполните все поля');
      return;
    }
    try {
      const res = await api.post('/api/sets/', {
        session: Number(id),
        exercise: Number(selectedExercise),
        weight: Number(weight),
        reps: Number(reps),
      });
      // res.data содержит { ..., is_pr, exercise_name }
      if (res.data.is_pr) {
        setLastIsPr(true);
        setLastPrName(res.data.exercise_name);
        // Автоскрытие баннера через 4 секунды
        setTimeout(() => setLastIsPr(false), 4000);
      }
      setWeight('');
      setReps('');
      await loadSession();
    } catch (err) {
      const data = err.response?.data;
      setError(
        data ? Object.values(data).flat().join('; ') : 'Ошибка добавления подхода'
      );
    }
  };

  if (!session) return <div className="muted">Загрузка...</div>;

  // Упражнения, доступные для выбора: из шаблона (если есть) + все остальные
  const templateExerciseIds = session.sets
    ? [...new Set(session.sets.map((s) => s.exercise))]
    : [];
  const availableExercises = exercises.filter(
    (ex) =>
      !session.template || // если шаблона нет - все доступны
      templateExerciseIds.includes(ex.id) || // уже использовались
      true 
  );

  return (
    <div className="session-page">
      <div className="session-header">
        <button onClick={() => navigate('/sessions')} className="back">
          ← Назад
        </button>
        <h2>{session.name}</h2>
        {session.template_name && (
          <div className="muted small">по шаблону: {session.template_name}</div>
        )}
      </div>

      {lastIsPr && (
        <div className="pr-banner">
          Новый личный рекорд в упражнении «{lastPrName}»!
        </div>
      )}

      <form onSubmit={addSet} className="set-form">
        <select
          value={selectedExercise}
          onChange={(e) => setSelectedExercise(e.target.value)}
        >
          <option value="">— упражнение —</option>
          {availableExercises.map((ex) => (
            <option key={ex.id} value={ex.id}>{ex.name}</option>
          ))}
        </select>
        <input
          type="number"
          step="0.5"
          min="0"
          placeholder="Вес, кг"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />
        <input
          type="number"
          min="1"
          placeholder="Повторы"
          value={reps}
          onChange={(e) => setReps(e.target.value)}
        />
        <button type="submit" className="primary">Добавить подход</button>
      </form>

      {error && <div className="error">{error}</div>}

      <h3>Подходы</h3>
      <table className="sets-table">
        <thead>
          <tr>
            <th>Упражнение</th>
            <th>Вес</th>
            <th>Повторы</th>
            <th>1RM (оценка)</th>
          </tr>
        </thead>
        <tbody>
          {session.sets && session.sets.length > 0 ? (
            session.sets.map((s) => (
              <tr key={s.id}>
                <td>{s.exercise_name}</td>
                <td>{s.weight} кг</td>
                <td>{s.reps}</td>
                <td><b>{s.estimated_1rm} кг</b></td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="muted">Пока нет подходов</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}