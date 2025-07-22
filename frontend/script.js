document.getElementById('leadForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const payload = {
    email: document.getElementById('email').value,
    credit_score: parseInt(document.getElementById('credit_score').value),
    age_group: document.getElementById('age_group').value,
    family: document.getElementById('family').value,
    income: parseInt(document.getElementById('income').value),
    comments: document.getElementById('comments').value,
    consent: document.getElementById('consent').checked
  };

  const response = await fetch('http://127.0.0.1:8000/score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const result = await response.json();

  if (result.error) {
    alert(result.error);
    return;
  }

  const table = document.getElementById('resultsTable');
  const row = table.insertRow();
  row.innerHTML = `
    <td>${result.email}</td>
    <td>${result.initial_score}</td>
    <td>${result.reranked_score}</td>
    <td>${result.comments}</td>
  `;
});