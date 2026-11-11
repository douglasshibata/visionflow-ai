const canvas = document.getElementById('video-canvas');
const ctx = canvas.getContext('2d');
let currentDetections = [];

const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const wsHost = window.location.hostname || 'localhost';
const wsPort = window.location.port || (wsProtocol === 'wss:' ? '443' : '80');

const client = new StompJs.Client({
    brokerURL: `${wsProtocol}//${wsHost}:${wsPort}/ws-vision`,
    onConnect: () => {
        console.log('Connected to VisionFlow WebSocket');
        document.getElementById('status').innerText = 'Conectado';
        document.getElementById('status').classList.remove('bg-red-600');
        document.getElementById('status').classList.add('bg-green-600');

        // Subscribe to live frames
        client.subscribe('/topic/frames', (message) => {
            const frame = JSON.parse(message.body);
            renderFrame(frame.base64);
        });

        // Subscribe to detections
        client.subscribe('/topic/detections', (message) => {
            const data = JSON.parse(message.body);
            currentDetections = data.detections || [];
            processAlerts(data);
        });
    },
    onDisconnect: () => {
        document.getElementById('status').innerText = 'Desconectado';
        document.getElementById('status').classList.add('bg-red-600');
        document.getElementById('status').classList.remove('bg-green-600');
    }
});

client.activate();

function renderFrame(base64) {
    const img = new Image();
    img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        // Render overlays
        drawDetections();
    };
    img.src = 'data:image/jpeg;base64,' + base64;
}

function drawDetections() {
    currentDetections.forEach(det => {
        const [x1, y1, x2, y2] = det.bbox;

        // Bounding Box
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        // Label
        ctx.fillStyle = '#00ff00';
        ctx.font = '16px Arial';
        ctx.fillText(`${det.class} (${(det.confidence * 100).toFixed(0)}%)`, x1, y1 - 5);
    });
}

function processAlerts(data) {
    if (data.detections && data.detections.length > 0) {
        data.detections.forEach(det => {
            if (det.confidence > 0.5) {
                addAlert({
                    object: det.class,
                    confidence: det.confidence,
                    cameraId: data.cameraId,
                    type: data.alertType || 'info'
                });
            }
        });
    }
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function addAlert(data) {
    const alertsContainer = document.getElementById('alerts');
    const alertDiv = document.createElement('div');

    let borderColor = 'border-blue-500';
    let bgColor = 'bg-gray-700';

    if (data.type === 'safety') {
        borderColor = 'border-red-500';
        bgColor = 'bg-red-900/20';
    } else if (data.type === 'quality') {
        borderColor = 'border-yellow-500';
        bgColor = 'bg-yellow-900/20';
    }

    alertDiv.className = `p-3 rounded-md ${bgColor} border-l-4 ${borderColor} mb-2`;

    // Use createElement + textContent instead of innerHTML to prevent XSS
    const headerDiv = document.createElement('div');
    headerDiv.className = 'flex justify-between items-start';

    const objectSpan = document.createElement('span');
    objectSpan.className = 'font-bold text-sm text-white';
    objectSpan.textContent = data.object.toUpperCase();

    const timeSpan = document.createElement('span');
    timeSpan.className = 'text-xs text-gray-400';
    timeSpan.textContent = new Date().toLocaleTimeString();

    headerDiv.appendChild(objectSpan);
    headerDiv.appendChild(timeSpan);

    const detailP = document.createElement('p');
    detailP.className = 'text-xs text-gray-300';
    detailP.textContent = `Confiança: ${(data.confidence * 100).toFixed(1)}%`;

    alertDiv.appendChild(headerDiv);
    alertDiv.appendChild(detailP);

    alertsContainer.prepend(alertDiv);

    if (alertsContainer.children.length > 15) {
        alertsContainer.removeChild(alertsContainer.lastChild);
    }
}
