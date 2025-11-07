// 永続化された文書を格納 (LocalStorageからロード)
let persistentDocuments = []; 
// 貼り付け画像からOCR処理で生成された一時文書を格納
let ocrDocuments = []; 
    
// Tesseract Workerを初期化（OCR処理用）
let worker;
    
const PREVIEW_MAX_DOCS = 5; // コンテンツ表示エリアに表示する最大ファイル数

// クラウド（Gemini API）モデルのリストを定義 (モデル判別に利用)
const GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
];

// --- LocalStorageからの文書ロードとファイル一覧の表示 ---
function loadDocuments() {
    try {
        const storedDocs = localStorage.getItem('plowerRAGDocs');
        persistentDocuments = storedDocs ? JSON.parse(storedDocs) : [];
        updateFileListDisplay();
    } catch (e) {
        console.error("Failed to load documents from LocalStorage:", e);
        persistentDocuments = [];
    }
}
    
// --- LocalStorageへの文書保存 ---
function saveDocuments() {
    try {
        localStorage.setItem('plowerRAGDocs', JSON.stringify(persistentDocuments));
    } catch (e) {
        console.error("Failed to save documents to LocalStorage:", e);
    }
}
    
// LocalStorageをリセットする関数
function resetDocuments() {
    if (confirm("本当にRAGソース文書を全て削除しますか？\n（この操作は元に戻せません。アップロードされたファイルがLocalStorageから全て消去されます。）")) {
        try {
            // LocalStorageからキーを削除
            localStorage.removeItem('plowerRAGDocs');
            
            // アプリケーション内のデータをクリア
            persistentDocuments = [];
            ocrDocuments = [];
            document.getElementById('pasteArea').value = '';
            // OCR関連の表示もクリア
            clearOcrDisplay();

            // UIを更新
            updateFileListDisplay(); 
            
            alert("RAGソース文書を全てリセットしました。");
        } catch (e) {
            console.error("Failed to reset documents:", e);
            alert("リセット中にエラーが発生しました。");
        }
    }
}

// OCR/画像関連の表示をクリアするヘルパー関数
function clearOcrDisplay() {
    // 既存のOCR関連要素をクリア
    // 画像とステータスを両方削除します
    document.querySelectorAll('#fileContent img, #fileContent .ocr-status').forEach(el => el.remove());
}

// --- ファイル一覧表示の更新とクリックイベント設定 ---
function updateFileListDisplay() {
    const fileListUl = document.getElementById('fileListUl');
    const fileContentDiv = document.getElementById('fileContent');
    fileListUl.innerHTML = '';
    
    // ファイル名のリストを生成
    persistentDocuments.forEach((doc, index) => {
        const li = document.createElement('li');
        li.textContent = doc.name;
        li.title = doc.name; // ホバーでフルネームを表示
        li.dataset.docIndex = index;
        li.onclick = (e) => {
            // 選択されたファイルを表示するときは、OCR関連の要素をクリア
            clearOcrDisplay(); 
            showDocumentContent(e.target.dataset.docIndex);
        };
        fileListUl.appendChild(li);
    });
    
    // コンテンツ表示エリアの初期表示（最新の数ファイル）
    let initialContent = '<h3>RAGソース文書プレビュー (最新5件)</h3>\n';
    const recentDocs = persistentDocuments.slice(-PREVIEW_MAX_DOCS).reverse();
    
    if (recentDocs.length > 0) {
        recentDocs.forEach(doc => {
            // ファイル名と内容を分かりやすく表示
            initialContent += `<p><strong>【${doc.name}】</strong></p><pre>--- ファイル名: ${doc.name} ---\n${doc.content.slice(0, 300)}${doc.content.length > 300 ? '...' : ''}</pre>\n`;
        });
    } else {
        initialContent += '<p>現在RAGのソースとなる文書はありません。</p>';
    }
    fileContentDiv.innerHTML = initialContent;
    
    // OCRで残っている画像やステータスがあれば再挿入（これは初期表示時のみの特殊な対応）
    // clearOcrDisplay() でクリアされるため、通常は空になるはずですが、念のため
    const existingOcrContent = document.querySelectorAll('#fileContent img, #fileContent .ocr-status');
    existingOcrContent.forEach(el => fileContentDiv.prepend(el));
}

// --- ファイル名クリック時の内容表示 ---
function showDocumentContent(index) {
    const fileContentDiv = document.getElementById('fileContent');
    const doc = persistentDocuments[index];
    if (doc) {
        // 選択されたファイルの全文表示
        fileContentDiv.innerHTML = `<h3>選択中のファイル: ${doc.name}</h3><pre>${doc.content}</pre>`;
    }
}

// --- Tesseract.js OCR処理関数 (改善版: 詳細ステータス表示付き) ---
async function runOcrOnImage(base64Image, statusElement) {
    try {
        if (!worker) {
            statusElement.innerHTML = '<div class="spinner"></div> OCRワーカーを初期化中... (1/3 初回時間がかかります)';
            statusElement.style.color = 'orange';

            // Tesseract Workerの作成 (ロガーを設定)
            worker = await Tesseract.createWorker({
                logger: m => {
                    const progress = Math.round(m.progress * 100);
                    let statusText = '';
                    
                    // 処理の進捗に合わせて詳細なメッセージを表示
                    if (m.status === 'downloading tesseract core') {
                        statusText = `OCRエンジンをダウンロード中... (${progress}%)`;
                    } else if (m.status === 'loading tesseract core') {
                        statusText = `OCRエンジンをロード中... (${progress}%)`;
                    } else if (m.status === 'initializing api') {
                        statusText = `APIを初期化中... (${progress}%)`;
                    } else if (m.status === 'loading language traineddata') {
                        statusText = `言語データ(jpn+eng)をロード中... (${progress}%)`;
                    } else if (m.status === 'initializing api') {
                        statusText = `OCR APIを初期化中... (${progress}%)`;
                    } else if (m.status === 'recognizing text' && m.progress > 0) {
                        // テキスト認識中の進捗
                        statusText = `テキスト認識中: ${progress}%`;
                        statusElement.style.color = 'blue'; 
                    } else if (m.status) {
                        statusText = `OCRステータス: ${m.status}`;
                    } else {
                        return; // 不要なログはスキップ
                    }
                    
                    statusElement.innerHTML = `<div class="spinner"></div> ${statusText}`;
                },
            });
            
            // 言語ロードと初期化フェーズ
            statusElement.innerHTML = '<div class="spinner"></div> 言語データをロード中 (jpn+eng)... (2/3)';
            await worker.loadLanguage('jpn+eng'); 
            
            statusElement.innerHTML = '<div class="spinner"></div> OCRワーカーを初期化中... (3/3)';
            await worker.initialize('jpn+eng');
            
            statusElement.textContent = 'OCRワーカーの初期化完了。テキスト認識中...';
        }

        // 認識フェーズ
        const { data: { text } } = await worker.recognize(base64Image);
        return text;
    } catch (error) {
        console.error("Tesseract OCR Error:", error);
        throw new Error(`OCR処理中に致命的なエラーが発生しました: ${error.message}`);
    }
}


// --- ファイル入力のイベントリスナー ---
document.getElementById('fileInput').addEventListener('change', function () {
    const files = this.files;
    if (files.length === 0) return;
    
    // ファイルの内容を読み込み、persistentDocuments に追加
    const fileReads = Array.from(files).map(file => {
        return new Promise((resolve, reject) => {
            if (file.size > 10 * 1024 * 1024) { // 10MB以上はスキップ
                alert(`ファイル「${file.name}」はサイズ制限（10MB）を超えているためスキップされました。`);
                return resolve();
            }
            const reader = new FileReader();
            reader.onload = function (e) {
                const newDoc = { name: file.name, content: e.target.result };
                persistentDocuments.push(newDoc);
                resolve();
            };
            reader.onerror = reject;
            reader.readAsText(file);
        });
    });

    Promise.all(fileReads.filter(p => p !== null))
        .then(() => {
            saveDocuments();
            updateFileListDisplay();
            alert(`新しいファイル ${persistentDocuments.length - (persistentDocuments.length - files.length)} 件をRAGソースに追加しました。`);
        })
        .catch(error => {
            alert('ファイルの読み込み中にエラーが発生しました。');
            console.error("File reading error:", error);
        });
    
    this.value = ''; // 連続アップロードのためにinputをクリア
});
    
// --- 貼り付け画像処理のイベントリスナー (OCR連携ロジック) ---
document.getElementById('pasteArea').addEventListener('paste', async function (e) {
    const items = e.clipboardData.items;
    let imageFound = false;
    
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.type.indexOf('image') !== -1) {
            e.preventDefault(); 
            const blob = item.getAsFile();
            const reader = new FileReader();
            imageFound = true;
            
            // OCR結果は一旦クリア
            ocrDocuments = [];
            clearOcrDisplay();

            // 処理中メッセージ表示要素 (ステータス表示用)
            const processingMessage = document.createElement('p');
            processingMessage.className = 'ocr-status';
            processingMessage.textContent = '画像を貼り付けました。OCR処理を開始しています...';
            const fileContentDiv = document.getElementById('fileContent');
            fileContentDiv.prepend(processingMessage);

            reader.onload = async function (event) {
                const base64Image = event.target.result;
                const imageName = `一時貼付画像_${Date.now()}`;
                
                // 画像をfileContentエリアに表示
                const img = document.createElement('img');
                img.src = base64Image;
                img.alt = imageName;
                fileContentDiv.prepend(img);
                
                try {
                    // 1. OCR処理を実行 (詳細ステータスはprocessingMessageで更新される)
                    const ocrText = await runOcrOnImage(base64Image, processingMessage);
                    
                    // 2. OCR結果を一時文書として保持
                    const fullOcrContent = ocrText.trim(); 
                    if (fullOcrContent) {
                        ocrDocuments.push({
                            name: imageName,
                            content: fullOcrContent
                        });
                    }
                    
                    // 3. ステータス更新（最終メッセージ）
                    if (fullOcrContent) {
                        processingMessage.innerHTML = `✅ OCR処理完了: <strong>${imageName}</strong> のテキストがRAG対象に追加されました (一時保存)。<br>「保存」ボタンで永続化できます。`;
                        processingMessage.style.color = 'green';
                    } else {
                        processingMessage.innerHTML = `⚠️ OCR処理完了: テキストを検出できませんでした。画像を削除するには「貼付けテキストを永続ファイルとして保存」するか、別の画像を貼り付けてください。`;
                        processingMessage.style.color = 'brown';
                    }
                    
                } catch (error) {
                    processingMessage.innerHTML = `❌ OCR処理中にエラーが発生しました: ${error.message}`;
                    processingMessage.style.color = 'red';
                    console.error("OCR Error:", error);
                } finally {
                    document.getElementById('pasteArea').value = ''; // 貼り付けエリアをクリア
                }
            };
            reader.readAsDataURL(blob);
            break;
        }
    }
    
    // 画像貼り付けではない場合は、テキスト貼り付けとして処理は継続される（pasteAreaに入る）
});
    
// --- OCR/貼付テキストのファイル保存と永続化 ---
document.getElementById('saveOcrButton').addEventListener('click', saveOcrTextAsFile);

function saveOcrTextAsFile() {
    const allTextDocuments = [...ocrDocuments];
    const pasteAreaContent = document.getElementById('pasteArea').value.trim();
    
    let contentToSave = '';
    
    // 1. OCRで抽出された一時文書を統合
    allTextDocuments.forEach(doc => {
        contentToSave += `--- ファイル名: ${doc.name} ---\n`;
        contentToSave += doc.content + '\n\n';
    });
    
    // 2. 貼り付けエリアのテキストを統合
    if (pasteAreaContent) {
        contentToSave += `--- ファイル名: 貼付テキスト ---\n`;
        contentToSave += pasteAreaContent + '\n\n';
    }

    if (!contentToSave.trim()) {
        alert("永続化するテキスト（OCR結果または貼付エリアの内容）がありません。");
        return;
    }

    // 3. LocalStorageに永続化 (ファイル名を付けて persistentDocuments に追加)
    const now = new Date();
    const pad = (num) => num.toString().padStart(2, '0');
    const filename = `plower_memo_${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}.txt`;
    
    persistentDocuments.push({ name: filename, content: contentToSave });
    saveDocuments();
    
    // 4. ローカルPCにダウンロード (エクスプローラへの保存)
    const blob = new Blob([contentToSave], { type: 'text/plain;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // 5. UIのクリーンアップ
    alert(`OCR/貼付テキストを「${filename}」として保存し、RAGソースとして永続化しました。`);
    
    document.getElementById('pasteArea').value = '';
    ocrDocuments = [];
    clearOcrDisplay(); // 重要な変更点：保存が完了したら画像とステータスをクリア
    updateFileListDisplay(); // ファイルリストを更新
}


// --- 関連文書検索ロジック (キーワードマッチング) ---
function findRelevantDocs(query, docs, topK = 3) {
    if (!docs || docs.length === 0) return [];
    
    // 💡 RAG検索ロジックを改善: 助詞や句読点を除去した単語リストで検索
    const contentCleanedQuery = query.toLowerCase()
        .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()？。、はがをにでと]/g, " ") // 日本語の助詞・句読点も除去
        .split(/\s+/)
        .filter(t => t.length > 1); // 1文字以下の単語は無視

    const searchTerms = Array.from(new Set([query.toLowerCase(), ...contentCleanedQuery])); // 元のクエリと単語リストを統合

    const scores = docs.map(doc => {
        const content = (doc.content || '').toLowerCase();
        let score = 0;
        
        searchTerms.forEach(term => {
            // 全体一致と部分一致の両方でスコアを計算
            const count = (content.match(new RegExp(term, 'g')) || []).length; 
            // キーワードの文字数で重み付け (長いキーワードほど重要)
            score += count * term.length; 
        });
        return { ...doc, score };
    });
    
    // スコアが0より大きい文書をソートして返す
    return scores.filter(doc => doc.score > 0).sort((a, b) => b.score - a.score).slice(0, topK);
}

// --- モデル送信ロジック (Ollama/Gemini 切り替え) ---
async function sendToModel() {
    const userInputElement = document.getElementById('userInput');
    const userInput = userInputElement.value.trim();
    const pasteAreaContent = document.getElementById('pasteArea').value.trim();
    const chatLog = document.getElementById('chatLog');
    const sendButton = document.getElementById('sendButton');
    const modelSelect = document.getElementById('modelSelect').value; 

    if (!userInput) {
        alert("質問を入力してください。");
        return;
    }
    
    sendButton.disabled = true;
    sendButton.textContent = '送信中...';
    chatLog.innerHTML += `<p><strong>質問:</strong> ${userInput}</p>`;
    const responseParagraph = document.createElement('p');
    responseParagraph.innerHTML = '<strong>回答:</strong> (応答待機中...)';
    chatLog.appendChild(responseParagraph);
    
    // 全てのRAGソースを統合
    let allDocuments = [...persistentDocuments, ...ocrDocuments];
    if (pasteAreaContent) {
        // 貼り付けエリアのテキストは一時文書として扱う
        allDocuments.push({ name: '貼付けテキスト(一時)', content: pasteAreaContent });
    }

    // RAGコンテキストの生成
    const relevantDocs = findRelevantDocs(userInput, allDocuments);
    const context = relevantDocs.map(doc => `【${doc.name}】\n${doc.content}`).join('\n\n').slice(0, 5000); // 5000文字に制限
    
    // プロンプトの生成
    const prompt = `あなたはRAGシステムとして機能します。提供された以下の文書に基づいて、ユーザーの質問に日本語で簡潔に答えてください。
    文書に関連情報がない場合は、「提供された文書に関連情報がないため回答できません。」と伝えてください。
    参照した文書名（【文書名】）を引用として回答の末尾に記載しても構いません。

--- 文書 ---
${context}
---

質問: ${userInput}`;

    let result = '';
    let endpoint = '';
    let bodyData = {};
    let isStreaming = false;
    
    // --- モデルの振り分けロジック ---
    const isGeminiCloudModel = GEMINI_MODELS.includes(modelSelect);
    
    if (isGeminiCloudModel) {
        // --- Gemini Cloud Model (FastAPIプロキシ経由) ---
        endpoint = 'http://localhost:8001/api/gemini_proxy'; 
        bodyData = {
            model: modelSelect, 
            prompt: prompt,
            temperature: 0.1
        };
        isStreaming = false; 

    } else {
        // --- Ollama Local Model ---
        endpoint = 'http://localhost:11434/api/generate';
        // コンテキストサイズ設定 (Ollamaモデルのみ)
        const numCtx = (modelSelect.includes('20b') || modelSelect.includes('12b') || modelSelect.includes('120b')) ? 8192 : 4096;
        
        bodyData = {
            model: modelSelect, 
            prompt: prompt,
            stream: true,
            options: { 
                temperature: 0.1, 
                num_ctx: numCtx
            }
        };
        isStreaming = true;
    }

    try {
        // --- APIリクエストの実行 ---
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });

        if (!response.ok) {
            const errorDetail = await response.text();
            const errorSource = isGeminiCloudModel ? 'FastAPIプロキシ/Gemini API' : 'Ollamaサーバー';
            throw new Error(`${errorSource} エラー: ${response.status} ${response.statusText}. モデル: ${modelSelect} のロードまたは通信に失敗しました。詳細: ${errorDetail.slice(0, 100)}...`);
        }

        // --- ストリーミング/非ストリーミングの処理分岐 ---
        if (isStreaming) {
            // Ollama (ストリーミング) 処理
            if (!response.body) throw new Error("Ollamaサーバーから応答ボディがありません。");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                chunk.trim().split('\n').forEach(line => {
                    if (line) {
                        try {
                            const json = JSON.parse(line);
                            if (json.response) {
                                result += json.response;
                                // 応答をリアルタイムで表示し、改行を<br>に変換
                                responseParagraph.innerHTML = `<strong>回答:</strong> ${result.replace(/\n/g, '<br>')}`;
                            }
                            } catch (e) {
                                // JSON解析エラーは無視 (部分的なストリームチャンクの可能性)
                            }
                            }
                        });
                }
        } else {
            // Gemini (非ストリーミング) 処理
            const json = await response.json();
            if (json.response) {
                result = json.response;
            } else if (json.detail) {
                throw new Error(`Geminiプロキシ処理エラー: ${json.detail}`);
            } else {
                throw new Error("FastAPIプロキシからの予期しない応答形式です。");
            }
        }
        
        // 最終結果の表示（非ストリーミングの場合、ここで一度に更新）
        responseParagraph.innerHTML = `<strong>回答:</strong> ${result.replace(/\n/g, '<br>')}`;
        userInputElement.value = ''; // 質問欄をクリア

    } catch (error) {
        responseParagraph.innerHTML = `<strong>回答:</strong> ❌ エラーが発生しました: ${error.message}`;
        console.error("Model request error:", error);
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = '送信';
        // 最新のチャットが見えるようにスクロール
        chatLog.scrollTop = chatLog.scrollHeight;
    }
}
    
// --- 初期化とイベントリスナー設定 ---
document.addEventListener('DOMContentLoaded', () => {
    loadDocuments(); 
    document.getElementById('sendButton').addEventListener('click', sendToModel);
    document.getElementById('resetDocsButton').addEventListener('click', resetDocuments);
    
    // Enterキーでの送信機能
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendToModel();
        }
    });
});