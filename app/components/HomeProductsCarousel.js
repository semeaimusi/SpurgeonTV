'use client';

import React, { useRef } from 'react';
import Link from 'next/link';

export default function HomeProductsCarousel({
  products = [],
  dict,
  lang = 'en'
}) {
  const scrollRef = useRef(null);

  if (!products || products.length === 0) {
    return null;
  }

  const scroll = (direction) => {
    if (scrollRef.current) {
      const scrollAmount = direction === 'left' ? -320 : 320;
      scrollRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  const carouselDict = dict?.home?.storeCarousel || {};
  const eyebrow = carouselDict.eyebrow || (lang === 'pt' ? 'LIVRARIA RECOMENDADA' : lang === 'es' ? 'LIBRERÍA RECOMENDADA' : 'RECOMMENDED BOOKSHOP');
  const title = carouselDict.title || (lang === 'pt' ? 'Recursos & Livros em Destaque' : lang === 'es' ? 'Recursos y Libros Destacados' : 'Featured Books & Resources');
  const subtitle = carouselDict.subtitle || (lang === 'pt' ? 'Obras selecionadas para aprofundar seu conhecimento bíblico e teológico' : lang === 'es' ? 'Obras seleccionadas para profundizar su conocimiento bíblico y teológico' : 'Curated works to deepen your biblical and theological knowledge');
  const viewStore = carouselDict.viewStore || (lang === 'pt' ? 'Visitar Livraria' : lang === 'es' ? 'Visitar Librería' : 'Visit Bookshop');

  return (
    <section className="home-store-section home-bible-card" style={{ marginTop: '3.5rem', marginBottom: '3.5rem' }}>
      <div className="home-section-header home-store-header" style={{ padding: '0 0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <p className="home-section-eyebrow">{eyebrow}</p>
          <h2 className="home-section-title">{title}</h2>
          <p className="home-section-subtitle">{subtitle}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Link href={`/${lang}/store`} className="home-see-all">
            {viewStore} <span>→</span>
          </Link>
          <div className="home-store-arrows">
            <button
              type="button"
              className="home-store-arrow-btn"
              onClick={() => scroll('left')}
              aria-label="Rolar para a esquerda"
            >
              ‹
            </button>
            <button
              type="button"
              className="home-store-arrow-btn"
              onClick={() => scroll('right')}
              aria-label="Rolar para a direita"
            >
              ›
            </button>
          </div>
        </div>
      </div>

      <div className="home-store-carousel-container">
        <div className="home-store-carousel-track" ref={scrollRef}>
          {products.map((product) => {
            const destUrl = product.externalUrl || `/${lang}/store`;
            const isExternal = !!product.externalUrl;

            return (
              <a
                key={product.id}
                href={destUrl}
                target={isExternal ? '_blank' : '_self'}
                rel={isExternal ? 'noopener noreferrer' : undefined}
                className="home-store-card"
                title={product.title}
              >
                <div className="home-store-cover-wrap">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={product.image}
                    alt={product.title}
                    className="home-store-cover-img"
                    loading="lazy"
                  />
                  <div className="home-store-cover-shine" aria-hidden="true" />
                </div>
                
                <div className="home-store-card-info">
                  <h3 className="home-store-card-title">{product.title}</h3>
                  <div className="home-store-card-meta">
                    <span className="home-store-platform">{product.platform || 'Oficial'}</span>
                    <span className="home-store-arrow-link" aria-hidden="true">→</span>
                  </div>
                </div>
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
}

