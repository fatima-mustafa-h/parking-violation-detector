const canvas = document.getElementById('zoneCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let currentZone = [];
let zones = [];

canvas.addEventListener('mousedown', (e) => {
  drawing = true;
  currentZone = [{x: e.offsetX, y: e.offsetY}];
});

canvas.addEventListener('mousemove', (e) => {
  if (!drawing) return;
  currentZone.push({x: e.offsetX, y: e.offsetY});
  redraw();
});

canvas.addEventListener('mouseup', (e) => {
  drawing = false;
  zones.push(currentZone);
  currentZone = [];
  redraw();
});

function redraw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
  zones.forEach(zone => {
    ctx.beginPath();
    zone.forEach((point, index) => {
      if (index === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    });
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  });
  if (currentZone.length > 0) {
    ctx.beginPath();
    currentZone.forEach((point, index) => {
      if (index === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    });
    ctx.stroke();
  }
}

document.getElementById('saveZones').addEventListener('click', () => {
  fetch('/set_zones', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({zones})
  })
  .then(res => res.json())
  .then(data => alert(data.status))
  .catch(() => alert('Failed to save zones'));
});
