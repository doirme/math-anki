## RAPPELS ET COMPLÉMENTS SUR LES FONCTIONS RÉELLES

Dans ce chapitre, E et F sont des parties quelconques de $/Rbbb$ , pas forcément des intervalles.

Le vocabulaire des applications a été présenté en toute généralité au chapitre « Relations binaires et applications », mais les fonctions de /Rbbb dans /Rbbb vont de pair avec un vocabulaire propre aux réels - monotonie, caractère majoré / minoré, continuité, dérivabilité. . . - qui est l'objet du chapitre.

Mais d'abord, un mot sur les composées. Soient f : E -→ /Rbbb et g : F -→ /Rbbb deux fonctions. La composée g ◦ f n'est définie que si f est à valeurs dans F , i.e. si f ( E ) ⊂ F . On donne ci-dessous quelques exemples de recherche d'ensemble de définition.

Quand la fonction extérieure g est définie sur /Rbbb tout entier, la condition f ( E ) ⊂ /Rbbb est trivialement vraie et g ◦ f est définie sans qu'aucun obstacle se soit présenté. La fonction e f ne pose par exemple jamais aucun problème de définition car la fonction exponentielle est définie sur /Rbbb tout entier.

Exemple La fonction $x /mapstochar-→ /radicallow x + 3$ est définie sur [ -3, + ∞ [ .

Démonstration La fonction $x /mapstochar-→ x + 3$ est définie sur /Rbbb et la fonction /radicallow · l'est sur /Rbbb + , mais quand x décrit /Rbbb , x + 3 n'appartient pas forcément à /Rbbb + . Pour quels x ∈ /Rbbb est-il vrai que x + 3 /greaterorequalslant 0? Réponse : x ∈ [ -3, + ∞ [ .

<!-- formula-not-decoded -->

Démonstration La fonction x /mapstochar-→ x 2 -3 x + 2 est définie sur /Rbbb et x /mapstochar-→ ln x l'est sur /Rbbb ∗ + , mais quand x décrit /Rbbb , x 2 -3 x + 2 n'appartient pas forcément à /Rbbb ∗ + . Pour quels x ∈ /Rbbb est-il vrai que x 2 -3 x + 2 &gt; 0? Réponse : x ∈ ] -∞ , 1 [ ∪ ] 2, + ∞ [ car les racines du polynôme sont 1 et 2 et son coefficient dominant est strictement positif.

/negationslash

<!-- formula-not-decoded -->

## 1 VOCABULAIRE USUEL

## 1.1 MONOTONIE

Définition (Fonction monotone) Soit f : E -→ /Rbbb une fonction.

- On dit que f est croissante si :

$$∀ x , y ∈ E , x < y = ⇒ f ( x ) /lessorequalslant f ( y ) .$$


- On dit que f est strictement croissante si :

$$∀ x , y ∈ E , x < y = ⇒ f ( x ) < f ( y ) .$$

- On dit que f est décroissante si :

<!-- formula-not-decoded -->

- On dit que f est (resp. strictement ) monotone si f est (resp. strictement) croissante ou décroissante.

Une fonction croissante (resp. décroissante) est une fonction qui préserve (resp. renverse) les inégalités.

On peut caractériser la monotonie d'une fonction dérivable par le signe de sa dérivée, mais il s'agit là d'un théorème et non d'une définition. La définition ci-dessus est générale et ne requiert pas la dérivabilité.

Le résultat qui suit a été démontré au chapitre « Relations binaires et applications ».

Théorème (Injectivité et stricte monotonie)

Soit f : E -→ /Rbbb une fonction.

Si f est strictement monotone, f est injective.

Les résultats qui suivent sont énoncés en termes de monotonie au sens large, mais ils sont valables pour des fonctions monotones au sens strict.

/negationslash

/negationslash

## Théorème (Opérations sur les fonctions monotones)

- (i) Addition : Soient f : E -→ /Rbbb et g : E -→ /Rbbb deux fonctions. Si f et g sont croissantes, f + g l'est aussi. Si f et g sont décroissantes, f + g
- (ii) Produit : Soient f : E -→ /Rbbb et g : E -→ /Rbbb deux fonctions.

l'est aussi.

Si f et g sont croissantes POSITIVES , f g est croissante. Si f et g sont décroissantes POSITIVES , f g est décroissante.

- (iii) Composition : Soient f : E -→ F et g : F -→ /Rbbb deux fonctions.
- Si f et g sont monotones de sens de variation opposés, g ◦ f est décroissante.
- Si f et g sont monotones de même sens de variation, g ◦ f est croissante.
- (iv) Réciproque : Soit f : E -→ F une fonction bijective de E sur F .

Si f est monotone, elle l'est strictement et f -1 est strictement monotone de même sens de variation.

- /enc-36 Attention ! La fonction identité x /mapstochar-→ x est croissante sur /Rbbb , mais quand on la multiplie par elle-même, le résultat x /mapstochar-→ x 2 n'est pas une fonction croissante sur /Rbbb . Comme quoi la positivité compte!

## Démonstration

- (i) Dans le cas où f et g sont croissantes, soient x , y ∈ E . Si x &lt; y , alors par hypothèse f ( x ) /lessorequalslant f ( y ) et g ( x ) /lessorequalslant g ( y ) , donc f ( x ) + g ( x ) /lessorequalslant f ( y ) + g ( y ) par somme.
- (ii) Dans le cas où f et g sont décroissantes, soient x , y ∈ E . Si x &lt; y , alors par hypothèse 0 /lessorequalslant f ( y ) /lessorequalslant f ( x ) et 0 /lessorequalslant g ( y ) /lessorequalslant g ( x ) , donc f ( y ) g ( y ) /lessorequalslant f ( x ) g ( x ) par produit d'inégalités POSITIVES .
- (iii) Dans le cas où f est croissante et g décroissante, soient x , y ∈ E . Si x &lt; y , alors f ( x ) /lessorequalslant f ( y ) par croissance de f , puis g ( f ( y )) /lessorequalslant g ( f ( x )) par décroissance de g .
- (iv) Dans le cas croissant : ∀ x , y ∈ E , x &lt; y = ⇒ f ( x ) /lessorequalslant f ( y ) , f est en fait strictement croissante, car si f ( x ) = f ( y ) , alors x = y par injectivité. Montrons que f -1 est strictement croissante. Soient y , y ′ ∈ F deux réels pour lesquels y &lt; y ′ . Si jamais f -1 ( y ) /greaterorequalslant f -1 ( y ′ ) , alors y = f ( f -1 ( y )) /greaterorequalslant f ( f -1 ( y ′ )) = y ′ par croissance de f -contradiction.

Exemple Pas besoin de dériver pour expliquer que les fonctions x /mapstochar-→ e x + x et x /mapstochar-→ e e x sont croissantes sur /Rbbb !

## 1.2 MAJORANTS / MINORANTS, MAXIMUM / MINIMUM

Définition (Fonction majorée / minorée / bornée) Soit f : E -→ /Rbbb une fonction.

- On dit que f est majorée si : ∃ M ∈ /Rbbb , ∀ x ∈ E , f ( x ) /lessorequalslant M . Un tel réel M est appelé UN majorant de f . On dit ausi que f est majorée par M ou que M majore f

.

- On dit que f est minorée si : ∃ m ∈ /Rbbb , ∀ x ∈ E , f ( x ) /greaterorequalslant m . Un tel réel m est appelé UN minorant de f . On dit aussi que f est minorée par m ou que m minore f

.

- On dit que f est bornée si f est à la fois majorée et minorée, i.e. si : ∃ K /greaterorequalslant 0, ∀ x ∈ E , | f ( x ) | /lessorequalslant K .

Fonction majorée non minorée

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000000_acfebc9116f60805611c1ad7308af5a080d6de1822c2e053b66445e5628ad2ad.png)

Fonction minorée non majorée

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000001_3680b9991c4217abdeaec9932bd26ce12ee543cd2f070456abf41ec58bd2e135.png)

Fonction bornée

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000002_ce3b75384b30db82afd28d0c4703d55d1508640e84a73266f415f17c313f5ad0.png)

Démonstration La proposition « f est majorée et minorée » s'écrit : ∃ m , M ∈ /Rbbb , ∀ x ∈ E , m /lessorequalslant f ( x ) /lessorequalslant M et nous voulons montrer qu'elle est équivalente à la proposition : ∃ K /greaterorequalslant 0, ∀ x ∈ E , | f ( x ) | /lessorequalslant K .

- Si pour un certain K /greaterorequalslant 0, il est vrai que | f ( x ) | /lessorequalslant K pour tout x ∈ E , alors -K /lessorequalslant f ( x ) /lessorequalslant K pour tout x ∈ E , donc f est minorée par -K et majorée par K .
- Pour la réciproque, supposons f minorée par m et majorée par M et posons K = max { | m | , | M | } . Pour tout x ∈ E : -K /lessorequalslant -| m | /lessorequalslant m /lessorequalslant f ( x ) /lessorequalslant M /lessorequalslant | M | /lessorequalslant K , donc | f ( x ) | /lessorequalslant K .

Définition (Maximum / minimum d'une fonction) Soient f : E -→ /Rbbb une fonction et a ∈ E .

- On dit que f possède un maximum en a si : ∀ x ∈ E , f ( x ) /lessorequalslant f ( a ) . Le réel f ( a ) est alors appelé le maximum de f et noté max E f ou max x ∈ E f ( x ) .
- On dit que f possède un minimum en a si : ∀ x ∈ E , f ( x ) /greaterorequalslant f ( a ) . Le réel f ( a ) est alors appelé le minimum de f et noté min E f ou min x ∈ E f ( x ) .

En résumé, un maximum est un majorant de la forme « f de quelqu'un », i.e. un majorant qui est aussi une valeur de f .

- /enc-36 Attention ! Une fonction peut ne pas avoir de maximum ou de minimum, même en étant bornée, et quand elle en a un, il peut être atteint plusieurs fois.

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000003_009464434c51fed5011a92c8bdd3019e482cc6461781ff483d806591546710a8.png)

/Bullet

## 1.3 TRANSFORMATIONS AFFINES DU GRAPHE D'UNE FONCTION

Dans le théorème qui suit, les fonctions sont représentés graphiquement dans un repère orthonormal ( O , # ' ı , # '  ) .

Théorème (Transformations affines du graphe d'une fonction) Soient f : E -→ /Rbbb une fonction, a , b ∈ /Rbbb et λ &gt; 0. On munit le plan d'un repère orthonormal direct ( O , # ' ı , # '  ) .

- Symétries :

Le graphe de la fonction x /mapstochar-→ f ( x ) s'obtient à partir de celui de f par une symétrie par rapport à ( Ox ) .

Le graphe de la fonction x /mapstochar-→ f ( -x ) s'obtient à partir de celui de f par une symétrie par rapport à ( Oy ) .

- Translations :

Le graphe de la fonction x /mapstochar-→ f ( x ) + a s'obtient à partir de celui de f par une translation de vecteur a # '  .

Le graphe de la fonction x /mapstochar-→ f ( x + a ) s'obtient à partir de celui de f par une translation de vecteur -a # ' ı .

- Contractions / dilatations :

Le graphe de la fonction x /mapstochar-→ λ f ( x ) s'obtient à partir de celui de f par une dilatation verticale de rapport λ si λ /greaterorequalslant 1 et une contraction verticale de rapport 1 λ si λ &lt; 1.

Le graphe de la fonction x /mapstochar-→ f ( λ x ) s'obtient à partir de celui de f par une contraction horizontale de rapport λ si λ /greaterorequalslant 1 et une dilatation horizontale de rapport 1 λ si λ &lt; 1.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000004_6bdd3b4a95fa4a1e44b63ec12f248e2d0fbef40fb5fad9e297c8294e3ce57634.png)

- /enc-36 Attention ! Dans le cas de la fonction x /mapstochar-→ f ( x + a ) , il y a un signe -dans l'expression du vecteur de translation -a # ' ı et c'est normal. La fonction x /mapstochar-→ f ( x + a ) atteint la valeur f ( 0 ) en -a , puis la valeur f ( 1 ) en -a + 1, etc. En résumé, on peut dire que x /mapstochar-→ f ( x + a ) est EN AVANCE de a sur x /mapstochar-→ f ( x ) .

/Bullet

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000005_552533e33d857ffc735404d95116e093a6b421d6b332ae87e58738f7fc91710b.png)

Exemple Pour tous a , x ∈ /Rbbb , les réels x et a -x sont symétriques l'un de l'autre par rapport

<!-- formula-not-decoded -->

Donnons-nous à présent une fonction f : E -→ /Rbbb et a , b ∈ /Rbbb . Comment peut-on représenter les fonctions x /mapstochar-→ a -f ( x ) et x /mapstochar-→ f ( a -x ) quand on connaît le graphe de f ? Le graphe de la fonction x /mapstochar-→ a -f ( x ) s'obtient à partir de celui de f par une symétrie par rapport à la droite d'équation y = a 2 . Le graphe de la fonction x /mapstochar-→ f ( a -x ) s'obtient quant à lui à partir de celui de f par une symétrie par rapport à la droite d'équation x = a 2 .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000006_ecdd969c71ab05f81d26bd2eef1dabf07716db00edd35f5505f6107eeda2bc03.png)

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000007_991d79789621cd189c65620b47e1041ea27da10ebf6d3137c4d64f941d2a6ae7.png)

Définition (Fonction paire / impaire) On suppose E symétrique par rapport à 0, i.e. que : x E , x E .

Soit f : E -→ /Rbbb

- ∀ ∈ -∈ une fonction.
- Parité : On dit que f est paire si : ∀ x ∈ E , f ( -x ) = f ( x ) . Le graphe de f est alors symétrique par rapport à l'axe des ordonnées.
- Imparité : On dit que f est impaire si : ∀ x ∈ E , f ( -x ) = -f ( x ) . Le graphe de f est alors symétrique par rapport à l'origine.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000008_643aa726d9b06acf6ca0ac362311d1f8d81e5c2a2afdb836a45dc3b3f889d638.png)

2

/Bullet

Le graphe d'une fonction impaire définie en 0 passe toujours par l'origine.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000009_e4347184e61c0dee97c2f6f42b859e5311cd6f67d07a8796dfd353d8214f1cf8.png)

Pas besoin d'étudier une fonction f : E -→ /Rbbb paire ou impaire sur E tout entier, une étude sur E ∩ /Rbbb + suffit.

- Théorème (Réciproque d'une fonction bijective impaire) Soit f : E -→ F une fonction bijective de E sur F . Si E est symétrique par rapport à 0 et si f est impaire, F est symétrique par rapport à 0 et f -1 est impaire.

Démonstration Soit y ∈ F , disons y = f ( x ) pour un certain x ∈ E . Aussitôt, -x ∈ E car E est symétrique par rapport à 0, donc -y = -f ( x ) = f ( -x ) ∈ F par imparité de f . Conclusion : F est symétrique par rapport à 0. Ensuite : f -1 ( -y ) = f -1 ( -f ( x )) = f -1 ( f ( -x )) = -x = -f -1 ( y ) , donc f -1 est impaire.

## Définition (Fonction périodique) Soit T &gt; 0.

On suppose que E est T-périodique

, i.e. que : ∀ x ∈ E , x + T ∈ E et x -T ∈ E .

Soit f : E -→ /Rbbb une fonction. On dit que f est T-périodique ou périodique de période T si : ∀ x ∈ E , f ( x + T ) = f ( x ) . Le réel T est alors appelé UNE période de f .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000010_663af9256b635d7c3976ce18df1c74568a5e954120ebcd7985328c80cedcc543.png)

Pas besoin d'étudier une fonction f : E -→ /Rbbb T -périodique sur E tout entier, une étude sur une période suffit, par exemple E ∩ [ 0, T [ .

- /enc-36 Attention ! Une fonction périodique ne possède jamais qu'une seule période. Tout multiple entier d'une période T est encore une période : 2 T , 3 T , 4 T . . . Voilà pourquoi on ne parle jamais de « la » période, mais toujours d' UNE période.

Certaines fonctions possèdent en revanche une plus petite période , mais pas toutes. On peut montrer que toute fonction continue non constante périodique possède une plus petite période. Les fonctions sinus et cosinus admettent par exemple 2 π pour plus petite période. Certaines fonctions admettent au contraire tout réel strictement positif pour période et n'en ont donc pas de plus petite. C'est le cas des fonctions constantes et de la fonction /Qbbb .

/BD

Théorème (Opérations sur les fonctions périodiques) Soit T &gt; 0. On suppose que E est T -périodique. Soient f : E -→ /Rbbb et g : E -→ /Rbbb deux fonctions T -périodiques.

- (ii) Pour tout ω&gt; 0, la fonction x /mapstochar-→ f ( ω x ) est T ω -périodique sur l'ensemble dilaté / contracté 1 ω E .
- (i) Les fonctions f + g et f × g sont aussi T -périodiques, ainsi que f g si g ne s'annule pas.

Par exemple, pour ω = 2, le graphe de la fonction x /mapstochar-→ f ( 2 x ) s'obtient à partir de celui de f par une contraction horizontale de facteur 2. Si f est T -périodique, rien d'étonnant du coup à ce que x /mapstochar-→ f ( 2 x ) soit T 2 -périodique.

## Démonstration

- (i) Concernant f + g , pour tout x ∈ E : ( f + g )( x + T ) = f ( x + T ) + g ( x + T ) = f ( x ) + g ( x ) = ( f + g )( x ) .

<!-- formula-not-decoded -->

- (ii) Notons g la fonction x /mapstochar-→ f ( ω x ) définie sur /braceleftbig2 x ∈ /Rbbb | ω x ∈ E /bracerightbig2 = 1 ω E . Pour tout x ∈ 1 ω E :

## 2 CONTINUITÉ, DÉRIVABILITÉ, CONVEXITÉ / CONCAVITÉ

Les grands théorèmes d'analyse de cette partie seront démontrés plus tard dans l'année aux chapitres « Limites et continuité », « Dérivabilité et convexité » et « Intégration sur un segment ».

## 2.1 CONTINUITÉ

## Définition (Fonction continue) Soit f : E -→ /Rbbb une fonction.

Pour tout a ∈ E , on dit que f est continue en a si f ( x ) --- → x → a f ( a ) .

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000011_3d648dba0bd202ec16b363e44a5b4c5440a8e4fecd2f32c76ed229bdcedfdeaf.png)

/Bullet

On dit que f est continue sur E si f est continue en tout point de E . L'ensemble des fonctions continues sur E est noté /Ccal ( E , /Rbbb ) .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000012_eb94c19bcb3f9a581a103eca5683b0ee2bb5ba0289a7d3496fbc4a0680386436.png)

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000013_a2cbd01806aa948ded29f7a3341fd70284729ec1bcb81d416b8d818b94a41806.png)

## Théorème (Opérations sur les fonctions continues)

- Combinaison linéaire, produit, quotient : Pour toutes fonctions f , g ∈ /Ccal ( E , /Rbbb ) et λ , µ ∈ /Rbbb , les fonctions λ f + µ g et f g sont continues sur E , ainsi que f g si g ne s'annule pas.
- Composition : Pour toutes fonctions f ∈ /Ccal ( E , /Rbbb ) et g ∈ /Ccal ( F , /Rbbb ) , si f ( E ) ⊂ F , alors g ◦ f est continue sur E .
- Réciproque : Soient I et J deux intervalles. Pour toute fonction f ∈ /Ccal ( I , /Rbbb ) bijective de I sur J , f -1 est continue sur J .
- /enc-36 Attention ! La composition est plus délicate à manier que l'addition et le produit car elle jongle avec plusieurs ensembles de définition. Ainsi, on ne peut pas dire que « la fonction x /mapstochar-→ /radicallow x 2 + 1 est continue sur /Rbbb comme composée de fonctions qui le sont » car /radicallow · n'est pas continue sur /Rbbb tout entier. Que dire alors ? Par exemple ceci : « La fonction x /mapstochar-→ x 2 + 1 est continue sur /Rbbb À VALEURS DANS /Rbbb + et /radicallow · est continue sur /Rbbb + , donc la fonction x /mapstochar-→ /radicallow x 2 + 1 est continue sur /Rbbb . »

## Théorème (Théorème des valeurs intermédiaires ou TVI)

Soient a et b deux réels pour lesquels a &lt; b et f ∈ /Ccal /parenleftbig1 [ a , b ] , /Rbbb /parenrightbig1 .

Tout réel y compris entre f ( a ) et f ( b ) possède au moins un antécédent par f dans [ a , b ] , éventuellement plusieurs.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000014_510c9c9638bf56a77a8dc86808cc0a9703f84ab9ea3ecb10ef70506949909846.png)

/Bullet

/Circle

/Bullet

/Bullet

/Bullet

/Circle

/Bullet

/Bullet

/Bullet

/Bullet

Le TVI est un théorème d' EXISTENCE - existence d'antécédent, existence de solutions pour les équations y = f ( x ) d'inconnue x avec y fixé.

Le TVI gagne cela dit à être énoncé autrement. Sans rentrer dans les détails, un intervalle n'est jamais qu'une partie sans trou de /Rbbb , i.e. une partie qui, quand elle contient deux réels, contient tous les réels intermédiaires. Question : si f est continue sur un intervalle I , son image f ( I ) peut-elle contenir un trou? Un trou dans f ( I ) serait le signe qu'un certain réel y compris entre f ( a ) et f ( b ) avec a , b ∈ I n'aurait pas d'antécédent par f , mais c'est exactement cela que le TVI interdit. Conclusion : f ( I ) est forcément un intervalle quand I en est un, du moins si f est continue.

## Théorème (Image d'un intervalle par une fonction continue)

- Version image d'un intervalle du TVI : Pour toute fonction f ∈ /Ccal ( E , /Rbbb ) et tout intervalle I inclus dans E , f ( I ) est aussi un intervalle.
- En cas de monotonie, cet énoncé peut être rendu plus précis. Soient a , b ∈ /Rbbb deux réels pour lesquels a &lt; b .
- Si f est continue et décroissante sur [ a , b ] , alors f /parenleftbig1 [ a , b ] /parenrightbig1 =[ f ( b ) , f ( a )] .
- Si f est continue et croissante sur [ a , b ] , alors f /parenleftbig1 [ a , b ] /parenrightbig1 = [ f ( a ) , f ( b )] .

## /enc-36 Attention !

Par exemple, si f est continue et croissante sur ] a , b [ avec f ( x ) - - - - → x → a + α et f ( x ) - - - - → x → b -β , f /parenleftbig1 ] a , b [ /parenrightbig1 peut être a priori n'importe lequel des intervalles ] α , β [ , [ α , β [ , ] α , β ] ou [ α , β ] comme on le voit ci-dessous.

<!-- formula-not-decoded -->

/Bullet

/Circle

/Bullet

/Circle

/Bullet

/Circle

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000015_ce8e3eb67db16e89fcc9273e856fdb2077be50354ba9282f30628e7d4ba04ce6.png)

/Bullet

/Circle

/Bullet

/Circle

/Bullet

/Circle

/Bullet

/Circle

Par ailleurs, si f n'est pas continue, l'image f /parenleftbig1 [ a , b ] /parenrightbig1 n'a aucune raison d'être un intervalle, elle peut avoir des trous et posséder plusieurs morceaux. Enfin, même quand f /parenleftbig1 [ a , b ] /parenrightbig1 est un intervalle, cet intervalle n'a aucune raison d'avoir f ( a ) et f ( b ) pour bornes si f n'est pas monotone.

/Bullet

/Circle

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000016_048dbfa0f2290650e8d30753a43aff4badc9fbb82519b15a075c247e4d011084.png)

b

b

En cas de CONTINUITÉ et STRICTE MONOTONIE , les égalités qui posaient problème à l'instant deviennent toutes vraies et le très important TVI strictement monotone va même plus loin en termes de bijectivité.

## Théorème (TVI strictement monotone) Soient a , b ∈ /Rbbb deux réels pour lesquels a &lt; b .

- En cas de continuité et monotonie stricte, la forme des intervalles est correctement préservée. Par exemple :
- si f est continue et strictement décroissante sur ] a , b [ , alors f /parenleftbig1 ] a , b [ /parenrightbig1 = /bracketrightbig1 lim b -f , lim a + f /bracketleftbig1 .
- si f est continue et strictement croissante sur [ a , b [ , alors f /parenleftbig1 [ a , b [ /parenrightbig1 = /bracketleftbig1 f ( a ) , lim b -f /bracketleftbig1 ,
- TVI strictement monotone : Par exemple :
- si f est continue et strictement croissante sur [ a , b ] , f est bijective de [ a , b ] sur [ f ( a ) , f ( b )] ,
- si f est continue et strictement décroissante sur [ a , b [ , f est bijective de [ a , b [ sur /bracketrightbig1 lim b -f , f ( a ) /bracketrightbig1 , - si f est continue et strictement croissante sur ] a , b [ , f est bijective de ] a , b [ sur /bracketrightbig1 lim a + f , lim b -f /bracketleftbig1 .

Par rapport au TVI de base, la stricte monotonie apporte l'injectivité, donc l'unicité dès lors qu'on s'intéresse aux équations y = f ( x ) d'inconnue x avec y fixé.

/Bullet

/Circle

/Bullet

/Circle

/Bullet

/Bullet

/Bullet

/Circle

/Bullet

/Bullet

À défaut de pouvoir démontrer le TVI et son corollaire strictement monotone maintenant, nous pouvons en comprendre dès maintenant les tenants et les aboutissants.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000017_22990ffe27eff85a20cd8753bf83a118d5f51e3dd69eeba6b30752e34bbeaafe.png)

En pratique, le TVI et sa version strictement monotone sont très utiles quand on cherche des points fixes.

<!-- formula-not-decoded -->

Exemple La fonction x /mapstochar-→ e -x possède un et un seul point fixe sur /Rbbb .

Démonstration La fonction x f /mapstochar-→ e -x -x est continue et strictement décroissante sur /Rbbb par somme des fonctions x /mapstochar-→ e -x et x /mapstochar-→ x qui le sont. Par ailleurs, f ( x ) - - - - - → x → + ∞ -∞ et f ( x ) - - - - - → x →-∞ + ∞ , donc f s'annule une et une seule fois sur /Rbbb d'après le TVI strictement monotone.

## 2.2 DÉRIVABILITÉ ET DÉRIVÉES SUCCESSIVES

Définition (Fonction dérivable, tangente) Soit f : E -→ /Rbbb une fonction.

- Dérivabilité : Pour tout a ∈ E , on dit que f est dérivable en a si la fonction x /mapstochar-→ f ( x ) -f ( a ) x -a possède une limite finie en a , notée f ′ ( a ) le cas échéant et appelée le nombre dérivé de f en a .

On dit que f est dérivable sur E si f est dérivable en tout point de E . Le cas échéant, la fonction x /mapstochar-→ f ′ ( x ) est appelée la dérivée de f . L'ensemble des fonctions dérivables sur E est noté /Dcal ( E , /Rbbb ) .

- Tangente : Pour tout a ∈ E en lequel f est dérivable en a , la droite d'équation y = f ( a ) + f ′ ( a ) ( x -a ) est appelée la tangente de f en a .
- Si f est dérivable en a et si x est proche de a , alors f ( x ) -f ( a ) x -a ≈ f ′ ( a ) , donc f ( x ) ≈ f ( a ) + f ′ ( a ) ( x -a ) . À défaut d'être rigoureux, c'est convaincant. La tangente de f en a est ainsi la droite la plus proche du graphe de f au voisinage de a .

Géométriquement, f ( x ) -f ( a ) x -a est le coefficient directeur de la corde reliant les points de coordonnées ( a , f ( a )) et ( x , f ( x )) . Après passage à la limite, le réel f ′ ( a ) = lim x → a f ( x ) -f ( a ) x -a est donc la « pente limite » des cordes en question.

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000018_5af8a2ad040c00188b7534adc26b3aabb0ad6195f8c6a921f959275d8d81071c.png)

## /enc-36 Attention !

/Bullet

La notation

(

f

(

x

))

′

est

INTERDITE

!

La quantité f ( x ) dépend de x , c'est une EXPRESSION et non pas une FONCTION . Pour la dériver, on a besoin de préciser par rapport à quelle variable on dérive. Notez désormais simplement d d x ( f ( x )) ce que vous auriez aimé noter ( f ( x )) ′ .

Théorème (Dérivable implique continue) Soient f : E -→ /Rbbb une fonction et a ∈ E . Si f est dérivable en a , alors f est continue en a .

/Bullet

- /enc-36 Attention ! La réciproque est fausse! Les fonctions valeur absolue et racine carrée sont continues en 0, mais n'y sont pas dérivables. Le graphe de | · | présente un pic en 0 et celui de /radicallow · une tangente verticale.

Démonstration Si f est dérivable en a :

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000019_bb65be6cd33c8de0aa1f56b676e5ed00287d5e117e0017ac0ab41cc7bb445f4f.png)

<!-- formula-not-decoded -->

Définition (Dérivées successives) Soit f : E -→ /Rbbb une fonction. On pose f ( 0 ) = f .

Ensuite, pour tout k ∈ /Nbbb ∗ , si on a réussi à définir f ( k -1 ) de proche en proche et si elle est dérivable sur E , on dit que f est k fois dérivable sur E et on pose f ( k ) = /parenleftbig1 f ( k -1 ) /parenrightbig1 ′ . La fonction f ( k ) est alors appelée la dérivée k ème de f .

On préfère généralement les notations f , f ′ , f ′′ et f ′′′ aux notations f ( 0 ) , f ( 1 ) , f ( 2 ) et f ( 3 ) .

- /enc-36 Attention ! La notation ( f ( x )) ′′ est INTERDITE !

<!-- formula-not-decoded -->

Exemple Soit n ∈ /Nbbb . La fonction x f /mapstochar-→ x n est indéfiniment dérivable sur /Rbbb et pour tous k ∈ /Nbbb et x ∈ /Rbbb :

<!-- formula-not-decoded -->

## Définition (Fonction de classe /Ccal k ) Soit f : E -→ /Rbbb une fonction.

- Classe /Ccal k : Pour tout k ∈ /Nbbb , on dit que f est de classe /Ccal k sur E si f est k fois dérivable sur E et si f ( k ) est continue sur E . L'ensemble des fonctions de classe /Ccal k sur E est noté /Ccal k ( E , /Rbbb ) .
- Classe /Ccal ∞ : On dit que f est de classe /Ccal ∞ sur E si f est k fois dérivable sur E pour tout k ∈ /Nbbb . L'ensemble des fonctions de classe /Ccal ∞ sur E est noté /Ccal ∞ ( E , /Rbbb ) .

## /enc-36 Attention !

De classe /Ccal 1 = Dérivable à dérivée continue = Dérivable ET continue.

Sur la figure ci-dessous, chaque flèche décrit une implication.

Maladroit, donc à éviter, car la dérivabilité implique la continuité!

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000020_1f7f3dfcf6075fac5f79519460d37ddeb29f8d9e9f709dbbd23643993163731b.png)

Théorème (Opérations sur les fonctions dérivables / k fois dérivables / de classe /Ccal k )

- Combinaison linéaire, produit, quotient : Pour toutes fonctions f , g ∈ /Dcal ( E , /Rbbb ) et λ , µ ∈ /Rbbb , les fonctions λ f + µ g et f g sont dérivables sur E , ainsi que f g si g ne s'annule pas. En outre :
- Composition : Pour toutes fonctions f ∈ /Dcal ( E , /Rbbb ) et g ∈ /Dcal ( F , /Rbbb ) , si f ( E ) ⊂ F , alors g ◦ f est dérivable sur E et : ( g f ) ′ = f ′ g ′ f .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

On peut remplacer partout « dérivable » par « k fois dérivable » pour tout k ∈ /Nbbb ou par « de classe /Ccal k » pour tout k ∈ /Nbbb ∪ { ∞ } , mais les formules énoncées ne sont valables que pour les dérivées premières.

- Réciproque : Soient I et J deux intervalles. Pour toute fonction f ∈ /Dcal ( I , /Rbbb ) bijective de I sur J , SI f ′ NE S'ANNULE PAS SUR I , alors f -1 est dérivable sur J et ( f -1 ) ′ = 1 f ′ ◦ f -1 .

Démonstration La dérivabilité de f -1 demande du travail, mais la formule de dérivation en découle aisément. En dérivant simplement la relation f ◦ f -1 = Id J , on obtient ( f -1 ) ′ × f ′ ◦ f -1 = 1.

/negationslash

/Bullet

/radicallow

## /enc-36 Attention !

- Pour la dérivabilité de f -1 , l'hypothèse de non-annulation de f ′ est cruciale ! Sur la figure ci-contre, f ′ s'annule en a , donc f possède une tangente horizontale en a . Il en découle que f -1 possède une tangente verticale en f ( a ) , donc n'est pas dérivable en f ( a ) .
- On n'a pas besoin de dériver 99 fois une fonction pour savoir qu'elle est 100 fois dérivable! Par exemple, la fonction x /mapstochar-→ x 2 e x est de classe /Ccal ∞ sur /Rbbb pour la seule raison que les fonctions x /mapstochar-→ x 2 et x /mapstochar-→ e x le sont.

Exemple La fonction x f /mapstochar-→ ln /parenleftbig1 x + /radicalbig1 x ( 1 -x ) /parenrightbig1 est définie et continue sur ] 0,1 ] et dérivable sur ] 0,1 [ . Démonstration

- Ensemble de définition :

<!-- formula-not-decoded -->

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000021_cd89ccb56ee8fbc882a9af18508578b386b84dbf386a63c02f40aa4eddc4395b.png)

/Bullet

| x         | -∞   | 0 1 +   |
|-----------|------|---------|
| x         | -    | 0 +     |
| 1 - x     | +    | 0 -     |
| x ( 1 x ) | 0    | + 0     |

-

-

-

- Ensemble de continuité : Les fonctions usuelles utilisées pour construire f sont toutes continues en tout point en lequel elles sont définies, donc f est continue sur ] 0,1 ] .
- Ensemble de dérivabilité : La fonction racine carrée est dérivable seulement sur /Rbbb ∗ + . La fonction f est donc dérivable sur /braceleftbig2 x ∈ /Rbbb | x ( 1 -x ) &gt; 0 et x + /radicalbig1 x ( 1 -x ) &gt; 0 /bracerightbig2 =] 0,1 [ .

Attention, nous n'avons pas prouvé la non-dérivabilité de f en 1. Les résultats du théorème précédent nous parlent de dérivabilité mais pas de NON -dérivabilité. Pour étudier la dérivabilité de f en 1, il faudrait revenir à la définition en termes de taux d'accroissement, mais nous ne le ferons pas.

Exemple La fonction x f /mapstochar-→ 1 x -1 est de classe /Ccal ∞ sur /Rbbb /integerdivide { 1 } , et pour calculer ses dérivées successives, il vaut mieux l'écrire comme une PUISSANCE NÉGATIVE que comme un quotient. En l'occurrence, pour tous k ∈ /Nbbb et x ∈ /Rbbb /integerdivide { 1 } :

<!-- formula-not-decoded -->

Théorème (Caractérisation des fonctions dérivables constantes / monotones) Soient I un INTERVALLE et f ∈ /Dcal ( I , /Rbbb ) . On ne traite ci-dessous que le cas des fonctions croissantes.

- Constance : f est constante sur I si et seulement si f ′ est nulle sur I .
- Monotonie : f est croissante sur I si et seulement si f ′ est positive (ou nulle) sur I .
- Monotonie stricte : f est strictement croissante sur I si et seulement si f ′ est positive (ou nulle) sur I et n'est identiquement nulle sur aucun intervalle [ a , b ] inclus dans I avec a &lt; b .

En particulier, si f ′ est strictement positive sur I , f est strictement croissante sur I .

- /enc-36 Attention ! Mine de rien, il est indispensable que I soit un intervalle.

f est constante sur I 1 et sur I 2 , donc f ′ = 0 sur I 1 et sur I 2 , mais f n'est pas constante sur I 1 ∪ I 2 .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000022_0a3274fb1a136aecc483f94981c9a59de93f43eeda069c5dd43e20073eba73be.png)

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000023_23550479a93624d235e9959c2188912d2b3ef591a3fd897d61ffa6aa6157e201.png)

f est croissante sur I 1 et sur I 2 , donc f ′ /greaterorequalslant 0 sur I 1 et sur I 2 , mais f n'est pas croissante sur I 1 ∪ I 2 .

On montre beaucoup d'inégalités en mathématiques, et l'une des premières techniques qu'on apprend à ce sujet, c'est l'étude des variations ou du signe d'une fonction, dont voici plusieurs exemples.

À ce stade, c'est pour leur signe qu'on calcule des dérivées, donc... FACTORISEZ VOS DÉRIVÉES LE PLUS POSSIBLE !

Exemple Pour tout x ∈ [ 0,2 ] :

<!-- formula-not-decoded -->

Par ailleurs, pour tout x ∈ /Rbbb :

<!-- formula-not-decoded -->

/Bullet

/Bullet

/Bullet

/Bullet

/Bullet

/Bullet

/Bullet

## Démonstration

- Tentative naïve : Pour tout x ∈ [ 0,2 ] , 0 /lessorequalslant x 2 /lessorequalslant 4 donc 3 /lessorequalslant x 2 + 3 /lessorequalslant 7, et par ailleurs 1 /lessorequalslant x + 1 /lessorequalslant 3, donc par quotient : 1 7 /lessorequalslant x + 1 x 2 + 3 /lessorequalslant 3 3 = 1. Hélas, c'est moins fin que le résultat attendu. En encadrant séparément le numérateur et le dénominateur, on obtient rarement des encadrements de qualité.
- Étude d'une fonction : La fonction x f /mapstochar-→ x + 1 x 2 + 3 est définie et dérivable sur /Rbbb et pour tout x ∈ /Rbbb : On factorise!

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000024_16d3852e5b1f71cf69bb5f18ffea4b82cb534887814fac286da01c95de07fbe1.png)

Démonstration Onpourrait étudier la fonction x /mapstochar-→ x + 1 x -1 ln x et la comparer à 2, mais la dérivée d'un quotient occasionne souvent d'affreux calculs, donc étudions plutôt le signe de x f /mapstochar-→ ( x + 1 ) ln x -2 ( x -1 ) sur /Rbbb ∗ + . Nous diviserons par x -1 à la fin pour obtenir le signe de x /mapstochar-→ x + 1 x -1 ln x -2. Pour tout x &gt; 0 : f ′ ( x ) = ln x + 1 x -1 et f ′′ ( x ) = x -1 x 2 . On conclut grâce au tableau ci-contre.

<!-- formula-not-decoded -->

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000025_665ef56bb4f6328835d170d46c3527d3bd322d421086b4f89017f34e3a5ac809.png)

-

Démonstration Pour prouver une inégalité de deux variables, on en fixe une, par exemple y , et on fait une étude de fonction par rapport à l'autre variable, ici x . Fixons donc y ∈ ] -1,1 [ .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

On conclut grâce au tableau ci-contre.

## 2.3 CONVEXITÉ / CONCAVITÉ

Soient I un intervalle I , f : I -→ /Rbbb une fonction et x , y ∈ /Rbbb . Quand λ décrit [ 0,1 ] , λ ( y -x ) décrit le segment d'extrémités 0 et y -x , donc ( 1 -λ ) x + λ y = x + λ ( y -x ) décrit le segment d'extrémités x + 0 = x et x +( y -x ) = y .

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000026_3048ce78764ea7352976a7027de50cc89dab25142a32769b36ab1124cbd9f865.png)

-

Définition (Fonction convexe / concave) Soient I un intervalle et f : I -→ /Rbbb une fonction.

- Fonction convexe : On dit que f est convexe

si son graphe est situé en-dessous de toutes ses cordes, i.e. si :

$$∀ x , y ∈ I , ∀ λ ∈ [ 0,1 ] , f (( 1 - λ ) x + λ y ) /lessorequalslant ( 1 - λ ) f ( x ) + λ f ( y ) .$$

- Fonction concave : On dit que f est concave si son graphe est situé au-dessus de toutes ses cordes, i.e. si : ∀ x , y ∈ I , ∀ λ ∈ [ 0,1 ] , f (( 1 - λ ) x + λ y ) /greaterorequalslant ( 1 - λ ) f ( x ) + λ f ( y ) .

Il est équivalent de dire que -f est convexe.

Fonction convexe, perpétuel virage à gauche

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000027_2d25761520685fe1b0cbe0dba79f888aa24d647750ac7a8e08154f8eb9234de7.png)

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000028_7cca66d00d1ecad343debc10f53dda32abb38533ae8c628b16101b7c66090769.png)

-

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000029_8425e6e3d5d3a2a569ee57bd26a41d37a86562d3cee20fb43a60443b36a54be0.png)

De la même manière, quand λ décrit [ 0,1 ] , ( 1 -λ ) f ( x )+ λ f ( y ) décrit le segment d'extrémités f ( x ) et f ( y ) , et dans le plan, le point de coordonnées /parenleftbig1 ( 1 -λ ) x + λ y , ( 1 -λ ) f ( x ) + λ f ( y ) /parenrightbig1 décrit le segment d'extrémités ( x , f ( x )) et ( y , f ( y )) , appelé une corde de f .

/Bullet

/Bullet

/Bullet

/Bullet

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000030_d217cbf743d42ec3ecd8dca69b56ca14dbfd056dc6c442059c35738bfd2e30d1.png)

Fonction concave, perpétuel virage à droite

Exemple La fonction valeur absolue est convexe sur /Rbbb car pour tous x , y ∈ /Rbbb et λ ∈ [ 0,1 ] , d'après l'inégalité triangulaire :

<!-- formula-not-decoded -->

Théorème (Caractérisation des fonctions convexes dérivables) Soient I un intervalle et f ∈ /Dcal ( I , /Rbbb ) . Les assertions suivantes sont équivalentes :

- (i) f est convexe sur I .
- (ii) f ′ est croissante sur I -ou bien f ′′ /greaterorequalslant 0 si f est deux fois dérivable sur I .
- (iii) Le graphe de f est situé au-dessus de toutes ses tangentes.

On dispose bien sûr d'une caractérisation analogue de la concavité.

Démonstration (Implication (ii) = ⇒ (iii)) Supposons f ′ croissante et fixons a ∈ I . Montrons que le graphe de f est situé au-dessus de sa tangente en a , i.e. que f ( x ) /greaterorequalslant f ′ ( a ) ( x -a ) + f ( a ) pour tout x ∈ I . Notons pour cela ϕ la fonction x /mapstochar-→ f ( x ) -f ′ ( a ) ( x -a ) -f ( a ) . Cette fonction est dérivable sur I et pour tout x ∈ I : ϕ ′ ( x ) = f ′ ( x ) -f ′ ( a ) , donc par croissance de f ′ , ϕ ′ est négative à gauche de a et positive à droite. Ainsi, ϕ est décroissante à gauche de a et croissante à droite, donc positive sur I tout entier puisque ϕ ( a ) = 0.

Exemple Soit n ∈ /Nbbb . La fonction puissance x /mapstochar-→ x 2 n est convexe sur /Rbbb car sa dérivée seconde x /mapstochar-→ 2 n ( 2 n -1 ) x 2 ( n -1 ) est positive sur /Rbbb . x + 1

Exemple

Pour tout x &gt; 0 :

Démonstration La fonction x /mapstochar-→ /radicallow x est concave sur /Rbbb ∗ + car sa dérivée x /mapstochar-→ 1 2 /radicallow x y est décroissante. Son graphe est situé sous sa tangente en 1, d'équation y = x + 1 2 .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000031_7cf53dd1a294bb8a733f2ba6afca47e5f149990148ac8c46f5293b693893dd2e.png)

/Bullet

Définition-théorème (Point d'inflexion) Soient I un intervalle, f : I -→ /Rbbb une fonction et a ∈ I un point qui n'est pas une borne de I . On dit que f possède un point d'inflexion en a si f est convexe au voisinage de a à gauche et concave au voisinage de a à droite - ou l'inverse.

Si f est deux fois dérivable sur I , f possède un point d'inflexion en a si et seulement si f ′′ s'annule en a et est positive au voisinage de a à gauche et négative au voisinage de a à droite - ou l'inverse.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000032_d456661c77ca15e77cb1c79c31efdcd8529b1abec5bdf4d7658bfba9e11ea4bd.png)

/Bullet

Exemple Soit n ∈ /Nbbb . La fonction puissance x /mapstochar-→ x 2 n + 1 possède un et un seul point d'inflexion, à savoir en 0, car sa dérivée seconde x /mapstochar-→ 2 n ( 2 n + 1 ) x 2 n -1 , s'annule en changeant de signe en 0 et ne le fait nulle part ailleurs.

Exemple Soient a ∈ /Rbbb ∗ et b , c , d ∈ /Rbbb . La fonction x /mapstochar-→ ax 3 + bx 2 + cx + d possède un et un seul point d'inflexion, à savoir en -b 3 a , car sa dérivée seconde x /mapstochar-→ 6 ax + 2 b s'annule en changeant de signe en -b 3 a et ne le fait nulle part ailleurs.

## 3 LOGARITHME, EXPONENTIELLE, PUISSANCES

## 3.1 FONCTIONS AFFINES, POLYNOMIALES ET RATIONNELLES

Théorème (La seule formule à connaître sur les fonctions affines) Le graphe d'une fonction affine f est une droite, donc coïncide avec sa tangente en tout point. Ainsi, pour tous a , x ∈ /Rbbb : f ( x ) = f ′ ( a ) ( x -a ) + f ( a ) .

- /enc-36 Attention ! On vous a habitués à utiliser l'ordonnée à l'origine p d'une fonction affine x f /mapstochar-→ mx + p , mais la plupart du temps, on se fiche royalement de ce qui se passe à l'origine. Si vous connaissez la pente m de f et sa valeur en un point a , f a pour expression x /mapstochar-→ m ( x -a ) + f ( a ) .

Exemple Quelle fonction affine f envoie 1 sur 3 et 2 sur 5 ? De pente f ( 2 ) -f ( 1 ) 2 -1 = 2, f a tout simplement pour expression x /mapstochar-→ 2 ( x -1 ) + 3 = 2 x + 1. Aucun calcul supplémentaire!

<!-- formula-not-decoded -->

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000033_1effe0c3c816263f835f1461426dfc9d45dc06b40934686b809147acfc99af77.png)

/Bullet

/Bullet

/Bullet

Concernant les fonctions puissances x /mapstochar-→ x n avec n ∈ /Zbbb , rappelons simplement l'allure de leurs graphes.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000034_fc98f1d40b22e162e7d0bf9836b526ba1b2566ede36b46f9881a84aa64997b8f.png)

Rappelons également qu'on appelle fonction rationnelle tout quotient d'une fonction polynomiale par une fonction polynomiale non nulle, par exemple x /mapstochar-→ x + 1 x 2 + 2 . En particulier, les fonctions polynomiales sont rationnelles. Enfin, pour calculer la limite en + ∞ ou -∞ d'une fonction polynomiale ou rationnelle, on factorise par le terme de plus haut degré au numérateur et au dénominateur, puis on simplifie. Par exemple :

## 3.2 FONCTIONS LOGARITHME ET EXPONENTIELLE

<!-- formula-not-decoded -->

## Définition-théorème (Fonction logarithme)

- Définition et régularité : La fonction logarithme ln est définie, de classe /Ccal ∞ et concave sur /Rbbb ∗ + . Pour tout x &gt; 0 : ln ′ ( x ) = 1 x et ln ( 1 ) = 0.
- Transformation des produits en sommes : Pour tous x , y &gt; 0 : ln ( x y ) = ln x + ln y et ln 1 x = -ln x .
- Constante de Néper : La fonction logarithme prend la valeur 1 en un unique réel e appelé parfois la constante de Néper : e ≈ 2,71828.
- Croissances comparées en 0 et + ∞ : x - - - - - → x → + ∞ 0 et x ln x --- → x → 0 0.
- Comportement au voisinage de 1 :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- Le graphe du logarithme est situé sous sa tangente en 1 : /braceleftbig5 ∀ x &gt; 0, ln x /lessorequalslant x -1 ∀ x &gt; -1, ln ( 1 + x ) /lessorequalslant x .

Par définition du nombre dérivé : ln x x -1 --- → x → 1 ln ′ ( 1 ) = 1, donc ln x ≈ x -1 pour x proche de 1. Par exemple, ln ( 1,1 ) ≈ 0,09531 et ln ( 1,01 ) ≈ 0,00995.

Les limites ln x x - - - - - → x → + ∞ 0 et x ln x --- → x → 0 0 sont quant à elles des formes indéterminées + ∞ + ∞ et 0 × (+ ∞ ) au premier abord, mais le combat de x et ln x est gagné par x dans les deux cas.

Démonstration D'après le théorème fondamental du calcul intégral que nous démontrerons plus tard, toute fonction continue sur un intervalle y possède des primitives. La fonction inverse possède donc des primitives sur /Rbbb ∗ + , mais plus précisément une et une seule primitive qui envoie 1 sur 0 et c'est elle que nous noterons ln.

- Variations et signe : La fonction ln est de classe /Ccal ∞ sur /Rbbb ∗ + car sa dérivée x /mapstochar-→ 1 x l'est, mais cette dérivée est aussi strictement positive, donc ln est strictement croissante sur /Rbbb ∗ + . Comme ln ( 1 ) = 0, ln est strictement négative sur ] 0,1 [ et strictement positive sur ] 1, + ∞ [ .
- Concavité et position par rapport à la tangente en 1 : Sa dérivée x /mapstochar-→ 1 x y étant décroissante, ln est concave sur /Rbbb ∗ + . Or sa tangente en 1 a pour équation y = ln ′ ( 1 ) ( x -1 ) + ln ( 1 ) = x -1, donc ln x /lessorequalslant x -1 pour tout x &gt; 0.
- Transformation des produits en sommes : Fixons y &gt; 0 et notons ϕ la fonction x /mapstochar-→ ln ( x y ) -ln x -ln y dérivable sur /Rbbb ∗ + . Pour tout x &gt; 0 : ϕ ′ ( x ) = y x y -1 x = 0, donc ϕ est constante de valeur ϕ ( 1 ) = 0, donc ln ( x y ) = ln x + ln y pour tout x &gt; 0. En particulier : ln x + ln 1 x = ln ( 1 ) = 0, donc ln 1 x = -ln x .
- Croissances comparées : Pour tout x /greaterorequalslant 1 : ln x = ln /parenleftbig1 /radicallow x /parenrightbig1 2 = 2ln /radicallow x /lessorequalslant 2 /parenleftbig1 /radicallow x -1 /parenrightbig1 /lessorequalslant 2 /radicallow x , donc : 0 /lessorequalslant ln x x /lessorequalslant 2 /radicallow x , et ainsi ln x x - - - - - → x → + ∞ 0 par encadrement.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000035_11a45497e279cf5f696d5e5095ac6ea49cc0d1f3d11bdf4563fdb4773f0b3108.png)

/Bullet

/Bullet

<!-- formula-not-decoded -->

- Limites en 0 et + ∞ : D'après le théorème de la limite monotone pour les fonctions que vous ne connaissez pas et que nous prouverons plus tard, toute fonction croissante sur /Rbbb ∗ + possède une limite en + ∞ , éventuellement + ∞ . La fonction ln possède donc une limite /lscript en + ∞ . Supposons par l'absurde que /lscript est un réel. Dans la relation ln ( x y ) = ln x + ln y , fixons x &gt; 0 et faisons tendre y vers + ∞ . Cela donne /lscript = ln x + /lscript , donc ln x = 0 pour tout x &gt; 0, mais cette égalité contredit la stricte croissance de ln, donc

<!-- formula-not-decoded -->

- Définition de la constante de Néper : La fonction ln est continue et strictement croissante sur /Rbbb ∗ + de limites -∞ et + ∞ aux bornes, donc bijective de /Rbbb ∗ + sur /Rbbb d'après le TVI strictement monotone. En particulier, 1 possède donc un et un seul antécédent par ln, noté e.

## Définition-théorème (Fonction exponentielle)

- Définition : La fonction logarithme est bijective de /Rbbb ∗ + sur /Rbbb . On appelle fonction exponentielle et on note exp sa réciproque, bijective de /Rbbb sur /Rbbb ∗ + . En particulier : exp ( 1 ) = e et les graphes des fonctions exp et ln sont symétriques l'un de l'autre par rapport à la droite d'équation y = x .

Pour tout x ∈ /Rbbb : ln ( exp ( x )) = x et pour tout x &gt; 0 : exp ( ln x ) = x .

- Régularité : La fonction exponentielle exp est de classe /Ccal ∞ et convexe sur /Rbbb et exp ′ = exp.
- Transformation des sommes en produits : Pour tous x , y ∈ /Rbbb : exp ( x + y ) = exp ( x ) exp ( y ) et exp ( -x ) = 1 exp ( x ) .
- Croissances comparées en + ∞ : x exp ( x ) - - - - - → x → + ∞ 0.
- Comportement au voisinage de 0 :

Le graphe de l'exponentielle est situé au-dessus sa tangente en 0 : x /Rbbb , exp ( x ) /greaterorequalslant 1 + x .

<!-- formula-not-decoded -->

∀ ∈ exp ( x ) -1 proche de 0.

Je me suis forcé à noter exp ( x ) plutôt que e x l'exponentielle de x , mais dans cinq minutes, nous pourrons la noter e x .

Par définition du nombre dérivé : exp ( x ) -1 x --- → x → 0 exp ′ ( 0 ) = 1, donc exp ( x ) -1 ≈ x pour x proche de 1. Par exemple, exp ( 0,1 ) ≈ 1,10517 et exp ( 0,01 ) ≈ 1,01005.

Démonstration Nous avons déjà tiré du TVI strictement monotone la bijectivité de ln de /Rbbb ∗ + sur /Rbbb . Cela justifie à la fois la définition de l'exponentielle et sa régularité. En effet, ln est de classe /Ccal ∞ sur /Rbbb ∗ + et SA DÉRIVÉE x /mapstochar-→ 1 x NE S'Y ANNULE PAS , donc d'après le théorème de dérivabilité d'une réciproque, ln -1 = exp est de classe /Ccal ∞ sur /Rbbb de dérivée exp ′ = ( ln -1 ) ′ = 1 ln ′ ◦ ln -1 = ln -1 = exp. En particulier, exp ′ est croissante sur /Rbbb , donc exp y est convexe, donc exp ( x ) /greaterorequalslant exp ′ ( 0 ) x + exp ( 0 ) = x + 1 pour tout x ∈ /Rbbb , autrement dit le graphe est au-dessus de la tangente en 0. Nous laisserons de côté les autres vérifications par souci de légèreté.

## 3.3 FONCTIONS PUISSANCES

Nous n'avons défini jusqu'ici que les puissances x n pour n ENTIER . La notation classique e x n'est-elle cependant pas celle d'une puissance, me direz-vous? Oui et non, car le réel e x n'est pas « e multiplié x fois par lui-même ». Que signifierait « e multiplié /radicallow 2 fois par lui-même »?! Voilà pourquoi, au paragraphe précédent, je me suis momentanément interdit la notation e x , mais nous pouvons maintenant généraliser proprement notre définition des puissances.

## Définition (Puissances quelconques et racines n èmes d'un réel strictement positif) Soit x &gt; 0.

- Puissances quelconques : Pour tout y ∈ /Rbbb , on appelle x puissance y le réel x y = exp ( y ln x ) .
- Racines n èmes : Pour tout n ∈ /Nbbb ∗ , le réel x 1 n est appelé la racine n ème de x et noté n /radicallow x .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000036_cc8bcde91baaedc49c8cc4e301be161dc975f13bac598e33834c92249f6e504f.png)

/Bullet

/Bullet

Pour x = e, cette définition signifie que e y = exp ( y lne ) = exp ( y ) pour tout y ∈ /Rbbb . Ouf, nous pouvons noter l'exponentielle comme une puissance!

En résumé, la notation puissance n'est qu'une notation. Pour y non entier, x y n'est pas le produit y fois de x . Quand vous manipulez une puissance quelconque, ayez toujours en tête qu'un logarithme et une exponentielle sont cachés derrière.

## /enc-36 Attention ! La définition

x

y

=

e

y

ln

x

n'est valable que pour x strictement positif à cause du logarithme.

Exemple Pour tout x &gt; 1 :

x = e × = e ln ln = ln x .

$$lnln x ln x lnln x ln x ln x x$$

## Théorème (Propriétés algébriques des puissances)

- (i) La nouvelle définition des puissances généralise bien l'ancienne.

<!-- formula-not-decoded -->

## Démonstration

n

termes

n

termes

n

termes

- (i) Pour tous x &gt; 0 et n ∈ /Nbbb : e n ln x = ︷ ︸︸ ︷ e ln x + . . . + ln x = ︷ ︸︸ ︷ e ln x × . . . × e ln x = ︷ ︸︸ ︷ x . . . x , donc la notation traditionnelle x n et notre nouvelle notation x n coïncident. Même chose dans le cas d'un entier négatif.

<!-- formula-not-decoded -->

## Théorème (Étude des fonctions puissances) Soient α , β ∈ /Rbbb .

- (i) Régularité : La fonction x /mapstochar-→ x α est définie et de classe /Ccal ∞ sur /Rbbb ∗ + de dérivée x /mapstochar-→ α x α -1 .

Elle est concave si α ∈ [ 0,1 ] et convexe sinon.

- (ii) Positions relatives : /braceleftbig5 Pour tout x ∈ ] 0,1 ] : α /lessorequalslant β = ⇒ x β /lessorequalslant x α . Pour tout x ∈ [ 1, + ∞ [ : α /lessorequalslant β = ⇒ x α /lessorequalslant x β .
- (iii) Prolongement par continuité en 0 : Pour α &gt; 0, on pose 0 α = 0. La fonction x /mapstochar-→ x α ainsi prolongée est continue sur /Rbbb + tout entier, y compris en 0. On dit qu'on a prolongé par continuité la fonction x /mapstochar-→ x α en 0.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000037_e5229dcbd6570fb39375b14a9146138ae8096053b003202dc60f9853561a6daf.png)

<!-- formula-not-decoded -->

- /enc-36 Attention ! Pour α ∈ ] 0,1 [ , la fonction x /mapstochar-→ x α est continue en 0 après prolongement, mais elle possède en 0 une tangente verticale, signe qu'elle n'est pas dérivable en 0. C'est typiquement ce qui arrive à la fonction racine carrée.

## Démonstration

- (i) Pour tout x &gt; 0 : d d x ( x α ) = d d x ( e α ln x ) = α x × e α ln x = α x -1 x α = α x α -1 . A fortiori : d 2 f d x 2 ( x α ) = α ( α -1 ) x α -2 , donc la dérivée seconde de x /mapstochar-→ x α est négative sur /Rbbb ∗ + si α ∈ [ 0,1 ] et positive si α ∈ ] -∞ , 0 ] ∪ [ 1, + ∞ [ .
- (ii) Soient x &gt; 0 et α , β ∈ /Rbbb avec α /lessorequalslant β .
- Si x ∈ ] 0,1 ] , alors ln x /lessorequalslant 0, donc β ln x /lessorequalslant α ln x , donc x β = e β ln x /lessorequalslant e α ln x = x α .
- Si x ∈ [ 1, + ∞ [ , alors ln x /greaterorequalslant 0, donc α ln x /lessorequalslant β ln x , donc x α = e α ln x /lessorequalslant e β ln x = x β .

<!-- formula-not-decoded -->

/Bullet

/Circle

/Bullet

/Bullet

Théorème (Croissances comparées des fonctions logarithme, exponentielle et puissances) Le principe général, c'est que l'exponentielle est plus puissante que les puissances, qui sont elles-mêmes plus puissantes que le logarithme.

Précisément, pour tous α &gt; 0 et β ∈ /Rbbb :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

et

x

|

ln

x

|

--- →

x

→

0

0.

Démonstration Montrons seulement la deuxième limite. Le résultat est clair si β /lessorequalslant 0, car sachant que α &gt; 0, lim x → + ∞ ( ln x ) β ∈ { 0,1 } et x α - - - - - → x → + ∞ + ∞ . Supposons désormais β &gt; 0. Le calcul qui suit a l'air affreux, mais on essaie juste de se ramener à la limite ln u u - - - - -→ u + 0. Pour tout x &gt; 0, si on pose u = x α β et v = ln u u :

Or ici x α β - - - - - → x → + ∞ + ∞ car α β &gt; 0. Également, ln u u - - - - -→ u → + ∞ 0 et v β --- → v → 0 0 car β &gt; 0, donc ( ln x ) β x α - - - - - → x → + ∞ 0 par composition.

α

<!-- formula-not-decoded -->

## 3.4 FONCTIONS HYPERBOLIQUES ch , sh ET th

## Définition-théorème (Fonctions cosinus hyperbolique et sinus hyperbolique)

Pour tout x ∈ /Rbbb , on appelle cosinus hyperbolique de x le réel ch x = e x + e -x 2 et sinus x x hyperbolique de x le réel sh x = e -e -2 .

Pour tout x ∈ /Rbbb :

ch 2 x -sh 2 x = 1.

Les fonctions ch et sh , respectivement paire et impaire, sont définies et de classe /Ccal ∞ sur /Rbbb avec : ch ′ = sh et sh ′ = ch.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000038_a5f3096bcfb4ddf1ab60340079b6dc1c72906468ce49270070ee65122e433124.png)

La fonction ch est convexe. La fonction sh est concave sur /Rbbb -et convexe sur /Rbbb + avec un point d'inflexion en 0.

Démonstration Les variations de ch et sh sont étudiées dans le tableau ci-dessous et pour tout x ∈ /Rbbb : ch 2 x -sh 2 x =( ch x + sh x )( ch x -sh x ) = e x e -x = 1.

Exemple L'équation ch x = 2 d'inconnue x ∈ /Rbbb possède deux solutions qu'on sait calculer explicitement.

Démonstration Les équations ch x = y et sh x = y d'inconnue x à y fixé se ramènent aisément à des équations du second degré. Pour tout x ∈ /Rbbb :

<!-- formula-not-decoded -->

## Définition-théorème (Fonction tangente hyperbolique)

La fonction tangente hyperbolique th = sh ch est définie sur /Rbbb .

Elle est impaire et de classe sur /Rbbb

/Ccal ∞ et : th ′ = 1 -th 2 = 1 ch 2 .

Elle est convexe sur /Rbbb -et concave sur /Rbbb + avec un point d'inflexion en 0.

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000039_896529c3b89737df80f6d80fbc55ef20072224d65c325f79191f67cceb1d1ff2.png)

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000040_5bb4a827ce1f984def3278548883b1c5283c99c43d37f79980a7fa223ac9c281.png)

-

Elle possède enfin une asymptote d'équation y = 1 au voisinage de + ∞ (resp. y = -1 au voisinage de -∞ ).

Démonstration La fonction th est de classe /Ccal ∞ par quotient et :

La stricte croissance en découle. En outre, par composition, la dérivée 1 ch 2 est croissante sur /Rbbb -et décroissante sur /Rbbb + , donc th est convexe sur /Rbbb -et concave sur /Rbbb + .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

β

## 4 DEUX OU TROIS GRANDS PRINCIPES DE CALCUL DES LIMITES

Un calcul de limite se mène toujours en deux temps :

- Dans un premier temps, on analyse l'expression étudiée en comparant de tête la taille des termes qui la composent. Qui est grand? Qui est petit ? Qui disparaît au profit de qui? Cette étape de défrichement doit être effectuée rapidement sans trop de rigueur formelle, par exemple au moyen du symbole ≈ , mais ATTENTION , ce symbole flou ne prouve jamais rien, il prépare juste le terrain du calcul rigoureux.
- Dans un deuxième temps, on traduit l'analyse précédente en calcul rigoureux. Les techniques de bases consistent à factoriser par le terme dominant et à exploiter les croissances comparées usuelles en ±∞ et certaines approximations de fonctions usuelles tirées de nombres dérivés. À ce sujet, le point important, c'est que si f est dérivable en a avec .

<!-- formula-not-decoded -->

/negationslash

Exemple Vérifiez que vous comprenez bien les approximations suivantes :

- pour x très grand : e x + x 2 ≈ e x , 3 x 2 -x + 1 ≈ 3 x 2 , ( x + ln x ) e x e 2 x + /radicallow x ≈ x e -x , /floorleft x /floorright x 2 + 1 ≈ 1 x et ch x ≈ sh x ≈ e x 2 .
- pour x proche de 0 : ln ( 1 + x ) ≈ x , e x -1 ≈ x , sh x ≈ x , x + ln ( 1 + x ) ln ( 1 + 3 x ) ≈ 2 3 et e 3 x -e x + x 2 ≈ 2 x .
- /enc-36 Attention ! Il faut y réfléchir à deux fois quand on veut composer une relation f 1 ( x ) ≈ f 2 ( x ) par une fonction g , car en général : g ◦ f 1 ( x ) ≈ g ◦ f 2 ( x ) . Tâchons de le comprendre sur l'exemple des fonctions logarithme et exponentielle.
- Pour x très grand : e x + 1 ≈ e x , mais comment le logarithme affecte-t-il les grandes quantités? Le logarithme tasse les infinis. Sur l'intervalle [ e x , e x + 1 ] de longueur 1, le logarithme est presque constant, donc ln ( e x + 1 ) ≈ lne x = x .
- Pour x très grand : x + ln x ≈ x , mais comment l'exponentielle affecte-t-elle les grandes quantités? L'exponentielle écarte les infinis. Par exemple, x + ln 2 ≈ x mais e x + ln2 = 2e x ≈ e x . L'intervalle [ x , x + ln2 ] a beau être de longueur ln 2 seulement, l'exponentielle y est terriblement croissante. La situation est encore pire sur [ x , x + ln x ] , dont la longueur ln x tend vers + ∞ avec x : e x + ln x = x e x ≈ e x .

Rappelons ici qu'en dépit de ces mises en garde, le symbole ≈ ne tient jamais lieu de preuve, il défriche le terrain.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Démonstration Au brouillon, pour x très grand : x + /radicallow x ≈ x , donc x 2 x + /radicallow x ≈ x 2 x = x -→ + ∞ . Rapide et convaincant, mais pas du tout rigoureux. Sur une copie :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Démonstration Au brouillon, pour x très grand : ln ( e x + 1 ) ≈ lne x = x et e x + ln x + 1 = x e x + 1 ≈ x e x , x donc

ln

(

e

e

x

+

ln

+

x

1

+

)

1

≈

x

x

e

x

=

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Démonstration Les deux quantités se ressemblent, mais elles sont très différentes en réalité.

<!-- formula-not-decoded -->

- Première limite : Pour x très grand : /radicallow x 2 + x /radicallow x 2 = x , donc /radicallow x 2 + x /radicallow x x +
- Deuxième limite : Pour x très grand, /radicallow x 2 ± x ≈ /radicallow x 2 = x , donc problème! Les quantités /radicallow x 2 + x et /radicallow x 2 -x se détruisent mutuellement par soustraction, mais que reste-t-il? Par exemple, quand on soustrait deux réels proches de 1000, que reste-t-il? Ça dépend de ce qu'on soustrait : 1010 -1000 = 10 et 1000,001 -1000 = 0,001, et pourtant 1010 et 1000,001 sont tous les deux proches de 1000.

La technique de la quantité conjuguée , qui repose sur l'identité remarquable ( a + b )( a -b ) = a 2 -b 2 , nous permet de mesurer la taille du reste après soustraction :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Démonstration Au brouillon, pour x proche de 0 : ln ( 1 + x ) ≈ x et sh x ≈ x , donc x + sh x ≈ 2 x ,

<!-- formula-not-decoded -->

Et si on avait voulu calculer lim x → 0 x 2 x -sh x ? C'est plus compliqué car au dénominateur, x et sh x ont à peu près la même taille. Que reste-t-il après soustraction? Nous ne le savons pas à ce stade de l'année et nous ne pouvons donc pas encore calculer cette limite.

## /enc-36 Attention ! 1 + ∞ est une nouvelle forme indéterminée!

Exemple ( 1 + x ) 1 x --- → x → 0 e.

Démonstration Il est tentant d'analyser la situation ainsi : 1 + ∞ = 1, mais c'est très faux ! Pour faire communiquer correctement 1 + x et son exposant 1 , plaçons-les AU MÊME NIVEAU , i.e. au sommet d'une exponentielle.

<!-- formula-not-decoded -->

- /enc-36 Attention ! Dans un calcul de limite, aucun théorème de substitution ne permet de remplacer un morceau par sa limite sans toucher au reste.

/negationslash

Par exemple, si f ( x ) - - - - - → x → + ∞ 2, il n'est pas du tout possible d'affirmer, contrairement à ce que vous pensez souvent, que : lim x → + ∞ x x + f ( x ) = lim x → + ∞ x x + 2 = 1 et lim x → + ∞ f ( x ) x = lim x → + ∞ 2 x = + ∞ . En d'autres termes, on ne peut pas remplacer f ( x ) par sa limite 2 dans les expressions x x + f ( x ) et f ( x ) x quand x tend vers + ∞ . Par exemple, ( 1 + x ) --- → x → 0 1 mais lim x → 0 ( 1 + x ) 1 x = e = 1 = lim x → 0 1 1 x .

## 5 FONCTIONS TRIGONOMÉTRIQUES

Soit α ∈ /Rbbb . Comme nous l'avons déjà vu, la relation ≡ [ α ] de congruence modulo α est une relation d'équivalence sur /Rbbb . Rappelons qu'elle est définie pour tous x , y ∈ /Rbbb par l'équivalence : x ≡ y [ α ] ⇐⇒ ∃ k ∈ /Zbbb , x = y + k α .

<!-- formula-not-decoded -->

Pour tout β ∈ /Rbbb , la classe d'équivalence de β pour ≡ [ α ] est l'ensemble /braceleftbig2 x ∈ /Rbbb | x ≡ β [ α ] /bracerightbig2 = /braceleftbig2 β + k α | k ∈ /Zbbb /bracerightbig2 et on le note β + α /Zbbb . Plus généralement, pour toute partie E de /Rbbb , on note E + α /Zbbb l'ensemble :

<!-- formula-not-decoded -->

Exemple On obtient /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 + π /Zbbb en répétant /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 tous les π .

Exemple L'ensemble π 4 + π /Zbbb est π -périodique, donc rencontre l'intervalle [ 0,3 π [ de longueur 3 π en exactement trois points : /parenleftbig3 π 4 + π /Zbbb /parenrightbig3 ∩ [ 0,3 π [ = /braceleftbig4 π 4 , 5 π 4 , 9 π 4 /bracerightbig4 .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Exemple On s'intéresse à la réunion A = /parenleftbig3 π 5 + π 2 /Zbbb /parenrightbig3 ∪ π 3 /Zbbb . L'ensemble π 5 + π 2 /Zbbb est π 2 -périodique, donc k π 2 -périodique pour tout k ∈ /Nbbb ∗ . De même, π 3 /Zbbb est l π 3 -périodique pour tout l ∈ /Nbbb ∗ . Ces deux ensembles ont donc une période commune si on arrive à trouver deux entiers k , l ∈ /Nbbb ∗ pour lesquels k π 2 = l π 3 , i.e. 3 k = 2 l . Or les entiers k = 2 et l = 3 conviennent et on ne peut pas les choisir plus petits. Conclusion : π 5 + π 2 /Zbbb et π 3 /Zbbb admettent 2 × π 2 = 3 × π 3 = π pour période commune, donc A est π -périodique. Pour comprendre A , il nous suffit dès lors de le décrire sur une seule période, par exemple [ 0, π [ , puis de translater indéfiniment tous les π . En d'autres termes : A = /parenleftbig1 A ∩ [ 0, π [ /parenrightbig1 + π /Zbbb = /braceleftbig4 π 5 , π 5 + π 2 , 0, π 3 , 2 π 3 /bracerightbig4 + π /Zbbb .

## 5.1 FONCTIONS COSINUS, SINUS ET TANGENTE

Définition-théorème (Lien du cosinus et du sinus avec le cercle trigonométrique)

- Lien avec le cercle trigonométrique : Pour tout θ ∈ /Rbbb : cos 2 θ + sin 2 θ = 1.

Réciproquement, pour tout couple ( x , y ) ∈ /Rbbb 2 pour lequel x 2 + y 2 = 1, il existe un réel θ , unique modulo 2 π , pour lequel ( x , y ) = ( cos θ , sin θ ) . En termes géométriques, tout point du cercle trigonométrique a des coordonnées de la forme ( cos θ , sin θ ) .

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000041_8fe740dbbd224902425a56bbdb95a6d2ef1ce14b8464d15fa5f5b0932b6bbe55.png)

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000042_64bea0570b5601ef3c88539f3905d6a2baaaaad7429fc6071c3a65c6b3cc5d77.png)

- Résolution d'équations : Pour tous x , y ∈ /Rbbb :

<!-- formula-not-decoded -->

- Transformations affines : Les relations suivantes se lisent toutes sur le cercle trigonométrique. Pour tout x ∈ /Rbbb :

cos ( x + π ) = -cos x cos ( π -x ) = -cos x cos /parenleftbig3 π 2 -x /parenrightbig3 = sin x cos /parenleftbig3 x + π 2 /parenrightbig3 = -sin x sin ( x + π ) = -sin x sin ( π -x ) = sin x sin /parenleftbig3 π 2 -x /parenrightbig3 = cos x sin /parenleftbig3 x + π 2 /parenrightbig3 = cos x ︸ ︷︷ ︸ Ajouter π dans un cosinus ou un sinus revient à le multiplier par -1. ︸ ︷︷ ︸ π 2 -x est LA transformation à utiliser quand on veut remplacer un cosinus par un sinus et vice versa.

Ainsi, pour tout k ∈ /Zbbb : cos ( x + k π ) = ( -1 ) k cos x et sin ( x + k π ) = ( -1 ) k sin x .

## /enc-36 Attention !

Exemple

Pour tout cos

x

x

∈

=

/Rbbb

:

⇐⇒

cos

x

=

x

sin

=

x

⇐⇒

À peine mieux :

<!-- formula-not-decoded -->

Démonstration Cette équivalence se lit bien sur le cercle trigonométrique, mais on peut aussi la démontrer par le calcul. Pour tout x ∈ /Rbbb : cos x = sin x ⇐⇒ sin /parenleftbig3 π -x /parenrightbig3 = sin x Impossible

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Les valeurs remarquables du cosinus, du sinus et de la tangente doivent être connues par cœur!

| x     |   0 | π 4             | π 6             | π 3             | π 2   |
|-------|-----|-----------------|-----------------|-----------------|-------|
| cos x |   1 | 1 /radicallow 2 | /radicallow 3 2 | 1 2             | 0     |
| sin x |   0 | 1 /radicallow 2 | 1 2             | /radicallow 3 2 | 1     |
| tan x |   0 | 1               | 1 /radicallow 3 | /radicallow 3   |       |

cos

y

y

.

cos

x

=

cos

y

⇐⇒

x

y

2

]

/Bullet

≡

[

π

.

## Définition-théorème (Propriétés des fonctions cosinus et sinus)

- •

- Fonction cosinus : La fonction cos est paire, 2 π -périodique, de classe /Ccal ∞ sur /Rbbb , et : cos ′ = - sin.

- •

- Fonction sinus : La fonction sin est impaire, 2 π -périodique, de classe /Ccal ∞ sur /Rbbb , et : sin ′ = cos.

Pour tout x ∈ /Rbbb : | sin x | /lessorequalslant | x | . En outre, sin x x --- → x → 0 1, autrement dit sin x ≈ x pour x proche de 0.

/Bullet

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000043_1104d4bd8e64830485164deb494d3599af01aa4c1dbf7e80840b596f1a2c7607.png)

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000044_cef3ca1745de33f7e3b8a01c89153f7f6fb5bf4bedabb2800f9e292ed3c1577b.png)

/Bullet

Démonstration La limite sin x x --- → x → 0 1 n'est rien de plus que le nombre dérivé de la fonction sin en 0.

Ensuite, la fonction sin est concave sur [ 0, π ] car sa dérivée cos y est décroissante, donc pour tout x ∈ [ 0, π ] : | sin x | = sin x /lessorequalslant sin ′ ( 0 ) x + sin 0 = x = | x | . A fortiori, pour tout x ∈ [ -π , 0 ] : | sin x | = | sin ( -x ) | /lessorequalslant |-x | = | x | . Enfin, l'inégalité est triviale pour x &gt;π et x &lt;π : | sin x | /lessorequalslant 1 /lessorequalslant π /lessorequalslant | x | .

## Théorème (Formules d'addition et de produit du cosinus et du sinus) Pour tous x , y ∈ /Rbbb :

sin ( x + y ) = sin x cos y + cos x sin y sin ( x -y ) = sin x cos y -cos x sin y

cos ( x + y ) = cos x cos y -sin x sin y cos ( x -y ) = cos x cos y + sin x sin y

Pour x = y , on parle de formules de duplication :

sin ( 2 x ) = 2sin x cos x

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

-

-

Les formules d'addition et de duplication doivent être connues par cœur - et ce même si les secondes découlent des premières. En revanche, vous devez juste savoir retrouver vite et bien les formules de produit, si possible de tête.

## Définition-théorème (Fonction tangente)

- Définition et régularité : On appelle fonction tangente la fonction tan = sin cos sur /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 + π /Zbbb .

Impaire et π -périodique, tan est de classe /Ccal ∞ sur son ensemble de définition et :

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000045_d489e08061228125015b9c1d7847b10607a013fd2e880abfa0153543671af68f.png)

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000046_175ee9ffc2351b98930952b4952773d7d4f03b4b8ce0c73590d541276e5eb941.png)

/Bullet

- Résolution d'équations : Pour tous x , y ∈ /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 + π /Zbbb : tan x = tan y ⇐⇒ x ≡ y [ π ] .

<!-- formula-not-decoded -->

- Formules d'addition et de duplication : Dès que chaque terme est bien défini :

<!-- formula-not-decoded -->

- •
- Expression de cos x , sin x et tan x en fonction de tan x : Pour tout x ] π , π [+ 2 π /Zbbb , si on pose t = tan x :

<!-- formula-not-decoded -->

/Bullet

/Bullet

/Bullet

La relation

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000047_e46d1f92949af45adeb1606e4d0dd8ae609cbd58b30a76751f26a52773bf0461.png)

ne sert pas tant à calculer tan ′ qu'à transformer cos en tan et vice versa. C'est comme ça qu'il faut la retenir!

Les expressions de cos x , sin x et tan x en fonction de tan x 2 ne sont pas à connaître par cœur, vous devez en revanche savoir les retrouver rapidement en cas de besoin.

## Démonstration

- Définition : La tangente est définie là où le cosinus ne s'annule pas, i.e. sur /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 + π /Zbbb .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Oncomprendici pourquoi la tangente est π -périodique alors que cosinus et sinus ne sont que 2 π -périodiques.

<!-- formula-not-decoded -->

- Variations et limites : Par imparité et π -périodicité, une étude sur /bracketleftbig3 0, π 2 /bracketleftbig3 suffit. La tangente y est strictement croissante car tan ′ = 1 cos 2 &gt; 0. Enfin, sin x - - - - - → x → π 2 -1 et cos x - - - - - → x → π 2 -0 + , donc tan x - - - - - → x → π 2 -+ ∞ .
- Équation tan x = tan y : tan x = tan y ⇐⇒ sin x cos x = sin y cos y ⇐⇒ sin x cos y -cos x sin y = 0

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 5.2 FONCTIONS ARCCOSINUS, ARCSINUS ET ARCTANGENTE

Périodiques, les fonctions cosinus, sinus et tangente ne sont pas injectives sur leurs ensembles de définition. Impossible de leur trouver une réciproque! Par exemple, l'équation cos x = 1 2 d'inconnue x ∈ /Rbbb a plein de solutions, en l'occurrence tous les réels congrus à π 3 ou -π 3 modulo 2 π , et aucun de ces antécédents de 1 2 par la fonction cosinus n'est a priori meilleur que les autres. Cela dit, d'après le TVI strictement monotone :

- la restriction cos [ 0, π ] est bijective de [ 0, π ] sur [ -1,1 ] ,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

L'équation cos x = 1 2 d'inconnue x ∈ [ 0, π ] ne possède à présent plus qu'une seule solution, à savoir π 3 . En restreignant le champ des possibles, nous avons créé de l'injectivité. On aurait pu choisir d'autres domaines, mais ce choix arbitraire est désormais officiellement arrêté une fois pour toutes.

|                    | cos      | sin         | tan         |
|--------------------|----------|-------------|-------------|
| Domaine privilégié | [ 0, π ] | - π 2 , π 2 | - π 2 , π 2 |

/bracketleftbig3

/bracketrightbig3

/bracketrightbig3

/bracketleftbig3

## Définition (Fonctions arccosinus, arcsinus et arctangente)

- Arccosinus : cos [ 0, π ] est bijective de [ 0, π ] sur [ -1,1 ] et sa réciproque arccosinus est notée Arccos. Pour tout x ∈ [ -1,1 ] , Arccos x est l'unique réel θ de [ 0, π ] pour lequel cos θ = x .

Pour tout x ∈ [ -1,1 ] , Arcsin x est l'unique réel θ de /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 pour lequel sin θ = x .

- Arcsinus : sin /bracketleftbig2 -π 2 , π 2 /bracketrightbig2 est bijective de /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 sur [ -1,1 ] et sa réciproque arcsinus est notée Arcsin .
- Arctangente : tan /bracketrightbig2 -π 2 , π 2 /bracketleftbig2 est bijective de /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 sur /Rbbb et sa réciproque arctangente est notée Arctan.

π

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000048_583871f75551f986c05f294496bb5875977deab4614abcdab995a564c762cffd.png)

/Bullet

| x        | - 1   | - /radicallow 3 2   | - 1 /radicallow 2   | - 1 2   | 0   | 1 2   | 1 /radicallow 2   | /radicallow 3 2   | 1   |
|----------|-------|---------------------|---------------------|---------|-----|-------|-------------------|-------------------|-----|
| Arcsin x | - π 2 | - π 3               | - π 4               | - π 6   | 0   | π 6   | π 4               | π 3               | π 2 |
| Arccos x | π     | 5 π 6               | 3 π 4               | 2 π 3   | π 2 | π 3   | π 4               | π 6               | 0   |

| x        |       | -∞ - /radicallow 3   | - 1   | - 1 /radicallow 3   |   0 | 1 /radicallow 3   | 1   | /radicallow 3   | + ∞   |
|----------|-------|----------------------|-------|---------------------|-----|-------------------|-----|-----------------|-------|
| Arctan x | - π 2 | - π 3                | - π 4 | - π 6               |   0 | π 6               | π 4 | π 3             | π 2   |

- /enc-36 Attention ! Arccos n'est pas la réciproque du cosinus, mais celle de cos [ 0, π ] et ça change tout. Cette mise en garde est détaillée ci-dessous dans le cas du cosinus, mais elle vaut aussi pour le sinus et la tangente.
- Pour tout x ∈ [ -1,1 ] , Arccos x est l'unique réel θ ∈ [ 0, π ] pour lequel cos θ = x , donc cosArccos x = x .
- En revanche, pour tout x ∈ /Rbbb , Arccos cos x est l'unique réel θ ∈ [ 0, π ] pour lequel cos θ = cos x . Ce n'est donc pas forcément x ! La question importante, c'est : « x appartient-il au domaine privilégié [ 0, π ] , oui ou non? »

Par exemple : Arccos cos ( 2 π ) = Arccos1 = 0 = 2 π .

/negationslash

VRAI : ∀ x ∈ [ -1,1 ] , cosArccos x = x . FAUX : ∀ x ∈ /Rbbb , Arccos cos x = x . VRAI : ∀ x ∈ [ 0, π ] , Arccos cos x = x .

Exemple On veut résoudre l'équation cos x = 1 3 d'inconnue x ∈ /Rbbb . Pour tout x ∈ /Rbbb :

<!-- formula-not-decoded -->

L'ensemble des solutions cherché est donc la réunion /parenleftbig4 Arccos 1 3 + 2 π /Zbbb /parenrightbig4 ∪ /parenleftbig4 -Arccos 1 3 + 2 π /Zbbb /parenrightbig4 .

<!-- formula-not-decoded -->

Démonstration Dans les deux cas, on commence par placer 20 π 3 sur le cercle trigonométrique ainsi que le domaine privilégié de la fonction sinus ou cosinus concernée.

Pour tout x ∈ /Rbbb , Arctan x est l'unique réel θ de /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 pour lequel tan θ = x .

/Bullet

/Bullet

/Bullet

- Arccosinus : 20 π 3 appartient à 2 π près au domaine privilégié du cosinus : 20 π 3 ∈ [ 0, π ] + 2 π /Zbbb . Il suffit donc d'ôter un certain nombre de fois 2 π et c'est fini.
- Arcsinus : 20 π 3 n'appartient pas au domaine privilégié du sinus : 20 π 3 / ∈ /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 + 2 π /Zbbb , même à 2 π près. Nous pouvons cependant nous y ramener À SINUS CONSTANT grâce à la relation sin ( π -x ) = sin x . Par 2 π -périodicité : sin 20 π 3 = sin 2 π 3 , puis sin 20 π 3 = sin /parenleftbig4 π -2 π 3 /parenrightbig4 = sin π 3 , et bien sûr π 3 ∈ /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 .

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000049_54862cac3848ca27a449f9f20a128bb8023a3d476925cd3713c1fcd760d14063.png)

/Bullet

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000050_1ec3d19b1a07564ac2d37593eb8b6dee182fdaf9c3b025c2db26f2a5a625a907.png)

## Théorème (Lien entre les coordonnées cartésiennes et les coordonnées polaires)

Soit M un point de coordonnées cartésiennes ( x , y ) et de coordonnées polaires ( r , θ ) .

- (i) /braceleftbig5 x = r cos θ y = r sin θ et r = /radicalbig1 x 2 + y 2 .

![Image]('out'\Cours - Rappels et complements sur les fonctions reelles_artifacts\image_000051_b047ea6b06126d6fbd26877183bbf62e5f913d8084d2d2fde5ebe35facdaecbb.png)

Démonstration C'est sous-entendu, mais on travaille bien sûr dans un repère orthonormal direct ( O , # ' ı , # '  ) .

<!-- formula-not-decoded -->

- (i) #    ' OM = x # ' ı + y # '  = r ( cos θ # ' ı + sin θ # '  ) , donc x = r cos θ et y = r sin θ par identification des coordonnées. En outre, r = ‖ #    ' OM ‖ = x 2 + y 2 .

<!-- formula-not-decoded -->

- /radicalbig1 (ii) Cas où x &gt; 0 : θ -2 k π ∈ /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 pour un certain k ∈ /Zbbb , or tan ( θ -2 k π ) = tan θ = r sin θ r cos θ = y x , donc θ -2 k π = Arctan y x , et enfin θ ≡ Arctan y x [ 2 π ] .

On a choisi d'exprimer θ comme une arctangente, mais on aurait pu l'exprimer comme un arccosinus ou un arcsinus, la stratégie est toujours la même. On place M dans l'un des quatre quadrants que le repère choisi délimite, puis selon qu'on souhaite atteindre un arccosinus ou un arcsinus, on ramène θ dans le domaine privilégié adapté.

Exemple Avec les notations du théorème, faisons l'hypothèse que x &gt; 0 et y &lt; 0. On peut donc choisir θ dans /bracketrightbig3 -π 2 , 0 /bracketleftbig3 , mais comment l'exprimer comme un arccosinus ou un arcsinus?

- Arccosinus : θ n'appartient pas au domaine privilégié [ 0, π ] , même à 2 π près, mais nous pouvons l'y ramener À COSINUS CONSTANT grâce à la relation cos ( -x ) = cos x . Précisément, cos ( -θ ) = cos θ = x r avec -θ ∈ [ 0, π ] , donc -θ = Arccos x r , i.e. θ = -Arccos x r .
- Arcsinus : θ appartient au domaine privilégié /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 et sin θ = y r , donc θ = Arcsin y r .

## Théorème (Propriétés des fonctions arccosinus, arcsinus et arctangente)

- Une relation mixte : Pour tout x ∈ [ -1,1 ] : cosArcsin x = sin Arccos x = /radicallow 1 -x 2 .

- Arccosinus : Arccos est continue sur [ - 1,1 ] et de classe /Ccal ∞ sur ] - 1,1 [ , mais pas dérivable en - 1 et 1. Pour tout x ∈ ] - 1,1 [ :

$$Arccos ′ ( x ) = - 1 /radicallow 1 - x 2 .$$

- Arcsinus : Arcsin est impaire et continue sur [ - 1,1 ] et de classe /Ccal ∞ sur ] - 1,1 [ , mais pas dérivable en - 1 et 1. Pour tout x ∈ ] - 1,1 [ : 1

$$Arcsin ′ ( x ) = /radicallow 1 - x 2 .$$

- Arctangente : Arctan est impaire et de classe /Ccal ∞ sur /Rbbb . Pour tout x ∈ /Rbbb : Arctan ′ ( x ) = 1 1 + x 2 .

/Bullet

/Bullet

/Bullet

/Bullet

/Bullet

/bracketleftbig3

/bracketrightbig3

/Bullet

La non-dérivabilité d'Arccos et Arcsin en ± 1 s'explique bien géométriquement, les tangentes horizontales de sin et cos deviennent verticales quand on les symétrise par rapport à la droite d'équation y = x .

## Démonstration (Fonction arcsinus)

- Continuité / imparité : La fonction sin /bracketleftbig2 -π 2 , π 2 /bracketrightbig2 est bijective de /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 sur [ -1,1 ] et continue / impaire, donc d'après le théorème de continuité / imparité d'une réciproque, sa réciproque Arcsin = /parenleftbig2 sin /bracketleftbig2 -π 2 , π 2 /bracketrightbig2 /parenrightbig2 -1 est continue / impaire sur [ -1,1 ] .
- Relation cosArcsin x : Pour tout x ∈ [ -1,1 ] : Arcsin x ∈ -, , donc cosArcsin x /greaterorequalslant
- Dérivabilité et dérivée : La fonction sin /bracketrightbig2 -π 2 , π 2 /bracketleftbig2 est bijective de /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 sur ] -1,1 [ , de classe /Ccal ∞ , et sa dérivée sin ′ = cos ne s'annule pas sur /bracketrightbig3 -π 2 , π 2 /bracketleftbig3 , donc d'après le théorème de dérivabilité d'une réciproque, Arcsin est de classe /Ccal ∞ sur ] -1,1 [ et pour tout x ∈ ] -1,1 [ :
- /bracketleftbig3 π 2 π 2 /bracketrightbig3 0, donc : cosArcsin x = | cosArcsin x | = /radicalbig1 1 -sin 2 Arcsin x = /radicalbig1 1 -x 2 .

<!-- formula-not-decoded -->

Le théorème de dérivabilité ne nous dit rien de la dérivabilité d'Arcsin en ± 1 car cos ′ ( 0 ) = cos ′ ( π ) = 0, mais on peut montrer qu'Arcsin n'est pas dérivable en ces points.

/negationslash

Démonstration (Fonction arctangente) Il s'agit là aussi essentiellement d'utiliser le théorème de dérivabilité / imparité d'une réciproque. La situation est cependant plus simple car tan ′ ( x ) = 1 + tan 2 x = 0 pour tout x ∈ /Rbbb . Pas de tangente horizontale sur le graphe de la fonction tangente, donc pas de problème de dérivabilité pour Arctan. Pour tout x ∈ /Rbbb : Arctan ′ ( x ) = 1 ( ) = 1 + = 1 + 2 .

<!-- formula-not-decoded -->

Exemple 3 5 est l'unique solution de l'équation Arcsin x = Arccos 4 5 d'inconnue x ∈ [ -1,1 ] .

/bracketleftbig3 2 2 /bracketrightbig3 5 /bracketleftbig3 2 /bracketrightbig3 4 5 ∈ [ 0,1 ] , donc pour tout x ∈ [ -1,1 ] :

Démonstration Pour tous x ∈ [ -1,1 ] et y ∈ /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 : y = Arcsin x ⇐⇒ x = sin y par définition de l'arcsinus, et attention, l'équivalence est vraie seulement si y appartient à -π , π . Ici, Arccos 4 ∈ 0, π car

<!-- formula-not-decoded -->

Démonstration Il s'agit de montrer que la fonction x f /mapstochar-→ Arccos x + Arcsin x est constante sur [ -1,1 ] de valeur π 2 . Or cette fonction est dérivable sur l' INTERVALLE ouvert ] -1,1 [ et sa dérivée est la fonction nulle, donc f est constante. Quelle valeur? Nous pouvons la calculer en 0 par exemple : f ( 0 ) = Arccos0 + Arcsin0 = π 2 + 0 = π 2 , et f ( 1 ) et f ( -1 ) valent la même chose par continuité de f sur l'intervalle fermé [ -1,1 ] .

Exemple Pour tout x ∈ [ -1,1 ] : Arccos x + Arcsin x = π 2 .

Exemple Pour tout x &gt; 0 : Arctan x + Arctan 1 x = π 2 et pour tout x &lt; 0 : Arctan x + Arctan 1 x = -π 2 .

Démonstration La fonction x g /mapstochar-→ Arctan x + Arctan 1 x est dérivable sur /Rbbb ∗ et pour tout x ∈ /Rbbb ∗ :

<!-- formula-not-decoded -->

Comme /Rbbb ∗ =] -∞ , 0 [ ∪ ] 0, + ∞ [ n'est pas un INTERVALLE , on ne peut pas en déduire que g est constante sur /Rbbb ∗ tout entier, mais seulement qu'elle l'est sur /Rbbb ∗ + et /Rbbb ∗ -indépendamment. Quelles valeurs? Calculons g ( 1 ) : g ( 1 ) = 2Arctan1 = 2 × π 4 = π 2 . Pour la valeur de g sur /Rbbb ∗ -, remarquer simplement que g est impaire.

Exemple On veut résoudre l'équation Arccos x = Arcsin x d'inconnue x ∈ [ -1,1 ] .

On a bien envie de passer au cosinus (ou au sinus) des deux côtés de l'équation, mais on perd l'équivalence en faisant cela car en toute généralité : cos x = cos y = ⇒ x = y , autrement dit la fonction cosinus n'est pas injective sur /Rbbb . Elle l'est sur de plus petits domaines sur lesquels elle est strictement monotone, par exemple [ -π , 0 ] , [ 0, π ] ou [ π , 2 π ] .

C'est parti. Pour tout x ∈ [ -1,1 ] :

Arccos x = Arcsin x /bigstar ⇐⇒ cosArccos x = cosArcsin x et Arcsin x ∈ [ 0, π ] Cette équivalence /bigstar est LE passage délicat, justifié plus loin. ⇐⇒ x = /radicallow 1 -x 2 et x ∈ [ 0,1 ] après contemplation du graphe d'arcsinus x 2 = 1 x 2 et x [ 0,1 ] x = 1 .

<!-- formula-not-decoded -->

Justification de l'équivalence /bigstar : Cette équivalence est la difficulté principale de l'équation et on ne peut pas s'en tirer sans réfléchir. N'espérez pas « la méthode » qui vous évitera de réfléchir, il n'y en a pas.

- L'implication : Arccos x = Arcsin x = ⇒ cosArccos x = cosArcsin x ne pose aucun problème.
- Le retour n'est possible que si Arccos x et Arcsin x appartiennent à un même domaine d'injectivité du cosinus. Ici, Arccos x appartient à [ 0, π ] , mais Arcsin x appartient a priori à /bracketleftbig3 -π 2 , π 2 /bracketrightbig3 et non pas à [ 0, π ] . En tout cas, l'implication suivante est correcte : cosArccos x = cosArcsin x et Arcsin x ∈ [ 0, π ] = ⇒ Arccos x = Arcsin x .
- Mais l'implication corrigée : Arccos x = Arcsin x = ⇒ cosArccos x = cosArcsin x et Arcsin x ∈ [ 0, π ] l'est-elle ? C'est ce qu'il nous reste à comprendre. Et tout simplement, si Arccos x = Arcsin x , alors oui, Arcsin x = Arccos x ∈ [ 0, π ] car un arccosinus est toujours dans [ 0, π ] .

## 6 TABLEAUX RÉCAPITULATIFS DES DÉRIVÉES USUELLES

| Fonction       | Fonction       | Dérivée               |
|----------------|----------------|-----------------------|
| e x            | e x            | e x                   |
| ln x           | ln x           | 1 x                   |
| x α = e α ln x | x α = e α ln x | α x α - 1             |
| ch x =         | e x - e - x 2  | sh x                  |
| sh x =         | e x + e - x 2  | ch x                  |
| th x =         | sh x ch x      | 1 - th 2 x = 1 ch 2 x |

| Fonction            | Dérivée                 |
|---------------------|-------------------------|
| sin x               | cos x                   |
| cos x               | - sin x                 |
| tan x = sin x cos x | 1 + tan 2 x = 1 cos 2 x |
| Arcsin x            | 1 /radicallow 1 - x 2   |
| Arccos x            | - 1 /radicallow 1 - x 2 |
| Arctan x            | 1 1 + x 2               |