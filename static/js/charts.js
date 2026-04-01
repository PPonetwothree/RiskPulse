/**
 * charts.js — Canvas-based phosphor-green chart renderer
 * Draws ASCII-style line charts for forecast data
 */

const Charts = (() => {
    const COLORS = {
        bg: '#000000',
        grid: '#1a1a1a',
        axis: '#333333',
        label: '#555555',
        arima: '#0077ff',
        prophet: '#00cc66',
        lstm: '#ff8800',
        ensemble: '#00ffff',
        phGlow: '#00ff00',
    };

    function drawForecastChart(canvas, data) {
        const { arima = [], prophet = [], lstm = [], ensemble = [], baseline = 0 } = data;
        const allVals = [...arima, ...prophet, ...lstm, ...ensemble, baseline];
        if (allVals.length === 0) return;

        const ctx = canvas.getContext('2d');
        const W = canvas.offsetWidth || 300;
        const H = 100;
        canvas.width = W;
        canvas.height = H;

        const pad = { top: 10, right: 8, bottom: 24, left: 36 };
        const chartW = W - pad.left - pad.right;
        const chartH = H - pad.top - pad.bottom;

        const maxV = Math.max(...allVals) * 1.1;
        const minV = Math.max(0, Math.min(...allVals) * 0.85);
        const range = maxV - minV || 1;

        const toX = (i, total) => pad.left + (i / (total - 1)) * chartW;
        const toY = (v) => pad.top + chartH - ((v - minV) / range) * chartH;

        // Background
        ctx.fillStyle = COLORS.bg;
        ctx.fillRect(0, 0, W, H);

        // Grid lines
        ctx.strokeStyle = COLORS.grid;
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = pad.top + (i / 4) * chartH;
            ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y);
            ctx.stroke();
        }

        // Baseline dashed line
        const baseY = toY(baseline);
        ctx.strokeStyle = '#333';
        ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.moveTo(pad.left, baseY); ctx.lineTo(W - pad.right, baseY);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#444';
        ctx.font = '8px Courier New';
        ctx.fillText('BASE', pad.left + 2, baseY - 2);

        // Y axis labels
        ctx.fillStyle = COLORS.label;
        ctx.font = '8px Courier New';
        ctx.textAlign = 'right';
        for (let i = 0; i <= 4; i++) {
            const v = minV + (range * i / 4);
            const y = pad.top + chartH - (i / 4) * chartH;
            ctx.fillText(v.toFixed(0), pad.left - 4, y + 3);
        }

        // X axis labels (D+0..D+6)
        ctx.textAlign = 'center';
        const days = ensemble.length || arima.length;
        for (let i = 0; i < days; i++) {
            ctx.fillStyle = COLORS.label;
            ctx.fillText(`D+${i}`, toX(i, days), H - 6);
        }

        // Draw series
        function drawLine(vals, color, lineWidth = 1.5, glowColor = null) {
            if (!vals || vals.length === 0) return;
            if (glowColor) {
                ctx.shadowColor = glowColor;
                ctx.shadowBlur = 4;
            }
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.lineWidth = lineWidth;
            vals.forEach((v, i) => {
                const x = toX(i, vals.length);
                const y = toY(v);
                if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            });
            ctx.stroke();
            ctx.shadowBlur = 0;

            // Dots
            vals.forEach((v, i) => {
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(toX(i, vals.length), toY(v), 2, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        drawLine(arima, COLORS.arima, 1);
        drawLine(prophet, COLORS.prophet, 1);
        drawLine(lstm, COLORS.lstm, 1);
        drawLine(ensemble, COLORS.ensemble, 2, '#00ffff');

        // Legend
        const legend = [
            { color: COLORS.arima, label: 'ARIMA' },
            { color: COLORS.prophet, label: 'PROPHТ' },
            { color: COLORS.lstm, label: 'LSTM' },
            { color: COLORS.ensemble, label: 'ENS' },
        ];
        ctx.font = '8px Courier New';
        ctx.textAlign = 'left';
        let lx = pad.left;
        legend.forEach(({ color, label }) => {
            ctx.fillStyle = color;
            ctx.fillRect(lx, 2, 8, 3);
            ctx.fillStyle = '#666';
            ctx.fillText(label, lx + 10, 9);
            lx += label.length * 5 + 20;
        });
    }

    return { drawForecastChart };
})();
