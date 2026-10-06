const { google } = require('googleapis');
const path = require('path');

async function refineAuditLog() {
    console.log('Starting refinement process...');
    const spreadsheetId = '1mT0Gzw3ugx16_tFGytU9hoDHO8bx6skqkLyrm8pDiVA';
    const credentialsPath = path.resolve('credentials.json');
    const tabName = 'Audit_Log';

    console.log(`Using credentials from: ${credentialsPath}`);
    const auth = new google.auth.GoogleAuth({
        keyFile: credentialsPath,
        scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    console.log('Initializing Google Sheets client...');
    const sheets = google.sheets({ version: 'v4', auth });

    try {
        console.log('Fetching spreadsheet metadata...');
        const spreadsheet = await sheets.spreadsheets.get({ spreadsheetId });
        console.log('Sheet metadata received.');

        const sheet = spreadsheet.data.sheets.find(s => s.properties.title === tabName);
        if (!sheet) {
            throw new Error(`Tab '${tabName}' not found.`);
        }
        const sheetId = sheet.properties.sheetId;
        console.log(`Found sheet '${tabName}' with ID: ${sheetId}`);

        console.log('Executing batchUpdate to delete Row 2 and set headers...');
        await sheets.spreadsheets.batchUpdate({
            spreadsheetId,
            resource: {
                requests: [
                    {
                        deleteDimension: {
                            range: {
                                sheetId: sheetId,
                                dimension: 'ROWS',
                                startIndex: 1, // Row 2 (0-indexed)
                                endIndex: 2    // Row 3 (exclusive)
                            }
                        }
                    },
                    {
                        updateCells: {
                            range: {
                                sheetId: sheetId,
                                startRowIndex: 0,
                                endRowIndex: 1,
                                startColumnIndex: 0,
                                endColumnIndex: 5
                            },
                            rows: [{
                                values: [
                                    { userEnteredValue: { stringValue: 'PO Number' } },
                                    { userEnteredValue: { stringValue: 'Item Name' } },
                                    { userEnteredValue: { stringValue: 'Invoice Qty' } },
                                    { userEnteredValue: { stringValue: 'Packing List Qty' } },
                                    { userEnteredValue: { stringValue: 'Status' } }
                                ]
                            }],
                            fields: 'userEnteredValue'
                        }
                    }
                ]
            }
        });
        console.log('batchUpdate successful.');

        const po = 'PO-45672';
        const data = [
            [po, 'Steel Bolts M8', 100, 100, 'MATCH'],
            [po, 'Nylon Washers', 200, 150, 'DISCREPANCY (UNDER_SHIP)'],
            [po, 'Packing Tape Roll', 50, 50, 'MATCH']
        ];

        console.log('Writing structured audit results...');
        await sheets.spreadsheets.values.update({
            spreadsheetId,
            range: `${tabName}!A2:E4`,
            valueInputOption: 'RAW',
            resource: {
                values: data
            }
        });
        console.log('Data write successful.');

        console.log('Refinement complete.');

    } catch (error) {
        console.error('Error details:', error);
        process.exit(1);
    }
}

refineAuditLog();
