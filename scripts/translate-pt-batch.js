/**
 * scripts/translate-pt-batch.js
 * 
 * Automação de tradução de sermões em lote para Português (Bing Translate).
 * Preserva 100% da estrutura Markdown, cabeçalho de título (# Sermão X | ...),
 * bloco de versículo bíblico e quebras de parágrafos idênticos ao padrão do Spurgeon.tv.
 * 
 * Uso:
 *   node scripts/translate-pt-batch.js               -> Traduz todos os sermões faltantes (01 a 63)
 *   node scripts/translate-pt-batch.js --vol=01       -> Traduz apenas o volume 01
 *   node scripts/translate-pt-batch.js --start=01 --end=10 -> Traduz do volume 01 ao 10
 *   node scripts/translate-pt-batch.js --slug=sermon-6 -> Traduz sermão específico
 *   node scripts/translate-pt-batch.js --limit=3      -> Traduz 3 sermões e para (teste)
 */

const fs = require('fs');
const path = require('path');
const { translate } = require('bing-translate-api');
const { execSync } = require('child_process');

process.on('uncaughtException', (err) => {
    console.error('⚠️ [Aviso Global] Erro transitório capturado (mantendo processo ativo):', err.message);
});
process.on('unhandledRejection', (reason) => {
    console.error('⚠️ [Aviso Global] Rejeição de Promise capturada:', (reason && reason.message) || reason);
});

const ROOT = path.resolve(__dirname, '..');
const SERMONS_EN_DIR = path.join(ROOT, 'chspurgeon-sermons-main');
const SERMONS_PT_DIR = path.join(ROOT, 'chspurgeon-sermons-pt');
const PUBLIC_PT_DIR = path.join(ROOT, 'public', 'data', 'sermons', 'pt');
const STATUS_FILE = path.join(ROOT, 'scratch', 'translation_pt_status.json');

// Mapeamento Canônico de Livros Bíblicos EN -> PT
const BIBLE_BOOKS_EN_TO_PT = {
    'Genesis': 'Gênesis', 'Exodus': 'Êxodo', 'Leviticus': 'Levítico', 'Numbers': 'Números', 'Deuteronomy': 'Deuteronômio',
    'Joshua': 'Josué', 'Judges': 'Juízes', 'Ruth': 'Rute', '1 Samuel': '1 Samuel', '2 Samuel': '2 Samuel',
    'I Samuel': '1 Samuel', 'II Samuel': '2 Samuel', '1 Kings': '1 Reis', '2 Kings': '2 Reis',
    'I Kings': '1 Reis', 'II Kings': '2 Reis', '1 Chronicles': '1 Crônicas', '2 Chronicles': '2 Crônicas',
    'I Chronicles': '1 Crônicas', 'II Chronicles': '2 Crônicas', 'Ezra': 'Esdras', 'Nehemiah': 'Neemias',
    'Esther': 'Ester', 'Job': 'Jó', 'Psalms': 'Salmos', 'Psalm': 'Salmo', 'Proverbs': 'Provérbios',
    'Ecclesiastes': 'Eclesiastes', 'Song of Solomon': 'Cantares', 'Song of Songs': 'Cantares', 'Canticles': 'Cantares',
    'Isaiah': 'Isaías', 'Jeremiah': 'Jeremias', 'Lamentations': 'Lamentações', 'Ezekiel': 'Ezequiel',
    'Daniel': 'Daniel', 'Hosea': 'Oseias', 'Joel': 'Joel', 'Amos': 'Amós', 'Obadiah': 'Obadias',
    'Jonah': 'Jonas', 'Micah': 'Miqueias', 'Nahum': 'Naum', 'Habakkuk': 'Habacuque', 'Zephaniah': 'Sofonias',
    'Haggai': 'Ageu', 'Zechariah': 'Zacarias', 'Malachi': 'Malaquias',
    'Matthew': 'Mateus', 'Mark': 'Marcos', 'Luke': 'Lucas', 'John': 'João', 'Acts': 'Atos',
    'Romans': 'Romanos', '1 Corinthians': '1 Coríntios', '2 Corinthians': '2 Coríntios',
    'I Corinthians': '1 Coríntios', 'II Corinthians': '2 Coríntios',
    'Galatians': 'Gálatas', 'Ephesians': 'Efésios', 'Philippians': 'Filipenses', 'Colossians': 'Colossenses',
    '1 Thessalonians': '1 Tessalonicenses', '2 Thessalonians': '2 Tessalonicenses',
    'I Thessalonians': '1 Tessalonicenses', 'II Thessalonians': '2 Tessalonicenses',
    '1 Timothy': '1 Timóteo', '2 Timothy': '2 Timóteo', 'I Timothy': '1 Timóteo', 'II Timothy': '2 Timóteo',
    'Titus': 'Tito', 'Philemon': 'Filemom', 'Hebrews': 'Hebreus', 'James': 'Tiago',
    '1 Peter': '1 Pedro', '2 Peter': '2 Pedro', 'I Peter': '1 Pedro', 'II Peter': '2 Pedro',
    '1 John': '1 João', '2 John': '2 João', '3 John': '3 João',
    'I John': '1 João', 'II John': '2 João', 'III John': '3 João',
    'Jude': 'Judas', 'Revelation': 'Apocalipse'
};

function normalizeBibleReference(ref) {
    if (!ref) return '';
    let normalized = ref.trim();
    for (const [enBook, ptBook] of Object.entries(BIBLE_BOOKS_EN_TO_PT)) {
        const regex = new RegExp(`\\b${enBook}\\b`, 'g');
        if (regex.test(normalized)) {
            normalized = normalized.replace(regex, ptBook);
            break;
        }
    }
    return normalized;
}

// Argumentos CLI
const args = process.argv.slice(2);
let targetVolume = null;
let startVol = 1;
let endVol = 63;
let limitTotal = null;
let forceOverwrite = false;
let targetSlug = null;

for (const arg of args) {
    if (arg.startsWith('--vol=')) {
        const v = parseInt(arg.split('=')[1], 10);
        targetVolume = `volume-${v.toString().padStart(2, '0')}`;
    } else if (arg.startsWith('--slug=')) {
        targetSlug = arg.split('=')[1].replace(/_/g, '-');
        if (!targetSlug.endsWith('.md')) targetSlug += '.md';
    } else if (arg.startsWith('--start=')) {
        startVol = parseInt(arg.split('=')[1], 10);
    } else if (arg.startsWith('--end=')) {
        endVol = parseInt(arg.split('=')[1], 10);
    } else if (arg.startsWith('--limit=')) {
        limitTotal = parseInt(arg.split('=')[1], 10);
    } else if (arg === '--force') {
        forceOverwrite = true;
    }
}

let volumesToProcess = [];
if (targetVolume) {
    volumesToProcess = [targetVolume];
} else {
    for (let i = startVol; i <= endVol; i++) {
        volumesToProcess.push(`volume-${i.toString().padStart(2, '0')}`);
    }
}

function updateStatus(info) {
    try {
        const current = fs.existsSync(STATUS_FILE) 
            ? JSON.parse(fs.readFileSync(STATUS_FILE, 'utf8')) 
            : {};
        const updated = {
            ...current,
            ...info,
            lastUpdate: new Date().toISOString()
        };
        fs.writeFileSync(STATUS_FILE, JSON.stringify(updated, null, 2), 'utf8');
    } catch (e) {}
}

async function translateText(text, targetLang = 'pt', retries = 5, delayMs = 3500) {
    if (!text || text.trim() === '') return '';
    try {
        const res = await translate(text, 'en', targetLang, false);
        return res.translation;
    } catch (e) {
        const errMsg = e.message || String(e);
        console.error(`  [Bing] Falha na tradução: ${errMsg}. Tentativas restantes: ${retries}`);
        
        if (retries > 0) {
            console.log(`  Aguardando ${(delayMs / 1000).toFixed(1)}s antes de tentar novamente...`);
            await new Promise(r => setTimeout(r, delayMs));
            return await translateText(text, targetLang, retries - 1, delayMs * 1.5);
        }
        
        console.error('  ❌ Esgotadas tentativas para o bloco. Retornando texto original.');
        return text;
    }
}

function isSermonAlreadyTranslated(filePath) {
    if (!fs.existsSync(filePath)) return false;
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const firstLine = content.split('\n')[0] || '';
        // Se o título ainda começa com 'Sermon ' em inglês ao invés de 'Sermão '
        if (/^#\s*Sermon\s+\d+/i.test(firstLine)) return false;

        // Verifica termos comuns em inglês nos primeiros 1000 caracteres
        const sample = content.substring(0, 1000).toLowerCase();
        if (sample.includes(' the ') && sample.includes(' and ') && sample.includes(' that ')) {
            return false;
        }
        return true;
    } catch (e) {
        return false;
    }
}

/**
 * Decomposição e reconstrução estrutural estrita do Sermão
 */
async function translateSermon(enRawContent) {
    const rawLines = enRawContent.split('\n');
    let lineIdx = 0;

    // 1. EXTRAÇÃO DO TÍTULO
    let sermonNumber = '';
    let enTitlePart = '';
    const firstLine = rawLines[0] || '';
    const titleMatch = firstLine.match(/#\s*(?:Sermon|Sermão|Sermón)\s*(\d+(?:\s*(?:&|-)\s*\d+)?)\s*(?:\||\—|\-)\s*(.+)/i);
    if (titleMatch) {
        sermonNumber = titleMatch[1].trim();
        enTitlePart = titleMatch[2].trim();
    } else {
        const fallbackMatch = firstLine.match(/#\s*(.+)/);
        enTitlePart = fallbackMatch ? fallbackMatch[1].trim() : 'Sermão';
    }
    lineIdx++;

    // 2. EXTRAÇÃO DO BLOCO DE ESCRITURA BÍBLICA (versículo-chave) APENAS NO TOPO
    const scriptureRawLines = [];
    const maxHeaderScan = Math.min(rawLines.length, 8);
    let scanIdx = lineIdx;
    while (scanIdx < maxHeaderScan) {
        const line = rawLines[scanIdx];
        if (line.trim().startsWith('>')) {
            scriptureRawLines.push(line.replace(/^>\s*/, '').trim());
            scanIdx++;
            lineIdx = scanIdx;
        } else if (scriptureRawLines.length > 0 && line.trim() === '') {
            scanIdx++;
            lineIdx = scanIdx;
            break;
        } else if (scriptureRawLines.length > 0) {
            break;
        } else if (line.trim() === '') {
            scanIdx++;
        } else {
            // Verifica se a linha tem formato de versículo entre aspas seguido de referência
            const inlineVerseMatch = line.trim().match(/^["“](.+?)["”]\s*(?:—|--|-)?\s*([1-3I]?\s*[A-Za-z]+\s+\d+:\d+(?:-\d+)?)\.?$/);
            if (inlineVerseMatch) {
                scriptureRawLines.push(inlineVerseMatch[1].trim());
                scriptureRawLines.push(inlineVerseMatch[2].trim());
                lineIdx = scanIdx + 1;
                break;
            }
            break;
        }
    }

    // 3. TRADUÇÃO DO TÍTULO E VERSÍCULO
    console.log(`  [1/3] Traduzindo Título: "${enTitlePart}"...`);
    const translatedTitlePart = await translateText(enTitlePart, 'pt');
    const ptTitle = sermonNumber ? `# Sermão ${sermonNumber} | ${translatedTitlePart}` : `# ${translatedTitlePart}`;
    await new Promise(r => setTimeout(r, 800));

    let ptScriptureBlock = '';
    if (scriptureRawLines.length > 0) {
        console.log(`  [2/3] Traduzindo Bloco Bíblico (${scriptureRawLines.length} linhas)...`);
        
        let verseText = '';
        let refText = '';
        
        if (scriptureRawLines.length >= 2) {
            verseText = scriptureRawLines.slice(0, -1).join(' ');
            refText = scriptureRawLines[scriptureRawLines.length - 1];
        } else {
            verseText = scriptureRawLines[0];
        }

        const ptVerseText = await translateText(verseText, 'pt');
        const ptRefText = normalizeBibleReference(refText);
        
        ptScriptureBlock = `> ${ptVerseText}\n`;
        if (ptRefText) {
            ptScriptureBlock += `> ${ptRefText}\n`;
        }
        await new Promise(r => setTimeout(r, 800));
    }

    // 4. EXTRAÇÃO E TRADUÇÃO DO CORPO DE PARÁGRAFOS
    const bodyLines = rawLines.slice(lineIdx);
    const paragraphs = [];
    let currentPara = [];

    for (const line of bodyLines) {
        if (line.trim() === '') {
            if (currentPara.length > 0) {
                paragraphs.push(currentPara.join('\n'));
                currentPara = [];
            }
        } else {
            currentPara.push(line);
        }
    }
    if (currentPara.length > 0) {
        paragraphs.push(currentPara.join('\n'));
    }

    console.log(`  [3/3] Traduzindo ${paragraphs.length} parágrafos do corpo do sermão...`);
    const translatedParagraphs = [];
    let chunkBuffer = [];
    let chunkLength = 0;

    const flushChunk = async () => {
        if (chunkBuffer.length === 0) return;
        const joined = chunkBuffer.join('\n\n---CHUNK_SEP---\n\n');
        const translatedChunk = await translateText(joined, 'pt');
        const split = translatedChunk.split(/\n\n---CHUNK_SEP---\n\n|\n*---CHUNK_SEP---\n*/);
        
        for (let j = 0; j < chunkBuffer.length; j++) {
            translatedParagraphs.push(split[j] ? split[j].trim() : chunkBuffer[j]);
        }
        
        chunkBuffer = [];
        chunkLength = 0;
        await new Promise(r => setTimeout(r, 1200));
    };

    for (let i = 0; i < paragraphs.length; i++) {
        const para = paragraphs[i];

        if (para.startsWith('>') || para.startsWith('<!--') || para.startsWith('#')) {
            await flushChunk();
            if (para.startsWith('>')) {
                const inner = para.replace(/^>\s*/gm, '');
                const tr = await translateText(inner, 'pt');
                translatedParagraphs.push(tr.split('\n').map(l => `> ${l}`).join('\n'));
            } else {
                translatedParagraphs.push(para);
            }
            await new Promise(r => setTimeout(r, 800));
            continue;
        }

        if (para.length > 850) {
            await flushChunk();
            const sentences = para.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [para];
            let subChunk = '';
            for (const s of sentences) {
                if (subChunk.length + s.length > 850) {
                    const tr = await translateText(subChunk, 'pt');
                    translatedParagraphs.push(tr);
                    subChunk = '';
                    await new Promise(r => setTimeout(r, 800));
                }
                subChunk += s;
            }
            if (subChunk) {
                const tr = await translateText(subChunk, 'pt');
                translatedParagraphs.push(tr);
                await new Promise(r => setTimeout(r, 800));
            }
            continue;
        }

        if (chunkLength + para.length > 850) {
            await flushChunk();
        }

        chunkBuffer.push(para);
        chunkLength += para.length + 2;
    }
    await flushChunk();

    // 5. RECONSTRUÇÃO FINAL
    let finalDoc = `${ptTitle}\n\n`;
    if (ptScriptureBlock) {
        finalDoc += `${ptScriptureBlock}\n`;
    }
    finalDoc += translatedParagraphs.join('\n\n').trim();
    finalDoc += '\n\n<!-- auto-translated-bing -->\n';

    return finalDoc;
}

async function run() {
    console.log('══════════════════════════════════════════════════════════════════');
    console.log('  AUTOMAÇÃO RIGOROSA DE TRADUÇÃO DE SERMÕES EM PORTUGUÊS (PT)');
    console.log('══════════════════════════════════════════════════════════════════');
    console.log(` Volumes: ${volumesToProcess[0]} até ${volumesToProcess[volumesToProcess.length - 1]}`);
    if (limitTotal) console.log(` Limite de sermões nesta execução: ${limitTotal}`);
    if (forceOverwrite) console.log(` Modo forçado: sobrescrevendo arquivos de destino`);
    console.log('──────────────────────────────────────────────────────────────────\n');

    let totalTranslated = 0;
    let totalSkipped = 0;
    const startTime = Date.now();

    updateStatus({
        status: 'running',
        startTime: new Date().toISOString(),
        totalTranslated: 0,
        currentVolume: '',
        currentFile: '',
    });

    for (const vol of volumesToProcess) {
        const enVolDir = path.join(SERMONS_EN_DIR, vol);
        const ptVolDir = path.join(SERMONS_PT_DIR, vol);
        const pubPtVolDir = path.join(PUBLIC_PT_DIR, vol);

        if (!fs.existsSync(enVolDir)) continue;
        if (!fs.existsSync(ptVolDir)) fs.mkdirSync(ptVolDir, { recursive: true });
        if (!fs.existsSync(pubPtVolDir)) fs.mkdirSync(pubPtVolDir, { recursive: true });

        const enFiles = fs.readdirSync(enVolDir)
            .filter(f => f.endsWith('.md'))
            .sort((a, b) => {
                const numA = parseInt(a.replace(/\D/g, ''), 10) || 0;
                const numB = parseInt(b.replace(/\D/g, ''), 10) || 0;
                return numA - numB;
            });

        console.log(`\n📁 Volume ${vol} (${enFiles.length} sermões no acervo)...`);

        for (const file of enFiles) {
            const standardSlug = file.replace(/_/g, '-');
            if (targetSlug && standardSlug !== targetSlug) {
                continue;
            }

            if (limitTotal && totalTranslated >= limitTotal) {
                console.log(`\n🛑 Limite de ${limitTotal} sermões atingido. Encerrando o lote.`);
                break;
            }

            const targetFileRepo = path.join(ptVolDir, standardSlug);
            const targetFilePub = path.join(pubPtVolDir, standardSlug);

            const isTranslated = isSermonAlreadyTranslated(targetFileRepo);

            if (isTranslated && !forceOverwrite && !targetSlug) {
                if (!fs.existsSync(targetFilePub)) {
                    fs.copyFileSync(targetFileRepo, targetFilePub);
                }
                totalSkipped++;
                continue;
            }

            console.log(`\n⏳ Traduzindo com estrutura preservada [${vol}/${standardSlug}]...`);
            updateStatus({
                currentVolume: vol,
                currentFile: standardSlug,
                totalTranslated,
                totalSkipped
            });

            const enContent = fs.readFileSync(path.join(enVolDir, file), 'utf8');
            const fileStart = Date.now();

            try {
                const finalContent = await translateSermon(enContent);

                // Dupla gravação simultânea
                fs.writeFileSync(targetFileRepo, finalContent, 'utf8');
                fs.writeFileSync(targetFilePub, finalContent, 'utf8');

                totalTranslated++;
                const duration = ((Date.now() - fileStart) / 1000).toFixed(1);
                console.log(`✅ Concluído: ${standardSlug} em ${duration}s (Total traduzidos: ${totalTranslated})`);

                updateStatus({
                    totalTranslated,
                    totalSkipped,
                    lastTranslated: `${vol}/${standardSlug}`
                });

                // Pausa prudente para não bloquear no Bing
                await new Promise(r => setTimeout(r, 3000));
            } catch (err) {
                console.error(`❌ Erro ao processar ${standardSlug}:`, err.message);
                await new Promise(r => setTimeout(r, 4000));
            }
        }

        if (limitTotal && totalTranslated >= limitTotal) {
            break;
        }
    }

    const totalMinutes = ((Date.now() - startTime) / 60000).toFixed(1);
    console.log('\n══════════════════════════════════════════════════════════════════');
    console.log(`  FINALIZADO EM ${totalMinutes} MINUTOS!`);
    console.log(`  • Sermões recém-traduzidos: ${totalTranslated}`);
    console.log(`  • Sermões existentes preservados: ${totalSkipped}`);
    console.log('══════════════════════════════════════════════════════════════════\n');

    if (totalTranslated > 0) {
        console.log('🔄 Atualizando o índice de busca (generate-search-index.mjs)...');
        try {
            execSync('node scripts/generate-search-index.mjs', { stdio: 'inherit' });
            console.log('✅ Índice de busca atualizado!');
            console.log('🔄 Atualizando páginas de sermões (generate-sermon-pages.mjs)...');
            execSync('node scripts/generate-sermon-pages.mjs', { stdio: 'inherit' });
            console.log('✅ Páginas de sermões atualizadas!');
        } catch (e) {
            console.error('⚠️ Aviso ao atualizar o índice de busca:', e.message);
        }
    }

    updateStatus({
        status: 'finished',
        totalTranslated,
        totalSkipped,
        finishTime: new Date().toISOString()
    });
}

run();
