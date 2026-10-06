const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    startAudit: () => ipcRenderer.send('start-audit-command'),
    onAuditSuccess: (callback) => ipcRenderer.on('audit-success', (_event, value) => callback(value)),
    openReport: (path) => ipcRenderer.send('open-report', path)
});