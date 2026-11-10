import { getStoreProducts } from '../../../lib/store';
import { getDictionary } from '../../../lib/dictionaries';
import StoreClient from './StoreClient';

export const revalidate = false;
export const dynamic = 'auto';

export async function generateStaticParams() {
  return [{ lang: 'en' }, { lang: 'pt' }, { lang: 'es' }];
}

export async function generateMetadata({ params }) {
  const { lang } = await params;
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://spurgeon.tv';

  const meta = {
    pt: {
      title: 'Livraria Spurgeon TV',
      description: 'Recomendações selecionadas para o seu crescimento bíblico: manuais de cronologia, e-books e recursos teológicos.',
      keywords: ['Livraria Spurgeon TV', 'Linha do Tempo Bíblica', 'O Sermão de Emaús', '143 Perguntas que a Bíblia Responde', 'A Ressurreição de Jesus Cristo', 'Livros Evangélicos', 'Amazon', 'Hotmart']
    },
    en: {
      title: 'Spurgeon TV Bookshop',
      description: 'Selected recommendations for your biblical growth: chronological manuals, e-books, and theological resources.',
      keywords: ['Spurgeon TV Bookshop', 'Biblical Timeline', 'The Emmaus Sermon', '143 Questions the Bible Answers', 'The Resurrection of Jesus Christ', 'Christian Books', 'Amazon', 'Hotmart']
    },
    es: {
      title: 'Librería Spurgeon TV',
      description: 'Recomendaciones seleccionadas para su crecimiento bíblico: manuales cronológicos, libros electrónicos y recursos teológicos.',
      keywords: ['Librería Spurgeon TV', 'Línea de Tiempo Bíblica', 'El Sermón de Emaús', '143 Preguntas que la Biblia Responde', 'La Resurrección de Jesucristo', 'Libros Cristianos', 'Amazon', 'Hotmart']
    }
  }[lang] || {};

  return {
    title: `${meta.title} | SPURGEON TV`,
    description: meta.description,
    keywords: meta.keywords,
    alternates: {
      canonical: `${siteUrl}/${lang}/store/`,
      languages: {
        'pt': `${siteUrl}/pt/store/`,
        'en': `${siteUrl}/en/store/`,
        'es': `${siteUrl}/es/store/`,
      }
    },
    openGraph: {
      title: `${meta.title} | SPURGEON TV`,
      description: meta.description,
      url: `${siteUrl}/${lang}/store/`,
      siteName: 'SpurgeonTV',
      images: [
        {
          url: `${siteUrl}/images/store/143_perguntas_biblia.png`,
          width: 500,
          height: 791,
          alt: meta.title,
        }
      ],
      type: 'website',
    }
  };
}

export default async function StorePage({ params }) {
  const { lang } = await params;
  const dict = await getDictionary(lang);
  const products = getStoreProducts(lang);

  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://spurgeon.tv';

  const schemaJsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": dict.navigation?.store || "Livraria Spurgeon TV",
    "url": `${siteUrl}/${lang}/store/`,
    "description": "Catálogo com livros, obras de Charles Spurgeon e recursos bíblicos recomendados.",
    "publisher": {
      "@type": "Organization",
      "name": "SpurgeonTV",
      "url": siteUrl
    },
    "mainEntity": {
      "@type": "ItemList",
      "itemListElement": products.map((p, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": {
          "@type": p.category === 'books' ? "Book" : "CreativeWork",
          "name": p.title,
          "description": p.shortDesc,
          "image": p.image?.startsWith('http') ? p.image : `${siteUrl}${p.image}`,
          "url": p.externalUrl?.startsWith('http') ? p.externalUrl : `${siteUrl}/${lang}/store/`,
          "author": {
            "@type": "Person",
            "name": p.author || "Charles Spurgeon"
          },
          "publisher": {
            "@type": "Organization",
            "name": p.platform || "Spurgeon TV"
          }
        }
      }))
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaJsonLd) }}
      />
      <StoreClient
        products={products}
        lang={lang}
        dict={dict}
      />
    </>
  );
}
