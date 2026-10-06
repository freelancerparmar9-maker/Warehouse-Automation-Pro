const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 600,
        height: 500,
        webPreferences: {
            // This connects your button in index.html to this file
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    win.loadFile(path.join(__dirname, 'index.html'));
}

// This listens for the "Run Audit" button click from your UI
ipcMain.on('start-audit-command', (event) => {
    console.log("Button clicked! Starting Local Audit Engine...");

    const command = 'py engine/report.py';
    console.log(`Executing command: ${command}`);

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Execution Error: ${error.message}`);
            event.reply('audit-success', { error: `Error: ${error.message}` });
            return;
        }

        if (stderr) {
            console.log(`Python Log: ${stderr}`);
        }

        try {
            const data = JSON.parse(stdout.trim());
            event.reply('audit-success', data);
        } catch (e) {
            console.error(`Failed to parse output: ${stdout}`);
            event.reply('audit-success', { error: `Error parsing engine output.` });
        }
    });
});

const { shell } = require('electron');
ipcMain.on('open-report', (event, reportPath) => {
    shell.openPath(reportPath);
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});