// Application state
let isExporting = false;
let statusInterval = null;

// DOM elements
const startBtn = document.getElementById('startBtn');
const cancelBtn = document.getElementById('cancelBtn');
const dbPath = document.getElementById('dbPath');
const browseBtn = document.getElementById('browseBtn');
const fileInput = document.getElementById('fileInput');
const progressBar = document.getElementById('progressBar');
const statusText = document.getElementById('statusText');
const progressText = document.getElementById('progressText');
const resultsCard = document.getElementById('resultsCard');
const resultsMessage = document.getElementById('resultsMessage');

// API endpoint base
const API_BASE = '/api';

// Event Listeners
startBtn.addEventListener('click', startExport);
cancelBtn.addEventListener('click', cancelExport);
browseBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);

// Use default path button
const useDefaultBtn = document.getElementById('useDefaultBtn');
if (useDefaultBtn) {
    useDefaultBtn.addEventListener('click', useDefaultPath);
}

// Use default Louvor JA path
function useDefaultPath() {
    const defaultPath = 'C:\\Program Files (x86)\\Louvor JA\\config\\database.db';
    dbPath.value = defaultPath;
    dbPath.dataset.file = '';
    dbPath.dataset.uploadFile = 'false';
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        dbPath.value = file.name;
        dbPath.dataset.file = 'selected';
        dbPath.dataset.uploadFile = 'true';
    }
}

// Show button loading state
function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        const spinner = document.createElement('span');
        spinner.className = 'spinner';
        button.prepend(spinner);
    } else {
        button.classList.remove('loading');
        const spinner = button.querySelector('.spinner');
        if (spinner) spinner.remove();
    }
}

// Start export
async function startExport() {
    let db_path = dbPath.value.trim();

    setButtonLoading(startBtn, true);

    try {
        // Check if user selected a file to upload
        if (dbPath.dataset.uploadFile === 'true' && fileInput.files.length > 0) {
            statusText.textContent = 'Enviando arquivo...';
            const uploadedPath = await uploadFile(fileInput.files[0]);
            if (!uploadedPath) {
                setButtonLoading(startBtn, false);
                return; // Error already shown
            }
            db_path = uploadedPath;
        }

        const response = await fetch(`${API_BASE}/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ db_path: db_path || undefined })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Erro ao iniciar exportação');
            setButtonLoading(startBtn, false);
            return;
        }

        // Update UI
        isExporting = true;
        startBtn.disabled = true;
        cancelBtn.disabled = false;
        resultsCard.style.display = 'none';

        // Start polling status
        startStatusPolling();

    } catch (error) {
        console.error('Error starting export:', error);
        alert('Erro ao conectar com o servidor');
        setButtonLoading(startBtn, false);
    }
}

// Upload file to server
async function uploadFile(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Erro ao enviar arquivo');
            return null;
        }

        return data.filepath;

    } catch (error) {
        console.error('Error uploading file:', error);
        alert('Erro ao enviar arquivo para o servidor');
        return null;
    }
}

// Cancel export
async function cancelExport() {
    setButtonLoading(cancelBtn, true);

    try {
        const response = await fetch(`${API_BASE}/cancel`, {
            method: 'POST'
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Erro ao cancelar exportação');
        }

        setButtonLoading(cancelBtn, false);

    } catch (error) {
        console.error('Error cancelling export:', error);
        alert('Erro ao conectar com o servidor');
        setButtonLoading(cancelBtn, false);
    }
}

// Start polling status
function startStatusPolling() {
    // Poll every 500ms
    statusInterval = setInterval(updateStatus, 500);
}

// Stop polling
function stopStatusPolling() {
    if (statusInterval) {
        clearInterval(statusInterval);
        statusInterval = null;
    }
}

// Update status from server
async function updateStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();

        // Update progress bar
        if (data.total > 0) {
            const percentage = (data.progress / data.total) * 100;
            progressBar.style.width = `${percentage}%`;
            progressText.textContent = `${data.progress} / ${data.total} músicas`;
        } else {
            progressBar.style.width = '0%';
            progressText.textContent = '0 / 0 músicas';
        }

        // Update status text
        statusText.textContent = data.message;

        // Check if export finished
        if (!data.running && isExporting) {
            isExporting = false;
            setButtonLoading(startBtn, false);
            startBtn.disabled = false;
            cancelBtn.disabled = true;
            stopStatusPolling();

            // Show results
            if (data.message.includes('✅')) {
                resultsCard.style.display = 'block';
                resultsMessage.textContent = data.message;

                // Load songs table
                setTimeout(() => loadSongsTable(), 500);
            }
        }

        // Add/remove loading animation
        if (data.running) {
            progressBar.classList.add('loading');
        } else {
            progressBar.classList.remove('loading');
        }

    } catch (error) {
        console.error('Error updating status:', error);
        // Don't stop polling on error, might be temporary
    }
}

// Download results as ZIP file
document.getElementById('downloadBtn')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    setButtonLoading(btn, true);

    try {
        // Trigger download from server
        window.location.href = `${API_BASE}/download`;

        // Remove loading after a delay
        setTimeout(() => setButtonLoading(btn, false), 1000);
    } catch (error) {
        console.error('Error downloading ZIP:', error);
        alert('Erro ao baixar arquivo ZIP');
        setButtonLoading(btn, false);
    }
});

// Load and display exported songs table
async function loadSongsTable() {
    try {
        const response = await fetch(`${API_BASE}/list`);
        const data = await response.json();

        if (!response.ok || !data.files || data.files.length === 0) {
            document.getElementById('songsTableCard').style.display = 'none';
            return;
        }

        const tbody = document.getElementById('songsTableBody');
        tbody.innerHTML = '';

        data.files.forEach((file, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td class="song-name" onclick="viewLyrics('${file.filename}')">${file.filename}</td>
                <td>${formatFileSize(file.size)}</td>
                <td>
                    <div class="action-btns">
                        <button class="btn-icon" onclick="downloadFile('${file.filename}')" title="Baixar">
                            📥
                        </button>
                        <button class="btn-icon" onclick="viewLyrics('${file.filename}')" title="Ver letra">
                            👁️
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });

        document.getElementById('songsTableCard').style.display = 'block';
        updateSearchCount();

    } catch (error) {
        console.error('Error loading songs table:', error);
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Search/filter table
document.getElementById('searchInput')?.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('#songsTableBody tr');

    rows.forEach(row => {
        const fileName = row.querySelector('.song-name').textContent.toLowerCase();
        if (fileName.includes(searchTerm)) {
            row.classList.remove('hidden');
        } else {
            row.classList.add('hidden');
        }
    });

    updateSearchCount();
});

// Update search result count
function updateSearchCount() {
    const total = document.querySelectorAll('#songsTableBody tr').length;
    const visible = document.querySelectorAll('#songsTableBody tr:not(.hidden)').length;
    const searchCount = document.getElementById('searchCount');

    if (searchCount) {
        if (visible === total) {
            searchCount.textContent = `${total} músicas`;
        } else {
            searchCount.textContent = `${visible} de ${total}`;
        }
    }
}

// View lyrics in modal
async function viewLyrics(filename) {
    const modal = document.getElementById('lyricsModal');
    modal.classList.add('show');

    // Show loading in modal
    document.getElementById('modalTitle').textContent = 'Carregando...';
    document.getElementById('modalLyrics').textContent = 'Carregando letra...';

    try {
        const response = await fetch(`${API_BASE}/file/${encodeURIComponent(filename)}`);
        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Erro ao carregar letra');
            closeLyricsModal();
            return;
        }

        // Update modal
        document.getElementById('modalTitle').textContent = filename;
        document.getElementById('modalLyrics').textContent = data.content;
        document.getElementById('modalDownloadBtn').onclick = () => downloadFile(filename);

    } catch (error) {
        console.error('Error viewing lyrics:', error);
        alert('Erro ao carregar letra da música');
        closeLyricsModal();
    }
}

// Close lyrics modal
function closeLyricsModal() {
    document.getElementById('lyricsModal').classList.remove('show');
}

// Close modal on click outside
document.getElementById('lyricsModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'lyricsModal') {
        closeLyricsModal();
    }
});

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeLyricsModal();
    }
});

// Download individual file
function downloadFile(filename) {
    window.location.href = `${API_BASE}/file/${encodeURIComponent(filename)}?download=true`;
}

// Initial status check
updateStatus();
