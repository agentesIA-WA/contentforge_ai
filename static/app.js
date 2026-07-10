const methodInput = document.getElementById('method');
const pathInput = document.getElementById('path');
const bodyInput = document.getElementById('body');
const sendButton = document.getElementById('sendRequest');
const responseEl = document.getElementById('response');
const statusEl = document.getElementById('status');
const timeEl = document.getElementById('time');
const quickHealth = document.getElementById('quickHealth');
const quickDocs = document.getElementById('quickDocs');
const shortcuts = document.querySelectorAll('.link-button');

const empresaIdInput = document.getElementById('empresaId');
const agenteInput = document.getElementById('agente');
const tipoPromptInput = document.getElementById('tipoPrompt');
const conteudoPromptInput = document.getElementById('conteudoPrompt');
const modeloIaInput = document.getElementById('modeloIa');
const createGenerateButton = document.getElementById('createGenerate');
const genResponseEl = document.getElementById('genResponse');
const genStatusEl = document.getElementById('genStatus');

function formatJson(value) {
  try {
    return JSON.stringify(JSON.parse(value), null, 2);
  } catch {
    return value;
  }
}

async function sendRequest() {
  const method = methodInput.value;
  const path = pathInput.value.trim();
  let body = bodyInput.value.trim();
  const url = path.startsWith('http') ? path : path;

  let options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  };

  if (method !== 'GET' && body) {
    try {
      options.body = JSON.stringify(JSON.parse(body));
    } catch (error) {
      responseEl.textContent = 'Corpo JSON inválido: ' + error.message;
      return;
    }
  }

  const startTime = performance.now();
  try {
    const res = await fetch(url, options);
    const elapsed = Math.round(performance.now() - startTime);
    statusEl.textContent = `Status: ${res.status} ${res.statusText}`;
    timeEl.textContent = `Tempo: ${elapsed} ms`;
    const text = await res.text();
    try {
      const parsed = JSON.parse(text);
      responseEl.textContent = JSON.stringify(parsed, null, 2);
    } catch {
      responseEl.textContent = text;
    }
  } catch (error) {
    statusEl.textContent = 'Status: erro';
    timeEl.textContent = '';
    responseEl.textContent = error.message;
  }
}

sendButton.addEventListener('click', sendRequest);
quickHealth.addEventListener('click', () => {
  methodInput.value = 'GET';
  pathInput.value = '/api/v1/health';
  bodyInput.value = '';
  sendRequest();
});
quickDocs.addEventListener('click', () => {
  window.location.href = '/docs';
});
shortcuts.forEach((button) => {
  button.addEventListener('click', () => {
    methodInput.value = 'GET';
    pathInput.value = button.dataset.path;
    bodyInput.value = '';
  });
});


async function createAndGenerate() {
  const empresa_id = empresaIdInput.value.trim();
  const agente = agenteInput.value.trim() || 'writer';
  const tipo = tipoPromptInput.value.trim() || 'conteudo';
  const conteudo = conteudoPromptInput.value.trim();
  const modelo_ia = modeloIaInput.value.trim() || undefined;

  if (!empresa_id) {
    genStatusEl.textContent = 'Status: informe empresa_id';
    return;
  }

  genStatusEl.textContent = 'Status: criando...';

  try {
    const createRes = await fetch('/api/v1/prompts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ empresa_id, agente, tipo, conteudo, modelo_ia }),
    });

    if (!createRes.ok) {
      const err = await createRes.text();
      genStatusEl.textContent = 'Status: erro ao criar';
      genResponseEl.textContent = err;
      return;
    }

    const prompt = await createRes.json();
    genStatusEl.textContent = 'Status: enviado';

    // trigger generation
    const genRes = await fetch(`/api/v1/prompts/${prompt.id}/gerar`, { method: 'POST' });
    const genJson = await genRes.json();

    genStatusEl.textContent = `Status: ${genJson.status}`;
    genResponseEl.textContent = JSON.stringify(genJson.resposta, null, 2);
  } catch (error) {
    genStatusEl.textContent = 'Status: erro';
    genResponseEl.textContent = error.message;
  }
}

createGenerateButton.addEventListener('click', createAndGenerate);
