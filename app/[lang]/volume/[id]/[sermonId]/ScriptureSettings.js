"use client";

import { useState, useEffect } from 'react';
import { useBibleSettings } from '../../../../components/BibleSettingsProvider';

const BIBLE_BOOKS = [
  'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth',
  '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra',
  'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
  'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos',
  'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
  'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians',
  'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
  '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
  '1 John', '2 John', '3 John', 'Jude', 'Revelation'
];

export default function ScriptureSettings({ dict }) {
  const { integrationEnabled, setIntegrationEnabled, tooltipTranslation, setTooltipTranslation } = useBibleSettings();
  const [inlineText, setInlineText] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  useEffect(() => {
    if (!integrationEnabled) {
      setInlineText(null);
      return;
    }
    
    async function fetchInlineVerse() {
      setIsLoading(true);
      try {
        const marker = document.querySelector('.reader-scripture-ref .bible-ref-marker');
        if (!marker) {
          setInlineText(null);
          return;
        }
        
        const book = marker.getAttribute('data-book');
        const chapter = parseInt(marker.getAttribute('data-chapter'), 10);
        const verse = parseInt(marker.getAttribute('data-verse'), 10);
        const endVerse = marker.getAttribute('data-end-verse') ? parseInt(marker.getAttribute('data-end-verse'), 10) : null;
        
        if (!book || !chapter || !verse) return;
        
        const res = await fetch(`/bibles/${tooltipTranslation}.json`);
        if (!res.ok) throw new Error('Failed to fetch bible translation');
        const data = await res.json();
        
        const bookIndex = BIBLE_BOOKS.findIndex(b => b === book);
        if (bookIndex === -1 || !data[bookIndex]) throw new Error('Book not found');
        
        const bookData = data[bookIndex];
        const chapterData = bookData.chapters[chapter - 1];
        if (!chapterData) throw new Error('Chapter not found');
        
        let text = '';
        if (endVerse) {
          for (let v = verse; v <= endVerse; v++) {
            if (chapterData[v - 1]) text += `[${v}] ${chapterData[v - 1]} `;
          }
        } else {
          text = `[${verse}] ${chapterData[verse - 1]}`;
        }
        
        setInlineText(text);
      } catch (err) {
        console.error("Failed to load inline scripture:", err);
        setInlineText(null);
      } finally {
        setIsLoading(false);
      }
    }
    
    fetchInlineVerse();
  }, [tooltipTranslation, integrationEnabled]);

  return (
    <div className="scripture-settings-container" style={{ marginTop: '1.5rem' }}>
      <div className="scripture-settings-inline" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <label className="toolbar-toggle" title={dict ? dict.reader.tools.settings : "Enable Bible Links"}>
          <input 
            type="checkbox" 
            checked={integrationEnabled}
            onChange={(e) => setIntegrationEnabled(e.target.checked)}
          />
          <span className="toolbar-toggle-slider"></span>
          <span className="toolbar-toggle-label">{dict ? dict.reader.tools.settings : "Bible Links"}</span>
        </label>
        
        {integrationEnabled && (
          <select 
            className="toolbar-select"
            value={tooltipTranslation}
            onChange={(e) => setTooltipTranslation(e.target.value)}
            title={dict ? dict.reader.tools.translation : "Translation for verses"}
            style={{ padding: '0.4rem 0.6rem', background: 'var(--surface-hover)', border: '1px solid var(--border)', borderRadius: '6px', color: 'var(--text)', fontSize: '0.9rem', minWidth: '140px' }}
          >
            <option value="kjv">KJV</option>
            <option value="niv">NIV 1984</option>
            <option value="asv">ASV</option>
            <option value="web">WEB</option>
            <option value="acf">ACF (PT)</option>
            <option value="nvi">NVI 2001 (PT)</option>
            <option value="nvies">NVI 1999 (ES)</option>
            <option value="rvr1960">RVR 1960 (ES)</option>
            <option value="lbla">LBLA (ES)</option>
            <option value="rvr">RVR 1909 (ES)</option>
            <option value="frlsg">FRLSG (FR)</option>
            <option value="lut">LUT (DE)</option>
            <option value="cuv">CUV (ZH)</option>
            <option value="synod">Synodal (Ru)</option>
            <option value="svd">SVD (Ar)</option>
            <option value="krv">KRV (Ko)</option>
            <option value="vi1934">1934 (Vi)</option>
            <option value="ncv">NCV (ZH)</option>
            <option value="el">Greek (EL)</option>
            <option value="eo">Esperanto (EO)</option>
            <option value="fi">Finnish (FI)</option>
            <option value="pr">Pyhä (FI)</option>
            <option value="ro">Dumitru (RO)</option>
            <option value="aa">AA (PT)</option>
            <option value="wlc">Hebrew</option>
            <option value="tr">Greek</option>
          </select>
        )}
      </div>

      {integrationEnabled && (inlineText || isLoading) && (
        <div 
          className="inline-scripture-viewer" 
          style={{ 
            marginTop: '1rem', 
            padding: '1rem', 
            background: 'var(--surface-hover)', 
            borderLeft: '3px solid var(--primary)', 
            borderRadius: '0 6px 6px 0',
            fontSize: '0.95rem',
            lineHeight: '1.6',
            color: 'var(--text-muted)'
          }}
        >
          <div 
            style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              marginBottom: isExpanded ? '0.5rem' : '0',
              cursor: 'pointer'
            }}
            onClick={() => setIsExpanded(!isExpanded)}
          >
            <span style={{ fontWeight: '600', color: 'var(--text)' }}>
              {isLoading ? '...' : (document.querySelector('.reader-scripture-ref .bible-ref-marker')?.textContent || 'Verse')} 
              <span style={{ 
                fontSize: '0.7rem', 
                marginLeft: '0.5rem', 
                background: 'rgba(255,255,255,0.1)', 
                padding: '2px 6px', 
                borderRadius: '10px' 
              }}>
                {tooltipTranslation.toUpperCase()}
              </span>
            </span>
            <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>
              {isExpanded ? '▲' : '▼'}
            </span>
          </div>
          
          {isExpanded && !isLoading && (
            <div style={{ marginTop: '0.5rem' }}>
              {inlineText}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
