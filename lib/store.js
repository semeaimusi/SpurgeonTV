import storeProducts from '../data/store-products.json';

export function getStoreProducts(lang = 'en') {
  const targetLang = ['pt', 'es', 'en'].includes(lang) ? lang : 'en';

  return storeProducts.map(product => {
    const isFree = product.pricingType === 'free';
    const isComingSoon = !!product.isComingSoon;
    const pricingType = isFree ? 'free' : (isComingSoon ? 'waitlist' : 'paid');

    const localized = product.i18n?.[targetLang] || product.i18n?.['en'] || {};

    return {
      id: product.id,
      category: product.category,
      type: product.type,
      pricingType,
      platform: product.platform,
      badge: localized.badge || product.badge,
      isOwnProduct: !!product.isOwnProduct,
      isComingSoon: isComingSoon,
      image: localized.image || product.image,
      externalUrl: localized.externalUrl || product.externalUrl,
      title: localized.title || product.title,
      author: localized.author || product.author,
      shortDesc: localized.shortDesc || product.shortDesc,
      fullDesc: localized.fullDesc || product.fullDesc,
      highlights: localized.highlights || product.highlights || [],
      targetAudience: localized.targetAudience || product.targetAudience || null,
      specs: localized.specs || product.specs || {}
    };
  });
}
