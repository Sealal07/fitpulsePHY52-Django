import { useState, useEffect } from 'react';
import api from '../api/client';

export default function PRs() {
  const [prs, setPrs] = useState([]);

  useEffect(() => {
    api.get('/api/prs/').then((res) =>
      setPrs(res.data.results || res.data)
    );
  }, []);

  const formatDate = (iso) => {
    return new Date(iso).toLocaleDateString('ru-RU');
  };

  return (
    <div className="prs-page">
      <h2>Личные рекорды</h2>
      <table className="sets-table">
        <thead>
          <tr>
            <th>Упражнение</th>
            <th>Вес</th>
            <th>1RM</th>
            <th>Дата</th>
          </tr>
        </thead>
        <tbody>
          {prs.length > 0 ? (
            prs.map((pr) => (
              <tr key={pr.id}>
                <td>{pr.exercise_name}</td>
                <td>{pr.weight} кг</td>
                <td><b>{pr.estimated_1rm} кг</b></td>
                <td>{formatDate(pr.achieved_at)}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="muted">Рекордов пока нет - добавьте подход!</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}