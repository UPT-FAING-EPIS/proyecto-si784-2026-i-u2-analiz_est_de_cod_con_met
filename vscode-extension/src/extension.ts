import * as vscode from 'vscode';
import axios from 'axios';
import FormData from 'form-data';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    console.log('Felicidades, tu extensión "upt-code-analyzer" ahora está activa.');

    let disposable = vscode.commands.registerCommand('uptAnalyzer.analyzeFile', async () => {
        const editor = vscode.window.activeTextEditor;

        if (!editor) {
            vscode.window.showErrorMessage('No hay ningún archivo abierto para analizar.');
            return;
        }

        const document = editor.document;
        const filePath = document.fileName;
        const fileName = path.basename(filePath);
        const fileContent = document.getText();
        
        // Extensiones soportadas
        const ext = path.extname(fileName).toLowerCase();
        const validExtensions = ['.java', '.cs', '.py', '.php', '.js', '.ts', '.jsx', '.tsx', '.c', '.cpp', '.h', '.go', '.rb', '.rs'];
        
        if (!validExtensions.includes(ext)) {
            vscode.window.showErrorMessage(`Extensión no soportada para análisis estático: ${ext}. Soportadas: ${validExtensions.join(', ')}`);
            return;
        }

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `Analizando ${fileName}...`,
            cancellable: false
        }, async (progress) => {
            try {
                // Preparar FormData
                const formData = new FormData();
                formData.append('project_name', `VSCode_${fileName}`);
                formData.append('files', Buffer.from(fileContent, 'utf-8'), {
                    filename: fileName,
                    contentType: 'text/plain',
                });

                // Enviar la petición POST al backend en Render
                const headers = formData.getHeaders();
                try {
                    headers['Content-Length'] = formData.getLengthSync();
                } catch (e) {
                    console.warn('No se pudo calcular Content-Length de forma síncrona');
                }

                const response = await axios.post('https://anestatico.onrender.com/api/analysis/external/upload_folder', formData, {
                    headers: headers,
                    timeout: 30000 // 30 segundos máximo de espera
                });

                const data = response.data;

                if (data.status === 'success') {
                    // Mostrar resultados
                    showResultsPanel(context, fileName, data);
                    vscode.window.showInformationMessage(`¡Análisis exitoso para ${fileName}!`);
                } else {
                    vscode.window.showErrorMessage('Error al analizar el código: La respuesta no fue exitosa.');
                }
            } catch (error: any) {
                console.error(error);
                vscode.window.showErrorMessage(`Error de conexión con el analizador: ${error.message}`);
            }
        });
    });

    context.subscriptions.push(disposable);
}

function showResultsPanel(context: vscode.ExtensionContext, fileName: string, data: any) {
    const panel = vscode.window.createWebviewPanel(
        'uptAnalyzerResults',
        `Resultados: ${fileName}`,
        vscode.ViewColumn.Beside,
        {}
    );

    panel.webview.html = getWebviewContent(fileName, data);
}

function getWebviewContent(fileName: string, data: any) {
    const smellsArray = data.code_smells && data.code_smells.smells 
        ? data.code_smells.smells 
        : (Array.isArray(data.code_smells) ? data.code_smells : []);

    const codeSmellsHtml = smellsArray.length > 0 
        ? smellsArray.map((smell: any) => `<li>${typeof smell === 'string' ? smell : JSON.stringify(smell)}</li>`).join('') 
        : '<li>No se detectaron Code Smells críticos.</li>';

    const metrics = data.code_smells && data.code_smells.metrics ? data.code_smells.metrics : {};

    return `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados de Análisis</title>
    <style>
        body { font-family: var(--vscode-font-family); padding: 20px; color: var(--vscode-editor-foreground); background-color: var(--vscode-editor-background); }
        h1 { color: var(--vscode-textLink-foreground); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .metric-card {
            background-color: var(--vscode-editorWidget-background);
            border: 1px solid var(--vscode-widget-border);
            border-radius: 6px;
            padding: 15px;
        }
        .metric-title { font-size: 1.1em; margin-bottom: 5px; font-weight: bold; }
        .metric-value { font-size: 1.8em; color: var(--vscode-terminal-ansiGreen); }
        .smells-list { background-color: var(--vscode-input-background); padding: 15px; border-radius: 6px; border-left: 4px solid var(--vscode-terminal-ansiYellow); }
        ul { padding-left: 20px; }
        li { margin-bottom: 10px; line-height: 1.4; }
    </style>
</head>
<body>
    <h1>UPT Analyzer Report</h1>
    <h2>Archivo: ${fileName}</h2>
    
    <div class="grid">
        <div class="metric-card">
            <div class="metric-title">Líneas (LOC / CLOC)</div>
            <div class="metric-value">${data.loc} / ${metrics.cloc !== undefined ? metrics.cloc : 'N/A'}</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-title">Complejidad</div>
            <div class="metric-value" style="color: ${data.complexity > 10 ? 'var(--vscode-terminal-ansiRed)' : 'var(--vscode-terminal-ansiGreen)'};">${data.complexity}</div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Métodos (Total / Pub)</div>
            <div class="metric-value">${metrics.nom !== undefined ? metrics.nom : 'N/A'} / ${metrics.npm !== undefined ? metrics.npm : 'N/A'}</div>
        </div>

        <div class="metric-card">
            <div class="metric-title">Atributos (NOA)</div>
            <div class="metric-value">${metrics.noa !== undefined ? metrics.noa : 'N/A'}</div>
        </div>
    </div>
    
    <div class="metric-card" style="grid-column: 1 / -1;">
        <div class="metric-title">Code Smells Encontrados</div>
        <div class="smells-list">
            <ul>
                ${codeSmellsHtml}
            </ul>
        </div>
    </div>
</body>
</html>`;
}

export function deactivate() {}
