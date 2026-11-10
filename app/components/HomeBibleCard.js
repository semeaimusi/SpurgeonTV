'use client';

import { useState, useEffect, useCallback } from 'react';
import { BIBLE_BOOKS } from '../../lib/bible-books';

const DAILY_VERSES = [
  { book: 'John', chapter: 3, verseIndex: 15,
    en: 'For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.',
    pt: 'Porque Deus tanto amou o mundo que deu o seu Filho Unigênito, para que todo o que nele crer não pereça, mas tenha a vida eterna.',
    es: 'Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna.'
  },
  { book: 'Psalms', chapter: 23, verseIndex: 0,
    en: 'The Lord is my shepherd; I shall not want.',
    pt: 'O Senhor é o meu pastor; de nada terei falta.',
    es: 'Jehová es mi pastor; nada me faltará.'
  },
  { book: 'Romans', chapter: 8, verseIndex: 27,
    en: 'And we know that all things work together for good to them that love God, to them who are the called according to his purpose.',
    pt: 'Sabemos que Deus age em todas as coisas para o bem daqueles que o amam, dos que foram chamados de acordo com o seu propósito.',
    es: 'Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien, esto es, a los que conforme a su propósito son llamados.'
  },
  { book: 'Philippians', chapter: 4, verseIndex: 12,
    en: 'I can do all things through Christ which strengtheneth me.',
    pt: 'Tudo posso naquele que me fortalece.',
    es: 'Todo lo puedo en Cristo que me fortalece.'
  },
  { book: 'Isaiah', chapter: 41, verseIndex: 9,
    en: 'Fear thou not; for I am with thee: be not dismayed; for I am thy God: I will strengthen thee; yea, I will help thee; yea, I will uphold thee with the right hand of my righteousness.',
    pt: 'Por isso não tema, pois estou com você; não tenha medo, pois sou o seu Deus. Eu o fortalecerei e o ajudarei; eu o segurarei com a minha mão direita vitoriosa.',
    es: 'No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo; siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia.'
  },
  { book: 'Proverbs', chapter: 3, verseIndex: 4,
    en: 'Trust in the Lord with all thine heart; and lean not unto thine own understanding.',
    pt: 'Confie no Senhor de todo o seu coração e não se apoie em seu próprio entendimento.',
    es: 'Fíate de Jehová de todo tu corazón, y no te apoyes en tu propia prudencia.'
  },
  { book: 'Matthew', chapter: 11, verseIndex: 27,
    en: 'Come unto me, all ye that labour and are heavy laden, and I will give you rest.',
    pt: 'Venham a mim, todos os que estão cansados e sobrecarregados, e eu darei descanso a vocês.',
    es: 'Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.'
  },
];

const getDayOfYear = () => {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = (now - start) + ((start.getTimezoneOffset() - now.getTimezoneOffset()) * 60 * 1000);
  return Math.floor(diff / (1000 * 60 * 60 * 24));
};

export default function HomeBibleCard({ lang, dict }) {
  const dailyVerseIndex = getDayOfYear() % DAILY_VERSES.length;
  const dailyVerse = DAILY_VERSES[dailyVerseIndex];

  const [isExpanded, setIsExpanded] = useState(false);
  const defaultTranslation = lang === 'pt' ? 'nvi' : (lang === 'es' ? 'nvies' : 'kjv');
  const [translation, setTranslation] = useState(defaultTranslation);
  const [selectedBook, setSelectedBook] = useState(BIBLE_BOOKS.find(b => b.name === dailyVerse.book) || BIBLE_BOOKS[0]);
  const [selectedChapter, setSelectedChapter] = useState(dailyVerse.chapter);
  const [verses, setVerses] = useState([]);
  const [bibleCache, setBibleCache] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const currentBible = bibleCache[translation];
  const bookIndex = BIBLE_BOOKS.findIndex(b => b.name === selectedBook.name);
  const localizedBookName = currentBible && currentBible[bookIndex] ? currentBible[bookIndex].name : selectedBook.name;

  const updateVerses = useCallback((bibleData) => {
    const idx = BIBLE_BOOKS.findIndex(b => b.name === selectedBook.name);
    if (idx !== -1 && bibleData[idx]) {
      const bookData = bibleData[idx];
      const chapterVerses = bookData.chapters[selectedChapter - 1] || [];
      setVerses(chapterVerses);
    } else {
      setVerses([]);
    }
  }, [selectedBook, selectedChapter]);

  useEffect(() => {
    if (!isExpanded) return;

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
        setError(dict?.bible?.reader?.error || 'Failed to load the Bible translation.');
        setVerses([]);
      } finally {
        setLoading(false);
      }
    }

    loadBible();
  }, [isExpanded, selectedBook, selectedChapter, translation, bibleCache, updateVerses, dict]);

  const handleToggle = () => {
    setIsExpanded(prev => !prev);
  };

  const bibleCardTitle = dict?.home?.bibleCard?.title || 'Read the Bible';
  const bibleCardSubtitle = dict?.home?.bibleCard?.subtitle || 'Read the Word of God right here on SpurgeonTV.';
  const expandLabel = dict?.home?.bibleCard?.expand || 'Open Reader';
  const collapseLabel = dict?.home?.bibleCard?.collapse || 'Close Reader';
  const fullPageLabel = dict?.home?.bibleCard?.fullPage || 'Full Bible Page';

  return (
    <section className="home-bible-card" style={{ marginTop: '1.5rem', marginBottom: '3.5rem' }}>
      <div className="home-bible-card-inner">
        {/* Header - always visible */}
        <div className="home-bible-card-header" onClick={handleToggle} role="button" tabIndex={0} aria-expanded={isExpanded}>
          <div className="home-bible-card-header-text">
            <div className="home-bible-card-icon">📖</div>
            <div>
              <h2 className="home-bible-card-title">{bibleCardTitle}</h2>
              <p className="home-bible-card-subtitle">{bibleCardSubtitle}</p>
            </div>
          </div>
          <button 
            className={`home-bible-toggle-btn ${isExpanded ? 'expanded' : ''}`} 
            onClick={(e) => { e.stopPropagation(); handleToggle(); }}
            aria-label={isExpanded ? collapseLabel : expandLabel}
          >
            <span className="home-bible-toggle-label">
              {isExpanded ? collapseLabel : expandLabel}
            </span>
            <svg className="home-bible-toggle-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>
        </div>

        {/* Sneak Peek - Visible when NOT expanded */}
        {!isExpanded && (
          <div className="home-devotional-snippet" onClick={handleToggle} style={{ cursor: 'pointer', padding: '0 2rem 1.5rem', opacity: 0.8 }}>
            <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--accent)', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '1px' }}>
              {lang === 'pt' ? 'Versículo do Dia' : lang === 'es' ? 'Versículo del Día' : 'Verse of the Day'} • {localizedBookName} {dailyVerse.chapter}:{dailyVerse.verseIndex + 1}
            </h4>
            <p style={{ margin: 0, fontStyle: 'italic', fontSize: '0.95rem' }}>
              &ldquo;{dailyVerse[lang] || dailyVerse.en}&rdquo; <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginLeft: '0.5rem', fontWeight: 'bold' }}>({translation.toUpperCase()})</span>
            </p>
          </div>
        )}

        {/* Controls - always visible when expanded (sticky) */}
        <div className={`home-bible-controls-wrapper ${isExpanded ? 'visible' : ''}`}>
          <div className="home-bible-controls">
            <div className="home-bible-control-group">
              <label>{dict?.bible?.reader?.version || "Version"}</label>
              <select
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
                <option value="aa">Almeida Revisada (Português)</option>
              </select>
            </div>

            <div className="home-bible-control-group">
              <label>{dict?.bible?.reader?.book || "Book"}</label>
              <select
                className="bible-select"
                value={selectedBook.name}
                onChange={(e) => {
                  const book = BIBLE_BOOKS.find(b => b.name === e.target.value);
                  setSelectedBook(book);
                  setSelectedChapter(1);
                }}
              >
                {BIBLE_BOOKS.map((b, i) => {
                  const locName = currentBible && currentBible[i] ? currentBible[i].name : b.name;
                  return <option key={b.name} value={b.name}>{locName}</option>;
                })}
              </select>
            </div>

            <div className="home-bible-control-group">
              <label>{dict?.bible?.reader?.chapter || "Chapter"}</label>
              <select
                className="bible-select"
                value={selectedChapter}
                onChange={(e) => setSelectedChapter(Number(e.target.value))}
              >
                {Array.from({ length: selectedBook.chapters }, (_, i) => i + 1).map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {/* Toggle button inside controls bar */}
            <div className="home-bible-control-group home-bible-control-toggle">
              <label>&nbsp;</label>
              <button
                className="home-bible-inline-toggle"
                onClick={handleToggle}
                title={collapseLabel}
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="18" height="18">
                  <polyline points="18 15 12 9 6 15" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Collapsible content */}
        <div className={`home-bible-content ${isExpanded ? 'expanded' : ''}`}>
          <div className="home-bible-content-inner">
            {loading && (
              <div className="bible-loading" style={{ textAlign: 'center', padding: '2rem' }}>
                {dict?.bible?.reader?.loading || "Loading Bible..."}
              </div>
            )}
            {error && (
              <div className="bible-error" style={{ textAlign: 'center', padding: '2rem', color: '#e74c3c' }}>
                {error}
              </div>
            )}

            {!loading && !error && isExpanded && (
              <div className="bible-verses">
                <h3 className="bible-chapter-title" style={{ margin: '0 0 1.5rem 0' }}>
                  {localizedBookName} {selectedChapter}
                </h3>

                {verses.length === 0 ? (
                  <p style={{ fontStyle: 'italic', opacity: 0.7, textAlign: 'center', marginTop: '2rem' }}>
                    {dict?.bible?.reader?.notAvailable || "Content not available in this translation."}
                  </p>
                ) : (
                  verses.map((text, i) => {
                    const isHighlighted = selectedBook.name === dailyVerse.book && selectedChapter === dailyVerse.chapter && i === dailyVerse.verseIndex;
                    return (
                      <p 
                        key={i} 
                        className="bible-verse" 
                        style={isHighlighted ? { backgroundColor: 'rgba(212, 175, 55, 0.15)', padding: '0.5rem', borderRadius: '8px', borderLeft: '3px solid var(--accent)' } : {}}
                      >
                        <sup className="bible-verse-num">{i + 1}</sup> {text}
                      </p>
                    );
                  })
                )}
              </div>
            )}

            {/* Chapter navigation */}
            {!loading && !error && isExpanded && verses.length > 0 && (
              <div className="home-bible-nav">
                <button
                  className="bible-nav-btn"
                  disabled={selectedChapter <= 1}
                  onClick={() => setSelectedChapter(c => c - 1)}
                >
                  &larr; {dict?.bible?.reader?.previous || "Previous"}
                </button>
                <a
                  href={`/${lang}/bible?book=${selectedBook.name}&chapter=${selectedChapter}`}
                  className="home-bible-fullpage-link"
                >
                  {fullPageLabel} →
                </a>
                <button
                  className="bible-nav-btn"
                  disabled={selectedChapter >= selectedBook.chapters}
                  onClick={() => setSelectedChapter(c => c + 1)}
                >
                  {dict?.bible?.reader?.next || "Next"} &rarr;
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
