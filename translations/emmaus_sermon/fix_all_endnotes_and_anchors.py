# -*- coding: utf-8 -*-
"""
Execution script to:
1. Realign all 50 endnote anchors in body paragraphs for ES and EN
2. Restore full, unabridged translations for Notes 5, 6, 7, 8, 9, 12, 20, 21, 32
3. Fix minor spelling/typos (e.g. 'distinção' -> 'distinción') in ES notes
4. Recompile final JSONs and DOCX files
"""
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Starting full realignment and endnote content restoration...")

# ==============================================================================
# FRENTE 1: REALINHAMENTO DAS ÂNCORAS NO CORPO DO TEXTO
# ==============================================================================

es_p = json.load(open('translations/emmaus_sermon/es_final_paragraphs.json', encoding='utf-8'))
en_p = json.load(open('translations/emmaus_sermon/en_final_paragraphs.json', encoding='utf-8'))

# Specific manual replacements for paragraphs with misaligned anchors
p_fixes_es = {
    # P40: Notes 1 and 2
    40: "Las referencias entre corchetes en el cuerpo del texto indican los pasajes bíblicos del Antiguo Testamento mencionados. En **notas finales**[EN_REF:1] se encuentran dispuestos los **comentarios exegéticos y teológicos**[EN_REF:2] y observaciones del autor, referenciando cada sección de la obra tras el desenlace de la narrativa, a fin de hacer más fluida la lectura del texto artístico.",
    # P49: Notes 3 and 4
    49: "Jesús divisó a Cleofás[EN_REF:3] y al joven Natanael[EN_REF:4], dos discípulos que, saliendo de Jerusalén, se dirigían a la aldea de Emaús. Comenzó a hablar con ellos. Su voz transmitía la autoridad serena y la luz de quien conoce cada palabra de las Escrituras y el fondo mismo del alma humana.",
    # P77: Note 8
    77: "La simiente permaneció en peligro[EN_REF:8]. Sin embargo, el Señor concedió a Adán y Eva otro hijo para ocupar el lugar de Abel. Lo llamaron **Set**, cuyo nombre significa *compensación* o *designado*. Set continuó el linaje de la adoración y la reverencia al Creador, transmitiendo a las generaciones siguientes la fe en la promesa de la salvación, a pesar de que el hombre había sido engendrado *«a su semejanza, conforme a su imagen»* [Gn 5:3].",
    # P89: Note 10
    89: "Uno murió en lugar del otro[EN_REF:10]. Noten que Dios perdonó al hijo de Abraham, pero siglos después, en ese mismo monte Moriah, no perdonó a su propio Hijo, sino que *«lo entregó por todos nosotros»* [Rm 8:32]. La sustitución que salvó a Isaac era solo la sombra; la realidad eterna es Cristo inmolado en el Calvario en nuestro favor.",
    # P96: Notes 11 and 12
    96: "Por eso profetizó Jacob que el cetro —el derecho de gobierno— permanecería con Judá[EN_REF:11] **hasta que viniera Siloh,** y a él todas las naciones rendirán obediencia.[EN_REF:12]",
    # P115: Note 14
    115: "«¿Ven el cordero? Cada familia debía tomar un animal sin defecto, sacrificarlo al atardecer y aplicar la sangre en los postes y dinteles de las puertas. Cuando el juicio del Señor pasó sobre la tierra de Egipto, la sangre fue la señal de rescate: donde había sangre, la muerte no entraba. Ese cordero fue la sustitución que libró a los primogénitos israelitas. Mas no era sino una sombra profética: un animal jamás podría quitar el pecado del mundo ni librarnos del juicio eterno[EN_REF:14]».",
    # P121: Note 15
    121: "«Así como la sangre en los dinteles libró a los primogénitos de la muerte en Egipto, así también la sangre de Cristo fue derramada para que nuestras vidas fueran libradas de la condenación eterna y fuéramos comprados para Dios[EN_REF:15]».",
    # P130: Note 16
    130: "«¡Contemplen la sublime perfección del diseño divino! En el tabernáculo del desierto, el pecador traía un cordero, y el sacerdote mediaba el sacrificio. Pero en el orden definitivo de la redención, Cristo es, al mismo tiempo, el Sumo Sacerdote perfecto y el Cordero inmaculado![EN_REF:16]».",
    # P138: Note 17
    138: "Moisés prometió que Dios levantaría a un Profeta semejante a él de entre sus hermanos, y pondría en su boca las palabras mismas de Dios.[EN_REF:17] Moisés fue el redentor temporal que condujo a Israel fuera de la esclavitud de Egipto; pero aquel Profeta anunciado sería el Redentor definitivo que liberaría al hombre de la cautividad eterna del pecado.",
    # P165: Note 23
    165: "Samuel fue un siervo leal que dedicó su vida entera a ungir reyes, a guiar a Israel y a vivir con fidelidad en los caminos del Señor.[EN_REF:23] Pero hablaremos con más detalle sobre los Reyes dentro de un momento.",
    # P174: Note 25
    174: "Samuel fue un profeta fiel, un sacerdote piadoso y un gobernante justo. Él combinó en su propia vida los tres oficios divinos para señalar hacia Aquel que reinaría eternamente sobre todas las cosas. El plan redentor avanzaba inexorablemente hacia su cumplimiento.[EN_REF:25]»",
    # P186: Note 28
    186: "Tenía la ley y la presencia del Señor para guiarlo.[EN_REF:28] Pero Saúl fracasó. Se corrompió por el poder, los celos asesinos y la obstinación.",
    # P189: Note 29
    189: "El linaje no se extinguiría, mas la corona pasaría a otro varón: David, un hombre conforme al corazón de Dios.[EN_REF:29]»",
    # P202: Note 31
    202: "Él es como la luz del alba y la lluvia sobre la tierra.[EN_REF:31] David era solo el primer paso, el vislumbre inicial de un diseño pactual que pertenecía a una gloria venidera».",
    # P239: Note 36
    239: "«¡Y la profecía termina en triunfo absoluto: la victoria del Rey glorificado conducirá a la adoración universal de todas las naciones![EN_REF:36]»",
    # P249: Note 38
    249: "«Salomón edificó un templo de piedras y cedro, pero no pudo evitar la ruina de su propio corazón al final de sus días. David, en cambio, vio más allá: vio a Aquel que es el Templo Viviente, el verdadero Rey de Paz, infinitamente mayor que Salomón[EN_REF:38]».",
    # P254: Note 39
    254: "«¿Cómo puede ser, al mismo tiempo, **hijo de David** y **Señor de David**?[EN_REF:39] Solo hay una respuesta: él debía ser humano —hijo de David— y Dios eterno —Señor soberano.",
    # P313: Note 43
    313: "«Piensen en esto: ¿puede un difunto ver a su simiente o prolongar sus días en la tierra, a no ser que... resucite de entre los muertos?[EN_REF:43]»"
}

p_fixes_en = {
    # P40: Notes 1 and 2
    40: "The references in brackets throughout the text indicate the Old Testament passages cited. In the **final endnotes**[EN_REF:1], the **theological and exegetical comments**[EN_REF:2] and observations from the author are arranged, annotating each section of the work following the conclusion of the narrative, so as to maintain the uninterrupted flow of the artistic prose.",
    # P49: Notes 3 and 4
    49: "Jesus drew near to Cleopas[EN_REF:3] and young Nathaniel[EN_REF:4], two disciples who, leaving Jerusalem, were traveling toward the village of Emmaus. He began to converse with them. His voice carried the gentle authority and profound clarity of One who knows every word of the Scriptures and the deepest depths of the human soul.",
    # P77: Note 8
    77: "The seed remained in peril[EN_REF:8]. Yet the Lord granted Adam and Eve another son to take the place of Abel. They named him **Seth**, meaning *appointed* or *compensation*. Seth continued the lineage of worship and devotion to the Creator, passing down to successive generations faith in the promise of redemption, even though man was now fathered *'in his own likeness, according to his image'* [Gn 5:3].",
    # P89: Note 10
    89: "One died in the place of the other[EN_REF:10]. Notice that God spared Abraham's son, but centuries later, on that very Mount Moriah, He did not spare His own Son, but *'gave him up for us all'* [Rm 8:32]. The substitution that rescued Isaac was merely the shadow; the eternal reality is Christ slain upon Calvary in our stead.",
    # P96: Notes 11 and 12
    96: "Therefore Jacob prophesied that the scepter—the right of sovereign rule—would remain with Judah[EN_REF:11] **until Shiloh comes,** and to him all nations owe obedience.[EN_REF:12]",
    # P115: Note 14
    115: "\"Do you see the lamb? Each household was commanded to take an unblemished animal, slaughter it at twilight, and apply its blood to the doorposts and lintels. When the judgment of the Lord swept across the land of Egypt, the blood served as the token of redemption: wherever the blood was applied, death could not enter. That lamb was the substitution that spared the firstborn of Israel. Yet it was only a prophetic shadow: an animal could never take away the sin of the world nor deliver us from eternal judgment[EN_REF:14].\"",
    # P121: Note 15
    121: "\"Just as the blood upon the doorposts delivered the firstborn from death in Egypt, so also the blood of Christ was shed that our lives might be delivered from eternal condemnation and that we might be purchased for God[EN_REF:15].\"",
    # P130: Note 16
    130: "\"Behold the exquisite perfection of the divine architecture! In the wilderness tabernacle, the sinner brought a lamb, and the priest mediated the sacrifice. But in the ultimate realm of redemption, Christ is at once the spotless High Priest and the spotless Lamb![EN_REF:16]\"",
    # P138: Note 17
    138: "Moses promised that God would raise up a Prophet like him from among their brothers, and put the very words of God into his mouth.[EN_REF:17] Moses was the temporal deliverer who led Israel out of Egyptian bondage; but that promised Prophet would be the everlasting Redeemer who delivers man from the eternal captivity of sin.",
    # P165: Note 23
    165: "Samuel was a devoted servant who spent his days anointing kings, instructing Israel, and walking faithfully in the ways of the Lord.[EN_REF:23] But we shall converse more fully about the Kings in just a moment.",
    # P174: Note 25
    174: "Samuel was a faithful prophet, a godly priest, and a righteous judge. He combined within his own life the three sacred offices to foreshadow Him who would reign forever over all creation. The plan of redemption was advancing toward its glorious fulfillment.[EN_REF:25]\"",
    # P186: Note 28
    186: "He possessed the law and the presence of the Lord to guide him.[EN_REF:28] Yet Saul failed. He became corrupted by power, deadly jealousy, and bitter stubbornness.",
    # P189: Note 29
    189: "The lineage would not be extinguished, but the crown would pass to another man: David, a man after God's own heart.[EN_REF:29]\"",
    # P202: Note 31
    202: "He is like the light of morning and rain upon the earth.[EN_REF:31] David was only the initial step, the earliest glimmer of a covenant design that belonged to an everlasting glory.\"",
    # P239: Note 36
    239: "\"And the psalm concludes in unmitigated triumph: the victory of the glorified King will culminate in the universal worship of all nations![EN_REF:36]\"",
    # P249: Note 38
    249: "\"Solomon constructed a temple of stone and cedar, yet he could not keep his own heart from faltering at the close of his days. David, however, looked far beyond: he saw Him who is the Living Temple, the true Prince of Peace, infinitely greater than Solomon[EN_REF:38].\"",
    # P254: Note 39
    254: "\"How can he be, at the same time, the **son of David** and the **Lord of David**?[EN_REF:39] There is but one answer: he had to be human—the son of David—and divine—the eternal Lord.",
    # P313: Note 43
    313: "\"Consider this: can a dead man see his offspring or prolong his days, unless... he rises again from the dead?[EN_REF:43]\""
}

# Update batch JSON files so compile_final_books.py picks up the changes
for b in range(8):
    batch_es_path = f'translations/emmaus_sermon/batch_{b}_es.json'
    batch_en_path = f'translations/emmaus_sermon/batch_{b}_en.json'
    
    b_es = json.load(open(batch_es_path, encoding='utf-8'))
    b_en = json.load(open(batch_en_path, encoding='utf-8'))
    
    modified_es = False
    modified_en = False
    
    for idx, text in p_fixes_es.items():
        if str(idx) in b_es:
            b_es[str(idx)] = text
            modified_es = True
            
    for idx, text in p_fixes_en.items():
        if str(idx) in b_en:
            b_en[str(idx)] = text
            modified_en = True
            
    if modified_es:
        with open(batch_es_path, 'w', encoding='utf-8') as f:
            json.dump(b_es, f, ensure_ascii=False, indent=2)
            print(f"Updated {batch_es_path}")
            
    if modified_en:
        with open(batch_en_path, 'w', encoding='utf-8') as f:
            json.dump(b_en, f, ensure_ascii=False, indent=2)
            print(f"Updated {batch_en_path}")

print("Applied anchor realignments to body paragraphs.")

# ==============================================================================
# FRENTE 2: RESTAURAÇÃO INTEGRAL DE CONTEÚDO NAS NOTAS FINAIS
# ==============================================================================

# Load current batches
b1_es = json.load(open('translations/emmaus_sermon/endnotes_batch_1_es.json', encoding='utf-8'))
b1_en = json.load(open('translations/emmaus_sermon/endnotes_batch_1_en.json', encoding='utf-8'))
b2_es = json.load(open('translations/emmaus_sermon/endnotes_batch_2_es.json', encoding='utf-8'))
b2_en = json.load(open('translations/emmaus_sermon/endnotes_batch_2_en.json', encoding='utf-8'))

# Fix Note 3 typo in Spanish ('distinção' -> 'distinción')
b1_es['3'][1] = b1_es['3'][1].replace("La distinção se fundamenta", "La distinción se fundamenta")

# NOTE 5 (5 paragraphs)
b1_es['5'] = [
    "Se designa a Gn 3:15 como el **protoevangelium** (primer evangelio) o «primer relato de las buenas nuevas de la redención» (GRONINGEN, 1995, p. 103). Cuatro aspectos mesiánicos son identificados en este pasaje: (1) un agente que surge de una fuente «real»; (2) una tarea que exige autoridad y poder soberanos; (3) una victoria sustitutiva que se ganará a favor de otros; y (4) la preparación del escenario para la plena restauración de los caídos portadores de la imagen de Dios (ibíd., p. 107).",
    "La gracia de Dios no esperó a que el hombre pidiera perdón; brotó del corazón del Creador en el instante mismo en que la maldición fue pronunciada. Noten bien que, incluso en medio de los espinos y del sudor, Dios siembra la semilla de la esperanza: «Pondré enemistad entre ti y la mujer, y entre tu simiente y la de ella; su simiente te aplastará la cabeza, pero tú le morderás el talón» (Génesis 3:15, NVI).",
    "A diferencia de las promesas superficiales de este mundo, la redención divina no pasa por alto el dolor; lo atraviesa. Como bien observa el comentarista en la *Guía Willmington para la Biblia*, este versículo no es simplemente un pronóstico histórico, sino una «visión arrebatadora de la cruz». La victoria sobre la serpiente —el aplastamiento de la cabeza de Satanás— no vendría por un decreto indoloro, sino a través de una herida en el talón del Salvador. No hay corona sin cruz, y no hay reposo sin que el «Varón de Dolores» cargara primero con la carga que nos correspondía. La redención, por ende, vendría con dolor porque el precio de nuestro *shalom* demandaba la sangre del Cordero.",
    "El socorro para expulsar el pecado y la muerte no provino de la ley ni de las obras humanas, sino únicamente a través de esta «simiente de la mujer», Cristo, quien fue prometido desde el principio. Es la primera «buena nueva» que llegó a los oídos de una humanidad que solo conocía el espanto de la condenación.",
    "¿Ha intentado usted alcanzar la victoria por sus propios esfuerzos, olvidando que el talón de Cristo ya fue herido en su lugar? ¿Puede usted discernir que su descanso no es un privilegio barato, sino el fruto de un sufrimiento vicario que transformó la maldición en bendición?"
]

b1_en['5'] = [
    "Genesis 3:15 is designated as the **protoevangelium** (the first gospel) or 'the first account of the good news of redemption' (GRONINGEN, 1995, p. 103). Four messianic aspects are identified in this passage: (1) an agent who emerges from a 'royal' source; (2) a task demanding sovereign authority and power; (3) a substitutionary victory to be won on behalf of others; and (4) the setting of the stage for the full restoration of fallen bearers of the image of God (ibid., p. 107).",
    "The grace of God did not wait for man to plead for forgiveness; it leapt from the Creator's heart at the exact moment the curse was pronounced. Mark well that, even amidst thorns and sweat, God plants the seed of hope: \"And I will put enmity between you and the woman, and between your offspring and hers; he will crush your head, and you will strike his heel\" (Genesis 3:15, NIV).",
    "Unlike the shallow promises of this world, divine redemption does not bypass pain; it presses through it. As the commentator in *Willmington's Guide to the Bible* aptly observes, this verse is not merely a historical forecast, but a \"breathtaking foresight of the cross.\" Victory over the serpent—the crushing of Satan's head—would not arrive by an effortless, painless decree, but through a wound inflicted upon the Savior's heel. There is no crown without a cross, and there is no rest unless the \"Man of Sorrows\" first bears the burden that belonged to us. Redemption, therefore, had to come with agony, because the purchase price of our *shalom* demanded the blood of the Lamb.",
    "The deliverance to banish sin and death did not arise from the law or human works, but exclusively through this \"seed of the woman,\" Christ, who was promised from the beginning. It is the very first \"good news\" that reached the ears of a humanity that hitherto knew only the terror of condemnation.",
    "Have you been striving to attain victory through your own strength, forgetting that Christ's heel has already been wounded in your place? Can you perceive that your rest is not a cheap privilege, but the fruit of a vicarious suffering that transformed the curse into an everlasting blessing?"
]

# NOTE 6 (4 paragraphs)
b1_es['6'] = [
    "Adán, habiendo visto y oído que la separación, la hostilidad, la destrucción y la muerte eran el fruto de su pecado común, acogió la proclamación de esperanza al reclamar la promesa de la continuidad de la maternidad para su mujer y el medio de restauración de la vida que dicha maternidad proveería.",
    "Asignación del nombre post-caída: Adán llamó a su esposa Eva únicamente tras la caída (Génesis 3:20), simbolizando esperanza y vida, aun después de la irrupción del pecado y de la muerte en el mundo.",
    "Al proclamar el nombre de Eva, el primer hombre estaba, en verdad, reclamando la restauración. Aceptó el anuncio de la esperanza, creyendo que la vida continuaría y que de aquel vientre afligido nacería Aquel que es la Vida misma. Aun siendo expulsados del paraíso, no fueron abandonados en el desamparo; fueron vestidos por Dios con túnicas de pieles, simbolizando que la muerte de un inocente cubriría su desnudez mientras aguardaban al Descendiente prometido.",
    "Adán miró a Eva y contempló el mañana de Dios. Si el primer Adán, bajo el abrumador peso de la culpa recién adquirida, pudo hallar refrigerio en el nombre «Vida», ¡cuánto más nosotros, que ya hemos visto a la Simiente brotar, morir y resucitar, podemos descansar en la obra consumada de Jesús!"
]

b1_en['6'] = [
    "Adam, having witnessed and heard that separation, hostility, destruction, and death were the direct consequence of their shared sin, embraced the proclamation of hope by laying hold of the promise of ongoing motherhood for his wife and the channel of life's restoration that motherhood would provide.",
    "Post-Fall Naming: Adam named his wife Eve only after the Fall (Genesis 3:20), symbolizing hope and life even after sin and death had invaded the created order.",
    "In bestowing the name Eve, the first man was in reality laying claim to redemption. He received the proclamation of hope, believing that life would endure and that from that suffering womb would be born He who is Life itself. Even when banished from Eden, they were not left forsaken; they were clothed by God with tunics of skin, symbolizing that the death of an innocent victim would cover their nakedness while they awaited the promised Offspring.",
    "Adam looked upon Eve and saw the tomorrow of God. If the first Adam, under the crushing weight of newly incurred guilt, could find solace in the name \"Life,\" how much more may we, who have seen the Seed sprout, die, and rise again, rest secure in the finished work of Jesus!"
]

# NOTE 7 (13 paragraphs)
b1_es['7'] = [
    "Estamos ante uno de los momentos más vibrantes y, al mismo tiempo, más conmovedores de la historia de la redención. Imaginen a la primera madre de la humanidad, con los dolores del parto aún latiendo —aquellos mismos dolores que le fueron anunciados como consecuencia de la transgresión— sosteniendo en sus brazos la primera vida engendrada en el tiempo y en el espacio.",
    "Eva contempla a aquel pequeño ser y, en un impulso de fe que desafía su propia miseria, exclama: *«¡He adquirido un varón, el Señor!»* (Génesis 4:1, traducción literal). Como bien observa el autor de *Sombras, Tipos y Misterios de la Biblia*, el regocijo de Eva no era meramente biológico; era mesiánico. No veía allí únicamente a un hijo, sino el cumplimiento inmediato de la promesa de que la «Simiente de la Mujer» aplastaría la cabeza de la serpiente.",
    "La frase hebrea ***qãnîthi 'îsh 'et-yhwh (קָנִיתִי אִישׁ אֶת־יְהוָה)*** puede traducirse literalmente tal como está, aunque desde la traducción griega de la Septuaginta hasta muchas versiones modernas se suele suavizar como «he adquirido un varón con el favor del Señor» o «con la ayuda del Señor», o bien «he tenido un varón del Señor», indicando que ella reconoció la intervención divina, pero sin entender a Caín literalmente como una encarnación del Mesías.",
    "Siendo así, bajo la óptica de los hebraístas más rigurosos, la expresión de Eva fue: «He adquirido un varón, Jehová». Como resalta el comentarista Markus DaSilva en la *Biblia de Estudio Sembradores*, ella creía piadosamente que aquel bebé era el propio Yahweh manifestado, el varón prometido en Génesis 3:15.",
    "Esto se debe a que la erudición bíblica nos desvela una capa mucho más profunda. La partícula hebrea *'et* (אֶת) actúa, en la mayoría de los casos, como la marca del objeto directo, la cual no admite separación del término que le sigue, indicando que el vocablo subsiguiente es el **objeto directo del verbo**. Gramaticalmente no debe traducirse como **«con»**.",
    "Si Eva hubiera querido decir «He adquirido un varón **con** el Señor», la frase habría sido: קָנִיתִי אִישׁ עִם יְהוָה (*Qaniti ish im YHWH*). No obstante, el texto **NO emplea** עִם (*im*, «con»), sino **אֶת (*et*)**, ¡lo cual transforma radicalmente el sentido!",
    "El *Targum Jonatán*, una antigua traducción aramea de la Torá, recoge una interpretación que refuerza la lectura literal del hebreo: *«He adquirido un varón: el Ángel del Señor»*. Esta traducción demuestra que, ya en la antigüedad, existía la comprensión de que Eva esperaba que Caín fuese más que un hombre común.",
    "Pero para el entendimiento esencial poco importa la discrepancia de traducción. De cualquier modo comprendemos que Eva vinculaba el nacimiento de su primogénito con la providencia divina. En su mente recién caída, pero ya redimida por la promesa, aguardaba que el remedio para la muerte llegara tan velozmente como el veneno. Llamó al niño Caín, que significa «posesión» o «adquirido», pues sentía que ya tenía en sus manos la garantía de la victoria final.",
    "La tragedia de Caín —quien pronto se revelaría como un «hijo del maligno»— sirve para enseñarnos que el descanso del alma no nace de la carne ni de la voluntad humana, sino del tiempo perfecto del Espíritu. El error de Eva consistió en intentar apresurar el *Tetelestai* de Dios. Anhelaba el alivio antes de atravesar el desierto.",
    "Eva estaba equivocada respecto al cronómetro de Dios, pero estaba magníficamente acertada en cuanto al objeto de su fe. Creía que la liberación provendría de Dios mediante la maternidad y que sería un descendiente suyo. Creía que la victoria sobre el pecado exigiría la venida de un Hombre que fuese también manifestación del propio Señor. Como bien describe la *Guía Willmington para la Biblia*, ella anhelaba al Salvador, aunque confundió al primer homicida de la historia con el Redentor del mundo.",
    "Creía Eva que aquel primer hijo ya podía ser la consumación de la promesa, que aquel niño en sus brazos era ya el Libertador destinado a aplastar el mal. No había comprendido que el tiempo de Dios no es el nuestro, ni que la simiente necesitaría atravesar generaciones de patriarcas, reyes y exiliados hasta que el terreno estuviese preparado. Lo que Eva exclamó con esperanza, el Padre lo selló con paciencia.",
    "Lo que comenzó como un clamor de alivio en el nacimiento de Caín hallaría su verdadero cumplimiento aquí, ahora, en el sacrificio de Aquel que es, de hecho, la Simiente prometida.",
    "¿Ha intentado usted fabricar su propio «Caín», creyendo que los frutos de su esfuerzo o las novedades de esta época son su salvador personal? ¿Tiene usted la fe de Eva para esperar en el Señor, pero posee la paciencia de Dios para aguardar su tiempo? Recuerde: el consuelo del alma no proviene de una posesión que adquirimos, sino de una Persona que nos adquirió en la Cruz."
]

b1_en['7'] = [
    "We stand here before one of the most vibrant and poignant moments in the history of redemption. Envision the first mother of humanity, with the pangs of childbirth still throbbing—those very pains announced to her as the consequence of transgression—holding in her arms the first life brought forth in time and space.",
    "Eve looks upon that fragile infant and, in a leap of faith that defies her own misery, exclaims: *'I have gotten a man, the LORD!'* (Genesis 4:1, literal translation). As the author of *Shadows, Types, and Mysteries of the Bible* perceptively observes, Eve's joy was not merely biological; it was messianic. She saw not merely a newborn son, but the immediate fulfillment of the promise that the 'Seed of the Woman' would crush the serpent's head.",
    "The Hebrew phrase ***qãnîthi 'îsh 'et-yhwh (קָנִיתִי אִישׁ אֶת־יְהוָה)*** can be translated literally just as it stands, although from the ancient Greek Septuagint down to modern translations it is often softened to 'I have acquired a man with the help of the Lord' or 'I have gotten a man from the Lord,' indicating that she acknowledged divine favor, yet without taking Cain literally as the incarnate Messiah.",
    "Consequently, from the standpoint of rigorous Hebraic grammar, Eve's exclamation was: 'I have gotten a man, Yahweh.' As commentator Markus DaSilva highlights in the *Semeadores Study Bible*, she piously believed that this infant was the manifest presence of Yahweh Himself, the deliverer promised in Genesis 3:15.",
    "Biblical scholarship reveals a far deeper grammatical reality. The Hebrew particle *'et* (אֶת) functions predominantly as the marker of the direct object, which binds irrevocably to the term that follows it, denoting that the noun is the **direct object of the verb**. Grammatically, it should not be translated as **'with'**.",
    "Had Eve intended to say 'I have gotten a man **with** the Lord,' the Hebrew phrasing would have been: קָנִיתִי אִישׁ עִם יְהוָה (*Qaniti ish im YHWH*). Yet the text **DOES NOT use** עִם (*im*, 'with'), but rather **אֶת (*et*)**, which fundamentally transforms the meaning!",
    "The ancient Aramaic *Targum Jonathan* preserves a rendering that reinforces the literal Hebrew reading: *'I have acquired a man: the Angel of the Lord.'* This ancient paraphrase demonstrates that, even in antiquity, there existed the understanding that Eve anticipated Cain to be far more than a common mortal.",
    "Yet for the fundamental truth of the passage, translational debates are secondary. In either case, we recognize that Eve connected the birth of her firstborn directly to divine providence. In her newly fallen mind, yet already redeemed by the promise, she expected the antidote to death to arrive as swiftly as the poison. She named the child Cain, meaning 'possession' or 'acquired,' feeling that she already held in her hands the guarantee of final victory.",
    "The tragedy of Cain—who soon proved to be of the 'evil one'—teaches us that soul-rest is not born of the flesh or the will of man, but of the Spirit's sovereign timing. Eve's mistake was attempting to hasten God's *Tetelestai*. She sought relief before journeying through the wilderness.",
    "Eve was mistaken concerning God's timetable, but she was magnificently right regarding the object of her faith. She believed that deliverance would come from God through motherhood, and that it would be her own offspring. She believed that victory over sin required the coming of a Man who was also the manifestation of the Lord Himself. As *Willmington's Guide to the Bible* beautifully describes, she yearned for the Savior, even though she mistook history's first murderer for the Redeemer of the world.",
    "Eve believed that her firstborn son could already be the fulfillment of the promise, that the child in her arms was the Deliverer destined to crush evil. She had not yet grasped that God's time is not our time, nor that the seed would need to journey through generations of patriarchs, monarchs, and exiles before the soil was prepared. What Eve exclaimed in hope, the Father sealed with divine patience.",
    "What began as a cry of relief at Cain's birth would find its true, unshakeable fulfillment here, now, in the sacrifice of Him who is indeed the promised Seed.",
    "Have you been attempting to construct your own 'Cain,' imagining that the fruit of your labor or the novelties of this age are your personal savior? Do you possess Eve's faith to hope in the Lord, while cultivating God's patience to wait upon His timing? Remember: soul-relief does not stem from a possession we acquire, but from a Person who acquired us upon the Cross."
]

# NOTE 8 (4 paragraphs - Caim, Abel e Sete)
b1_es['8'] = [
    "**El Fratricidio como Estrategia del Infierno —** Existe una ironía sombría y estremecedora en este acto. El Señor había decretado que la simiente de la mujer aplastaría la cabeza de la serpiente (Génesis 3:15). En una tentativa desesperada y perversa de revertir este veredicto, el adversario incitó a Caín a «aplastar la cabeza» de su hermano. Al asesinar a Abel, Caín dio expresión concreta al empeño satánico de interrumpir el flujo de la gracia antes de que alcanzara la plenitud de los tiempos. Caín se convirtió así en el instrumento de la enemistad de la serpiente, pretendiendo asesinar la esperanza cuando aún era un tierno brote.",
    "Contemplen, amados, el campo ensangrentado donde yace el cuerpo del justo Abel. A los ojos humanos, vemos a un hermano asesinado por envidia; a los ojos de Dios, contemplamos el primer intento del infierno por aniquilar el linaje del Mesías. Como bien observa el comentarista en la *Biblia de Estudio de Ginebra*, la humanidad, a partir de Génesis 3, quedó dividida en dos comunidades: los redimidos, que aman a Dios, y los réprobos, que se aman a sí mismos. Caín, al levantar su mano contra su hermano, desertó de la familia real de Dios para erigirse en el arquetipo de los seguidores de Satanás.",
    "El linaje de la promesa parecía haber sido cercenado en su mismo nacimiento. Pero la gracia de Dios no puede ser frustrada por la tragedia de un homicida. En el momento preciso en que las tinieblas parecían cantar victoria, el Señor concedió a Eva otro hijo. Ella lo llamó **Set** (*Sheth*), nombre que en el suelo sagrado de las Escrituras florece con el significado de «compensación» o «designado». Set fue puesto por Dios para ocupar el lugar de Abel. El nacimiento de Set no fue un simple consuelo maternal; constituyó un acto soberano del Rey para garantizar que la línea real y el fuego de la adoración genuina no se extinguieran sobre la tierra.",
    "A partir de Set, el registro bíblico nos hace saber que «se comenzó a invocar el nombre del Señor» (Génesis 4:26). Mientras la descendencia de Caín construía con orgullo ciudades amuralladas para escudarse de la maldición divina, el linaje de Set erigía altares para refugiarse en la misericordia del Señor. Set prolongó la línea regia que culminaría en Jesucristo, el verdadero Descendiente que, definitiva y verdaderamente, aplastaría la cabeza de la serpiente, no con la espada de Caín, sino en Su propia cruz."
]

b1_en['8'] = [
    "**Fratricide as Hell's Strategy —** There is a dark and terrible irony in this act. The Lord had pronounced that the seed of the woman would crush the serpent's head (Genesis 3:15). In a desperate and perverse attempt to overturn that verdict, the enemy incited Cain to \"crush the head\" of his brother. In slaying Abel, Cain gave tangible expression to the satanic effort to sever the stream of grace before it could reach the fullness of time. Cain thus became the instrument of the serpent's enmity, attempting to assassinate hope while it was still a tender shoot.",
    "Behold, beloved, the blood-soaked field where the body of righteous Abel lies. In human eyes, we see a brother murdered out of envy; in the eyes of God, we behold hell's first strike to eradicate the messianic line. As the commentator in the *Geneva Study Bible* perceptively notes, humanity, from Genesis 3 onward, was divided into two distinct communities: the redeemed, who love God, and the reprobate, who love themselves. Cain, by raising his hand against his brother, deserted the royal family of God to become the archetype of Satan's followers.",
    "The lineage of promise appeared to be cut off at its inception. Yet the grace of God cannot be thwarted by the tragedy of a murderer. In the very hour when darkness seemed to triumph, the Lord granted Eve another son. She named him **Seth** (*Sheth*), which in the sacred terrain of the Scriptures blossoms with the meaning of \"appointed\" or \"compensation.\" Seth was set in place by God to take the place of Abel. The birth of Seth was not merely maternal solace; it was a sovereign decree of the King ensuring that the royal line and the sacred flame of true worship would never be extinguished from the earth.",
    "Beginning with Seth, the biblical record informs us that \"people began to call on the name of the Lord\" (Genesis 4:26). While the offspring of Cain pridefully built fortified cities to shield themselves from divine judgment, the lineage of Seth built altars to take refuge in divine mercy. Seth extended the royal line that would culminate in Jesus Christ, the true Offspring who would ultimately and decisively crush the serpent's head—not with Cain's murderous weapon, but upon His own cross."
]

# NOTE 9 (7 paragraphs - Noé e a Arca)
b1_es['9'] = [
    "El arca de Noé es uno de los tipos más elocuentes de nuestro Señor Jesucristo; en ella, la justicia de Dios y Su misericordia navegan juntas sobre el abismo de la destrucción. ¡Qué maravilla contemplar cómo el hilo escarlata de la redención, iniciado en el Edén, atraviesa las aguas implacables del diluvio para hallar cobijo en el linaje de un solo hombre! Nos encontramos ahora ante el arca: no simplemente un cajón de madera de gofer, sino el vientre de la nueva humanidad y el santuario móvil de la promesa mesiánica.",
    "El testimonio bíblico en Génesis 6:5 es de una crudeza sobrecogedora: *«la maldad de los hombres era mucha en la tierra, y todo designio de los pensamientos del corazón de ellos era de continuo solamente el mal»*. La humanidad había demostrado su depravación absoluta mediante una venganza desenfrenada y una tiranía que desafiaba el trono del Altísimo. La tierra, que debía ser un huerto de *shalom*, se había convertido en un matadero de violencia.",
    "Ante semejante escenario, el Señor, con el corazón traspasado de dolor, determinó traer juicio. El diluvio no fue un mero accidente geográfico, sino un acto judicial del Creador y Rey contra la rebelión de Su criatura. Sin embargo, en medio del estruendo del juicio, resonó la melodía de la gracia: *«Pero Noé halló gracia a los ojos del Señor»* (Génesis 6:8).",
    "Es preciso comprender que Noé no fue salvado por ser intrínsecamente perfecto ante la ley, sino porque la gracia soberana de Dios lo alcanzó y lo capacitó para caminar con su Creador. Como bien explica Markus DaSilva en la *Biblia de Estudio Sembradores*, la gracia jamás es un «favor barato» que pasa por alto el pecado, sino el poder que rescata al justo de en medio de la condenación universal.",
    "El arca fue el instrumento soberano para preservar la «simiente de la mujer» —aquella Simiente prometida en Génesis 3:15 que habría de aplastar la cabeza de la serpiente—. Si Noé hubiese perecido, la promesa divina habría fracasado. ¡Pero Dios es fiel! El arca, calafateada con la brea de la expiación (*kapar*), flotó sobre las aguas de muerte para garantizar que la vida continuara.",
    "Al salir del arca, el horizonte de la historia redentora se vuelve más específico. Noé, actuando como patriarca y profeta, anunció el destino de sus hijos. Y sobre Sem pronunció las palabras que moldearían el porvenir de las naciones: *«¡Bendito sea el Señor, el Dios de Sem!»* (Génesis 9:26). Es a través de Sem como el nombre de Dios es exaltado de forma singular. De su linaje provino Éber —de cuyo nombre deriva el apelativo «hebreo»— y de donde surgiría, milenios más tarde, el patriarca Abraham. La promesa dada en el Edén y preservada en el arca halló en Sem su cauce real. En esta línea genealógica edificó Dios a la nación de Israel, transformándola en depositaria de la revelación y en la cuna donde el Verbo se haría carne. En la «tienda de Sem», el Dios que no cabe en el universo escogió morar entre los hombres para, finalmente, en Cristo, conceder descanso eterno a nuestras almas.",
    "El diluvio remite asimismo a la segunda venida del Mesías, en ocasión del arrebatamiento de la Iglesia y del Gran Juicio, tal como Jesús advirtió en Mateo 24:39: *«Y no entendieron hasta que vino el diluvio y se los llevó a todos; así será también la venida del Hijo del Hombre»*."
]

b1_en['9'] = [
    "Noah's ark is one of the most eloquent typologies of our Lord Jesus Christ; within it, God's justice and His mercy sail together across the abyss of destruction. What a wonder it is to behold how the scarlet thread of redemption, commenced in Eden, traverses the merciless floodwaters to find shelter in the lineage of a single faithful man! We stand now before the ark—not merely a chest of gopher wood, but the womb of new humanity and the mobile sanctuary of the messianic promise.",
    "The biblical record in Genesis 6:5 presents an arresting starkness: *'every inclination of the thoughts of the human heart was only evil all the time'*. Humanity had demonstrated its radical depravity through unrestrained vengeance and violent tyranny that defied the throne of the Most High. The earth, intended to be a garden of *shalom*, had degenerated into a slaughterhouse of violence.",
    "Faced with such wickedness, the Lord, with a heart grieved by pain, determined to execute divine judgment. The flood was no random geological catastrophe, but the formal judicial decree of the Creator-King against the rebellion of His creation. Yet, amidst the rumblings of judgment, the sweet chord of grace was sounded: *'Noah, however, found favor in the eyes of the LORD'* (Genesis 6:8).",
    "We must recognize that Noah was not delivered because he was intrinsically sinless under the law, but because God's sovereign grace reached him and empowered him to walk with his Maker. As Markus DaSilva elucidates in the *Semeadores Study Bible*, grace is never a 'cheap favor' that trivializes sin, but the divine power that rescues the righteous from the midst of universal condemnation.",
    "The ark was the sovereign vessel appointed to preserve the 'seed of the woman'—that promised Offspring of Genesis 3:15 destined to crush the serpent's head. Had Noah perished, the covenant promise would have failed. But God is faithful! The ark, sealed inside and out with the pitch of atonement (*kapar*), rode above the waters of death to ensure that life would endure.",
    "Upon disembarking from the ark, the unfolding narrative of redemption narrows with laser precision. Noah, acting as prophet-patriarch, pronounced the destiny of his sons. Over Shem he uttered the words that would shape the spiritual destiny of nations: *'Praise be to the LORD, the God of Shem!'* (Genesis 9:26). It was uniquely through Shem that the name of Yahweh was exalted. From his line emerged Eber—from whom the name 'Hebrew' derives—and centuries later, the patriarch Abraham. The Edenic promise preserved through the deluge found in Shem its royal conduit. Within this lineage God established Israel as the custodian of divine revelation and the cradle wherein the Word would become flesh. In the 'tents of Shem,' the God whom heaven cannot contain chose to tabernacle among men, so that in Christ He might finally grant eternal rest to our souls.",
    "The flood also points forward to the Second Coming of the Messiah, the gathering of the Church, and the Great White Throne Judgment, as Jesus Himself warned in Matthew 24:39: *'and they knew nothing about what would happen until the flood came and took them all away. That is how it will be at the coming of the Son of Man.'*"
]

# NOTE 12 (4 paragraphs - Siló e o cetro de Judá)
b1_es['12'] = [
    "El término hebreo *Šīlōh* es objeto de profunda deliberación académica. Van Groningen expone diversas interpretaciones —«aquel cuyo derecho es», «pacificador» o «aquel que ha de venir»— y concluye que alude inequívocamente a un Gobernante personal venidero: el Mesías (GRONINGEN, 1995, p. 158-167). Los Tárgumes traducen: «hasta que venga el Mesías, a quien pertenece el reino» (Tárgum Onquelos, apud GRONINGEN, 1995, p. 74).",
    "Pero, ¿quién es este Siloh, en quien Jacob depositó su postrera esperanza? La erudición bíblica, como resalta el *Comentario Bíblico Beacon*, sugiere que el vocablo evoca «descanso» o «el dador de reposo». Otras vertientes traducen como «Aquel a quien pertenece» el señorío. Ambas corrientes fluyen hacia el mismo manantial: Siloh es Jesucristo.",
    "Aunque la dinastía de David (de la tribu de Judá) gobernó sobre Israel a lo largo de siglos, constituía únicamente la sombra de la sustancia venidera. El cetro permaneció con Judá a través de destierros y turbulencias, como testimonio vivo de que la Simiente continuaba latiendo, hasta que el verdadero Siloh entró en Jerusalén montado sobre un pollino —exactamente como Jacob profetizó al evocar al «hijo de su asna» en Génesis 49:11—.",
    "Siloh es Aquel a quien rinden obediencia las naciones. No nos convoca a un gravoso sistema de exigencias legales, sino que, como el auténtico Dador de Descanso, exclama amoroso: *«¡Vengan a mí!»*. El alivio del alma, estimado lector, es una realidad gloriosa únicamente porque el León de la Tribu de Judá venció para desatar los sellos de nuestra redención."
]

b1_en['12'] = [
    "The Hebrew title *Šīlōh* has generated extensive scholarly debate. Van Groningen presents several leading interpretations—'he whose right it is,' 'peacemaker,' or 'he who is to come'—and concludes that it definitively designates a personal, future Ruler: the Messiah (GRONINGEN, 1995, pp. 158–167). The Targums explicitly render: 'until the Messiah comes, to whom the kingdom belongs' (Targum Onkelos, cited in GRONINGEN, 1995, p. 74).",
    "Yet who is this Shiloh, in whom Jacob anchored his dying hope? Biblical scholarship, as highlighted in the *Beacon Bible Commentary*, suggests that the term fundamentally signifies 'rest' or 'the rest-giver.' Other philological traditions translate it as 'He to whom it belongs.' Both streams converge at the very same fountain: Shiloh is Jesus Christ.",
    "While the Davidic dynasty (of the tribe of Judah) reigned in Jerusalem for centuries, it served merely as the temporal shadow of the substance to come. The scepter remained with Judah through exile and crisis, as a living token that the Seed was alive, until the true Shiloh entered Jerusalem humble and riding upon a donkey—precisely as Jacob foretold when speaking of 'the foal of his donkey' in Genesis 49:11.",
    "Shiloh is He to whom belongs the obedience of the nations. He calls us not to a crushing burden of legalism, but as the true Rest-Giver, He proclaims: *\"Come to me!\"*. Soul-rest, beloved reader, is possible only because the Lion of the Tribe of Judah has conquered to open the scroll of our redemption."
]

# Save updated Batch 1
with open('translations/emmaus_sermon/endnotes_batch_1_es.json', 'w', encoding='utf-8') as f:
    json.dump(b1_es, f, ensure_ascii=False, indent=2)
with open('translations/emmaus_sermon/endnotes_batch_1_en.json', 'w', encoding='utf-8') as f:
    json.dump(b1_en, f, ensure_ascii=False, indent=2)

print("Batch 1 endnotes updated.")

# NOTE 20 (3 paragraphs - Josué, Yehoshua e o Príncipe do Exército do Senhor)
b2_es['20'] = [
    "El nombre hebreo *Yehoshua* (יְהוֹשֻׁעַ) —contraído como *Yeshua* (יֵשׁוּעַ) en el período posexílico— es exactamente el mismo nombre vertido al griego como *Iesous* (Ἰηsouς), esto es, **Jesús**. El autor de la Epístola a los Hebreos explora de forma explícita esta conexión: «Porque si Josué les hubiera dado el reposo, no hablaría después de otro día» (Hebreos 4:8), empleando el mismo vocablo griego *Iesous* tanto para Josué como para Jesús.",
    "El punto culminante de la vivencia de Josué no acaeció en un consejo de guerra humano, sino en un encuentro sobrenatural junto a las puertas de Jericó. Josué divisó a un varón con una espada desenvainada en la mano y, cual centinela alerta, le preguntó: *«¿Eres de los nuestros o de nuestros enemigos?»*. La réplica fue un relámpago de majestad: *«No; más bien he venido ahora como Príncipe del ejército del Señor»* (Josué 5:14).",
    "Advierta bien, amado lector: el Señor no se presenta para tomar partido en nuestros planes humanos; Él viene a asumir el mando supremo. Al escuchar la orden: *«Quítate las sandalias de los pies, porque el lugar donde estás es sagrado»*, Josué reconoció al instante la misma voz soberana que le había hablado a Moisés desde la zarza ardiente. Este Príncipe no era un mero ángel creado, sino una teofanía: el propio Hijo de Dios en forma visible, el Verbo Eterno allanando el camino de la redención. El auténtico Conquistador de Jericó no fue Josué, sino el Señor de los Ejércitos, quien derribó las murallas mientras el pueblo simplemente obedecía en rendida adoración."
]

b2_en['20'] = [
    "The Hebrew name *Yehoshua* (יְהוֹשֻׁעַ)—contracted to *Yeshua* (יֵשׁוּעַ) in the post-exilic era—is the exact same name translated into Greek as *Iesous* (Ἰησοῦς), which is **Jesus**. The author of Hebrews explicitly expounds this connection: \"For if Joshua had given them rest, God would not have spoken later about another day\" (Hebrews 4:8), utilizing the identical Greek name *Iesous* for both Joshua and Jesus.",
    "The crowning moment of Joshua's pilgrimage occurred not in a human war council, but in a supernatural encounter outside the gates of Jericho. Joshua looked up and saw a man standing before him with a drawn sword in his hand. Like a vigilant soldier, Joshua challenged him: *\"Are you for us or for our enemies?\"* The reply came as a shattering declaration of authority: *\"Neither,\" he replied, \"but as commander of the army of the LORD I have now come\"* (Joshua 5:14, NIV).",
    "Mark well, dear reader: the Lord does not come to take sides in our human agendas; He comes to take absolute command. Upon hearing the sovereign command, *\"Take off your sandals, for the place where you are standing is holy,\"* Joshua instantly recognized the very same voice that had spoken to Moses from the burning bush. This Commander was no mere created angel, but a glorious Christophany—the pre-incarnate Son of God in visible form, the Eternal Word blazing the trail for redemption. The true Conqueror of Jericho was not Joshua, but the Lord of Hosts, who brought down the impenetrable walls while the people simply obeyed in reverent worship."
]

# NOTE 21 (3 paragraphs - Josué como tipo messiânico)
b2_es['21'] = [
    "El Señor, en Su infinita gracia, concedió a Josué una promesa que constituye el ancla inamovible de todo liderazgo espiritual: *«Como estuve con Moisés, estaré contigo; no te dejaré, ni te desampararé»* (Josué 1:5). Aquella no fue solo una palabra de consuelo, sino la garantía soberana de que la misma Presencia que abrió el Mar Rojo ahora detendría las aguas del Jordán. Josué comprendió que su autoridad no radicaba en sus talentos personales, sino en su sumisión incondicional al «Libro de la Ley», en la meditación constante y en la valentía que brota de la convicción de que el Señor pelea por Su pueblo.",
    "Van Groningen identifica cuatro factores determinantes en el papel mesiánico de Josué: (1) fue un tipo mesiánico consumado —«Yahweh operó a través de él para llevar adelante Su programa del pacto»—; (2) se desempeñó «cual si fuera una figura regia, con investidura real y prerrogativas regias»—; (3) «llevó a cabo actos de salvación a vasta escala»—; y (4) «sirvió predominantemente como figura real» que a su vez reflejó la dignidad profética (GRONINGEN, 1995, p. 242-243). El «Príncipe del ejército del Señor» (Josué 5:13-15) es identificado como una teofanía —manifestación preencarnada del Ángel del Señor, según Meredith Kline en *Images of the Spirit* (Grand Rapids: Baker, 1980), p. 75-79—.",
    "Josué prefiguró al Mesías en cada etapa de su ministerio. Si Moisés personifica la Ley que nos conduce hasta la frontera del desierto, Josué encarna la Gracia que nos hace vadear el Jordán de nuestra impotencia para tomar posesión de la herencia celestial. Fue el «Jesús del Antiguo Testamento», un tipo intachable que guio a Israel hacia la victoria sin que vestigio alguno de vanagloria empañara la nobleza de su andar. Mientras el nombre familiar de Josué era *Oseas* («salvación»), el Señor añadió el prefijo divino (*Yahweh*) para proclamar que la redención no proviene del esfuerzo humano, sino de la soberanía de Dios."
]

b2_en['21'] = [
    "The Lord, in His boundless grace, bestowed upon Joshua a promise that remains the unshakeable bedrock of all spiritual leadership: *\"As I was with Moses, so I will be with you; I will never leave you nor forsake you\"* (Joshua 1:5). This was not merely an encouraging word, but the sovereign guarantee that the very Presence that divided the Red Sea would now heap up the waters of the Jordan. Joshua understood that his authority rested not upon natural talent, but upon unconditional submission to the 'Book of the Law,' daily meditation, and the steadfast courage born of the certainty that the Lord fights for His people.",
    "Van Groningen identifies four foundational dimensions of Joshua's messianic role: (1) he was an authentic messianic type—'Yahweh worked through him in advancing His covenantal program'; (2) he functioned 'as a royal figure, in royal capacity, with royal prerogatives'; (3) he 'wrought deeds of salvation on a magnificent scale'; and (4) he 'served predominantly as a royal deliverer' who also reflected prophetic dignity (GRONINGEN, 1995, pp. 242–243). The 'Commander of the army of the LORD' (Joshua 5:13–15) is identified as a Christophanic appearance of the Angel of the Lord, as documented by Meredith Kline, *Images of the Spirit* (Grand Rapids: Baker, 1980), pp. 75–79.",
    "Joshua foreshadowed the Messiah at every milestone of his journey. If Moses represents the Law that brings us to the outer boundary of our strength, Joshua typifies the Grace that carries us through the Jordan of our helplessness into full possession of the divine inheritance. He stood as the 'Jesus of the Old Testament,' an unblemished type who led Israel to triumphant victory without a single trace of personal vanity tarnishing his noble character. While his ancestral family name was *Hoshea* ('salvation'), the Lord attached the divine prefix (*Yahweh*) to declare that salvation originates not from mortal man, but from Yahweh alone."
]

# NOTE 32 (2 paragraphs - Dupla genealogia, Zelofejad e Calebe)
b2_es['32'] = [
    "Jesús es descendiente de Judá y David tanto por José (legalmente) como por María (biológicamente), cumpliendo las profecías mesiánicas a través de ambas líneas genealógicas. Mateo 1 traza la línea real a través de José y Salomón, mientras que Lucas 3 presenta el linaje de María y Natán, conectándose ambos con David y, por ende, con la tribu de Judá. **Linaje de José (Legal/Real):** Al adoptar José a Jesús como hijo primogénito, le confirió los plenos derechos sucesorios al trono de David, pues José provenía de la estirpe regia de Salomón. **Linaje de María (Biológico/Consanguíneo):** El Evangelio de Lucas documenta la genealogía de María, demostrando que Jesús, también a través de Su madre terrenal, era descendiente directo de Natán, otro de los hijos de David, asegurando la continuidad biológica según la carne. **Conexión con Judá:** Ambas genealogías corroboran de forma indiscutible que la familia entera desciende de la tribu real de Judá.",
    "Adicionalmente, podemos profundizar en esta comprensión para corroborar la legitimidad por vía complementaria. Incluso el observador más apegado a la patrilinealidad estricta reconocerá que el Antiguo Testamento contempla situaciones providentes específicas donde la ley divina afirma y resguarda la primacía de la herencia materna: **a)** Las Hijas de Zelofejad (Caso Excepcional en Números 27:1-11; 36:1-12): Cuando un varón fallecía sin descendencia masculina, la jurisprudencia divina determinó que su patrimonio e identidad tribal pasaban legítimamente a sus hijas, siempre que contrajeran nupcias dentro de su propia tribu para evitar la transferencia de la herencia; **b)** Caleb es llamado reiteradamente «hijo de Jefone el cenezeo» (Números 32:12; Josué 14:6, 14). Los cenezeos eran pueblos nómadas que habitaban Canaán y no pertenecían originalmente a las doce tribus de Israel. Sin embargo, Caleb fue plenamente integrado como príncipe de la tribu de Judá porque su madre era una israelita de dicha tribu, y porque su parentela fue incorporada pactualmente durante la travesía del desierto (Números 13:6; 34:19). Josué 15:13 ratifica que Caleb recibió su heredad en Hebrón «en medio de los hijos de Judá», confirmando su pleno derecho tribal a pesar de la ascendencia paterna foránea; **c)** Precedentes Análogos: En Levítico 24:10, la Escritura relata el caso del hijo de una mujer israelita (de la tribu de Dan) y un padre egipcio, quien fue formalmente inscrito en la congregación de Israel a través de la ascendencia materna. Así, tanto por derecho legal como por consanguinidad biológica, Cristo es el León legítimo de la Tribu de Judá."
]

b2_en['32'] = [
    "Jesus is the descendant of Judah and David both through Joseph (legally) and through Mary (biologically), fulfilling Old Testament messianic prophecies across both genealogical lines. Matthew 1 traces the royal line through Joseph via Solomon, while Luke 3 presents the maternal lineage of Mary through Nathan, both converging upon David and, consequently, upon the royal tribe of Judah. **Joseph's Lineage (Legal/Royal):** Because Joseph adopted Jesus as his legal firstborn, he conferred upon Him full hereditary succession rights to the Davidic throne, since Joseph belonged to the royal dynasty of Solomon. **Mary's Lineage (Biological/Physical Seed):** The Gospel of Luke records Mary's genealogy, demonstrating that Jesus was also, through His human mother, a direct physical descendant of Nathan, another son of David, guaranteeing His biological Davidic seed according to the flesh. **Connection with Judah:** Both genealogies establish beyond dispute that the family descends squarely from the tribe of Judah.",
    "Furthermore, we can deepen our understanding through additional biblical precedents. Even the reader most strictly committed to patrilineal descent must recognize that the Old Testament Scriptures record specific providential circumstances affirming the validity and protection of maternal inheritance: **a)** The Daughters of Zelophehad (A Landmark Legal Precedent in Numbers 27:1–11; 36:1–12): When an Israelite man died without male heirs, divine jurisprudence established that his inheritance and tribal name passed directly to his daughters, provided they married within their father's tribe to prevent the transfer of the ancestral allotment; **b)** Caleb is repeatedly identified as 'the son of Jephunneh the Kenizzite' (Numbers 32:12; Joshua 14:6, 14). The Kenizzites were originally non-Israelite nomadic peoples dwelling in Canaan. Yet Caleb was fully numbered among Judah because his mother was an Israelite woman of that tribe, and his family was covenantally assimilated during the wilderness wanderings. So complete was his integration that Caleb represented Judah as prince (Numbers 13:6; 34:19), and Joshua 15:13 confirms that Caleb was allotted Hebron 'in the midst of the children of Judah,' validating his rightful place despite his father's Kenizzite origin; **c)** Similar Biblical Cases: In Leviticus 24:10, Scripture records the instance of a man whose mother was an Israelite of the tribe of Dan and whose father was an Egyptian, who was registered within the congregation of Israel through maternal lineage. Thus, both by royal legal right and by sacred physical consanguinity, Christ is the legitimate Lion of the Tribe of Judah."
]

# Save updated Batch 2
with open('translations/emmaus_sermon/endnotes_batch_2_es.json', 'w', encoding='utf-8') as f:
    json.dump(b2_es, f, ensure_ascii=False, indent=2)
with open('translations/emmaus_sermon/endnotes_batch_2_en.json', 'w', encoding='utf-8') as f:
    json.dump(b2_en, f, ensure_ascii=False, indent=2)

print("Batch 2 endnotes updated.")

# ==============================================================================
# CONSOLIDAÇÃO DOS JSONS FINAIS E RECOMPILAÇÃO DOS DOCX
# ==============================================================================

import compile_final_books
print("Successfully recompiled books and updated all JSONs.")
