# -*- coding: utf-8 -*-
"""
Bible Translation Data - Part 1:
- kjv (King James Version 1611/1769)
- niv (New International Version 1984)
- web (World English Bible 2000)
- asv (American Standard Version 1901)
- acf (Almeida Corrigida Fiel 1994/2011)
- nvi (Nova Versão Internacional - PT 2001)
- nvies (Nueva Versión Internacional - ES 1999/2022)
- rvr1960 (Reina-Valera 1960)
- lbla (La Biblia de las Américas 1986/1997)
"""

PART1 = {}

def reg(k, en, pt, es):
    PART1[k] = {'key': k, 'en': en, 'pt': pt, 'es': es}

# 1. KJV
reg(
    'kjv',
    en={
        'name': 'King James Version (KJV)',
        'fullName': 'The Authorized King James Version (1611 / 1769 Blayney Revision)',
        'year': '1611 (Standardized 1769)',
        'abbrev': 'KJV',
        'language': 'English',
        'philosophy': 'Formal Equivalence (Literal Word-for-Word Fidelity)',
        'manuscripts': 'Old Testament: Masoretic Text (Second Rabbinic Bible by Jacob ben Hayyim / Daniel Bomberg, Venice, 1524–1525). New Testament: Textus Receptus (primarily Robert Estienne/Stephanus 1550 and Theodore Beza 1598 editions).',
        'translators': 'Commissioned by King James I of England following the Hampton Court Conference (1604). Translated by 47 eminent scholars and linguists organized into six working companies across Westminster, Oxford, and Cambridge (including Lancelot Andrewes, Edward Lively, and John Bois).',
        'history': (
            'Commissioned in 1604 to resolve ecclesiastical friction between Anglicans and Puritans, '
            'the King James Version sought a single, majestic, and unified translation without divisive marginal polemics. '
            'The six translation committees met rigorously for seven years, comparing Tyndale, Coverdale, the Matthew Bible, '
            'the Great Bible, the Bishops’ Bible, and the Geneva Bible against the original Hebrew and Greek texts. '
            'Published by the King’s Printer Robert Barker in 1611, it became the undisputed English Bible for over three centuries, '
            'shaping modern English vocabulary, idioms, syntax, and Christian preaching across the British Empire and America.'
        ),
        'features': [
            'Profound literary cadence designed specifically for oral reading and public preaching in Christian assemblies.',
            'Italicized words indicate words supplied by translators to complete English grammar not explicitly present in original manuscripts.',
            'Distinct singular ("thou/thee/thy") and plural ("ye/you/your") pronouns, reflecting precise Greek and Hebrew grammar.',
            'Renders the Divine Name (Tetragrammaton YHWH) as "LORD" in small capitals, and "Jehovah" in specific exalted instances (Exodus 6:3; Psalm 83:18).',
            'Incorporates the standardized Oxford spelling and punctuation revised by Dr. Benjamin Blayney in 1769.'
        ],
        'theologyAndLegacy': (
            'The King James Version was the foundational pulpit Bible of Charles Haddon Spurgeon throughout his entire 38-year '
            'ministry at the Metropolitan Tabernacle in London. Spurgeon famously proclaimed: "This volume is the city of God, '
            'whereof the Lord is the eternal light... Love this book, believe it, practice it, and you shall never be ashamed." '
            'Its rich theological vocabulary (justification, propitiation, redemption, sanctification) formed the backbone of English Reformed and Evangelical theology.'
        ),
        'scopeAndUsage': 'Unquestionably the most printed and influential book in the history of the English language, used globally in public worship, personal devotions, and classical literature.',
        'copyright': 'Public Domain worldwide (Perpetual Crown Copyright held by the British Crown in the United Kingdom via Cambridge University Press).'
    },
    pt={
        'name': 'King James Version (KJV)',
        'fullName': 'The Authorized King James Version (1611 / Revisão de Blayney de 1769)',
        'year': '1611 (Padronizada em 1769)',
        'abbrev': 'KJV',
        'language': 'Inglês',
        'philosophy': 'Equivalência Formal Estrita (Fidelidade Literal Palavra por Palavra)',
        'manuscripts': 'Antigo Testamento: Texto Massorético Hebraico (Segunda Bíblia Rabínica de Daniel Bomberg / Jacob ben Hayyim, 1524–1525). Novo Testamento: Textus Receptus Grego (principalmente edições de Robert Estienne/Stephanus 1550 e Theodore Beza 1598).',
        'translators': 'Comissionada pelo Rei James I da Inglaterra após a Conferência de Hampton Court (1604). Executada por 47 dos maiores eruditos, linguistas e teólogos da época, divididos em seis companhias de tradução em Westminster, Oxford e Cambridge (incluindo Lancelot Andrewes e John Bois).',
        'history': (
            'Convocada em 1604 para pacificar as tensões entre anglicanos e puritanos, a King James Version almejava uma tradução pública única, '
            'solene e autorizada, desprovida de notas marginais polêmicas. Durante sete anos, as comissões examinaram minuciosamente as traduções de '
            'William Tyndale, Miles Coverdale, a Bíblia de Genebra e a Bíblia dos Bispos, cotejando cada versículo diretamente com os originais hebraicos e gregos. '
            'Publicada em 1611 pelo impressor real Robert Barker, consolidou-se como o padrão supremo da língua inglesa por mais de três séculos, moldando a literatura ocidental.'
        ),
        'features': [
            'Cadência rítmica e majestade sonora concebida propositalmente para proclamação em voz alta no púlpito.',
            'Uso sistemático de itálicos para indicar palavras adicionadas pelos tradutores para clareza em inglês que não constavam explicitamente no original.',
            'Distinção rigorosa entre pronomes da segunda pessoa do singular ("thou/thee") e do plural ("ye/you"), refletindo fielmente a morfologia grega e hebraica.',
            'Tradução do Tetragrama YHWH como "LORD" (SENHOR em versalete) e "Jehovah" em passagens emblemáticas (Êxodo 6:3; Salmo 83:18).',
            'Adota a padronização ortográfica e tipográfica clássica de Oxford, realizada pelo Dr. Benjamin Blayney em 1769.'
        ],
        'theologyAndLegacy': (
            'A KJV foi a Bíblia de púlpito e de coração de Charles Haddon Spurgeon durante todo o seu lendário ministério no Metropolitan Tabernacle de Londres. '
            'Spurgeon afirmava que as páginas da Authorized Version eram ricas como as minas de Ofir e doces como o favo de mel. '
            'Sua teologia calvinista e batista floresceu respaldada na riqueza vocabular e exatidão doutrinária desta tradução.'
        ),
        'scopeAndUsage': 'A obra literária mais publicada e influente de todos os tempos no mundo de língua inglesa, reverenciada globalmente por pregadores, acadêmicos e leigos.',
        'copyright': 'Domínio Público mundial (sob prerrogativa Perpétua da Coroa Britânica administrada pela Cambridge University Press apenas no Reino Unido).'
    },
    es={
        'name': 'King James Version (KJV)',
        'fullName': 'The Authorized King James Version (1611 / Revisión de Blayney de 1769)',
        'year': '1611 (Estandarizada en 1769)',
        'abbrev': 'KJV',
        'language': 'Inglés',
        'philosophy': 'Equivalencia Formal Estricta (Fidelidad Literal Palabra por Palabra)',
        'manuscripts': 'Antiguo Testamento: Texto Masorético Hebreo (Segunda Biblia Rabínica de Bomberg / Jacob ben Hayyim, 1524–1525). Nuevo Testamento: Textus Receptus Griego (edición de Stephanus 1550 y Beza 1598).',
        'translators': 'Encargada por el rey Jacobo I de Inglaterra tras la Conferencia de Hampton Court (1604). Realizada por 47 eminentes eruditos bíblicos y lingüistas organizados en seis compañías en Westminster, Oxford y Cambridge.',
        'history': (
            'Comisionada en 1604 para brindar una versión autorizada y sin notas sectarias que unificara a la iglesia angloparlante. '
            'Durante siete años de exhaustiva labor colegiada, los eruditos compararon las traducciones de Tyndale y la Biblia de Ginebra con los textos originales. '
            'Impresa en 1611, se convirtió en la cúspide de la lengua inglesa y en el texto canónico indiscutible del cristianismo anglosajón por más de trescientos años.'
        ),
        'features': [
            'Prosa de extraordinaria belleza poética y musicalidad, creada especialmente para la proclamación pública desde el púlpito.',
            'Letras cursivas (itálicas) que señalan vocablos necesarios en inglés que no aparecen en los manuscritos hebreos o griegos originales.',
            'Diferenciación exacta de pronombres singulares y plurales de segunda persona, preservando la precisión gramatical bíblica.',
            'Representación del Nombre Divino YHWH como "LORD" (SEÑOR en mayúsculas pequeñas) y "Jehovah" en proclamaciones solemnes.',
            'Edición estandarizada conforme a la revisión de Oxford de 1769 dirigida por el Dr. Benjamin Blayney.'
        ],
        'theologyAndLegacy': (
            'Fue la versión viva desde la cual predicó Charles H. Spurgeon durante más de 38 años en el Tabernáculo Metropolitano de Londres. '
            'Spurgeon la describió como un manantial inagotable de gracia y autoridad evangélica, inspirando a generaciones de predicadores reformados y puritanos.'
        ),
        'scopeAndUsage': 'La traducción bíblica más distribuida e influyente de la historia en el idioma inglés, venerada en congregaciones, seminarios y academias internacionales.',
        'copyright': 'Dominio Público universal (con derechos de Corona administrados por Cambridge University Press en el Reino Unido).'
    }
)

# 2. NIV (1984)
reg(
    'niv',
    en={
        'name': 'New International Version (NIV 1984)',
        'fullName': 'The Holy Bible: New International Version (1984 Classic Edition)',
        'year': '1978 (Complete Bible), 1984 (Canonical Classic Revision)',
        'abbrev': 'NIV 1984',
        'language': 'English',
        'philosophy': 'Optimal Equivalence (Balance of Formal Accuracy and Natural Modern Clarity)',
        'manuscripts': 'Old Testament: Biblia Hebraica Stuttgartensia (Masoretic Text), Samaritan Pentateuch, Septuagint, and Dead Sea Scrolls. New Testament: Eclectic Greek New Testament (Nestle-Aland 26th / United Bible Societies 3rd edition).',
        'translators': 'Committee on Bible Translation (CBT), sponsored by the New York International Bible Society (now Biblica). Over 100 interdenominational evangelical scholars from the United States, Great Britain, Canada, Australia, and New Zealand, chaired by Dr. Edwin H. Palmer and Dr. Kenneth L. Barker.',
        'history': (
            'The NIV originated in the 1950s and 1960s among evangelical scholars who recognized the need for a contemporary English translation '
            'that was not tied to Elizabethan archaic English (like the KJV) nor compromised by theological liberalism (felt by many in the RSV). '
            'In 1965, committees from the Christian Reformed Church and the National Association of Evangelicals met in Palos Heights and Chicago, '
            'initiating the project. The New Testament appeared in 1973, the full Bible in 1978, and the landmark 1984 revision became the gold standard '
            'evangelical Bible for three decades.'
        ),
        'features': [
            'Avoids both wooden hyper-literalism and paraphrastic liberties, translating thought-for-thought where necessary while preserving grammatical contours.',
            'Retains traditional theological terminology (e.g., "justification", "covenant", "saints", "propitiation").',
            'Preserves historical gender references faithfully reflecting the Hebrew and Greek text (e.g., Psalm 1:1 "Blessed is the man", 1 Tim 2:12), unlike later 2011 gender-neutral revisions.',
            'Poetic formatting for Hebrew poetry, wisdom literature, and prophecies with indented parallelisms.',
            'Extensive translational footnotes detailing alternative readings in ancient manuscripts (Septuagint, Dead Sea Scrolls, Vulgate).'
        ],
        'theologyAndLegacy': (
            'The 1984 edition of the NIV is widely recognized as the peak of modern evangelical Bible translation. '
            'It was praised by theologians such as J. I. Packer, D. A. Carson, John Stott, and F. F. Bruce. '
            'When publisher Biblica withdrew the 1984 edition in 2011 to replace it with a gender-modified text, '
            'millions of evangelical pastors, theologians, and churches worldwide rallied to preserve the 1984 text as their canonical study standard.'
        ),
        'scopeAndUsage': 'The best-selling Bible translation in the English-speaking world from 1986 to 2011, standard across thousands of evangelical churches and seminaries.',
        'copyright': 'Copyright © 1973, 1978, 1984 by Biblica, Inc. (formerly International Bible Society). Archived for classical historical study.'
    },
    pt={
        'name': 'New International Version (NIV 1984)',
        'fullName': 'The Holy Bible: New International Version (Edição Clássica de 1984)',
        'year': '1978 (Bíblia Completa), 1984 (Revisão Canônica Clássica)',
        'abbrev': 'NIV 1984',
        'language': 'Inglês',
        'philosophy': 'Equivalência Equilibrada / Ótima (Equilíbrio entre Precisão e Clareza Contemporânea)',
        'manuscripts': 'Antigo Testamento: Biblia Hebraica Stuttgartensia (Texto Massorético), Manuscritos do Mar Morto e Septuaginta. Novo Testamento: Texto Crítico Eclético Grego (Nestle-Aland 26ª ed. / Sociedades Bíblicas Unidas 3ª ed.).',
        'translators': 'Committee on Bible Translation (CBT), patrocinado pela Sociedade Bíblica Internacional (Biblica). Mais de 100 eruditos e biblistas evangélicos dos EUA, Grã-Bretanha, Canadá, Austrália e Nova Zelândia, sob a liderança do Dr. Edwin H. Palmer e Dr. Kenneth L. Barker.',
        'history': (
            'Nascida na década de 1960 da necessidade de uma tradução moderna em língua inglesa fiel à inerrância bíblica, '
            'livre do inglês arcaico da KJV e das inclinações teológicas liberais percebidas na RSV. '
            'O Novo Testamento foi lançado em 1973 e a Bíblia completa em 1978. A revisão de 1984 alcançou aclamação global, '
            'tornando-se por mais de 25 anos a Bíblia de cabeceira e de púlpito de quase todo o mundo evangélico de língua inglesa.'
        ),
        'features': [
            'Comunicação natural em inglês contemporâneo de alto nível, mantendo fidelidade absoluta ao sentido gramatical original.',
            'Preservação rigorosa dos termos teológicos clássicos da fé cristã histórica (propiciação, justificação, redenção).',
            'Fidelidade ao gênero dos termos bíblicos originais (ex.: Salmo 1:1 "Blessed is the man", 1 Tm 2:12), sem adoção de linguagem neutra.',
            'Estrutura poética com recuos e paralelismos hebraicos nos livros sapienciais e proféticos.',
            'Notas de rodapé que documentam variantes textuais significativas de manuscritos antigos.'
        ],
        'theologyAndLegacy': (
            'Considerada a "edição de ouro" da NIV em inglês. Apoiada por teólogos de estatura como J. I. Packer, F. F. Bruce e D. A. Carson. '
            'A substituição forçada desta edição em 2011 por uma revisão com linguagem neutra gerou grande resistência entre evangélicos tradicionais, '
            'fazendo com que a edição de 1984 se tornasse um tesouro raro e altamente valorizado para estudos e pregação bíblica.'
        ),
        'scopeAndUsage': 'A versão bíblica mais vendida e citada do mundo anglófono nas décadas de 1980, 1990 e 2000.',
        'copyright': 'Copyright © 1973, 1978, 1984 por Biblica, Inc. Preservada para pesquisa teológica e estudo histórico.'
    },
    es={
        'name': 'New International Version (NIV 1984)',
        'fullName': 'The Holy Bible: New International Version (Edición Clásica de 1984)',
        'year': '1978 (Biblia Completa), 1984 (Revisión Canónica Clásica)',
        'abbrev': 'NIV 1984',
        'language': 'Inglés',
        'philosophy': 'Equivalencia Óptima (Equilibrio entre Precisión Formal y Fluidez Moderna)',
        'manuscripts': 'Antiguo Testamento: Biblia Hebraica Stuttgartensia (Texto Masorético) y Rollos del Mar Muerto. Nuevo Testamento: Texto Crítico Griego (Nestle-Aland 26ª ed. / UBS 3ª ed.).',
        'translators': 'Committee on Bible Translation (CBT), auspiciado por Biblica (antes International Bible Society). Más de 100 eruditos bíblicos evangélicos internacionales liderados por el Dr. Edwin H. Palmer.',
        'history': (
            'Surgida en la década de 1960 para ofrecer al mundo de habla inglesa una traducción contemporánea de máxima fidelidad bíblica. '
            'Publicada en 1978 y perfeccionada en su célebre revisión de 1984, fue el texto estándar más leído y respetado por predicadores y seminaristas evangélicos durante tres décadas.'
        ),
        'features': [
            'Prosa inglesa moderna fluida, ideal para lectura continua y memorización devocional.',
            'Mantiene los términos teológicos clásicos de la teología reformada y evangélica.',
            'Fidelidad a la traducción literal de géneros en textos canónicos (ej. Salmo 1:1 "Blessed is the man") antes de las revisiones de lenguaje neutro de 2011.',
            'Estructuración poética fiel de los paralelismos hebreos en Salmos y Profetas.'
        ],
        'theologyAndLegacy': (
            'La edición de 1984 es considerada la cúspide de la traducción evangélica moderna en inglés. '
            'Cuando la editorial la descatalogó en 2011 para promover una revisión de lenguaje inclusivo, miles de iglesias mantuvieron la edición de 1984 como su texto canónico inalterable.'
        ),
        'scopeAndUsage': 'La Biblia moderna en inglés más vendida y distribuida entre 1986 y 2011 en los Estados Unidos, Reino Unido y países de la Mancomunidad.',
        'copyright': 'Copyright © 1973, 1978, 1984 por Biblica, Inc. Preservada para consulta y estudio histórico canónico.'
    }
)

# 3. WEB (World English Bible)
reg(
    'web',
    en={
        'name': 'World English Bible (WEB)',
        'fullName': 'World English Bible (Complete Modern Public Domain Bible)',
        'year': '2000 (Ongoing refinements)',
        'abbrev': 'WEB',
        'language': 'English',
        'philosophy': 'Formal Equivalence (Faithful, Modern, and Completely Free of Royalties)',
        'manuscripts': 'Old Testament: Biblia Hebraica Stuttgartensia (Masoretic Text). New Testament: Greek Majority Text (Hodges & Farstad) with reference to the Byzantine Textform (Robinson-Pierpont) and critical readings in footnotes.',
        'translators': 'Initiated and coordinated by Michael Paul Johnson, with a dedicated community of Christian linguists, Hebrew/Greek scholars, and volunteer proofreaders worldwide.',
        'history': (
            'Begun in 1997, the World English Bible project was founded on a noble premise: to provide a high-quality, modern English translation '
            'of the Holy Scriptures that is completely free from copyright restrictions, licensing fees, and legal entanglements. '
            'Using the 1901 American Standard Version (ASV) as its base, the team methodically modernized archaic pronouns, verb endings, and obsolete grammar '
            'while checking every verse against the original Hebrew and Greek texts.'
        ),
        'features': [
            '100% Dedicated to the Public Domain — anyone can freely print, quote, publish, program, and distribute without asking permission.',
            'Translates God’s Covenant Name as "Yahweh" in the Old Testament, recovering the divine memorial name revealed to Moses.',
            'Uses clear, natural, contemporary English grammar without colloquialism or theological watering-down.',
            'Greek New Testament text is rooted in the historic Majority Text consensus of ancient manuscripts.'
        ],
        'theologyAndLegacy': (
            'The WEB represents the modern continuation of the historic Protestant open-access ideal: that the Word of God belongs to all mankind '
            'and should never be monopolized by commercial publishing houses. Its theological stance is orthodox, Protestant, and deeply reverent.'
        ),
        'scopeAndUsage': 'Extensively used worldwide in digital Bible software, mobile apps, missionary translations, print-on-demand publishing, and Christian websites.',
        'copyright': 'Dedicated to the Public Domain (No copyright restrictions worldwide).'
    },
    pt={
        'name': 'World English Bible (WEB)',
        'fullName': 'World English Bible (Tradução Moderna em Domínio Público Total)',
        'year': '2000 (com refinamentos contínuos)',
        'abbrev': 'WEB',
        'language': 'Inglês',
        'philosophy': 'Equivalência Formal Clara (Fiel, Moderna e 100% Livre de Direitos Autorais)',
        'manuscripts': 'Antigo Testamento: Biblia Hebraica Stuttgartensia (Texto Massorético). Novo Testamento: Texto Majoritário Grego (Majority Text / Byzantine Textform de Hodges & Farstad e Robinson-Pierpont).',
        'translators': 'Iniciado e coordenado por Michael Paul Johnson, com o apoio de uma rede internacional de biblistas, revisores e teólogos cristãos voluntários.',
        'history': (
            'Iniciado em 1997, o projeto World English Bible nasceu para superar uma das maiores barreiras do mundo digital cristão: os direitos autorais '
            'e royalties restritivos de editoras comerciais. Tomando a respeitada American Standard Version (ASV de 1901) como base textual, '
            'os colaboradores atualizaram meticulosamente o vocabulário e a sintaxe para o inglês contemporâneo fluente, '
            'confrontando cada termo com os manuscritos originais em hebraico e grego.'
        ),
        'features': [
            'Completamente dedicada ao Domínio Público: pode ser copiada, impressa, citada e embutida em aplicativos sem taxas ou autorizações.',
            'Verte o Tetragrama Sagrado como "Yahweh" no Antigo Testamento, resgatando a memória do nome pactual do Deus de Israel.',
            'Inglês contemporâneo claro, digno e gramaticalmente esmerado, sem recorrer a gírias ou simplificações banais.',
            'Base do Novo Testamento fundamentada na linhagem do Texto Majoritário/Bizantino grego.'
        ],
        'theologyAndLegacy': (
            'Encarna o espírito da Reforma Protestante do século XVI: a Bíblia livre e acessível a todo ser humano em sua própria língua. '
            'É amplamente adotada em plataformas digitais globais e projetos missionários independentes.'
        ),
        'scopeAndUsage': 'Padrão ouro para desenvolvedores de software bíblico, ministérios em países em desenvolvimento e publicações acadêmicas abertas.',
        'copyright': 'Domínio Público universal (livre de direitos autorais).'
    },
    es={
        'name': 'World English Bible (WEB)',
        'fullName': 'World English Bible (Traducción Moderna en Dominio Público Total)',
        'year': '2000 (con revisiones continuas)',
        'abbrev': 'WEB',
        'language': 'Inglés',
        'philosophy': 'Equivalencia Formal Moderna (Fiel y 100% Libre de Regalías)',
        'manuscripts': 'Antiguo Testamento: Biblia Hebraica Stuttgartensia (Texto Masorético). Nuevo Testamento: Texto Mayoritario Griego (Majority Text).',
        'translators': 'Coordinada por Michael Paul Johnson y un equipo internacional de lingüistas y eruditos bíblicos voluntarios.',
        'history': (
            'Iniciada en 1997 con el propósito de crear una Biblia en inglés moderno de altísima fidelidad formal sin las trabas de copyright '
            'que imponen las editoriales comerciales. Actualizó la clásica American Standard Version (ASV 1901) al inglés del siglo XXI.'
        ),
        'features': [
            '100% en Dominio Público: libre de regalías, permisos o restricciones legales para cualquier ministerio o creyente en el mundo.',
            'Traduce el Nombre del Pacto como "Yahweh" en el Antiguo Testamento.',
            'Lenguaje contemporáneo digno, fiel a los manuscritos originales y desprovisto de arcaísmos confusos.'
        ],
        'theologyAndLegacy': (
            'Restaura el ideal reformado de acceso libre y universal a las Sagradas Escrituras, ampliamente utilizada por aplicaciones y comunidades cristianas de todo el planeta.'
        ),
        'scopeAndUsage': 'Muy popular en aplicaciones bíblicas digitales, ministerios misioneros y distribución en internet.',
        'copyright': 'Dominio Público universal.'
    }
)

# 4. ASV (American Standard Version 1901)
reg(
    'asv',
    en={
        'name': 'American Standard Version (ASV)',
        'fullName': 'The Holy Bible: American Standard Version (Standard American Edition of the Revised Version)',
        'year': '1901',
        'abbrev': 'ASV',
        'language': 'English',
        'philosophy': 'Strict Formal Equivalence (Extreme Literal Precision and Textual Rigor)',
        'manuscripts': 'Old Testament: Masoretic Text with reference to ancient versions. New Testament: Greek Critical Text of Westcott & Hort (1881) and Tregelles.',
        'translators': 'The American Bible Revision Committee, composed of 30 of the most distinguished biblical scholars in the United States (including Philip Schaff, Charles Hodge, Benjamin B. Warfield, and William Henry Green), working in coordination with the British Revision Committee.',
        'history': (
            'In 1870, the Church of England initiated a revision of the 1611 King James Version to incorporate the wealth of newly discovered '
            'ancient biblical manuscripts (such as Codex Sinaiticus and Codex Vaticanus). An American committee was formed in 1871 under the chairmanship '
            'of Church historian Philip Schaff. When the English Revised Version (ERV) was released in 1881–1885, the American scholars pledged not to publish '
            'their own preferred readings for 14 years. In 1901, Thomas Nelson & Sons published the American Standard Version containing the American preferences, '
            'praised universally for its uncompromising, word-for-word accuracy.'
        ),
        'features': [
            'Regarded by scholars as the most rigorously literal translation of the Bible into English ever executed.',
            'Systematically translates the divine Tetragrammaton YHWH as "Jehovah" in all 6,823 occurrences in the Old Testament.',
            'Translates "Sheol" and "Hades" directly rather than conflating them into "grave" or "hell", clarifying biblical eschatology.',
            'Faithfully preserves Greek verbal aspects (aorist, perfect, present) and sentence structure.',
            'Served as the textual fountainhead and foundation for the RSV (1952), NASB (1971), Amplified Bible (1965), and ESV (2001).'
        ],
        'theologyAndLegacy': (
            'The ASV was celebrated by conservative Princeton theologians like B. B. Warfield and J. Gresham Machen as a masterwork '
            'of grammatical fidelity. Although criticized by some for its stiff English syntax, it became the indispensable baseline '
            'reference for seminary students, Bible colleges, and serious exegetical work for over a century.'
        ),
        'scopeAndUsage': 'Foundational textbook Bible in American theological seminaries throughout the 20th century.',
        'copyright': 'Public Domain worldwide.'
    },
    pt={
        'name': 'American Standard Version (ASV)',
        'fullName': 'The Holy Bible: American Standard Version (Edição Padrão Americana da Revisão Inglesa)',
        'year': '1901',
        'abbrev': 'ASV',
        'language': 'Inglês',
        'philosophy': 'Equivalência Formal Rígida (Extrema Precisão Literal e Gramatical)',
        'manuscripts': 'Antigo Testamento: Texto Massorético Hebraico. Novo Testamento: Texto Crítico Grego de Westcott & Hort (1881) e Samuel Tregelles.',
        'translators': 'Comitê Americano de Revisão Bíblica, reunindo 30 dos mais notáveis eruditos e teólogos norte-americanos (incluindo Philip Schaff, B. B. Warfield e Charles Hodge), em diálogo com a comissão britânica da ERV.',
        'history': (
            'Fruto do movimento de revisão da King James no final do século XIX, motivado pela descoberta de manuscritos bíblicos milenares '
            '(como o Códice Sinaítico e o Códice Vaticano). A comissão americana, liderada pelo historiador Philip Schaff, trabalhou em conjunto '
            'com os revisores britânicos. Em 1901, expirado o pacto de espera de 14 anos, a editora Thomas Nelson publicou a versão final americana, '
            'consagrada pela erudição como o mais exato monumento de tradução literal palavra por palavra em língua inglesa.'
        ),
        'features': [
            'Fidelidade morfológica e sintática incomparável à gramática grega e hebraica.',
            'Verte consistentemente o Tetragrama Divino YHWH como "Jehovah" nas mais de 6.800 ocorrências do Antigo Testamento.',
            'Distingue com exatidão teológica os termos "Sheol", "Hades" e "Geena", evitando confusões escatológicas.',
            'Base textual direta que deu origem à NASB (1971), à RSV (1952) e à ESV (2001).'
        ],
        'theologyAndLegacy': (
            'Altamente estimada pelos gigantes da teologia de Princeton, como B. B. Warfield e J. Gresham Machen, pela sua absoluta recusa em '
            'parafrasear os textos sagrados. Permanece como a ferramenta padrão de referência acadêmica e exegética em língua inglesa há mais de cem anos.'
        ),
        'scopeAndUsage': 'A Bíblia de referência analítica clássica nos seminários teológicos e faculdades bíblicas da América do Norte.',
        'copyright': 'Domínio Público universal.'
    },
    es={
        'name': 'American Standard Version (ASV)',
        'fullName': 'The Holy Bible: American Standard Version (Edición Estándar Americana de 1901)',
        'year': '1901',
        'abbrev': 'ASV',
        'language': 'Inglés',
        'philosophy': 'Equivalencia Formal Estricta (Máximo Rigor Literal y Textual)',
        'manuscripts': 'Antiguo Testamento: Texto Masorético. Nuevo Testamento: Texto Crítico Griego de Westcott y Hort (1881).',
        'translators': 'Comité de Revisión Bíblica de los Estados Unidos, integrado por 30 distinguidos teólogos y hebraístas dirigidos por Philip Schaff.',
        'history': (
            'Publicada en 1901 por Thomas Nelson & Sons tras décadas de cuidadoso cotejo textual con los grandes códices antiguos. '
            'Se distinguió como la Biblia en inglés más literal y gramaticalmente exacta de su época, siendo la base directa de la célebre NASB (1971).'
        ),
        'features': [
            'Traducción rigurosa término a término, sin interpolaciones libres ni paráfrasis.',
            'Traduce uniformemente el Nombre Divino YHWH como "Jehovah" en el Antiguo Testamento.',
            'Preserva distinciones precisas entre los términos originales del más allá (Seol y Hades).'
        ],
        'theologyAndLegacy': (
            'Reconocida por los teólogos reformados como un monumento de fidelidad exegética indiscutible para el estudio profundo de la Escritura.'
        ),
        'scopeAndUsage': 'Texto de referencia en academias bíblicas y seminarios teológicos mundiales.',
        'copyright': 'Dominio Público universal.'
    }
)

# 5. ACF (Almeida Corrigida Fiel)
reg(
    'acf',
    en={
        'name': 'Almeida Corrigida Fiel (ACF)',
        'fullName': 'Bíblia Sagrada: Tradução de João Ferreira de Almeida — Corrigida e Fiel ao Texto Original',
        'year': '1994 (Revisions: 2007, 2011)',
        'abbrev': 'ACF',
        'language': 'Portuguese',
        'philosophy': 'Strict Formal Equivalence (Preservation of Textus Receptus & Masoretic Text)',
        'manuscripts': 'Old Testament: Masoretic Text (Second Rabbinic Bible by Jacob ben Hayyim / Daniel Bomberg, 1524–1525). New Testament: Textus Receptus (Scrivener 1894 / Stephanus 1550).',
        'translators': 'Originally translated from original Hebrew and Greek by João Ferreira de Almeida (1628–1691), finished by Jacobus op den Akker (1753). Revised, corrected, and maintained by the Trinitarian Bible Society of Brazil (Sociedade Bíblica Trinitariana do Brasil - SBTB).',
        'history': (
            'João Ferreira de Almeida, a Portuguese Protestant pastor who converted at age 14, devoted his life to translating the Bible '
            'into Portuguese directly from original tongues. His New Testament appeared in Amsterdam in 1681, and his Old Testament was finished after his death in 1753. '
            'Over the centuries, various editions drifted away from Almeida’s original manuscript base. '
            'In 1968, the Sociedade Bíblica Trinitariana do Brasil (SBTB) was founded to restore and publish an edition of Almeida '
            'strictly aligned with the Reformation texts (Textus Receptus and traditional Masoretic Text). The result was the ACF, completed in 1994 and refined in 2007 and 2011.'
        ),
        'features': [
            'The definitive Portuguese equivalent to the English King James Version, sharing the exact same manuscript roots (Textus Receptus and Bomberg Masoretic Text).',
            'Strict adherence to formal equivalence, translating Hebrew and Greek idioms literally wherever possible.',
            'Preserves traditional Protestant ecclesiastical vocabulary (e.g., "propiciação", "conciliação", "redenção", "graça").',
            'Refuses to omit verses or phrases that are absent in modern critical Greek texts (such as the Comma Johanneum in 1 John 5:7-8, the doxology of the Lord’s Prayer in Matt 6:13, and the ending of Mark 16:9-20).'
        ],
        'theologyAndLegacy': (
            'The ACF is the most beloved translation among conservative Reformed, Baptist, Presbyterian, and traditional Pentecostal churches in Brazil and Portugal. '
            'Portuguese translations of Charles Spurgeon’s classic sermons and puritan works have historically relied on the Almeida Corrigida text family '
            'because its theological rhythm and doctrinal architecture mirror the English King James Version that Spurgeon preached.'
        ),
        'scopeAndUsage': 'Primary pulpit and devotional Bible for hundreds of Reformed, Baptist, and conservative evangelical denominations throughout the Lusophone world.',
        'copyright': 'Copyright © 1994, 2007, 2011 by Sociedade Bíblica Trinitariana do Brasil (SBTB).'
    },
    pt={
        'name': 'Almeida Corrigida Fiel (ACF)',
        'fullName': 'Bíblia Sagrada: Tradução de João Ferreira de Almeida — Corrigida e Fiel ao Texto Original',
        'year': '1994 (Revisões: 2007, 2011)',
        'abbrev': 'ACF',
        'language': 'Português',
        'philosophy': 'Equivalência Formal Estrita (Fidelidade ao Textus Receptus e Texto Massorético Tradicional)',
        'manuscripts': 'Antigo Testamento: Texto Massorético Hebraico Tradicional (Bíblia Rabínica de Bomberg / Jacob ben Hayyim, 1524–1525). Novo Testamento: Textus Receptus Grego (compilado por Scrivener 1894 e Stephanus 1550).',
        'translators': 'Originalmente traduzida das línguas originais pelo ministro reformado português João Ferreira de Almeida (1628–1691). Revisada e mantida meticulosamente pela Sociedade Bíblica Trinitariana do Brasil (SBTB).',
        'history': (
            'João Ferreira de Almeida dedicou sua existência a dar ao povo de língua portuguesa a Palavra de Deus em seu próprio idioma. '
            'Seu Novo Testamento foi publicado em Amsterdã em 1681, e o Antigo Testamento completado em Batávia em 1753. '
            'Ao longo dos séculos XIX e XX, muitas revisões passaram a sofrer influência de manuscritos do Texto Crítico. '
            'Diante disso, a Sociedade Bíblica Trinitariana do Brasil (SBTB) empreendeu um trabalho colossal de resgate e restauração textual, '
            'confrontando cada versículo de Almeida estritamente com os textos da Reforma Protestante. A ACF foi publicada em 1994 e aperfeiçoada em 2007 e 2011.'
        ),
        'features': [
            'É a exata correspondente em língua portuguesa da King James Version em inglês, compartilhando a mesma base de manuscritos (Textus Receptus e Texto Massorético de Ben Hayyim).',
            'Fidelidade formal estrita: traduz palavra por palavra, preservando a sintaxe e a riqueza formal do hebraico e do grego.',
            'Vocabulário solene, clássico e reverente, ideal para leitura orante, memorização de versículos e pregação bíblica expositiva.',
            'Mantém integralmente as passagens que foram omitidas ou colocadas em dúvida pelas edições críticas modernas (como a doxologia do Pai-Nosso em Mt 6:13, a passagem de Mc 16:9-20 e o relato da mulher adúltera em Jo 7:53-8:11).'
        ],
        'theologyAndLegacy': (
            'A ACF é a Bíblia predileta de ministros reformados, batistas confessionais, presbiterianos tradicionais e cristãos que prezam '
            'a doutrina da Preservação Providencial das Escrituras. Todas as obras históricas de Spurgeon traduzidas para o português encontram '
            'na ACF o casamento teológico e textual perfeito com a KJV utilizada pelo próprio pregador.'
        ),
        'scopeAndUsage': 'Amplamente utilizada no Brasil, Portugal, Angola, Moçambique e comunidades lusófonas globais em púlpitos, escolas dominicais e lares cristãos.',
        'copyright': 'Copyright © 1994, 2007, 2011 Sociedade Bíblica Trinitariana do Brasil (SBTB).'
    },
    es={
        'name': 'Almeida Corrigida Fiel (ACF)',
        'fullName': 'Bíblia Sagrada: Tradução de João Ferreira de Almeida — Corrigida e Fiel ao Texto Original',
        'year': '1994 (Revisiones: 2007, 2011)',
        'abbrev': 'ACF',
        'language': 'Portugués',
        'philosophy': 'Equivalencia Formal Estricta (Fiel al Textus Receptus y Texto Masorético)',
        'manuscripts': 'Antiguo Testamento: Texto Masorético Tradicional (Jacob ben Hayyim). Nuevo Testamento: Textus Receptus Griego.',
        'translators': 'Traducida originalmente por el pastor reformado João Ferreira de Almeida en el siglo XVII y minuciosamente revisada por la Sociedade Bíblica Trinitariana do Brasil (SBTB).',
        'history': (
            'Almeida fue la primera traducción de la Biblia completa al portugués desde las lenguas originales. '
            'La revisión ACF fue desarrollada por la Sociedad Bíblica Trinitaria para garantizar una fidelidad absoluta e inalterable a los textos del Textus Receptus de la Reforma Protestante.'
        ),
        'features': [
            'Equivalente en portugués a la Reina-Valera clásica en español y a la King James en inglés.',
            'Lenguaje reverente, noble y de máxima precisión gramatical y teológica.',
            'Preserva intactas las lecturas tradicionales de la Iglesia histórica.'
        ],
        'theologyAndLegacy': (
            'La versión preferida de las iglesias reformadas, bautistas y conservadoras del mundo lusófono por su solidez doctrinal.'
        ),
        'scopeAndUsage': 'Utilizada extensamente en Brasil, Portugal y naciones de habla portuguesa.',
        'copyright': 'Copyright © 1994, 2007, 2011 SBTB.'
    }
)

# 6. NVI (Nova Versão Internacional 2001 - Português)
reg(
    'nvi',
    en={
        'name': 'Nova Versão Internacional (NVI 2001 - Português)',
        'fullName': 'Bíblia Sagrada: Nova Versão Internacional (Edição Clássica Brasileira de 2001)',
        'year': '2001 (Classic Original Edition / New Testament 1993)',
        'abbrev': 'NVI 2001',
        'language': 'Portuguese',
        'philosophy': 'Dynamic / Optimal Equivalence (Natural, Clear, and Accurate Contemporary Portuguese)',
        'manuscripts': 'Old Testament: Biblia Hebraica Stuttgartensia (Masoretic Text) and Dead Sea Scrolls. New Testament: Greek New Testament (Nestle-Aland 27th ed. / United Bible Societies 4th ed.).',
        'translators': 'Commissioned by the International Bible Society (now Biblica) and Editora Vida. A dedicated committee of 30+ leading Brazilian evangelical biblicists, theologians, and linguists chaired by Luiz Sayão, Russel Shedd, Estevan Kirschner, and Robinson Cavalcanti.',
        'history': (
            'Initiated in 1990 to provide Portuguese-speaking Christians with a translation translated directly from the original Hebrew, Aramaic, and Greek '
            'that matched the naturalness, clarity, and communicative excellence of the English NIV. The New Testament appeared in 1993, and after nine years '
            'of collaborative translation directly from the ancient critical texts, the complete Bible was launched in March 2001. '
            'It became an instant landmark across Brazil, transforming youth ministry, expository preaching, and daily Bible reading.'
        ),
        'features': [
            'Contemporary, elegant, and culturally natural Brazilian Portuguese without vulgarity or excessive colloquialism.',
            'Preserves the original 2001 classic Brazilian edition coordinated by Luiz Sayão and Dr. Russel Shedd, prior to the vocabulary modifications of the 2023 revision.',
            'Exceptional readability, making complex Pauline sentences and Old Testament narratives easily understandable.',
            'Retains core biblical theological terms while updating archaic vocabulary that had become unintelligible in modern Portuguese.',
            'Accurate metric conversions and cultural footnotes explaining historical measurements and ancient customs.'
        ],
        'theologyAndLegacy': (
            'The Brazilian NVI (2001) represented a milestone in evangelical cooperation, bringing together Baptist, Presbyterian, Pentecostal, and Anglican '
            'scholars under the theological mentorship of legendary missionary-theologian Dr. Russel P. Shedd. It is widely considered one of the '
            'finest vernacular Bible translations in the Portuguese language.'
        ),
        'scopeAndUsage': 'The most popular modern study and reading Bible in Brazil and among Portuguese-speaking evangelicals worldwide.',
        'copyright': 'Copyright © 1993, 2000, 2001 by Biblica, Inc. (formerly International Bible Society). Published by Editora Vida.'
    },
    pt={
        'name': 'Nova Versão Internacional (NVI 2001 - Português)',
        'fullName': 'Bíblia Sagrada: Nova Versão Internacional (Edição Clássica Brasileira de 2001)',
        'year': '2001 (Edição Clássica Original / Novo Testamento em 1993)',
        'abbrev': 'NVI 2001',
        'language': 'Português',
        'philosophy': 'Equivalência Dinâmica / Ótima (Clareza Comunicativa, Fidelidade Exegética e Elegância Contemporânea)',
        'manuscripts': 'Antigo Testamento: Biblia Hebraica Stuttgartensia (Texto Massorético) cotejada com os Manuscritos do Mar Morto e versões antigas. Novo Testamento: Texto Crítico Grego (Nestle-Aland 27ª edição / Sociedades Bíblicas Unidas 4ª edição corrigida).',
        'translators': 'Comissão de Tradutores da Sociedade Bíblica Internacional (Biblica) em parceria com a Editora Vida. Composta por mais de 30 renomados eruditos, teólogos e linguistas brasileiros, com coordenação de Luiz Sayão, Dr. Russel Shedd, Estevan Kirschner e Robinson Cavalcanti.',
        'history': (
            'Iniciada em 1990 para suprir uma histórica necessidade: uma Bíblia vertida diretamente dos textos originais para um português '
            'fluente, culto e natural, que comunicasse a Palavra com vigor às novas gerações sem as barreiras dos arcaísmos ibéricos. '
            'O Novo Testamento foi publicado em 1993 e a Bíblia completa chegou às igrejas em março de 2001. '
            'Em pouquíssimo tempo, a NVI de 2001 consolidou-se como um fenômeno editorial e espiritual, revolucionando o ensino bíblico no Brasil.'
        ),
        'features': [
            'Fluência verbal incomparável em português contemporâneo, facilitando a compreensão de textos densos como as epístolas paulinas e a literatura poética.',
            'Preserva integralmente o texto clássico original de 2001 (coordenado pelo Pr. Luiz Sayão e pelo Dr. Russel Shedd), anterior às alterações de vocabulário da revisão de 2023.',
            'Equilíbrio entre fidelidade ao texto original e clareza para o leitor de hoje, sem desvios para paráfrases liberais.',
            'Preservação zelosa dos grandes termos doutrinários do cristianismo histórico (redenção, propiciação, regeneração, graça, santificação).',
            'Notas de rodapé elucidativas com pesos, medidas e dados históricos essenciais para a compreensão do contexto bíblico.'
        ],
        'theologyAndLegacy': (
            'A NVI brasileira de 2001 uniu as mentes mais brilhantes da erudição evangélica nacional sob a mentoria do inesquecível Dr. Russel Shedd. '
            'Sua aceitação unânime em igrejas batistas, presbiterianas, congregacionais e pentecostais confirmou seu status como a tradução '
            'contemporânea de maior impacto no Brasil no início do século XXI.'
        ),
        'scopeAndUsage': 'A tradução contemporânea mais lida, citada e impressa no Brasil, padrão nas principais editoras evangélicas e faculdades teológicas.',
        'copyright': 'Copyright © 1993, 2000, 2001 Sociedade Bíblica Internacional (Biblica, Inc.). Preservada para estudo bíblico e histórico.'
    },
    es={
        'name': 'Nova Versão Internacional (NVI 2001 - Português)',
        'fullName': 'Bíblia Sagrada: Nova Versão Internacional (Edición Clásica Brasileña de 2001)',
        'year': '2001 (Edición Clásica Original / Nuevo Testamento 1993)',
        'abbrev': 'NVI 2001 (PT)',
        'language': 'Portugués',
        'philosophy': 'Equivalencia Dinámica / Óptima (Claridad, Fidelidad y Fluidez Contemporánea)',
        'manuscripts': 'Antiguo Testamento: Biblia Hebraica Stuttgartensia. Nuevo Testamento: Texto Crítico Griego (Nestle-Aland 27ª ed.).',
        'translators': 'Comité de la Sociedad Bíblica Internacional (Biblica) liderado por teólogos brasileños de renombre como Luiz Sayão y el Dr. Russel Shedd.',
        'history': (
            'Desarrollada directamente desde el hebreo y griego a lo largo de una década para ofrecer al mundo de habla portuguesa '
            'una Biblia moderna, elegante y de extrema fidelidad académica, publicada íntegramente en marzo de 2001.'
        ),
        'features': [
            'Prosa contemporánea de altísima calidad estilística, ideal para la lectura congregacional y la memorización.',
            'Preserva el texto clásico original de 2001, previo a las revisiones léxicas posteriores de 2023.',
            'Notas al pie con aclaraciones culturales, de pesos y medidas y variantes de manuscritos.'
        ],
        'theologyAndLegacy': (
            'La versión moderna más leída e influyente de Brasil, referente en el estudio teológico y la predicación expositiva en portugués.'
        ),
        'scopeAndUsage': 'Ampliamente adoptada en todo Brasil, Portugal y comunidades de habla portuguesa.',
        'copyright': 'Copyright © 1993, 2000, 2001 Sociedad Bíblica Internacional (Biblica, Inc.).'
    }
)

# 7. NVIES (Nueva Versión Internacional 1999 - Español)
reg(
    'nvies',
    en={
        'name': 'Nueva Versión Internacional (NVI 1999 - Español)',
        'fullName': 'Santa Biblia: Nueva Versión Internacional (Edición Clásica de 1999)',
        'year': '1999 (Classic Original Edition / New Testament 1990)',
        'abbrev': 'NVI 1999 (ES)',
        'language': 'Spanish',
        'philosophy': 'Dynamic / Optimal Equivalence (Pan-Hispanic Natural Clarity and Textual Accuracy)',
        'manuscripts': 'Old Testament: Biblia Hebraica Stuttgartensia (Masoretic Text) with Dead Sea Scrolls evidence. New Testament: Greek New Testament (Nestle-Aland 27th ed. / UBS 4th ed.).',
        'translators': 'An international committee of 20+ Spanish-speaking evangelical scholars from across Latin America and Spain, sponsored by the International Bible Society (Biblica) and Editorial Vida, chaired by Dr. Luciano Jaramillo and René Padilla.',
        'history': (
            'Begun in 1979 with the New Testament released in 1990, the Spanish NVI aimed to provide the Spanish-speaking world with a translation '
            'directly from the original Hebrew, Aramaic, and Greek that avoided regional idioms while matching the clarity and textual integrity '
            'of the classic 1984 English NIV. Erudites from Colombia, Argentina, Mexico, Ecuador, Spain, and other nations worked for a decade '
            'from the ancient manuscripts, culminating in the landmark 1999 first complete edition.'
        ),
        'features': [
            'Pure, pan-Hispanic modern Spanish understood equally in Madrid, Mexico City, Bogotá, and Buenos Aires.',
            'Preserves the original 1999 classic Spanish text prior to the 2015 and 2022 revisions, retaining beloved readings such as "Dios formó al hombre del polvo de la tierra" (Gen 2:7) and "Dichoso el hombre" (Psalm 1:1).',
            'Replaces archaic 16th-century Castilian conjugations (vosotros) with universal contemporary forms (ustedes) without sacrificing dignity.',
            'Strict adherence to orthodox evangelical theology, rendering Christological and doctrinal passages with supreme reverence.'
        ],
        'theologyAndLegacy': (
            'The classic 1999 edition of the Spanish NVI became the preferred modern pulpit and study Bible for a vast generation of Spanish-speaking '
            'pastors, seminary students, and believers seeking biblical precision combined with natural, living communication.'
        ),
        'scopeAndUsage': 'Widely read across 20+ Spanish-speaking nations in Latin America, the Caribbean, Spain, and the Hispanic church in the United States.',
        'copyright': 'Santa Biblia, Nueva Versión Internacional® NVI® © 1985, 1990, 1999 por Sociedad Bíblica Internacional (Biblica, Inc.). Archived for classical study.'
    },
    pt={
        'name': 'Nueva Versión Internacional (NVI 1999 - Español)',
        'fullName': 'Santa Biblia: Nueva Versión Internacional (Edição Clássica Hispânica de 1999)',
        'year': '1999 (Edição Clássica Original / Novo Testamento 1990)',
        'abbrev': 'NVI 1999 (ES)',
        'language': 'Espanhol',
        'philosophy': 'Equivalência Dinâmica / Ótima (Espanhol Neutro Internacional, Precisão e Fluidez Contemporânea)',
        'manuscripts': 'Antigo Testamento: Biblia Hebraica Stuttgartensia (Texto Massorético) e Manuscritos de Qumran. Novo Testamento: Texto Crítico Grego (Nestle-Aland 27ª ed. / Sociedades Bíblicas Unidas 4ª ed.).',
        'translators': 'Comissão Internacional de mais de 20 eruditos, teólogos e linguistas evangélicos hispano-americanos representando mais de 10 nações da América Latina e Espanha, patrocinada pela Sociedade Bíblica Internacional (Biblica), sob coordenação do Dr. Luciano Jaramillo e René Padilla.',
        'history': (
            'Iniciada com o Novo Testamento (1990) pela Sociedade Bíblica Internacional para proporcionar ao mundo hispânico uma tradução contemporânea '
            'em "espanhol pan-hispânico neutro", livre de regionalismos locais e sem os arcaísmos castelhanos do século XVI. '
            'Traduzida diretamente dos manuscritos hebraicos, aramaicos e gregos, a Bíblia completa foi lançada em sua consagrada 1ª edição em 1999, '
            'alinhada à filosofia clássica da NIV 1984 inglesa e da NVI 2001 brasileira.'
        ),
        'features': [
            'Espanhol moderno, culto e compreensível em qualquer país de língua espanhola, da Espanha ao México e à Argentina.',
            'Preserva integralmente o texto clássico original de 1999, anterior às revisões posteriores de 2015 e 2022, mantendo leituras tradicionais como «La tierra era un caos total» (Gn 1:2), «Dios formó al hombre del polvo de la tierra» (Gn 2:7) e «Dichoso el hombre» (Sl 1:1).',
            'Adota a forma pronominal universal "ustedes", eliminando formas arcaicas ou regionalistas restritas.',
            'Rigor exegético em conformidade com as melhores edições críticas acadêmicas do hebraico e do grego.'
        ],
        'theologyAndLegacy': (
            'A edição clássica de 1999 da NVI é a versão moderna de referência para pregação e estudo em espanhol no SpurgeonTV, formando com a '
            'NIV 1984 (Inglês) e a NVI 2001 (Português) a tríade histórica original das traduções internacionais contemporâneas.'
        ),
        'scopeAndUsage': 'Padrão em centenas de seminários teológicos, publicações e comunidades cristãs em todo o continente americano e na Espanha.',
        'copyright': 'Santa Biblia, Nueva Versión Internacional® NVI® © 1985, 1990, 1999 por Sociedad Bíblica Internacional (Biblica, Inc.). Preservada para consulta e estudo histórico canônico.'
    },
    es={
        'name': 'Nueva Versión Internacional (NVI 1999 - Español)',
        'fullName': 'Santa Biblia: Nueva Versión Internacional (Edición Clásica Original de 1999)',
        'year': '1999 (Edición Clásica Original / Nuevo Testamento 1990)',
        'abbrev': 'NVI 1999 (ES)',
        'language': 'Español',
        'philosophy': 'Equivalencia Dinámica / Óptima (Español Neutro Internacional, Claridad y Fidelidad Exegética)',
        'manuscripts': 'Antiguo Testamento: Biblia Hebraica Stuttgartensia (Texto Masorético) y Rollos del Mar Muerto. Nuevo Testamento: Texto Crítico Griego (Nestle-Aland 27ª ed. / UBS 4ª ed.).',
        'translators': 'Comité internacional de más de veinte biblistas, hebraístas y lingüistas hispanos de más de diez países de Iberoamérica y España, coordinados por el Dr. Luciano Jaramillo y René Padilla bajo el auspicio de la Sociedad Bíblica Internacional (Biblica).',
        'history': (
            'Concebida para brindar al pueblo hispanoparlante una traducción directa desde el hebreo, arameo y griego que preservara la exactitud '
            'de los textos sagrados en un lenguaje comprensible y natural para todo el mundo hispano, siguiendo los mismos principios de excelencia '
            'de la clásica NIV 1984 en inglés. Tras la publicación del Nuevo Testamento en 1990 y una década de labor exegética colegiada, '
            'la Biblia completa vio la luz en su histórica primera edición de 1999.'
        ),
        'features': [
            'Español neutro y universal, comprendido con la misma calidez y distinción en España, México, Centroamérica y Sudamérica.',
            'Preserva íntegramente el texto clásico original de 1999 (previo a las revisiones posteriores de 2015 y 2022), conservando lecturas consagradas como «La tierra era un caos total» (Gn 1:2), «Dios el Señor formó al hombre del polvo de la tierra» (Gn 2:7), «su simiente te aplastará la cabeza, pero tú le morderás el talón» (Gn 3:15) y «Dichoso el hombre» (Sal 1:1).',
            'Sustitución de formas arcaicas por giros verbales contemporáneos dignos (uso de "ustedes").',
            'Traducción directa desde los textos críticos hebreos, arameos y griegos con total fidelidad a la teología evangélica histórica.'
        ],
        'theologyAndLegacy': (
            'La edición clásica de 1999 es la versión contemporánea predeterminada en SpurgeonTV en español, formando junto con la NIV 1984 (inglés) '
            'y la NVI 2001 (portugués) la tríada histórica original de la Nueva Versión Internacional sin alteraciones de revisiones recientes.'
        ),
        'scopeAndUsage': 'Ampliamente empleada y atesorada en iglesias, seminarios y hogares evangélicos de toda Hispanoamérica y España.',
        'copyright': 'Santa Biblia, Nueva Versión Internacional® NVI® © 1985, 1990, 1999 por Sociedad Bíblica Internacional (Biblica, Inc.). Preservada para consulta y estudio histórico canónico.'
    }
)

# 8. RVR1960 (Reina-Valera 1960)
reg(
    'rvr1960',
    en={
        'name': 'Reina-Valera 1960 (RVR 1960)',
        'fullName': 'Santa Biblia: Versión Reina-Valera Revisión de 1960',
        'year': '1960',
        'abbrev': 'RVR 1960',
        'language': 'Spanish',
        'philosophy': 'Formal Equivalence (Classic Biblical Cadence with Modest 20th Century Harmonization)',
        'manuscripts': 'Old Testament: Masoretic Text (Jacob ben Hayyim). New Testament: Textus Receptus (Stephanus 1550 / Beza 1598) with conservative reference to ancient codices.',
        'translators': 'Revision committee assembled by the United Bible Societies (Sociedades Bíblicas Unidas), chaired by Latin American scholars including Juan Díaz, Alfonso Lloreda, Honorio Espinoza, and Dr. Eugene Nida (consultant).',
        'history': (
            'The Reina-Valera translation traces its roots to the golden age of Spanish literature: Casiodoro de Reina’s monumental 1569 "Biblia del Oso", '
            'revised by Cipriano de Valera in 1602 ("Biblia del Cántaro"). As the language evolved through the 18th and 19th centuries, the United Bible Societies '
            'undertook a major, reverent revision in the 1950s. The goal was to remove obsolete Spanish grammar without altering the historic cadences and phrases '
            'beloved by generations of Spanish-speaking Protestants. Published in 1960, it became the undisputed "King James of the Spanish-speaking world".'
        ),
        'features': [
            'The standard liturgical and pulpit Bible of Hispanic Protestantism for over six decades.',
            'Preserves the classical Castilian second-person plural ("vosotros"), maintaining solemnity in public reading.',
            'Strict adherence to the Textus Receptus, ensuring identical verse coverage to the historic English KJV and Portuguese Almeida.',
            'Melodious, memorable cadence deeply embedded in the devotional memory of hundreds of millions of Spanish speakers.'
        ],
        'theologyAndLegacy': (
            'Virtually every Spanish translation of the Puritans, Charles Spurgeon, and classical evangelical commentaries produced between 1960 and the 2000s '
            'was keyed directly to the text of the RVR 1960. It is the spiritual backbone of the historic revival in Latin America.'
        ),
        'scopeAndUsage': 'The most widespread, memorized, and ubiquitous Bible translation in the history of the Spanish evangelical church.',
        'copyright': 'Copyright © 1960 Sociedades Bíblicas Unidas (United Bible Societies).'
    },
    pt={
        'name': 'Reina-Valera 1960 (RVR 1960)',
        'fullName': 'Santa Biblia: Versión Reina-Valera Revisión de 1960',
        'year': '1960',
        'abbrev': 'RVR 1960',
        'language': 'Espanhol',
        'philosophy': 'Equivalência Formal Clássica (Solenidade, Ritmo Tradicional e Fidelidade Literal)',
        'manuscripts': 'Antigo Testamento: Texto Massorético Hebraico. Novo Testamento: Textus Receptus Grego da Reforma Protestante.',
        'translators': 'Comissão constituída pelas Sociedades Bíblicas Unidas (SBU), formada por eruditos latino-americanos e espanhóis como Juan Díaz, Alfonso Lloreda, Honorio Espinoza e consultoria de Eugene Nida.',
        'history': (
            'Descendente direta da histórica "Bíblia do Urso" de Casiodoro de Reina (1569) e da revisão de Cipriano de Valera (1602). '
            'Em meados do século XX, as Sociedades Bíblicas Unidas reuniram uma comissão para atualizar a ortografia e eliminar expressões caídas em desuso, '
            'preservando religiosamente a musicalidade e a majestade que consagraram a obra. Lançada em 1960, converteu-se na mais amada e influente Bíblia em espanhol.'
        ),
        'features': [
            'Considerada a "King James do mundo hispânico", sendo a Bíblia padrão de púlpito de quase todas as denominações tradicionais.',
            'Emprega a solenidade do castelhano clássico ("vosotros"), ideal para a liturgia solene e leitura em voz alta.',
            'Alinhamento com o Textus Receptus, garantindo correspondência direta com as versões clássicas da Reforma como a KJV e a Almeida Corrigida.',
            'O texto mais decorado, memorizado e citado na história da hinologia e da pregação em língua espanhola.'
        ],
        'theologyAndLegacy': (
            'Toda a literatura puritana e os sermões de Charles H. Spurgeon traduzidos para o espanhol no século XX tiveram na RVR 1960 sua grande referência canônica.'
        ),
        'scopeAndUsage': 'Presente em milhões de templos e lares evangélicos na América Latina, Espanha e Estados Unidos.',
        'copyright': 'Copyright © 1960 Sociedades Bíblicas Unidas.'
    },
    es={
        'name': 'Reina-Valera 1960 (RVR 1960)',
        'fullName': 'Santa Biblia: Versión Reina-Valera Revisión de 1960',
        'year': '1960',
        'abbrev': 'RVR 1960',
        'language': 'Español',
        'philosophy': 'Equivalencia Formal Clásica (Fidelidad Textual, Belleza Literaria y Solemnidad de Púlpito)',
        'manuscripts': 'Antiguo Testamento: Texto Masorético Hebreo (segunda edición rabínica). Nuevo Testamento: Textus Receptus Griego.',
        'translators': 'Comité de eruditos y teólogos hispanoamericanos auspiciado por las Sociedades Bíblicas Unidas (SBU), entre ellos Juan Díaz, Alfonso Lloreda y Honorio Espinoza.',
        'history': (
            'Heredera de la joya cumbre de la Reforma Española: la traducción de Casiodoro de Reina de 1569 (Biblia del Oso) revisada por Cipriano de Valera en 1602. '
            'La revisión de 1960 actualizó la ortografía y puntuación arcaicas conservando la majestuosidad y unción que cautivaron a generaciones enteras. '
            'Es el texto por antonomasia de las iglesias cristianas evangélicas en todo el mundo hispano.'
        ),
        'features': [
            'La versión más memorizada, amada y citada en la historia del cristianismo de habla hispana.',
            'Conserva el pronombre "vosotros" con la máxima solemnidad litúrgica.',
            'Base textual ligada a los manuscritos del Textus Receptus de la Reforma Protestante.',
            'Ritmo verbal sonoro y poético que resuena con reverencia en la proclamación del Evangelio.'
        ],
        'theologyAndLegacy': (
            'Es el texto con el cual varias generaciones de creyentes hispanos han leído y estudiado los sermones de Charles Spurgeon y los teólogos reformados.'
        ),
        'scopeAndUsage': 'La Biblia por excelencia en millones de congregaciones de toda Hispanoamérica y España.',
        'copyright': 'Copyright © 1960 Sociedades Bíblicas Unidas.'
    }
)

# 9. LBLA (La Biblia de las Américas 1986/1997)
reg(
    'lbla',
    en={
        'name': 'La Biblia de las Américas (LBLA)',
        'fullName': 'La Biblia de las Américas (Edición de Estudio y Referencia 1986 / 1997)',
        'year': '1986 (Complete Bible), 1997 (Definitive Revision)',
        'abbrev': 'LBLA',
        'language': 'Spanish',
        'philosophy': 'Strict Formal Equivalence (Literal Word-for-Word Spanish Translation of Ancient Texts)',
        'manuscripts': 'Old Testament: Biblia Hebraica Stuttgartensia (Masoretic Text) and Dead Sea Scrolls. New Testament: Novum Testamentum Graece (Nestle-Aland 27th ed. / UBS 4th ed.).',
        'translators': 'Translated by a team of Latin American evangelical scholars from different countries, published by The Lockman Foundation (creators of the New American Standard Bible - NASB) in La Habra, California.',
        'history': (
            'In the 1970s, the Lockman Foundation recognized that while the Spanish-speaking church loved the Reina-Valera, '
            'there was a critical need for an ultra-literal, scholarly, word-for-word translation in clear, contemporary Spanish '
            'comparable to what the NASB represented in the English language. A team of dedicated Latin American scholars worked for over a decade '
            'directly from the Hebrew, Aramaic, and Greek manuscripts. The New Testament appeared in 1973, the full Bible in 1986, and the definitive revision in 1997.'
        ),
        'features': [
            'The Spanish counterpart to the New American Standard Bible (NASB), famous for strict word-for-word grammatical fidelity.',
            'Italicized words identify necessary Spanish grammatical words not present in the original Hebrew/Greek texts.',
            'Uses clear Latin American Spanish with "ustedes" pronouns while retaining the highest level of scholarly precision.',
            'Extensive marginal cross-references and linguistic footnotes analyzing grammatical nuances and variant manuscript readings.'
        ],
        'theologyAndLegacy': (
            'LBLA is universally praised by expository preachers, Reformed pastors, and seminary professors across Latin America. '
            'Famous expositors like John MacArthur and Miguel Núñez frequently adopt LBLA as their primary study text due to its '
            'uncompromising grammatical precision.'
        ),
        'scopeAndUsage': 'The definitive exegetical reference Bible for pastors, scholars, and serious Bible students throughout the Spanish-speaking world.',
        'copyright': 'Copyright © 1986, 1995, 1997 by The Lockman Foundation. All rights reserved.'
    },
    pt={
        'name': 'La Biblia de las Américas (LBLA)',
        'fullName': 'La Biblia de las Américas (Edição de Estudo e Referência 1986 / 1997)',
        'year': '1986 (Bíblia Completa), 1997 (Revisão Definitiva)',
        'abbrev': 'LBLA',
        'language': 'Espanhol',
        'philosophy': 'Equivalência Formal Estrita (Tradução Literal Palavra por Palavra em Espanhol)',
        'manuscripts': 'Antigo Testamento: Biblia Hebraica Stuttgartensia (Texto Massorético) e Manuscritos do Mar Morto. Novo Testamento: Novum Testamentum Graece (Nestle-Aland 27ª ed. / Sociedades Bíblicas Unidas 4ª ed.).',
        'translators': 'Produzida por uma comissão internacional de eruditos e hebraístas hispano-americanos patrocinada pela conceituada The Lockman Foundation (criadora da NASB em inglês) na Califórnia.',
        'history': (
            'Desenvolvida para oferecer ao mundo de fala espanhola o equivalente exato da New American Standard Bible (NASB): '
            'uma tradução que não fizesse concessões à paráfrase e traduzisse com o máximo de precisão literal cada palavra das línguas originais. '
            'Publicada em 1986 e aperfeiçoada em 1997, consolidou-se como o texto padrão para exegese bíblica rigorosa em seminários de teologia.'
        ),
        'features': [
            'A versão em espanhol mais rigorosamente literal e fiel à sintaxe do hebraico, aramaico e grego.',
            'Palavras em itálico indicam acréscimos necessários à gramática em espanhol que não constam no manuscrito original.',
            'Adota o espanhol latino-americano com "ustedes", combinando clareza contemporânea com máxima erudição.',
            'Notas de rodapé analíticas incomparáveis com nuances de tradução e dados lexicais.'
        ],
        'theologyAndLegacy': (
            'É a tradução de preferência de grandes pregadores expositivos contemporâneos como John MacArthur e Dr. Miguel Núñez. '
            'Sua precisão cirúrgica a torna ideal para dissecar as proposições lógicas e teológicas dos sermões de Charles Spurgeon.'
        ),
        'scopeAndUsage': 'Bíblia indispensável em seminários teológicos, cátedras de teologia sistemática e estudos acadêmicos em espanhol.',
        'copyright': 'Copyright © 1986, 1995, 1997 por The Lockman Foundation.'
    },
    es={
        'name': 'La Biblia de las Américas (LBLA)',
        'fullName': 'La Biblia de las Américas (Edición de Estudio y Referencia 1986 / 1997)',
        'year': '1986 (Biblia Completa), 1997 (Revisión Definitiva)',
        'abbrev': 'LBLA',
        'language': 'Español',
        'philosophy': 'Equivalencia Formal Estricta (Traducción Literal Palabra por Palabra en Español)',
        'manuscripts': 'Antiguo Testamento: Biblia Hebraica Stuttgartensia (Texto Masorético) y Manuscritos del Mar Muerto. Nuevo Testamento: Texto Crítico Griego (Nestle-Aland 27ª ed.).',
        'translators': 'Comité de destacados eruditos y lingüistas bíblicos hispanoamericanos convocado y auspiciado por The Lockman Foundation (creadora de la NASB).',
        'history': (
            'Creada para brindar a los pastores, teólogos y estudiantes hispanohablantes una herramienta de máxima fidelidad palabra por palabra, '
            'análoga a la NASB en el idioma inglés. Tras más de una década de trabajo minucioso directo de los textos hebreo y griego, '
            'vio la luz en 1986 con una revisión definitiva en 1997.'
        ),
        'features': [
            'La traducción en español más rigurosamente literal y precisa de la actualidad.',
            'Uso de palabras en cursiva para señalar términos agregados para la comprensión gramatical que no están en el texto original.',
            'Emplea el pronombre "ustedes" con un lenguaje solemne, digno y pulcro.',
            'Notas filológicas de incalculable valor sobre los matices de los verbos griegos y hebreos.'
        ],
        'theologyAndLegacy': (
            'Ampliamente utilizada por maestros de la predicación expositiva en toda América Latina por su precisión doctrinal innegociable.'
        ),
        'scopeAndUsage': 'El estándar académico por excelencia en seminarios e institutos bíblicos del mundo de habla hispana.',
        'copyright': 'Copyright © 1986, 1995, 1997 por The Lockman Foundation.'
    }
)

print(f"Part 1 loaded ({len(PART1)} translations).")
