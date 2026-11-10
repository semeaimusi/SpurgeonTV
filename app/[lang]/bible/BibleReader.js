'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { BIBLE_BOOKS } from '../../../lib/bible-books';
import { BOOK_NORMALIZER } from '../../../lib/linkifyBible';
import ShareButton from '../../components/ShareButton';
import CitationBox from '../../components/CitationBox';
import BibleVersionDetails from '../../components/BibleVersionDetails';

export default function BibleReader({ lang, dict }) {
  const searchParams = useSearchParams();
  const defaultTranslation = lang === 'pt' ? 'nvi' : (lang === 'es' ? 'nvies' : 'kjv');
  const [translation, setTranslation] = useState(defaultTranslation);
  const [sermons, setSermons] = useState([]);
  
  const urlBook = searchParams.get('book');
  const urlChapter = searchParams.get('chapter');
  
  const resolveBook = (bookQuery) => {
    if (!bookQuery) return BIBLE_BOOKS[0];
    const norm = BOOK_NORMALIZER[bookQuery] || bookQuery;
    return BIBLE_BOOKS.find(b => b.name.toLowerCase() === norm.toLowerCase()) ||
           BIBLE_BOOKS.find(b => b.name.toLowerCase() === bookQuery.toLowerCase()) ||
           BIBLE_BOOKS[0];
  };

  const initialBook = resolveBook(urlBook);
  const initialChapter = urlChapter ? parseInt(urlChapter, 10) : 1;
  
  const [selectedBook, setSelectedBook] = useState(initialBook);
  const [selectedChapter, setSelectedChapter] = useState(initialChapter);
  const [verses, setVerses] = useState([]);
  
  // Sync if URL search params change while staying on Bible page
  useEffect(() => {
    if (urlBook) {
      setSelectedBook(resolveBook(urlBook));
    }
    if (urlChapter) {
      const parsedChapter = parseInt(urlChapter, 10);
      if (!isNaN(parsedChapter)) {
        setSelectedChapter(parsedChapter);
      }
    }
  }, [urlBook, urlChapter]);

  // Cache the bibles so we don't re-fetch when switching back and forth
  const [bibleCache, setBibleCache] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadSermons() {
      try {
        const res = await fetch('/search-index.json');
        if (res.ok) {
          const data = await res.json();
          const localizedSermons = data[lang] || data['en'] || [];
          setSermons(localizedSermons);
        }
      } catch (err) {
        console.error('Failed to load sermons index', err);
      }
    }
    loadSermons();
  }, [lang]);

  useEffect(() => {
    async function loadBible() {
      if (bibleCache[translation]) {
        return updateVerses(bibleCache[translation]);
      }

      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`/bibles/${translation}.json`);
        if (!res.ok) throw new Error('Failed to load Bible data');
        const data = await res.json();
        
        setBibleCache(prev => ({ ...prev, [translation]: data }));
        updateVerses(data);
      } catch (err) {
        setError(dict ? dict.bible.reader.error : 'Failed to load the Bible translation. Please try again.');
        setVerses([]);
      } finally {
        setLoading(false);
      }
    }

    function updateVerses(bibleData) {
      // Find book by index since English names won't match localized names in JSON
      const bookIndex = BIBLE_BOOKS.findIndex(b => b.name === selectedBook.name);
      if (bookIndex !== -1 && bibleData[bookIndex]) {
        const bookData = bibleData[bookIndex];
        const chapterVerses = bookData.chapters[selectedChapter - 1] || [];
        setVerses(chapterVerses);
      } else {
        setVerses([]);
      }
    }
    
    loadBible();
  }, [selectedBook, selectedChapter, translation, bibleCache]);

  // When changing translation, the book name displayed should probably be localized, 
  // but keeping it simple using BIBLE_BOOKS for the dropdown is fine.
  // We can get the localized book name from the current loaded translation for the title.
  const currentBible = bibleCache[translation];
  const bookIndex = BIBLE_BOOKS.findIndex(b => b.name === selectedBook.name);
  const localizedBookName = currentBible && currentBible[bookIndex] ? currentBible[bookIndex].name : selectedBook.name;

  // Filter related sermons
  const relatedSermons = sermons.filter(sermon => {
    const scriptureText = sermon.scripture?.reference || sermon.scripture?.verse || '';
    // Exact match for "Book Chapter:" to avoid "John 1" matching "1 John 1" or "John 11"
    const searchString1 = `${selectedBook.name} ${selectedChapter}:`;
    const searchString2 = `${selectedBook.name} ${selectedChapter} `; // e.g., if there's no colon but space
    return scriptureText.includes(searchString1) || scriptureText.includes(searchString2) || scriptureText.endsWith(`${selectedBook.name} ${selectedChapter}`);
  });

  return (
    <div className="bible-reader-container">
      <div className="bible-controls">
        <div className="control-group">
          <label htmlFor="translation-select">{dict ? dict.bible.reader.version : "Version"}</label>
          <select 
            id="translation-select"
            className="bible-select"
            value={translation}
            onChange={(e) => setTranslation(e.target.value)}
          >
            <option value="kjv">KJV (English)</option>
            <option value="niv">NIV 1984 (English - Classic)</option>
            <option value="web">WEB (English)</option>
            <option value="asv">ASV (English)</option>
            <option value="acf">Almeida Corrigida (Português)</option>
            <option value="nvi">NVI 2001 (Português - Clássica)</option>
            <option value="nvies">Nueva Versión Internacional 1999 (Español - Clásica)</option>
            <option value="rvr1960">Reina-Valera 1960 (Español)</option>
            <option value="lbla">La Biblia de las Américas (Español)</option>
            <option value="rvr">Reina-Valera 1909 (Español - Clásica)</option>
            <option value="frlsg">Louis Segond 1910 (Français)</option>
            <option value="lut">Lutherbibel 1912 (Deutsch)</option>
            <option value="cuv">Chinese Union Version (中文)</option>
            <option value="synod">Synodal Translation (Русский)</option>
            <option value="svd">Smith-Van Dyck (العربية)</option>
            <option value="krv">Korean Revised Version (한국어)</option>
            <option value="vi1934">Kinh Thánh 1934 (Tiếng Việt)</option>
            <option value="ncv">New Chinese Version (中文)</option>
            <option value="el">Modern Greek (Ελληνικά)</option>
            <option value="eo">Esperanto (Esperanto)</option>
            <option value="fi">Finnish Bible (Suomi)</option>
            <option value="pr">Pyhä Raamattu (Suomi)</option>
            <option value="ro">Dumitru Cornilescu (Română)</option>
            <option value="aa">Almeida Revisada (Português)</option>
            <option value="wlc">WLC (Ancient Hebrew - OT)</option>
            <option value="tr">TR (Ancient Greek - NT)</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="book-select">{dict ? dict.bible.reader.book : "Book"}</label>
          <select 
            id="book-select"
            className="bible-select"
            value={selectedBook.name}
            onChange={(e) => {
              const book = BIBLE_BOOKS.find(b => b.name === e.target.value);
              if (book) {
                setSelectedBook(book);
                // Preserve chapter if the new book has at least that many chapters, otherwise fallback to chapter 1
                if (selectedChapter > book.chapters || selectedChapter < 1) {
                  setSelectedChapter(1);
                }
              }
            }}
          >
            {BIBLE_BOOKS.map((b, i) => {
              const locName = currentBible && currentBible[i] ? currentBible[i].name : b.name;
              return <option key={b.name} value={b.name}>{locName}</option>;
            })}
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="chapter-select">{dict ? dict.bible.reader.chapter : "Chapter"}</label>
          <select 
            id="chapter-select"
            className="bible-select"
            value={selectedChapter}
            onChange={(e) => setSelectedChapter(Number(e.target.value))}
          >
            {Array.from({ length: selectedBook.chapters }, (_, i) => i + 1).map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="bible-content-area">
        {loading && <div className="bible-loading">{dict ? dict.bible.reader.loading : "Loading Bible..."}</div>}
        {error && <div className="bible-error">{error}</div>}
        
        {!loading && !error && (
          <div className="bible-verses">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
              <h2 className="bible-chapter-title" style={{ margin: 0 }}>{localizedBookName} {selectedChapter}</h2>
              <ShareButton 
                title={`Bíblia - ${localizedBookName} ${selectedChapter}`}
                text={lang === 'pt' ? 'Leia este capítulo da Bíblia no Spurgeon.tv' : lang === 'es' ? 'Lee este capítulo de la Biblia en Spurgeon.tv' : 'Read this Bible chapter on Spurgeon.tv'}
              />
            </div>
            
            {verses.length === 0 ? (
              <p className="bible-verse" style={{ fontStyle: 'italic', opacity: 0.7, textAlign: 'center', marginTop: '2rem' }}>
                {dict ? dict.bible.reader.notAvailable : "Content not available in this translation."}
                {(translation === 'tr' && selectedBook.name !== 'Matthew') ? (dict ? dict.bible.reader.ntOnly : ' (Textus Receptus only contains the New Testament)') : ''}
                {(translation === 'wlc' && selectedBook.name === 'Matthew') ? (dict ? dict.bible.reader.otOnly : ' (WLC only contains the Old Testament)') : ''}
              </p>
            ) : (
              verses.map((text, i) => (
                <p key={i} className="bible-verse">
                  <sup className="bible-verse-num">{i + 1}</sup> {text}
                </p>
              ))
            )}
            
            {!loading && !error && verses.length > 0 && (
              <div style={{ marginTop: '3rem', marginBottom: '1.5rem', display: 'flex', justifyContent: 'center' }}>
                <ShareButton 
                  className="dev-share-large"
                  title={`Bíblia - ${localizedBookName} ${selectedChapter}`}
                  text={lang === 'pt' ? 'Leia este capítulo da Bíblia no Spurgeon.tv' : lang === 'es' ? 'Lee este capítulo de la Biblia en Spurgeon.tv' : 'Read this Bible chapter on Spurgeon.tv'}
                />
              </div>
            )}
          </div>
        )}

        {/* ── RELATED SERMONS SECTION ── */}
        {!loading && !error && relatedSermons.length > 0 && (
          <div style={{ marginTop: '4rem', paddingTop: '2rem', borderTop: '1px solid var(--border)' }}>
            <h3 style={{ color: 'var(--accent)', marginBottom: '1rem', fontSize: '1.2rem' }}>
              {dict ? dict.bible.reader.relatedSermons.replace('{book}', selectedBook.name).replace('{chapter}', selectedChapter) : `💡 Sermons based on ${selectedBook.name} ${selectedChapter}`}
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              {relatedSermons.map(sermon => (
                <li key={sermon.slug}>
                  <a href={`/${lang}/volume/${sermon.volume}/${sermon.slug}`} style={{ textDecoration: 'none', color: 'var(--text-primary)' }}>
                    <div style={{ background: 'var(--surface-2)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)', transition: 'border-color 0.2s' }}
                         onMouseOver={(e) => e.currentTarget.style.borderColor = 'var(--accent)'}
                         onMouseOut={(e) => e.currentTarget.style.borderColor = 'var(--border)'}>
                      <strong style={{ display: 'block', marginBottom: '0.25rem' }}>{sermon.title}</strong>
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        Volume {sermon.volumeNum} ({sermon.year}) • {sermon.scripture?.reference || sermon.scripture?.verse || ''}
                      </span>
                    </div>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      
      {/* Chapter Navigation */}
      <div className="bible-nav-footer">
        <button 
          className="bible-nav-btn"
          disabled={selectedChapter <= 1}
          onClick={() => setSelectedChapter(c => c - 1)}
        >
          &larr; {dict ? dict.bible.reader.previous : "Previous"}
        </button>
        <button 
          className="bible-nav-btn"
          disabled={selectedChapter >= selectedBook.chapters}
          onClick={() => setSelectedChapter(c => c + 1)}
        >
          {dict ? dict.bible.reader.next : "Next"} &rarr;
        </button>
      </div>

      {/* ── REFERÊNCIA CANÔNICA (CITATION BOX) ── */}
      <div style={{ marginTop: '2.5rem' }}>
        <CitationBox
          type="bible"
          lang={lang}
          url={typeof window !== 'undefined' ? window.location.href : `https://www.spurgeon.tv/${lang}/bible`}
          bibleRef={`${selectedBook ? selectedBook.name : ''} ${selectedChapter}`}
          compact
        />
      </div>

      {/* ── DETALHES RETRÁTEIS DA VERSÃO BÍBLICA ── */}
      <BibleVersionDetails 
        translation={translation} 
        lang={lang} 
      />
    </div>
  );
}
