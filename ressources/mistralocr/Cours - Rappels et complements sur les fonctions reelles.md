# RAPPELS ET COMPLÉMENTS SUR LES FONCTIONS RÉELLES 

Dans ce chapitre, $E$ et $F$ sont des parties quelconques de $\mathbb{R}$, pas forcément des intervalles.
Le vocabulaire des applications a été présenté en toute généralité au chapitre «Relations binaires et applications», mais les fonctions de $\mathbb{R}$ dans $\mathbb{R}$ vont de pair avec un vocabulaire propre aux réels - monotonie, caractère majoré/minoré, continuité, dérivabilité... - qui est l'objet du chapitre.

Mais d'abord, un mot sur les composées. Soient $f: E \longrightarrow \mathbb{R}$ et $g: F \longrightarrow \mathbb{R}$ deux fonctions. La composée $g \circ f$ n'est définie que si $f$ est à valeurs dans $F$, i.e. si $f(E) \subset F$. On donne ci-dessous quelques exemples de recherche d'ensemble de définition.

Quand la fonction extérieure $g$ est définie sur $\mathbb{R}$ tout entier, la condition $f(E) \subset \mathbb{R}$ est trivialement vraie et $g \circ f$ est définie sans qu'aucun obstacle se soit présenté. La fonction $\mathrm{e}^{f}$ ne pose par exemple jamais aucun problème de définition car la fonction exponentielle est définie sur $\mathbb{R}$ tout entier.

Exemple La fonction $x \longmapsto \sqrt{x+3}$ est définie sur $[-3,+\infty[$.
Démonstration La fonction $x \longmapsto x+3$ est définie sur $\mathbb{R}$ et la fonction $\sqrt{ }$ l'est sur $\mathbb{R}_{+}$, mais quand $x$ décrit $\mathbb{R}$, $x+3$ n'appartient pas forcément à $\mathbb{R}_{+}$. Pour quels $x \in \mathbb{R}$ est-il vrai que $x+3 \geqslant 0$ ? Réponse : $x \in[-3,+\infty[$.

Exemple La fonction $x \longmapsto \ln \left(x^{2}-3 x+2\right)$ est définie sur $]-\infty, 1[\cup] 2,+\infty[$.
Démonstration La fonction $x \longmapsto x^{2}-3 x+2$ est définie sur $\mathbb{R}$ et $x \longmapsto \ln x$ l'est sur $\mathbb{R}_{+}^{*}$, mais quand $x$ décrit $\mathbb{R}, x^{2}-3 x+2$ n'appartient pas forcément à $\mathbb{R}_{+}^{*}$. Pour quels $x \in \mathbb{R}$ est-il vrai que $x^{2}-3 x+2>0$ ? Réponse : $x \in]-\infty, 1[\cup] 2,+\infty[$ car les racines du polynôme sont 1 et 2 et son coefficient dominant est strictement positif.

Exemple La fonction $x \longmapsto \frac{1+\mathrm{e}^{\sqrt{x}}}{x \sqrt{2-x}}$ est définie sur $\{x \in \mathbb{R} \mid x \sqrt{2-x} \neq 0 \quad$ et $\quad 2-x \geqslant 0 \quad$ et $\quad x \geqslant 0\}$

$$
=\{x \in \mathbb{R} \mid x \neq 0 \quad \text { et } \quad x \neq 2 \quad \text { et } \quad 0 \leqslant x \leqslant 2\}=] 0,2[
$$

## 1 VOCABULAIRE USUEL

### 1.1 MONOTONIE

Définition (Fonction monotone) Soit $f: E \longrightarrow \mathbb{R}$ une fonction.

- On dit que $f$ est croissante si :

$$
\forall x, y \in E, \quad x<y \quad \Longrightarrow \quad f(x) \leqslant f(y)
$$

- On dit que $f$ est strictement croissante si :

$$
\forall x, y \in E, \quad x<y \quad \Longrightarrow \quad f(x)<f(y)
$$

- On dit que $f$ est décroissante si :

$$
\forall x, y \in E, \quad x<y \quad \Longrightarrow \quad f(x) \geqslant f(y)
$$

- On dit que $f$ est (resp. strictement) monotone si $f$ est (resp. strictement) croissante ou décroissante.

Une fonction croissante (resp. décroissante) est une fonction qui préserve (resp. renverse) les inégalités.
On peut caractériser la monotonie d'une fonction dérivable par le signe de sa dérivée, mais il s'agit là d'un théorème et non d'une définition. La définition ci-dessus est générale et ne requiert pas la dérivabilité.

Le résultat qui suit a été démontré au chapitre «Relations binaires et applications».

Théorème (Injectivité et stricte monotonie) Soit $f: E \longrightarrow \mathbb{R}$ une fonction.
Si $f$ est strictement monotone, $f$ est injective.

Les résultats qui suivent sont énoncés en termes de monotonie au sens large, mais ils sont valables pour des fonctions monotones au sens strict.

# Théorème (Opérations sur les fonctions monotones) 

(i) Addition : Soient $f: E \longrightarrow \mathbb{R}$ et $g: E \longrightarrow \mathbb{R}$ deux fonctions.

Si $f$ et $g$ sont croissantes, $f+g$ l'est aussi. Si $f$ et $g$ sont décroissantes, $f+g$ l'est aussi.
(ii) Produit : Soient $f: E \longrightarrow \mathbb{R}$ et $g: E \longrightarrow \mathbb{R}$ deux fonctions.

Si $f$ et $g$ sont croissantes POSITIVES, $f g$ est croissante. Si $f$ et $g$ sont décroissantes POSITIVES, $f g$ est décroissante.
(iii) Composition : Soient $f: E \longrightarrow F$ et $g: F \longrightarrow \mathbb{R}$ deux fonctions.

Si $f$ et $g$ sont monotones de même sens de variation, $g \circ f$ est croissante.
Si $f$ et $g$ sont monotones de sens de variation opposés, $g \circ f$ est décroissante.
(iv) Réciproque : Soit $f: E \longrightarrow F$ une fonction bijective de $E$ sur $F$.

Si $f$ est monotone, elle l'est strictement et $f^{-1}$ est strictement monotone de même sens de variation.

Attention！ La fonction identité $x \longmapsto x$ est croissante sur $\mathbb{R}$, mais quand on la multiplie par elle-même, le résultat $x \longmapsto x^{2}$ n'est pas une fonction croissante sur $\mathbb{R}$. Comme quoi la positivité compte!

## Démonstration

(i) Dans le cas où $f$ et $g$ sont croissantes, soient $x, y \in E$. Si $x<y$, alors par hypothèse $f(x) \leqslant f(y)$ et $g(x) \leqslant g(y)$, donc $f(x)+g(x) \leqslant f(y)+g(y)$ par somme.
(ii) Dans le cas où $f$ et $g$ sont décroissantes, soient $x, y \in E$. Si $x<y$, alors par hypothèse $0 \leqslant f(y) \leqslant f(x)$ et $0 \leqslant g(y) \leqslant g(x)$, donc $f(y) g(y) \leqslant f(x) g(x)$ par produit d'inégalités POSITIVES.
(iii) Dans le cas où $f$ est croissante et $g$ décroissante, soient $x, y \in E$. Si $x<y$, alors $f(x) \leqslant f(y)$ par croissance de $f$, puis $g(f(y)) \leqslant g(f(x))$ par décroissance de $g$.
(iv) Dans le cas croissant : $\forall x, y \in E, \quad x<y \quad \Longrightarrow \quad f(x) \leqslant f(y), \quad f$ est en fait strictement croissante, car si $f(x)=f(y)$, alors $x=y$ par injectivité.
Montrons que $f^{-1}$ est strictement croissante. Soient $y, y^{\prime} \in F$ deux réels pour lesquels $y<y^{\prime}$. Si jamais $f^{-1}(y) \geqslant f^{-1}\left(y^{\prime}\right)$, alors $y=f\left(f^{-1}(y)\right) \geqslant f\left(f^{-1}\left(y^{\prime}\right)\right)=y^{\prime}$ par croissance de $f-$ contradiction.

Exemple Pas besoin de dériver pour expliquer que les fonctions $x \longmapsto \mathrm{e}^{x}+x$ et $x \longmapsto \mathrm{e}^{y^{x}}$ sont croissantes sur $\mathbb{R}$ !

### 1.2 MAJORANTS/MINORANTS, MAXIMUM/MINIMUM

Définition (Fonction majorée/minorée/bornée) Soit $f: E \longrightarrow \mathbb{R}$ une fonction.

- On dit que $f$ est majorée si : $\exists M \in \mathbb{R}, \quad \forall x \in E, \quad f(x) \leqslant M$.

Un tel réel $M$ est appelé un majorant de $f$. On dit ausi que $f$ est majorée par $M$ ou que $M$ majore $f$.

- On dit que $f$ est minorée si : $\exists m \in \mathbb{R}, \quad \forall x \in E, \quad f(x) \geqslant m$.

Un tel réel $m$ est appelé UN minorant de $f$. On dit aussi que $f$ est minorée par $m$ ou que $m$ minore $f$.

- On dit que $f$ est bornée si $f$ est à la fois majorée et minorée, i.e. si : $\exists K \geqslant 0, \forall x \in E,|f(x)| \leqslant K$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-0.jpeg)

Démonstration La proposition « $f$ est majorée et minorée» s'écrit : $\exists m, M \in \mathbb{R}, \quad \forall x \in E, \quad m \leqslant f(x) \leqslant M$ et nous voulons montrer qu'elle est équivalente à la proposition : $\exists K \geqslant 0, \quad \forall x \in E, \quad|f(x)| \leqslant K$.

- Si pour un certain $K \geqslant 0$, il est vrai que $|f(x)| \leqslant K$ pour tout $x \in E$, alors $-K \leqslant f(x) \leqslant K$ pour tout $x \in E$, donc $f$ est minorée par $-K$ et majorée par $K$.
- Pour la réciproque, supposons $f$ minorée par $m$ et majorée par $M$ et posons $K=\max \{|m|,|M|\}$. Pour tout $x \in E: \quad-K \leqslant-|m| \leqslant m \leqslant f(x) \leqslant M \leqslant|M| \leqslant K, \quad \operatorname{donc}|f(x)| \leqslant K$.

Définition (Maximum/minimum d'une fonction) Soient $f: E \longrightarrow \mathbb{R}$ une fonction et $a \in E$.

- On dit que $f$ possède un maximum en a si : $\forall x \in E, \quad f(x) \leqslant f(a)$. Le réel $f(a)$ est alors appelé le maximum de $f$ et noté $\max _{x} f$ ou $\max _{x \in E} f(x)$.
- On dit que $f$ possède un minimum en a si : $\forall x \in E, \quad f(x) \geqslant f(a)$. Le réel $f(a)$ est alors appelé le minimum de $f$ et noté $\min _{E} f$ ou $\min _{x \in E} f(x)$.

En résumé, un maximum est un majorant de la forme « $f$ de quelqu'un », i.e. un majorant qui est aussi une valeur de $f$.

X Attention! Une fonction peut ne pas avoir de maximum ou de minimum, même en étant bornée, et quand elle en a un, il peut être atteint plusieurs fois.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-1.jpeg)

# 1.3 Transformations affines du graphe d'une fonction 

Dans le théorème qui suit, les fonctions sont représentés graphiquement dans un repère orthonormal $(O, \vec{\imath}, \vec{\jmath})$.

Théorème (Transformations affines du graphe d'une fonction) Soient $f: E \longrightarrow \mathbb{R}$ une fonction, $a, b \in \mathbb{R}$ et $\lambda>0$. On munit le plan d'un repère orthonormal direct $(O, \vec{\imath}, \vec{\jmath})$.

## - Symétries :

Le graphe de la fonction $x \longmapsto-f(x)$ s'obtient à partir de celui de $f$ par une symétrie par rapport à $(O x)$.
Le graphe de la fonction $x \longmapsto f(-x)$ s'obtient à partir de celui de $f$ par une symétrie par rapport à $(O y)$.

## - Translations :

Le graphe de la fonction $x \longmapsto f(x)+a$ s'obtient à partir de celui de $f$ par une translation de vecteur $a \vec{\jmath}$.
Le graphe de la fonction $x \longmapsto f(x+a)$ s'obtient à partir de celui de $f$ par une translation de vecteur $-a \vec{\imath}$.

## - Contractions/dilatations :

Le graphe de la fonction $x \longmapsto \lambda f(x)$ s'obtient à partir de celui de $f$ par une dilatation verticale de rapport $\lambda$ si $\lambda \geqslant 1$ et une contraction verticale de rapport $\frac{1}{\lambda}$ si $\lambda<1$.
Le graphe de la fonction $x \longmapsto f(\lambda x)$ s'obtient à partir de celui de $f$ par une contraction horizontale de rapport $\lambda$ si $\lambda \geqslant 1$ et une dilatation horizontale de rapport $\frac{1}{\lambda}$ si $\lambda<1$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-2.jpeg)

X Attention! Dans le cas de la fonction $x \longmapsto f(x+a)$, il y a un signe - dans l'expression du vecteur de translation $-a \vec{\imath}$ et c'est normal. La fonction $x \longmapsto f(x+a)$ atteint la valeur $f(0)$ en $-a$, puis la valeur $f(1)$ en $-a+1$, etc. En résumé, on peut dire que $x \longmapsto f(x+a)$ est EN AVANCE de $a$ sur $x \longmapsto f(x)$.

Exemple
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-3.jpeg)

Exemple Pour tous $a, x \in \mathbb{R}$, les réels $x$ et $a-x$ sont symétriques l'un de l'autre par rapport à $\frac{a}{2}$ car $\frac{a}{2}$ est le milieu du segment d'extrémités $x$ et $a-x: \frac{x+(a-x)}{2}=\frac{a}{2}$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-4.jpeg)

Donnons-nous à présent une fonction $f: E \longrightarrow \mathbb{R}$ et $a, b \in \mathbb{R}$. Comment peut-on représenter les fonctions $x \longmapsto a-f(x)$ et $x \longmapsto f(a-x)$ quand on connaît le graphe de $f$ ? Le graphe de la fonction $x \longmapsto a-f(x)$ s'obtient à partir de celui de $f$ par une symétrie par rapport à la droite d'équation $y=\frac{a}{2}$. Le graphe de la fonction $x \longmapsto f(a-x)$ s'obtient quant à lui à partir de celui de $f$ par une symétrie par rapport à la droite d'équation $x=\frac{a}{2}$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-5.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-6.jpeg)

Définition (Fonction paire/impaire) On suppose $E$ symétrique par rapport à 0 , i.e. que : $\forall x \in E, \quad-x \in E$.
Soit $f: E \longrightarrow \mathbb{R}$ une fonction.

- Parité : On dit que $f$ est paire si : $\quad \forall x \in E, \quad f(-x)=f(x)$.

Le graphe de $f$ est alors symétrique par rapport à l'axe des ordonnées.

- Imparité : On dit que $f$ est impaire si : $\quad \forall x \in E, \quad f(-x)=-f(x)$.

Le graphe de $f$ est alors symétrique par rapport à l'origine.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-7.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-8.jpeg)

Pas besoin d'étudier une fonction $f: E \longrightarrow \mathbb{R}$ paire ou impaire sur $E$ tout entier, une étude sur $E \cap \mathbb{R}_{+}$suffit.

Théorème (Réciproque d'une fonction bijective impaire) Soit $f: E \longrightarrow F$ une fonction bijective de $E$ sur $F$.
Si $E$ est symétrique par rapport à 0 et si $f$ est impaire, $F$ est symétrique par rapport à 0 et $f^{-1}$ est impaire.

Démonstration Soit $y \in F$, disons $y=f(x)$ pour un certain $x \in E$. Aussitôt, $-x \in E$ car $E$ est symétrique par rapport à 0 , donc $-y=-f(x)=f(-x) \in F$ par imparité de $f$. Conclusion : $F$ est symétrique par rapport à 0 . Ensuite : $\quad f^{-1}(-y)=f^{-1}(-f(x))=f^{-1}(f(-x))=-x=-f^{-1}(y), \quad$ donc $f^{-1}$ est impaire.

Définition (Fonction périodique) Soit $T>0$.
On suppose que $E$ est $T$-périodique, i.e. que : $\quad \forall x \in E, \quad x+T \in E \quad$ et $\quad x-T \in E$.
Soit $f: E \longrightarrow \mathbb{R}$ une fonction. On dit que $f$ est $T$-périodique ou périodique de période $T$ si : $\quad \forall x \in E, \quad f(x+T)=f(x)$. Le réel $T$ est alors appelé UNE période de $f$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-9.jpeg)

Pas besoin d'étudier une fonction $f: E \longrightarrow \mathbb{R} T$-périodique sur $E$ tout entier, une étude sur une période suffit, par exemple $E \cap[0, T[$.
$\mathbf{X}$ Attention！ Une fonction périodique ne possède jamais qu'une seule période. Tout multiple entier d'une période $T$ est encore une période : $2 T, \quad 3 T, \quad 4 T \ldots$ Voilà pourquoi on ne parle jamais de «la » période, mais toujours d'UNE période.

Certaines fonctions possèdent en revanche une plus petite période, mais pas toutes. On peut montrer que toute fonction continue non constante périodique possède une plus petite période. Les fonctions sinus et cosinus admettent par exemple $2 \pi$ pour plus petite période. Certaines fonctions admettent au contraire tout réel strictement positif pour période et n'en ont donc pas de plus petite. C'est le cas des fonctions constantes et de la fonction $\mathbb{1}_{Q}$.

- Théorème (Opérations sur les fonctions périodiques) Soit $T>0$. On suppose que $E$ est $T$-périodique. Soient $f: E \longrightarrow \mathbb{R}$ et $g: E \longrightarrow \mathbb{R}$ deux fonctions $T$-périodiques.
(i) Les fonctions $f+g$ et $f \times g$ sont aussi $T$-périodiques, ainsi que $\frac{f}{g}$ si $g$ ne s'annule pas.
(ii) Pour tout $\omega>0$, la fonction $x \longmapsto f(\omega x)$ est $\frac{T}{\omega}$-périodique sur l'ensemble dilaté/contracté $\frac{1}{\omega} E$.

Par exemple, pour $\omega=2$, le graphe de la fonction $x \longmapsto f(2 x)$ s'obtient à partir de celui de $f$ par une contraction horizontale de facteur 2. Si $f$ est $T$-périodique, rien d'étonnant du coup à ce que $x \longmapsto f(2 x)$ soit $\frac{T}{2}$-périodique.

# Démonstration 

(i) Concernant $f+g$, pour tout $x \in E: \quad(f+g)(x+T)=f(x+T)+g(x+T)=f(x)+g(x)=(f+g)(x)$.
(ii) Notons $g$ la fonction $x \longmapsto f(\omega x)$ définie sur $\{x \in \mathbb{R} \mid \omega x \in E\}=\frac{1}{\omega} E$. Pour tout $x \in \frac{1}{\omega} E$ :

$$
g\left(x+\frac{T}{\omega}\right)=f\left(\omega\left(x+\frac{T}{\omega}\right)\right)=f(\omega x+T)=f(\omega x)=g(x)
$$

## 2 CONTINUITÉ, DÉRIVABILITÉ, CONVEXITÉ/CONCAVITÉ

Les grands théorèmes d'analyse de cette partie seront démontrés plus tard dans l'année aux chapitres «Limites et continuité », «Dérivabilité et convexité » et «Intégration sur un segment».

### 2.1 CONTINUITÉ

Définition (Fonction continue) Soit $f: E \longrightarrow \mathbb{R}$ une fonction.
Pour tout $a \in E$, on dit que $f$ est continue en $a$ si $f(x) \xrightarrow[x \rightarrow a]{ } f(a)$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-10.jpeg)

On dit que $f$ est continue sur $E$ si $f$ est continue en tout point de $E$. L'ensemble des fonctions continues sur $E$ est noté $\mathscr{C}(E, \mathbb{R})$.

## Théorème (Opérations sur les fonctions continues)

- Combinaison linéaire, produit, quotient : Pour toutes fonctions $f, g \in \mathscr{C}(E, \mathbb{R})$ et $\lambda, \mu \in \mathbb{R}$, les fonctions $\lambda f+\mu g$ et $f g$ sont continues sur $E$, ainsi que $\frac{f}{g}$ si $g$ ne s'annule pas.
- Composition : Pour toutes fonctions $f \in \mathscr{C}(E, \mathbb{R})$ et $g \in \mathscr{C}(F, \mathbb{R})$, si $f(E) \subset F$, alors $g \circ f$ est continue sur $E$.
- Réciproque : Soient $I$ et $J$ deux intervalles. Pour toute fonction $f \in \mathscr{C}(I, \mathbb{R})$ bijective de $I$ sur $J, f^{-1}$ est continue sur $J$.

X Attention！ La composition est plus délicate à manier que l'addition et le produit car elle jongle avec plusieurs ensembles de définition. Ainsi, on ne peut pas dire que «la fonction $x \longmapsto \sqrt{x^{2}+1}$ est continue sur $\mathbb{R}$ comme composée de fonctions qui le sont» car $\sqrt{ }$ n'est pas continue sur $\mathbb{R}$ tout entier. Que dire alors? Par exemple ceci : «La fonction $x \longmapsto x^{2}+1$ est continue sur $\mathbb{R}$ À VALEURS DANS $\mathbb{R}_{+}$et $\sqrt{ }$ est continue sur $\mathbb{R}_{+}$, donc la fonction $x \longmapsto \sqrt{x^{2}+1}$ est continue sur $\mathbb{R}$.»

## Théorème (Théorème des valeurs intermédiaires ou TVI)

Soient $a$ et $b$ deux réels pour lesquels $a<b$ et $f \in \mathscr{C}([a, b], \mathbb{R})$.
Tout réel $y$ compris entre $f(a)$ et $f(b)$ possède au moins un antécédent par $f$ dans $[a, b]$, éventuellement plusieurs.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-11.jpeg)

Le TVI est un théorème d'existence - existence d'antécédent, existence de solutions pour les équations $y=f(x)$ d'inconnue $x$ avec $y$ fixé.

Le TVI gagne cela dit à être énoncé autrement. Sans rentrer dans les détails, un intervalle n'est jamais qu'une partie sans trou de $\mathbb{R}$, i.e. une partie qui, quand elle contient deux réels, contient tous les réels intermédiaires. Question : si $f$ est continue sur un intervalle $I$, son image $f(I)$ peut-elle contenir un trou? Un trou dans $f(I)$ serait le signe qu'un certain réel $y$ compris entre $f(a)$ et $f(b)$ avec $a, b \in I$ n'aurait pas d'antécédent par $f$, mais c'est exactement cela que le TVI interdit. Conclusion : $f(I)$ est forcément un intervalle quand $I$ en est un, du moins si $f$ est continue.

# Théorème (Image d'un intervalle par une fonction continue) 

- Version image d'un intervalle du TVI : Pour toute fonction $f \in \mathscr{C}(E, \mathbb{R})$ et tout intervalle $I$ inclus dans $E, f(I)$ est aussi un intervalle.
- En cas de monotonie, cet énoncé peut être rendu plus précis. Soient $a, b \in \mathbb{R}$ deux réels pour lesquels $a<b$.
- Si $f$ est continue et croissante sur $[a, b]$, alors $f([a, b])=[f(a), f(b)]$.
- Si $f$ est continue et décroissante sur $[a, b]$, alors $f([a, b])=[f(b), f(a)]$.
$X$ Attention！ En général : $\quad f([a, b]) \times[f(a), f(b)], \quad f(] a, b[) \times] f(a), f(b)[, \quad \ldots$
Par exemple, si $f$ est continue et croissante sur $] a, b[$ avec $f(x) \longrightarrow \alpha$ et $f(x) \longrightarrow \beta, f(] a, b[)$ peut être a priori n'importe lequel des intervalles $] \alpha, \beta[,[\alpha, \beta[,] \alpha, \beta]$ ou $[\alpha, \beta]$ comme on le voit ci-dessous.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-12.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-13.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-14.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-15.jpeg)

Par ailleurs, si $f$ n'est pas continue, l'image $f([a, b])$ n'a aucune raison d'être un intervalle, elle peut avoir des trous et posséder plusieurs morceaux. Enfin, même quand $f([a, b])$ est un intervalle, cet intervalle n'a aucune raison d'avoir $f(a)$ et $f(b)$ pour bornes si $f$ n'est pas monotone.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-16.jpeg)

En cas de CONTINUITÉ et STRICTE MONOTONIE, les égalités qui posaient problème à l'instant deviennent toutes vraies et le très important TVI strictement monotone va même plus loin en termes de bijectivité.

Théorème (TVI strictement monotone) Soient $a, b \in \mathbb{R}$ deux réels pour lesquels $a<b$.

- En cas de continuité et monotonie stricte, la forme des intervalles est correctement préservée. Par exemple :
- si $f$ est continue et strictement croissante sur $[a, b[$, alors $f([a, b[)=[f(a), \lim _{b} f[$,
- si $f$ est continue et strictement décroissante sur $] a, b[$, alors $f(] a, b[)=] \lim _{b} f, \lim _{a^{2}} f[$.
- TVI strictement monotone : Par exemple :
- si $f$ est continue et strictement croissante sur $[a, b], f$ est bijective de $[a, b]$ sur $[f(a), f(b)]$,
- si $f$ est continue et strictement décroissante sur $[a, b[, f$ est bijective de $[a, b[$ sur $] \lim _{a^{2}} f, f(a)]$,
- si $f$ est continue et strictement croissante sur $] a, b[, f$ est bijective de $] a, b[$ sur $] \lim _{a^{2}} f, \lim _{b} f[$.

Par rapport au TVI de base, la stricte monotonie apporte l'injectivité, donc l'unicité dès lors qu'on s'intéresse aux équations $y=f(x)$ d'inconnue $x$ avec $y$ fixé.

À défaut de pouvoir démontrer le TVI et son corollaire strictement monotone maintenant, nous pouvons en comprendre dès maintenant les tenants et les aboutissants.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-17.jpeg)

En pratique, le TVI et sa version strictement monotone sont très utiles quand on cherche des points fixes.

Étudier les POINTS FIXES de $f$, c'est étudier les ZÉROS de $x \longmapsto f(x)-x$, i.e. résoudre l'équation $f(x)-x=0$ d'inconnue $x$.

Exemple La fonction $x \longmapsto \mathrm{e}^{-x}$ possède un et un seul point fixe sur $\mathbb{R}$.
Démonstration La fonction $x \xrightarrow{f} \mathrm{e}^{-x}-x$ est continue et strictement décroissante sur $\mathbb{R}$ par somme des fonctions $x \longmapsto \mathrm{e}^{-x}$ et $x \longmapsto-x$ qui le sont. Par ailleurs, $f(x) \xrightarrow[x \rightarrow+\infty]{ }-\infty$ et $f(x) \xrightarrow[x \rightarrow-\infty]{ }+\infty$, donc $f$ s'annule une et une seule fois sur $\mathbb{R}$ d'après le TVI strictement monotone.

# 2.2 DÉRIVABILITÉ ET DÉRIVÉES SUCCESSIVES 

Définition (Fonction dérivable, tangente) Soit $f: E \longrightarrow \mathbb{R}$ une fonction.

- Dérivabilité : Pour tout $a \in E$, on dit que $f$ est dérivable en $a$ si la fonction $x \longmapsto \frac{f(x)-f(a)}{x-a}$ possède une limite finie en $a$, notée $f^{\prime}(a)$ le cas échéant et appelée le nombre dérivé de $f$ en $a$.

On dit que $f$ est dérivable sur $E$ si $f$ est dérivable en tout point de $E$. Le cas échéant, la fonction $x \longmapsto f^{\prime}(x)$ est appelée la dérivée de $f$. L'ensemble des fonctions dérivables sur $E$ est noté $\mathscr{D}(E, \mathbb{R})$.

- Tangente : Pour tout $a \in E$ en lequel $f$ est dérivable en $a$, la droite d'équation $y=f(a)+f^{\prime}(a)(x-a)$ est appelée la tangente de $f$ en $a$.

Si $f$ est dérivable en $a$ et si $x$ est proche de $a$, alors $\frac{f(x)-f(a)}{x-a} \approx f^{\prime}(a)$, donc $f(x) \approx f(a)+f^{\prime}(a)(x-a)$. À défaut d'être rigoureux, c'est convaincant. La tangente de $f$ en $a$ est ainsi la droite la plus proche du graphe de $f$ au voisinage de $a$.

Géométriquement, $\frac{f(x)-f(a)}{x-a}$ est le coefficient directeur de la corde reliant les points de coordonnées $(a, f(a))$ et $(x, f(x))$. Après passage à la limite, le réel $f^{\prime}(a)=\lim _{x \rightarrow a} \frac{f(x)-f(a)}{x-a}$ est donc la «pente limite» des cordes en question.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-18.jpeg)

## Attention！ <br> La notation $(f(x))^{\prime}$ est INTERDITE！

La quantité $f(x)$ dépend de $x$, c'est une EXPRESSION et non pas une FONCTION. Pour la dériver, on a besoin de préciser par rapport à quelle variable on dérive. Notez désormais simplement $\frac{\mathrm{d}}{\mathrm{d} x}(f(x))$ ce que vous auriez aimé noter $(f(x))^{\prime}$.

Théorème (Dérivable implique continue) Soient $f: E \longrightarrow \mathbb{R}$ une fonction et $a \in E$. Si $f$ est dérivable en $a$, alors $f$ est continue en $a$.

X Attention! La réciproque est fausse! Les fonctions valeur absolue et racine carrée sont continues en 0 , mais n'y sont pas dérivables. Le graphe de $|\cdot|$ présente un pic en 0 et celui de $\sqrt{ }$. une tangente verticale.

Démonstration Si $f$ est dérivable en $a$ :

$$
f(x)=\frac{f(x)-f(a)}{x-a} \times(x-a)+f(a) \underset{x \rightarrow a}{\longrightarrow} f^{\prime}(a) \times 0+f(a)=f(a)
$$

![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-19.jpeg)

Décrêt est continue en $a$.

Définition (Dérivées successives) Soit $f: E \longrightarrow \mathbb{R}$ une fonction. On pose $f^{(0)}=f$.
Ensuite, pour tout $k \in \mathbb{N}^{*}$, si on a réussi à définir $f^{(k-1)}$ de proche en proche et si elle est dérivable sur $E$, on dit que $f$ est $k$ fois dérivable sur $E$ et on pose $f^{(k)}=\left(f^{(k-1)}\right)^{\prime}$. La fonction $f^{(k)}$ est alors appelée la dérivée $k^{\text {ème }}$ de $f$.

On préfère généralement les notations $f, f^{\prime}, f^{\prime \prime}$ et $f^{\prime \prime \prime}$ aux notations $f^{(0)}, f^{(1)}, f^{(2)}$ et $f^{(3)}$.
$X$ Attention！ La notation $(f(x))^{\prime \prime}$ est INTERDITE！Notez $\frac{\mathrm{d}^{k}}{\mathrm{~d} x^{k}}(f(x))$ ce que vous auriez aimé noter $(f(x))^{(k)}$.

Exemple Soit $n \in \mathbb{N}$. La fonction $x \xrightarrow{f} x^{n}$ est indéfiniment dérivable sur $\mathbb{R}$ et pour tous $k \in \mathbb{N}$ et $x \in \mathbb{R}$ :

$$
f^{(k)}(x)=\left\{\begin{array}{cl}
n(n-1) \ldots(n-k+1) x^{n-k}=\frac{n!}{(n-k)!} x^{n-k} & \text { si } k \leqslant n \\
0 & \text { si } k>n
\end{array}\right.
$$

Définition (Fonction de classe $\mathscr{C}^{k}$ ) Soit $f: E \longrightarrow \mathbb{R}$ une fonction.

- Classe $\mathscr{C}^{k}$ : Pour tout $k \in \mathbb{N}$, on dit que $f$ est de classe $\mathscr{C}^{k}$ sur $E$ si $f$ est $k$ fois dérivable sur $E$ et si $f^{(k)}$ est continue sur $E$. L'ensemble des fonctions de classe $\mathscr{C}^{k}$ sur $E$ est noté $\mathscr{C}^{k}(E, \mathbb{R})$.
- Classe $\mathscr{C}^{\infty}$ : On dit que $f$ est de classe $\mathscr{C}^{\infty}$ sur $E$ si $f$ est $k$ fois dérivable sur $E$ pour tout $k \in \mathbb{N}$. L'ensemble des fonctions de classe $\mathscr{C}^{\infty}$ sur $E$ est noté $\mathscr{C}^{\infty}(E, \mathbb{R})$.


# $X$ Attention！ 

De classe $\mathscr{C}^{1}=$ Dérivable à dérivée continue $\neq$ Dérivable ET continue.

Maladroit, donc à éviter,
Car la dérivabilité implique la continuité!
Sur la figure ci-dessous, chaque flèche décrit une implication.
Classe $\mathscr{C}^{\infty} \longrightarrow \cdots \longrightarrow$ Classe $\mathscr{C}^{2} \longrightarrow$ Dérivabilité deux fois $\longrightarrow$ Classe $\mathscr{C}^{1} \longrightarrow$ Dérivabilité $\longrightarrow$ Continuité (Classe $\mathscr{C}^{0}$ )

## Théorème (Opérations sur les fonctions dérivables/ $k$ fois dérivables/de classe $\mathscr{C}^{k}$ )

- Combinaison linéaire, produit, quotient : Pour toutes fonctions $f, g \in \mathscr{D}(E, \mathbb{R})$ et $\lambda, \mu \in \mathbb{R}$, les fonctions $\lambda f+\mu g$ et $f g$ sont dérivables sur $E$, ainsi que $\frac{f}{g}$ si $g$ ne s'annule pas. En outre :

$$
(\lambda f+\mu g)^{\prime}=\lambda f^{\prime}+\mu g^{\prime}, \quad(f g)^{\prime}=f^{\prime} g+f g^{\prime} \quad \text { et } \quad\left(\frac{f}{g}\right)^{\prime}=\frac{f^{\prime} g-f g^{\prime}}{g^{2}}
$$

- Composition : Pour toutes fonctions $f \in \mathscr{D}(E, \mathbb{R})$ et $g \in \mathscr{D}(F, \mathbb{R})$, si $f(E) \subset F$, alors $g \circ f$ est dérivable sur $E$ et :

$$
(g \circ f)^{\prime}=f^{\prime} \times g^{\prime} \circ f
$$

- Réciproque : Soient $I$ et $J$ deux intervalles. Pour toute fonction $f \in \mathscr{D}(I, \mathbb{R})$ bijective de $I$ sur $J$, si $f^{\prime}$ NE s'ANNULE PAS SUR $I$, alors $f^{-1}$ est dérivable sur $J$ et $\left(f^{-1}\right)^{\prime}=\frac{1}{f^{\prime} \circ f^{-1}}$.
On peut remplacer partout «dérivable» par « $k$ fois dérivable» pour tout $k \in \mathbb{N}$ ou par «de classe $\mathscr{C}^{k}$ » pour tout $k \in \mathbb{N} \cup\{\infty\}$, mais les formules énoncées ne sont valables que pour les dérivées premières.

Démonstration La dérivabilité de $f^{-1}$ demande du travail, mais la formule de dérivation en découle aisément. En dérivant simplement la relation $f \circ f^{-1}=\operatorname{Id}_{J}$, on obtient $\left(f^{-1}\right)^{\prime} \times f^{\prime} \circ f^{-1}=1$.

# X Attention！ 

- Pour la dérivabilité de $f^{-1}$, l'hypothèse de non-annulation de $f^{\prime}$ est cruciale! Sur la figure ci-contre, $f^{\prime}$ s'annule en $a$, donc $f$ possède une tangente horizontale en $a$. Il en découle que $f^{-1}$ possède une tangente verticale en $f(a)$, donc n'est pas dérivable en $f(a)$.
- On n'a pas besoin de dériver 99 fois une fonction pour savoir qu'elle est 100 fois dérivable! Par exemple, la fonction $x \longmapsto x^{2} \mathrm{e}^{x}$ est de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$ pour la seule raison que les fonctions $x \longmapsto x^{2}$ et $x \longmapsto \mathrm{e}^{x}$ le sont.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-20.jpeg)

Exemple La fonction $x \stackrel{f}{\longmapsto} \ln (x+\sqrt{x(1-x)})$ est définie et continue sur $] 0,1]$ et dérivable sur $] 0,1[$.
Démonstration

- Ensemble de définition :

$$
\begin{gathered}
\{x \in \mathbb{R} \mid x(1-x) \geqslant 0 \text { et } x+\sqrt{x(1-x)}>0\} \\
=\{x \in \mathbb{R} \mid x \in[0,1] \text { et } x>0\}=] 0,1]
\end{gathered}
$$

| $x$ | $-\infty$ | 0 | 1 | $+\infty$ |
| :--: | :--: | :--: | :--: | :--: |
| $x$ | - | 0 | + |  |
| $1-x$ |  | + | 0 | - |
| $x(1-x)$ | - | 0 | + |  |

- Ensemble de continuité : Les fonctions usuelles utilisées pour construire $f$ sont toutes continues en tout point en lequel elles sont définies, donc $f$ est continue sur $] 0,1]$.
- Ensemble de dérivabilité : La fonction racine carrée est dérivable seulement sur $\mathbb{R}_{+}^{*}$. La fonction $f$ est donc dérivable sur $\{x \in \mathbb{R} \mid x(1-x)>0$ et $x+\sqrt{x(1-x)}>0\}=] 0,1[$.
Attention, nous n'avons pas prouvé la non-dérivabilité de $f$ en 1. Les résultats du théorème précédent nous parlent de dérivabilité mais pas de NON-dérivabilité. Pour étudier la dérivabilité de $f$ en 1, il faudrait revenir à la définition en termes de taux d'accroissement, mais nous ne le ferons pas.

Exemple La fonction $x \stackrel{f}{\longmapsto} \frac{1}{x-1}$ est de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R} \backslash\{1\}$, et pour calculer ses dérivées successives, il vaut mieux l'écrire comme une PUISSANCE NÉGATIVE que comme un quotient. En l'occurrence, pour tous $k \in \mathbb{N}$ et $x \in \mathbb{R} \backslash\{1\}$ :

$$
f^{(k)}(x)=\frac{\mathrm{d}^{k}}{\mathrm{~d} x^{k}}\left((x-1)^{-1}\right)=(-1)(-2) \ldots(-k)(x-1)^{-k-1}=\frac{(-1)^{k} k!}{(x-1)^{k+1}}
$$

Théorème (Caractérisation des fonctions dérivables constantes/monotones) Soient I un INTERVALLE et $f \in \mathscr{D}(I, \mathbb{R})$. On ne traite ci-dessous que le cas des fonctions croissantes.

- Constance : $f$ est constante sur $I$ si et seulement si $f^{\prime}$ est nulle sur $I$.
- Monotonie : $f$ est croissante sur $I$ si et seulement si $f^{\prime}$ est positive (ou nulle) sur $I$.
- Monotonie stricte : $f$ est strictement croissante sur $I$ si et seulement si $f^{\prime}$ est positive (ou nulle) sur $I$ et n'est identiquement nulle sur aucun intervalle $[a, b]$ inclus dans $I$ avec $a<b$.

En particulier, si $f^{\prime}$ est strictement positive sur $I, f$ est strictement croissante sur $I$.

X Attention！Mine de rien, il est indispensable que $I$ soit un intervalle.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-21.jpeg)

On montre beaucoup d'inégalités en mathématiques, et l'une des premières techniques qu'on apprend à ce sujet, c'est l'étude des variations ou du signe d'une fonction, dont voici plusieurs exemples.

À ce stade, c'est pour leur signe qu'on calcule des dérivées, donc...

# Démonstration 

- Tentative naïve : Pour tout $x \in[0,2], 0 \leqslant x^{2} \leqslant 4$ donc $3 \leqslant x^{2}+3 \leqslant 7$, et par ailleurs $1 \leqslant x+1 \leqslant 3$, donc par quotient : $\frac{1}{7} \leqslant \frac{x+1}{x^{2}+3} \leqslant \frac{3}{3}=1$. Hélas, c'est moins fin que le résultat attendu. En encadrant séparément le numérateur et le dénominateur, on obtient rarement des encadrements de qualité.
- Étude d'une fonction : La fonction $x \xrightarrow{f} \frac{x+1}{x^{2}+3}$ est définie et dérivable sur $\mathbb{R}$ et pour tout $x \in \mathbb{R}$ :
$f^{\prime}(x)=\frac{1 \times\left(x^{2}+3\right)-(x+1) \times 2 x}{\left(x^{2}+3\right)^{2}}=-\frac{x^{2}+2 x-3}{\left(x^{2}+3\right)^{2}}=-\frac{(x-1)(x+3)}{(x^{2}+3)^{2}}}{\text { On conclut grâce au tableau ci-contre car } f(0)=\frac{1}{3} \leqslant \frac{3}{7}=f(2) .}$
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-22.jpeg)

Exemple Pour tout $x \in \mathbb{R}_{+}^{*} \searrow\{1\}: \quad \frac{x+1}{x-1} \ln x \geqslant 2$.
Démonstration On pourrait étudier la fonction $x \longmapsto \frac{x+1}{x-1} \ln x$ et la comparer à 2 , mais la dérivée d'un quotient occasionne souvent d'affreux calculs, donc étudions plutôt le signe de $x \xrightarrow{f}(x+1) \ln x-2(x-1)$ sur $\mathbb{R}_{+}^{*}$. Nous diviserons par $x-1$ à la fin pour obtenir le signe de $x \longmapsto \frac{x+1}{x-1} \ln x-2$.
Pour tout $x>0: \quad f^{\prime}(x)=\ln x+\frac{1}{x}-1 \quad$ et $\quad f^{\prime \prime}(x)=\frac{x-1}{x^{2}}$.
On conclut grâce au tableau ci-contre.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-23.jpeg)

Exemple Pour tous $x, y \in]-1,1\left[: \quad \frac{x+y}{1+x y} \in\right]-1,1[$.
Démonstration Pour prouver une inégalité de deux variables, on en fixe une, par exemple $y$, et on fait une étude de fonction par rapport à l'autre variable, ici $x$. Fixons donc $y \in]-1,1[$.
La fonction $x \stackrel{f}{\longmapsto} \frac{x+y}{1+x y}$ est dérivable sur $\mathbb{R} \backslash\left\{-\frac{1}{y}\right\}$, donc sur $]-1,1\left[\operatorname{car}-\frac{1}{y} \notin\right]-1,1[$, et pour tout $x \in]-1,1\left[: \quad f^{\prime}(x)=\frac{1-y^{2}}{(1+x y)^{2}}>0\right.$.
On conclut grâce au tableau ci-contre.

### 2.3 CONVEXITÉ/CONCAVITÉ

Soient $I$ un intervalle $I, f: I \longrightarrow \mathbb{R}$ une fonction et $x, y \in \mathbb{R}$. Quand $\lambda$ décrit $[0,1], \lambda(y-x)$ décrit le segment d'extrémités 0 et $y-x$, donc $(1-\lambda) x+\lambda y=x+\lambda(y-x)$ décrit le segment
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-24.jpeg)
d'extrémités $x+0=x$ et $x+(y-x)=y$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-25.jpeg)

De la même manière, quand $\lambda$ décrit $[0,1],(1-\lambda) f(x)+\lambda f(y)$ décrit le segment d'extrémités $f(x)$ et $f(y)$, et dans le plan, le point de coordonnées $\left((1-\lambda) x+\lambda y,(1-\lambda) f(x)+\lambda f(y)\right)$ décrit le segment d'extrémités $(x, f(x))$ et $(y, f(y))$, appelé une corde de $f$.

Définition (Fonction convexe/concave) Soient $I$ un intervalle et $f: I \longrightarrow \mathbb{R}$ une fonction.

- Fonction convexe : On dit que $f$ est convexe si son graphe est situé en-dessous de toutes ses cordes, i.e. si :

$$
\forall x, y \in I, \quad \forall \lambda \in[0,1], \quad f((1-\lambda) x+\lambda y) \leqslant(1-\lambda) f(x)+\lambda f(y)
$$

- Fonction concave : On dit que $f$ est concave si son graphe est situé au-dessus de toutes ses cordes, i.e. si :

$$
\forall x, y \in I, \quad \forall \lambda \in[0,1], \quad f((1-\lambda) x+\lambda y) \geqslant(1-\lambda) f(x)+\lambda f(y)
$$

Il est équivalent de dire que $-f$ est convexe.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-26.jpeg)

Exemple La fonction valeur absolue est convexe sur $\mathbb{R}$ car pour tous $x, y \in \mathbb{R}$ et $\lambda \in[0,1]$, d'après l'inégalité triangulaire :

$$
|(1-\lambda) x+\lambda y| \leqslant|1-\lambda| \cdot|x|+|\lambda| \cdot|y|=(1-\lambda)|x|+\lambda|y|
$$

- Théorème (Caractérisation des fonctions convexes dérivables) Soient $I$ un intervalle et $f \in \mathscr{D}(I, \mathbb{R})$. Les assertions suivantes sont équivalentes :
(i) $f$ est convexe sur $I$.
(ii) $f^{\prime}$ est croissante sur $I$ - ou bien $f^{\prime \prime} \geqslant 0$ si $f$ est deux fois dérivable sur $I$.
(iii) Le graphe de $f$ est situé au-dessus de toutes ses tangentes.

On dispose bien sûr d'une caractérisation analogue de la concavité.

Démonstration (Implication (ii) $\Longrightarrow$ (iii)) Supposons $f^{\prime}$ croissante et fixons $a \in I$. Montrons que le graphe de $f$ est situé au-dessus de sa tangente en $a$, i.e. que $f(x) \geqslant f^{\prime}(a)(x-a)+f(a)$ pour tout $x \in I$. Notons pour cela $\varphi$ la fonction $x \longmapsto f(x)-f^{\prime}(a)(x-a)-f(a)$. Cette fonction est dérivable sur $I$ et pour tout $x \in I$ : $\varphi^{\prime}(x)=f^{\prime}(x)-f^{\prime}(a), \quad$ donc par croissance de $f^{\prime}, \varphi^{\prime}$ est négative à gauche de $a$ et positive à droite. Ainsi, $\varphi$ est décroissante à gauche de $a$ et croissante à droite, donc positive sur $I$ tout entier puisque $\varphi(a)=0$.

Exemple Soit $n \in \mathbb{N}$. La fonction puissance $x \longmapsto x^{2 n}$ est convexe sur $\mathbb{R}$ car sa dérivée seconde $x \longmapsto 2 n(2 n-1) x^{2(n-1)}$ est positive sur $\mathbb{R}$.

Exemple Pour tout $x>0: \quad \sqrt{x} \leqslant \frac{x+1}{2}$.
Démonstration La fonction $x \longmapsto \sqrt{x}$ est concave sur $\mathbb{R}_{+}^{*}$ car sa dérivée $x \longmapsto \frac{1}{2 \sqrt{x}}$ y est décroissante. Son graphe est situé sous sa tangente en 1, d'équation $y=\frac{x+1}{2}$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-27.jpeg)

Définition-théorème (Point d'inflexion) Soient $I$ un intervalle, $f: I \longrightarrow \mathbb{R}$ une fonction et $a \in I$ un point qui n'est pas une borne de $I$. On dit que $f$ possède un point d'inflexion en a si $f$ est convexe au voisinage de $a$ à gauche et concave au voisinage de $a$ à droite - ou l'inverse.
Si $f$ est deux fois dérivable sur $I, f$ possède un point d'inflexion en $a$ si et seulement si $f^{\prime \prime}$ s'annule en $a$ et est positive au voisinage de $a$ à gauche et négative au voisinage de $a$ à droite - ou l'inverse.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-28.jpeg)

Exemple Soit $n \in \mathbb{N}$. La fonction puissance $x \longmapsto x^{2 n+1}$ possède un et un seul point d'inflexion, à savoir en 0 , car sa dérivée seconde $x \longmapsto 2 n(2 n+1) x^{2 n-1}$, s'annule en changeant de signe en 0 et ne le fait nulle part ailleurs.

Exemple Soient $a \in \mathbb{R}^{*}$ et $b, c, d \in \mathbb{R}$. La fonction $x \longmapsto a x^{3}+b x^{2}+c x+d$ possède un et un seul point d'inflexion, à savoir en $-\frac{b}{3 a}$, car sa dérivée seconde $x \longmapsto 6 a x+2 b$ s'annule en changeant de signe en $-\frac{b}{3 a}$ et ne le fait nulle part ailleurs.

# 3 LOGARITHME, EXPONENTIELLE, PUISSANCES 

### 3.1 FONCTIONS AFFINES, POLYNOMIALES ET RATIONNELLES

Théorème (La seule formule à connaître sur les fonctions affines) Le graphe d'une fonction affine $f$ est une droite, donc coïncide avec sa tangente en tout point. Ainsi, pour tous $a, x \in \mathbb{R}: \quad f(x)=f^{\prime}(a)(x-a)+f(a)$.

X Attention! On vous a habitués à utiliser l'ordonnée à l'origine $p$ d'une fonction affine $x \stackrel{f}{\longleftrightarrow} m x+p$, mais la plupart du temps, on se fiche royalement de ce qui se passe à l'origine. Si vous connaissez la pente $m$ de $f$ et sa valeur en un point $a, f$ a pour expression $x \longmapsto m(x-a)+f(a)$.

Exemple Quelle fonction affine $f$ envoie 1 sur 3 et 2 sur 5 ? De pente $\frac{f(2)-f(1)}{2-1}=2, f$ a tout simplement pour expression $x \longmapsto 2(x-1)+3=2 x+1$. Aucun calcul supplémentaire !

Concernant les fonctions puissances $x \longmapsto x^{n}$ avec $n \in \mathbb{Z}$, rappelons simplement l'allure de leurs graphes.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-29.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-30.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-31.jpeg)
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-32.jpeg)

Rappelons également qu'on appelle fonction rationnelle tout quotient d'une fonction polynomiale par une fonction polynomiale non nulle, par exemple $x \longmapsto \frac{x+1}{x^{2}+2}$. En particulier, les fonctions polynomiales sont rationnelles. Enfin, pour calculer la limite en $+\infty$ ou $-\infty$ d'une fonction polynomiale ou rationnelle, on factorise par le terme de plus haut degré au numérateur et au dénominateur, puis on simplifie. Par exemple :
$4 x^{5}-x^{4}+5=\underbrace{4 x^{5}}_{x \rightarrow+\infty} \times \underbrace{\left(1-\frac{1}{4 x}+\frac{5}{4 x^{5}}\right)}_{x \rightarrow+\infty} \xrightarrow[x \rightarrow+\infty]{ }+\infty \quad$ et $\quad \frac{x^{2}+2 x+1}{3 x^{2}-1}=\frac{x^{2}\left(1+\frac{2}{x}+\frac{1}{x^{2}}\right)}{3 x^{2}\left(1-\frac{1}{3 x^{2}}\right)}=\frac{1}{3} \times \frac{1+\frac{2}{x}+\frac{1}{x^{2}}}{1-\frac{1}{3 x^{2}}} \xrightarrow[x \rightarrow+\infty]{ } \frac{1}{3}$.

# 3.2 FonCTIONS LOGARITHME ET EXPONENTIELLE 

## Définition-théorème (Fonction logarithme)

- Définition et régularité : La fonction logarithme $\ln$ est définie, de classe $\mathscr{C}^{\infty}$ et concave sur $\mathbb{R}_{+}^{*}$. Pour tout $x>0: \quad \ln ^{\prime}(x)=\frac{1}{x} \quad$ et $\quad \ln (1)=0$.
- Transformation des produits en sommes :

Pour tous $x, y>0: \quad \ln (x y)=\ln x+\ln y \quad$ et $\quad \ln \frac{1}{x}=-\ln x$.

- Constante de Néper : La fonction logarithme prend la valeur 1 en un unique réel e appelé parfois la constante de Néper: $\quad \mathrm{e} \approx 2,71828$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-33.jpeg)
- Croissances comparées en 0 et $+\infty: \quad \frac{\ln x}{x} \xrightarrow[x \rightarrow+\infty]{ } 0 \quad$ et $\quad x \ln x \xrightarrow[x \rightarrow 0]{ } 0$.
- Comportement au voisinage de 1 :

Le graphe du logarithme est situé sous sa tangente en 1 :

$$
\left\{\begin{array}{l}
\forall x>0, \quad \ln x \leqslant x-1 \\
\forall x>-1, \quad \ln (1+x) \leqslant x
\end{array}\right.
$$

En outre, $\frac{\ln x}{x-1} \xrightarrow{x \rightarrow 1} 1$ et $\frac{\ln (1+x)}{x} \xrightarrow[x \rightarrow 0]{ } 1$, i.e. intuitivement : $\left\{\begin{array}{l}\ln x \approx x-1 \text { pour } x \text { proche de } 1 \\ \ln (1+x) \approx x \text { pour } x \text { proche de } 1 .\end{array}\right.$

Par définition du nombre dérivé : $\frac{\ln x}{x-1} \xrightarrow[x \rightarrow 1]{ } \ln ^{\prime}(1)=1, \quad$ donc $\ln x \approx x-1$ pour $x$ proche de 1. Par exemple, $\ln (1,1) \approx 0,09531$ et $\ln (1,01) \approx 0,00995$.

Les limites $\frac{\ln x}{x} \xrightarrow[x \rightarrow+\infty]{ } 0$ et $x \ln x \xrightarrow[x \rightarrow 0]{ } 0$ sont quant à elles des formes indéterminées $\frac{+\infty}{+\infty}$ et $0 \times(+\infty)$ au premier abord, mais le combat de $x$ et $\ln x$ est gagné par $x$ dans les deux cas.

Démonstration D'après le théorème fondamental du calcul intégral que nous démontrerons plus tard, toute fonction continue sur un intervalle y possède des primitives. La fonction inverse possède donc des primitives sur $\mathbb{R}_{+}^{*}$, mais plus précisément une et une seule primitive qui envoie 1 sur 0 et c'est elle que nous noterons $\ln$.

- Variations et signe : La fonction $\ln$ est de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}_{+}^{*}$ car sa dérivée $x \longmapsto \frac{1}{x}$ l'est, mais cette dérivée est aussi strictement positive, donc $\ln$ est strictement croissante sur $\mathbb{R}_{+}^{*}$. Comme $\ln (1)=0, \ln$ est strictement négative sur $] 0,1[$ et strictement positive sur $] 1,+\infty[$.
- Concavité et position par rapport à la tangente en 1 : Sa dérivée $x \longmapsto \frac{1}{x}$ y étant décroissante, $\ln$ est concave sur $\mathbb{R}_{+}^{*}$. Or sa tangente en 1 a pour équation $y=\ln ^{\prime}(1)(x-1)+\ln (1)=x-1$, donc $\ln x \leqslant x-1$ pour tout $x>0$.
- Transformation des produits en sommes : Fixons $y>0$ et notons $\varphi$ la fonction $x \longmapsto \ln (x y)-\ln x-\ln y$ dérivable sur $\mathbb{R}_{+}^{*}$. Pour tout $x>0: \quad \varphi^{\prime}(x)=\frac{y}{x y}-\frac{1}{x}=0, \quad$ donc $\varphi$ est constante de valeur $\varphi(1)=0$, donc $\ln (x y)=\ln x+\ln y$ pour tout $x>0$. En particulier : $\quad \ln x+\ln \frac{1}{x}=\ln (1)=0, \quad$ donc $\ln \frac{1}{x}=-\ln x$.
- Croissances comparées : Pour tout $x \geqslant 1: \quad \ln x=\ln (\sqrt{x})^{2}=2 \ln \sqrt{x} \leqslant 2(\sqrt{x}-1) \leqslant 2 \sqrt{x}, \quad$ donc : $0 \leqslant \frac{\ln x}{x} \leqslant \frac{2}{\sqrt{x}}, \quad$ et ainsi $\frac{\ln x}{x} \xrightarrow[x \rightarrow+\infty]{ } 0$ par encadrement.

Ensuite, si on pose $t=\frac{1}{x}: \quad x \ln x=-x \ln \frac{1}{x}=-\frac{\ln t}{t}, \quad$ or $\frac{1}{x} \xrightarrow[x \rightarrow 0^{+}]{\ }+\infty$ et $\frac{\ln t}{t} \xrightarrow[t \rightarrow+\infty]{ } 0$, donc $x \ln x \underset{x \rightarrow 0}{ } 0$ par composition.

- Limites en 0 et $+\infty$ : D'après le théorème de la limite monotone pour les fonctions que vous ne connaissez pas et que nous prouverons plus tard, toute fonction croissante sur $\mathbb{R}_{+}^{s}$ possède une limite en $+\infty$, éventuellement $+\infty$. La fonction $\ln$ possède donc une limite $\ell$ en $+\infty$. Supposons par l'absurde que $\ell$ est un réel. Dans la relation $\ln (x y)=\ln x+\ln y$, fixons $x>0$ et faisons tendre $y$ vers $+\infty$. Cela donne $\ell=\ln x+\ell$, donc $\ln x=0$ pour tout $x>0$, mais cette égalité contredit la stricte croissance de $\ln$, donc $\ell=+\infty$. Il en découle par composition que : $\quad \ln x=-\ln \frac{1}{x} \xrightarrow[x \rightarrow 0^{+}]{\ }-\infty$.
- Définition de la constante de Néper : La fonction $\ln$ est continue et strictement croissante sur $\mathbb{R}_{+}^{s}$ de limites $-\infty$ et $+\infty$ aux bornes, donc bijective de $\mathbb{R}_{+}^{s}$ sur $\mathbb{R}$ d'après le TVI strictement monotone. En particulier, 1 possède donc un et un seul antécédent par $\ln$, noté e.


# Définition-théorème (Fonction exponentielle) 

- Définition : La fonction logarithme est bijective de $\mathbb{R}_{+}^{s}$ sur $\mathbb{R}$. On appelle fonction exponentielle et on note exp sa réciproque, bijective de $\mathbb{R}$ sur $\mathbb{R}_{+}^{s}$. En particulier : $\quad \exp (1)=\mathrm{e} \quad$ et les graphes des fonctions exp et $\ln$ sont symétriques l'un de l'autre par rapport à la droite d'équation $y=x$.
Pour tout $x \in \mathbb{R}: \quad \ln (\exp (x))=x \quad$ et pour tout $x>0: \quad \exp (\ln x)=x$.
- Régularité : La fonction exponentielle exp est de classe $\mathscr{C}^{\infty}$ et convexe sur $\mathbb{R}$ et $\exp ^{\prime}=\exp$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-34.jpeg)
- Transformation des sommes en produits :

Pour tous $x, y \in \mathbb{R}: \quad \exp (x+y)=\exp (x) \exp (y) \quad$ et $\quad \exp (-x)=\frac{1}{\exp (x)}$.

- Croissances comparées en $+\infty: \quad \frac{x}{\exp (x)} \xrightarrow[x \rightarrow+\infty]{ } 0$.
- Comportement au voisinage de 0 :

Le graphe de l'exponentielle est situé au-dessus sa tangente en $0: \quad \forall x \in \mathbb{R}, \quad \exp (x) \geqslant 1+x$.
En outre, $\frac{\exp (x)-1}{x} \xrightarrow[x \rightarrow 0]{ } 1$, i.e. intuitivement $\exp (x)-1 \approx x$ pour $x$ proche de 0 .

Je me suis forcé à noter $\exp (x)$ plutôt que $\mathrm{e}^{x}$ l'exponentielle de $x$, mais dans cinq minutes, nous pourrons la noter $\mathrm{e}^{x}$.
Par définition du nombre dérivé : $\quad \frac{\exp (x)-1}{x} \xrightarrow[x \rightarrow 0]{ } \exp ^{\prime}(0)=1, \quad$ donc $\exp (x)-1 \approx x$ pour $x$ proche de 1. Par exemple, $\exp (0,1) \approx 1,10517$ et $\exp (0,01) \approx 1,01005$.

Démonstration Nous avons déjà tiré du TVI strictement monotone la bijectivité de $\ln$ de $\mathbb{R}_{+}^{s}$ sur $\mathbb{R}$. Cela justifie à la fois la définition de l'exponentielle et sa régularité. En effet, $\ln$ est de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}_{+}^{s}$ et SA DÉRIVÉe $x \longmapsto \frac{1}{x}$ NE s'y ANNULE PAS, donc d'après le théorème de dérivabilité d'une réciproque, $\ln ^{-1}=\exp$ est de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$ de dérivée $\exp ^{\prime}=\left(\ln ^{-1}\right)^{\prime}=\frac{1}{\ln ^{\prime} \circ \ln ^{-1}}=\ln ^{-1}=\exp$. En particulier, $\exp ^{\prime}$ est croissante sur $\mathbb{R}$, donc exp y est convexe, donc $\exp (x) \geqslant \exp ^{\prime}(0) x+\exp (0)=x+1$ pour tout $x \in \mathbb{R}$, autrement dit le graphe est au-dessus de la tangente en 0 . Nous laisserons de côté les autres vérifications par souci de légèreté.

### 3.3 Fonctions PUISSANCES

Nous n'avons défini jusqu'ici que les puissances $x^{n}$ pour $n$ ENTIER. La notation classique $\mathrm{e}^{x}$ n'est-elle cependant pas celle d'une puissance, me direz-vous? Oui et non, car le réel $\mathrm{e}^{x}$ n'est pas «e multiplié $x$ fois par lui-même ». Que signifierait «e multiplié $\sqrt{2}$ fois par lui-même »? ! Voilà pourquoi, au paragraphe précédent, je me suis momentanément interdit la notation $\mathrm{e}^{x}$, mais nous pouvons maintenant généraliser proprement notre définition des puissances.

Définition (Puissances quelconques et racines $n^{\text {èmes }}$ d'un réel strictement positif) Soit $x>0$.

- Puissances quelconques : Pour tout $y \in \mathbb{R}$, on appelle $x$ puissance $y$ le réel $x^{y}=\exp (y \ln x)$.
- Racines $n^{\text {èmes }}$ : Pour tout $n \in \mathbb{N}^{*}$, le réel $x^{\frac{1}{n}}$ est appelé la racine $n^{\text {ème }} d e x$ et noté $\sqrt[n]{x}$.

Pour $x=\mathrm{e}$, cette définition signifie que $\mathrm{e}^{y}=\exp (y \ln \mathrm{e})=\exp (y)$ pour tout $y \in \mathbb{R}$. Ouf, nous pouvons noter l'exponentielle comme une puissance!

En résumé, la notation puissance n'est qu'une notation. Pour $y$ non entier, $x^{y}$ n'est pas le produit $y$ fois de $x$. Quand vous manipulez une puissance quelconque, ayez toujours en tête qu'un logarithme et une exponentielle sont cachés derrière.

X Attention！ La définition $x^{y}=\mathrm{e}^{y \ln x}$ n'est valable que pour $x$ strictement positif à cause du logarithme.
Exemple Pour tout $x>1: \quad x^{\frac{\ln \ln x}{\ln x}}=\mathrm{e}^{\frac{\ln \ln x}{\ln x} \times \ln x}=\mathrm{e}^{\ln \ln x}=\ln x$.

# Théorème (Propriétés algébriques des puissances) 

(i) La nouvelle définition des puissances généralise bien l'ancienne.
(ii) Pour tous $x, x^{\prime}>0$ et $y, y^{\prime} \in \mathbb{R}$ :

$$
\ln \left(x^{y}\right)=y \ln x, \quad x^{y+y^{\prime}}=x^{y} x^{y^{\prime}}, \quad x^{y y^{\prime}}=\left(x^{y}\right)^{y^{\prime}}, \quad\left(x x^{\prime}\right)^{y}=x^{y} x^{\prime y} \quad \text { et } \quad x^{-y}=\frac{1}{x^{y}}=\left(\frac{1}{x}\right)^{y}
$$

## Démonstration

(i) Pour tous $x>0$ et $n \in \mathbb{N}: \quad \mathrm{e}^{n \ln x}=\overbrace{\ln x+\ldots+\ln x}^{n \text { termes }}=\overbrace{\mathrm{e}^{\ln x} \times \ldots \times \mathrm{e}^{\ln x}}^{n \text { termes }}=\overbrace{x \ldots x}^{n \text { termes }}, \quad$ donc la notation traditionnelle $x^{n}$ et notre nouvelle notation $x^{n}$ coïncident. Même chose dans le cas d'un entier négatif.
(ii) $\quad \ln \left(x^{y}\right)=\ln \left(\mathrm{e}^{y \ln x}\right)=y \ln x, \quad x^{y+y^{\prime}}=\mathrm{e}^{\left(y+y^{\prime}\right) \ln x}=\mathrm{e}^{y \ln x+y^{\prime} \ln x}=\mathrm{e}^{y \ln x} \mathrm{e}^{y^{\prime} \ln x}=x^{y} x^{y^{\prime}}$, $x^{y y^{\prime}}=\mathrm{e}^{y y^{\prime} \ln x}=\mathrm{e}^{y^{\prime} \ln \left(x^{y}\right)}=\left(x^{y}\right)^{y^{\prime}}, \quad\left(x x^{\prime}\right)^{y}=\mathrm{e}^{y \ln \left(x x^{\prime}\right)}=\mathrm{e}^{y \ln x+y \ln x^{\prime}}=\mathrm{e}^{y \ln x} \mathrm{e}^{y \ln x^{\prime}}=x^{y} x^{\prime y}$, $x^{-y}=\mathrm{e}^{-y \ln x}=\frac{1}{\mathrm{e}^{y \ln x}}=\frac{1}{x^{y}} \quad$ et $\quad x^{-y}=\mathrm{e}^{-y \ln x}=\mathrm{e}^{y \ln \left(\frac{1}{x}\right)}=\left(\frac{1}{x}\right)^{y}$.

Théorème (Étude des fonctions puissances) Soient $\alpha, \beta \in \mathbb{R}$.
(i) Régularité : La fonction $x \longmapsto x^{\alpha}$ est définie et de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}_{+}^{*}$ de dérivée $x \longmapsto \alpha x^{\alpha-1}$.
Elle est concave si $\alpha \in[0,1]$ et convexe sinon.
(ii) Positions relatives : $\left\{\begin{array}{ll}\text { Pour tout } x \in] 0,1]: & \alpha \leqslant \beta \quad \Longrightarrow \quad x^{\beta} \leqslant x^{\alpha} \\ \text { Pour tout } x \in[1,+\infty[: & \alpha \leqslant \beta \quad \Longrightarrow \quad x^{\alpha} \leqslant x^{\beta}\end{array}\right.$.
(iii) Prolongement par continuité en 0 : Pour $\alpha>0$, on pose $0^{\alpha}=0$. La fonction $x \longmapsto x^{\alpha}$ ainsi prolongée est continue sur $\mathbb{R}_{+}$tout entier, y compris en 0 . On dit qu'on a prolongé par continuité la fonction $x \longmapsto x^{\alpha}$ en 0 .
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-35.jpeg)

Ainsi, pour $x \in] 0,1]: \quad \ldots \leqslant x^{2} \leqslant x \leqslant 1 \leqslant \frac{1}{x} \leqslant \frac{1}{x^{2}} \leqslant \frac{1}{x^{3}} \leqslant \ldots$ et pour $x \geqslant 1: \quad \ldots \leqslant \frac{1}{x^{2}} \leqslant \frac{1}{x} \leqslant 1 \leqslant x \leqslant x^{2} \leqslant x^{3} \leqslant \ldots$
$\mathbf{X}$ Attention！Pour $\alpha \in] 0,1\left[\right.$, la fonction $x \longmapsto x^{\alpha}$ est continue en 0 après prolongement, mais elle possède en 0 une tangente verticale, signe qu'elle n'est pas dérivable en 0 . C'est typiquement ce qui arrive à la fonction racine carrée.

## Démonstration

(i) Pour tout $x>0: \quad \frac{\mathrm{d}}{\mathrm{d} x}\left(x^{\alpha}\right)=\frac{\mathrm{d}}{\mathrm{d} x}\left(\mathrm{e}^{\alpha \ln x}\right)=\frac{\alpha}{x} \times \mathrm{e}^{\alpha \ln x}=\alpha x^{-1} x^{\alpha}=\alpha x^{\alpha-1}$.

A fortiori : $\quad \frac{\mathrm{d}^{2} f}{\mathrm{~d} x^{2}}\left(x^{\alpha}\right)=\alpha(\alpha-1) x^{\alpha-2}, \quad$ donc la dérivée seconde de $x \longmapsto x^{\alpha}$ est négative sur $\mathbb{R}_{+}^{*}$ si $\alpha \in[0,1]$ et positive si $\alpha \in]-\infty, 0] \cup[1,+\infty[$.
(ii) Soient $x>0$ et $\alpha, \beta \in \mathbb{R}$ avec $\alpha \leqslant \beta$.
— Si $x \in] 0,1]$, alors $\ln x \leqslant 0$, donc $\beta \ln x \leqslant \alpha \ln x$, donc $x^{\beta}=\mathrm{e}^{\beta \ln x} \leqslant \mathrm{e}^{\alpha \ln x}=x^{\alpha}$.
— Si $x \in[1,+\infty[$, alors $\ln x \geqslant 0$, donc $\alpha \ln x \leqslant \beta \ln x$, donc $x^{\alpha}=\mathrm{e}^{\alpha \ln x} \leqslant \mathrm{e}^{\beta \ln x}=x^{\beta}$.
(iii) Pour $\alpha>0: \quad x^{\alpha}=\mathrm{e}^{\alpha \ln x} \xrightarrow[x \rightarrow 0]{ } 0=0^{\alpha}, \quad$ donc la fonction $x \longmapsto x^{\alpha}$ est continue en 0 .

- Théorème (Croissances comparées des fonctions logarithme, exponentielle et puissances) Le principe général, c'est que l'exponentielle est plus puissante que les puissances, qui sont elles-mêmes plus puissantes que le logarithme. Précisément, pour tous $\alpha>0$ et $\beta \in \mathbb{R}: \quad \frac{x^{\beta}}{\mathrm{e}^{x}} \xrightarrow[x \rightarrow+\infty]{ } 0, \quad \frac{(\ln x)^{\beta}}{x^{\alpha}} \xrightarrow[x \rightarrow+\infty]{ } 0 \quad$ et $\quad x^{\alpha}|\ln x|^{\beta} \xrightarrow[x \rightarrow 0]{ } 0$.

Démonstration Montrons seulement la deuxième limite. Le résultat est clair si $\beta \leqslant 0$, car sachant que $\alpha>0$, $\lim _{x \rightarrow+\infty}(\ln x)^{\beta} \in\{0,1\}$ et $x^{\alpha} \xrightarrow[x \rightarrow+\infty]{ }+\infty$. Supposons désormais $\beta>0$. Le calcul qui suit a l'air affreux, mais on essaie juste de se ramener à la limite $\frac{\ln u}{u} \xrightarrow[u \rightarrow+\infty]{ } 0$. Pour tout $x>0$, si on pose $u=x^{\frac{\alpha}{\beta}}$ et $v=\frac{\ln u}{u}$ :

$$
\frac{(\ln x)^{\beta}}{x^{\alpha}}=\left(\frac{\ln x}{x^{\frac{\alpha}{\beta}}}\right)^{\beta}=\left(\frac{\frac{\beta}{\alpha} \times \ln x^{\frac{\alpha}{\beta}}}{x^{\frac{\alpha}{\beta}}}\right)^{\beta}=\left(\frac{\beta}{\alpha}\right)^{\beta}\left(\frac{\ln u}{u}\right)^{\beta}=\left(\frac{\beta}{\alpha}\right)^{\beta} v^{\beta}
$$

Or ici $x^{\frac{\alpha}{\beta}} \xrightarrow[x \rightarrow+\infty]{ }+\infty$ car $\frac{\alpha}{\beta}>0$. Également, $\frac{\ln u}{u} \xrightarrow[u \rightarrow+\infty]{ } 0$ et $v^{\beta} \xrightarrow[v \rightarrow 0]{ } 0$ car $\beta>0$, donc $\frac{(\ln x)^{\beta}}{x^{\alpha}} \xrightarrow[x \rightarrow+\infty]{ } 0$
par composition.

# 3.4 FonCTIONS HYPERBOLIQUES ch, sh ET th 

## Définition-théorème (Fonctions cosinus hyperbolique et sinus hyperbolique)

Pour tout $x \in \mathbb{R}$, on appelle cosinus hyperbolique de $x$ le réel $\operatorname{ch} x=\frac{\mathrm{e}^{x}+\mathrm{e}^{-x}}{2}$ et sinus hyperbolique de $x$ le réel $\operatorname{sh} x=\frac{\mathrm{e}^{x}-\mathrm{e}^{-2}}{2}$.
Pour tout $x \in \mathbb{R}: \quad \operatorname{ch}^{2} x-\operatorname{sh}^{2} x=1$.
Les fonctions ch et sh, respectivement paire et impaire, sont définies et de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$ avec : $\quad \mathrm{ch}^{\prime}=\mathrm{sh} \quad$ et $\quad \mathrm{sh}^{\prime}=\mathrm{ch}$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-36.jpeg)

La fonction ch est convexe. La fonction sh est concave sur $\mathbb{R}_{-}$et convexe sur $\mathbb{R}_{+}$avec un point d'inflexion en 0 .

Démonstration Les variations de ch et sh sont étudiées dans le tableau ci-dessous et pour tout $x \in \mathbb{R}$ : $\operatorname{ch}^{2} x-\operatorname{sh}^{2} x=(\operatorname{ch} x+\operatorname{sh} x)(\operatorname{ch} x-\operatorname{sh} x)=\mathrm{e}^{x} \mathrm{e}^{-x}=1$.

Exemple L'équation $\operatorname{ch} x=2$ d'inconnue $x \in \mathbb{R}$ possède deux solutions qu'on sait calculer explicitement.

Démonstration Les équations $\operatorname{ch} x=y$ et $\operatorname{sh} x=y$ d'inconnue $x$ à $y$ fixé se ramènent aisément à des équations du second degré. Pour tout $x \in \mathbb{R}$ :

$$
\begin{aligned}
& \operatorname{ch} x=2 \quad \Longleftrightarrow \quad \mathrm{e}^{x}-4+\mathrm{e}^{-x}=0 \quad \stackrel{x \in^{x}}{\Longleftrightarrow}\left(\mathrm{e}^{x}\right)^{2}-4 \mathrm{e}^{x}+1=0 \\
& \Longleftrightarrow \quad \mathrm{e}^{x}=2+\sqrt{3} \quad \text { ou } \quad \mathrm{e}^{x}=2-\sqrt{3} \\
& \Longleftrightarrow \quad x=\ln (2+\sqrt{3}) \quad \text { ou } \quad x=\ln (2-\sqrt{3}) .
\end{aligned}
$$

| $x$ | $-\infty$ | 0 | $+\infty$ |
| :--: | :--: | :--: | :--: |
| $\operatorname{ch} x$ |  | + |  |
| $\operatorname{sh} x$ |  | 0 |  |
| $\operatorname{sh} x$ | - | 0 | + |
| $\operatorname{ch} x$ |  | 1 |  |

## Définition-théorème (Fonction tangente hyperbolique)

La fonction tangente hyperbolique $\mathrm{th}=\frac{\mathrm{sh}}{\mathrm{ch}}$ est définie sur $\mathbb{R}$.
Elle est impaire et de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$ et : $\quad \mathrm{th}^{\prime}=1-\mathrm{th}^{2}=\frac{1}{\mathrm{ch}^{2}}$.
Elle est convexe sur $\mathbb{R}_{-}$et concave sur $\mathbb{R}_{+}$avec un point d'inflexion en 0 .
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-37.jpeg)

Elle possède enfin une asymptote d'équation $y=1$ au voisinage de $+\infty$ (resp. $y=-1$ au voisinage de $-\infty$ ).

Démonstration La fonction th est de classe $\mathscr{C}^{\infty}$ par quotient et :

$$
\mathrm{th}^{\prime}=\frac{\mathrm{sh}^{\prime} \mathrm{ch}-\mathrm{ch}^{\prime} \mathrm{sh}}{\mathrm{ch}^{2}}=\frac{\mathrm{ch}^{2}-\mathrm{sh}^{2}}{\mathrm{ch}^{2}}, \quad \text { quantité qui vaut à la fois } \frac{1}{\mathrm{ch}^{2}} \text { et } 1-\frac{\mathrm{sh}^{2}}{\mathrm{ch}^{2}}=1-\mathrm{th}^{2}
$$

La stricte croissance en découle. En outre, par composition, la dérivée $\frac{1}{\mathrm{ch}^{2}}$ est croissante sur $\mathbb{R}_{-}$et décroissante sur $\mathbb{R}_{+}$, donc th est convexe sur $\mathbb{R}_{-}$et concave sur $\mathbb{R}_{+}$.
Pour la limite en $+\infty: \quad \operatorname{th} x=\frac{\operatorname{sh} x}{\operatorname{ch} x}=\frac{\mathrm{e}^{x}-\mathrm{e}^{-x}}{\mathrm{e}^{x}+\mathrm{e}^{-x}}=\frac{1-\mathrm{e}^{-2 x}}{1+\mathrm{e}^{-2 x}} \xrightarrow[x \rightarrow+\infty]{ } 1$.

# 4 DEUX OU TROIS GRANDS PRINCIPES DE CALCUL DES LIMITES 

Un calcul de limite se mène toujours en deux temps :

- Dans un premier temps, on analyse l'expression étudiée en comparant de tête la taille des termes qui la composent. Qui est grand? Qui est petit? Qui disparaît au profit de qui? Cette étape de défrichement doit être effectuée rapidement sans trop de rigueur formelle, par exemple au moyen du symbole $\approx$, mais attention, ce symbole flou ne prouve jamais rien, il prépare juste le terrain du calcul rigoureux.
- Dans un deuxième temps, on traduit l'analyse précédente en calcul rigoureux. Les techniques de bases consistent à factoriser par le terme dominant et à exploiter les croissances comparées usuelles en $\pm \infty$ et certaines approximations de fonctions usuelles tirées de nombres dérivés. À ce sujet, le point important, c'est que si $f$ est dérivable en $a$ avec $f^{\prime}(a) \neq 0$, alors $f(x)-f(a) \approx f^{\prime}(a)(x-a) \operatorname{car} \frac{f(x)-f(a)}{x-a} \xrightarrow[x \rightarrow a]{ } f^{\prime}(a)$.

Exemple Vérifiez que vous comprenez bien les approximations suivantes :

- pour $x$ très grand : $\mathrm{e}^{x}+x^{2} \approx \mathrm{e}^{x}, \quad 3 x^{2}-x+1 \approx 3 x^{2}, \quad \frac{(x+\ln x) \mathrm{e}^{x}}{\mathrm{e}^{2 x}+\sqrt{x}} \approx x \mathrm{e}^{-x}, \quad \frac{|x|}{x^{2}+1} \approx \frac{1}{x} \quad$ et $\quad \operatorname{ch} x \approx \operatorname{sh} x \approx \frac{\mathrm{e}^{x}}{2}$.
- pour $x$ proche de $0: \quad \ln (1+x) \approx x, \quad \mathrm{e}^{x}-1 \approx x, \quad \operatorname{sh} x \approx x, \quad \frac{x+\ln (1+x)}{\ln (1+3 x)} \approx \frac{2}{3} \quad$ et $\quad \mathrm{e}^{3 x}-\mathrm{e}^{x}+x^{2} \approx 2 x$.

Attention！ Il faut y réfléchir à deux fois quand on veut composer une relation $f_{1}(x) \approx f_{2}(x)$ par une fonction $g$, car en général : $\quad g \circ f_{1}(x) \times g \circ f_{2}(x)$. Tâchons de le comprendre sur l'exemple des fonctions logarithme et exponentielle.

- Pour $x$ très grand : $\mathrm{e}^{x}+1 \approx \mathrm{e}^{x}, \quad$ mais comment le logarithme affecte-t-il les grandes quantités? Le logarithme tasse les infinis. Sur l'intervalle $\left[\mathrm{e}^{x}, \mathrm{e}^{x}+1\right]$ de longueur 1 , le logarithme est presque constant, donc $\ln \left(\mathrm{e}^{x}+1\right) \approx \ln \mathrm{e}^{x}=x$.
- Pour $x$ très grand : $\quad x+\ln x \approx x, \quad$ mais comment l'exponentielle affecte-t-elle les grandes quantités? L'exponentielle écarte les infinis. Par exemple, $x+\ln 2 \approx x$ mais $\mathrm{e}^{x+\ln 2}=2 \mathrm{e}^{x} \times \mathrm{e}^{x}$. L'intervalle $[x, x+\ln 2]$ a beau être de longueur $\ln 2$ seulement, l'exponentielle y est terriblement croissante. La situation est encore pire sur $[x, x+\ln x]$, dont la longueur $\ln x$ tend vers $+\infty$ avec $x: \quad \mathrm{e}^{x+\ln x}=x \mathrm{e}^{x} \times \mathrm{e}^{x}$.
Rappelons ici qu'en dépit de ces mises en garde, le symbole $\approx$ ne tient jamais lieu de preuve, il défriche le terrain.

Exemple $\frac{x^{2}}{x+\sqrt{x}} \xrightarrow[x \rightarrow+\infty]{ }+\infty$.
Démonstration Au brouillon, pour $x$ très grand : $\quad x+\sqrt{x} \approx x, \quad$ donc $\frac{x^{2}}{x+\sqrt{x}} \approx \frac{x^{2}}{x}=x \longrightarrow+\infty$. Rapide et convaincant, mais pas du tout rigoureux. Sur une copie :

$$
\frac{x^{2}}{x+\sqrt{x}}=\frac{x^{2}}{x\left(1+\frac{1}{\sqrt{x}}\right)}=\frac{x}{1+\frac{1}{\sqrt{x}}} \xrightarrow[x \rightarrow+\infty]{ }+\infty \quad \text { et rien de plus. }
$$

Exemple $\frac{\ln \left(\mathrm{e}^{x}+1\right)}{\mathrm{e}^{x+\ln x}+1} \xrightarrow[x \rightarrow+\infty]{ } 0$.
Démonstration Au brouillon, pour $x$ très grand : $\quad \ln \left(\mathrm{e}^{x}+1\right) \approx \ln \mathrm{e}^{x}=x \quad$ et $\quad \mathrm{e}^{x+\ln x}+1=x \mathrm{e}^{x}+1 \approx x \mathrm{e}^{x}$, donc $\frac{\ln \left(\mathrm{e}^{x}+1\right)}{\mathrm{e}^{x+\ln x}+1} \approx \frac{x}{x \mathrm{e}^{x}}=\mathrm{e}^{-x} \longrightarrow 0$. Sur une copie :

$$
\frac{\ln \left(\mathrm{e}^{x}+1\right)}{\mathrm{e}^{x+\ln x}+1}=\frac{\ln \mathrm{e}^{x}+\ln \left(1+\mathrm{e}^{-x}\right)}{x \mathrm{e}^{x}\left(1+\frac{1}{x \mathrm{e}^{x}}\right)}=\frac{1+\frac{\ln \left(1+\mathrm{e}^{-x}\right)}{x}}{\mathrm{e}^{x}\left(1+\frac{1}{x \mathrm{e}^{x}}\right)} \xrightarrow[x \rightarrow+\infty]{ } 0
$$

Exemple $\left(\sqrt{x^{2}+x}-\sqrt{x}\right) \xrightarrow[x \rightarrow+\infty]{ }+\infty \quad$ et $\quad\left(\sqrt{x^{2}+x}-\sqrt{x^{2}-x}\right) \xrightarrow[x \rightarrow+\infty]{ } 1$.
Démonstration Les deux quantités se ressemblent, mais elles sont très différentes en réalité.

- Première limite : Pour $x$ très grand : $\quad \sqrt{x^{2}+x} \approx \sqrt{x^{2}}=x, \quad$ donc $\sqrt{x^{2}+x}-\sqrt{x} \approx x \longrightarrow+\infty$.

Sur une copie : $\quad \sqrt{x^{2}+x}-\sqrt{x}=x\left(\sqrt{1+\frac{1}{x}}-\frac{1}{\sqrt{x}}\right) \xrightarrow[x \rightarrow+\infty]{ } 0$.

- Deuxième limite : Pour $x$ très grand, $\sqrt{x^{2} \pm x} \approx \sqrt{x^{2}}=x$, donc problème! Les quantités $\sqrt{x^{2}+x}$ et $\sqrt{x^{2}-x}$ se détruisent mutuellement par soustraction, mais que reste-t-il? Par exemple, quand on soustrait deux réels proches de 1000, que reste-t-il? Ça dépend de ce qu'on soustrait : $1010-1000=10$ et $1000,001-1000=0,001, \quad$ et pourtant 1010 et 1000,001 sont tous les deux proches de 1000.
La technique de la quantité conjuguée, qui repose sur l'identité remarquable $(a+b)(a-b)=a^{2}-b^{2}$, nous permet de mesurer la taille du reste après soustraction :

$$
\sqrt{x^{2}+x}-\sqrt{x^{2}-x}=\frac{\left(x^{2}+x\right)-\left(x^{2}-x\right)}{\sqrt{x^{2}+x}+\sqrt{x^{2}-x}}=\frac{2 x}{x\left(\sqrt{1+\frac{1}{x}}+\sqrt{1-\frac{1}{x}}\right)}=\frac{2}{\sqrt{1+\frac{1}{x}}+\sqrt{1-\frac{1}{x}}} \xrightarrow[x \rightarrow+\infty]{ } \frac{2}{1+1}=1
$$

Exemple $\quad \frac{\ln (1+x)}{x+\operatorname{sh} x} \xrightarrow[x \rightarrow 0]{ } \frac{1}{2}$.
Démonstration Au brouillon, pour $x$ proche de $0: \quad \ln (1+x) \approx x \quad$ et $\quad \operatorname{sh} x \approx x, \quad$ donc $x+\operatorname{sh} x \approx 2 x$,
donc $\frac{\ln (1+x)}{x+\operatorname{sh} x} \approx \frac{x}{2 x}=\frac{1}{2}$. Sur une copie : $\quad \frac{\ln (1+x)}{x+\operatorname{sh} x}=\frac{\frac{\ln (1+x)}{x}}{1+\frac{\operatorname{sh} x}{x}} \xrightarrow[x \rightarrow 0]{ } \frac{1}{1+1}=\frac{1}{2}$.
Et si on avait voulu calculer $\lim _{x \rightarrow 0} \frac{x^{2}}{x-\operatorname{sh} x}$ ? C'est plus compliqué car au dénominateur, $x$ et $\operatorname{sh} x$ ont à peu près la même taille. Que reste-t-il après soustraction? Nous ne le savons pas à ce stade de l'année et nous ne pouvons donc pas encore calculer cette limite.

# $X$ Attention！ $1^{+\infty}$ est une nouvelle forme indéterminée！ 

Exemple $\quad(1+x)^{\frac{1}{x}} \xrightarrow[x \rightarrow 0]{ } \mathrm{e}$.
Démonstration Il est tentant d'analyser la situation ainsi : $\quad 1^{+\infty}=1, \quad$ mais c'est très faux ! Pour faire communiquer correctement $1+x$ et son exposant $\frac{1}{x}$, plaçons-les AU MÊME NIVEAU, i.e. au sommet d'une exponentielle. Aussitôt : $\quad(1+x)^{\frac{1}{x}}=\mathrm{e}^{\frac{\ln (1+x)}{x}} \xrightarrow[x \rightarrow 0]{ } \mathrm{e}^{1}=\mathrm{e}$.

X Attention！Dans un calcul de limite, aucun théorème de substitution ne permet de remplacer un morceau par sa limite sans toucher au reste.

Par exemple, si $f(x) \xrightarrow[x \rightarrow+\infty]{ } 2$, il n'est pas du tout possible d'affirmer, contrairement à ce que vous pensez souvent, que : $\lim _{x \rightarrow+\infty} \frac{x}{x+f(x)}=\lim _{x \rightarrow+\infty} \frac{x}{x+2}=1 \quad$ et $\quad \lim _{x \rightarrow+\infty} f(x)^{x}=\lim _{x \rightarrow+\infty} 2^{x}=+\infty$. En d'autres termes, on ne peut pas remplacer $f(x)$ par sa limite 2 dans les expressions $\frac{x}{x+f(x)}$ et $f(x)^{x}$ quand $x$ tend vers $+\infty$. Par exemple, $(1+x) \xrightarrow[x \rightarrow 0]{ } 1$ mais $\lim _{x \rightarrow 0}(1+x)^{\frac{1}{x}}=\mathrm{e} \neq 1=\lim _{x \rightarrow 0} 1^{\frac{1}{x}}$.

## 5 FonCTIONS TRIGONOMÉTRIQUES

Soit $\alpha \in \mathbb{R}$. Comme nous l'avons déjà vu, la relation $\equiv[\alpha]$ de congruence modulo $\alpha$ est une relation d'équivalence sur $\mathbb{R}$. Rappelons qu'elle est définie pour tous $x, y \in \mathbb{R}$ par l'équivalence : $\quad x \equiv y[\alpha] \quad \Longleftrightarrow \quad \exists k \in \mathbb{Z}, \quad x=y+k \alpha$.

Pour tout $\beta \in \mathbb{R}$, la classe d'équivalence de $\beta$ pour $\equiv[\alpha]$ est l'ensemble $\{x \in \mathbb{R} \mid x \equiv \beta[\alpha]\}=\{\beta+k \alpha \mid \quad k \in \mathbb{Z}\}$ et on le note $\beta+\alpha \mathbb{Z}$. Plus généralement, pour toute partie $E$ de $\mathbb{R}$, on note $E+\alpha \mathbb{Z}$ l'ensemble :

$$
\{x+k \alpha \mid \quad k \in \mathbb{Z}\}=\bigcup_{x \in E}(x+\alpha \mathbb{Z})=\bigcup_{k \in \mathbb{Z}}(E+k \alpha)
$$

![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-38.jpeg)

Exemple On obtient $\rceil-\frac{\pi}{2}, \frac{\pi}{2}\left[+\pi \mathbb{Z}\right.$ en répétant $\rceil-\frac{\pi}{2}, \frac{\pi}{2}[$ tous les $\pi$.
Le résultat final est presque $\mathbb{R}$ tout entier, mais pas tout à fait : $\rceil-\frac{\pi}{2}, \frac{\pi}{2}\left[+\pi \mathbb{Z}=\mathbb{R} \backslash\left(\frac{\pi}{2}+\pi \mathbb{Z}\right)\right.$.
Exemple L'ensemble $\frac{\pi}{4}+\pi \mathbb{Z}$ est $\pi$-périodique, donc rencontre l'intervalle $[0,3 \pi[$ de longueur $3 \pi$ en exactement trois points : $\left(\frac{\pi}{4}+\pi \mathbb{Z}\right) \cap\left[0,3 \pi\left[=\left\{\frac{\pi}{4}, \frac{5 \pi}{4}, \frac{9 \pi}{4}\right\}\right.\right.$.

Exemple On s'intéresse à la réunion $A=\left(\frac{\pi}{5}+\frac{\pi}{2} \mathbb{Z}\right) \cup \frac{\pi}{3} \mathbb{Z}$. L'ensemble $\frac{\pi}{5}+\frac{\pi}{2} \mathbb{Z}$ est $\frac{\pi}{2}$-périodique, donc $\frac{k \pi}{2}$-périodique pour tout $k \in \mathbb{N}^{*}$. De même, $\frac{\pi}{3} \mathbb{Z}$ est $\frac{l \pi}{3}$-périodique pour tout $l \in \mathbb{N}^{*}$. Ces deux ensembles ont donc une période commune si on arrive à trouver deux entiers $k, l \in \mathbb{N}^{*}$ pour lesquels $\frac{k \pi}{2}=\frac{l \pi}{3}$, i.e. $3 k=2 l$. Or les entiers $k=2$ et $l=3$ conviennent et on ne peut pas les choisir plus petits. Conclusion : $\frac{\pi}{5}+\frac{\pi}{2} \mathbb{Z}$ et $\frac{\pi}{3} \mathbb{Z}$ admettent $2 \times \frac{\pi}{2}=3 \times \frac{\pi}{3}=\pi$ pour période commune, donc $A$ est $\pi$-périodique. Pour comprendre $A$, il nous suffit dès lors de le décrire sur une seule période, par exemple $[0, \pi[$, puis de translater indéfiniment tous les $\pi$. En d'autres termes : $\quad A=(A \cap[0, \pi[)+\pi \mathbb{Z}=\left\{\frac{\pi}{5}, \frac{\pi}{5}+\frac{\pi}{2}, 0, \frac{\pi}{3}, \frac{2 \pi}{3}\right\}+\pi \mathbb{Z}$.

# 5.1 FonCTIONS COSINUS, SINUS ET TANGENTE 

## Définition-théorème (Lien du cosinus et du sinus avec le cercle trigonométrique)

- Lien avec le cercle trigonométrique : Pour tout $\theta \in \mathbb{R}: \quad \cos ^{2} \theta+\sin ^{2} \theta=1$.

Réciproquement, pour tout couple $(x, y) \in \mathbb{R}^{2}$ pour lequel $x^{2}+y^{2}=1$, il existe un réel $\theta$, unique modulo $2 \pi$, pour lequel $(x, y)=(\cos \theta, \sin \theta)$. En termes géométriques, tout point du cercle trigonométrique a des coordonnées de la forme $(\cos \theta, \sin \theta)$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-39.jpeg)

- Transformations affines : Les relations suivantes se lisent toutes sur le cercle trigonométrique. Pour tout $x \in \mathbb{R}$ :

$$
\begin{aligned}
& \cos (x+\pi)=-\cos x \quad \cos (\pi-x)=-\cos x \quad \cos \left(\frac{\pi}{2}-x\right)=\sin x \quad \cos \left(x+\frac{\pi}{2}\right)=-\sin x \\
& \sin (x+\pi)=-\sin x \quad \sin (\pi-x)=\sin x \quad \sin \left(\frac{\pi}{2}-x\right)=\cos x \quad \sin \left(x+\frac{\pi}{2}\right)=\cos x \\
& \text { Ajouter } \pi \text { dans un cosinus ou un sinus } \\
& \text { revient à le multiplier par }-1 \text {. }
\end{aligned}
$$

$\frac{\pi}{2}-x$ est LA transformation à utiliser quand on veut remplacer un cosinus par un sinus et vice versa.
Ainsi, pour tout $k \in \mathbb{Z}: \quad \cos (x+k \pi)=(-1)^{k} \cos x \quad$ et $\quad \sin (x+k \pi)=(-1)^{k} \sin x$.

## Attention！ $\cos x=\cos y \quad x=y$.

À peine mieux : $\quad \cos x=\cos y \quad x \equiv y[2 \pi]$.

Exemple Pour tout $x \in \mathbb{R}: \quad \cos x=\sin x \quad \Longleftrightarrow \quad x \equiv \frac{\pi}{4}[\pi]$.
Démonstration Cette équivalence se lit bien sur le cercle trigonométrique, mais on peut aussi la démontrer par le calcul. Pour tout $x \in \mathbb{R}: \quad \cos x=\sin x \quad \Longleftrightarrow \quad \sin \left(\frac{\pi}{2}-x\right)=\sin x \quad$ impossible

$$
\Longleftrightarrow \quad \frac{\pi}{2}-x \equiv x[2 \pi] \text { ou } \frac{\pi}{2}-x \equiv \pi-x[2 \pi] \quad \Longleftrightarrow \quad 2 x \equiv \frac{\pi}{2}[2 \pi] \text { ou } \frac{\pi}{2} \equiv \pi[2 \pi] \quad \Longleftrightarrow \quad x \equiv \frac{\pi}{4}[\pi] .
$$

Les valeurs remarquables du cosinus, du sinus et de la tangente doivent être connues par cœur!

| $x$ | 0 | $\frac{\pi}{4}$ | $\frac{\pi}{6}$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |
| :--: | :--: | :--: | :--: | :--: | :--: |
| $\cos x$ | 1 | $\frac{1}{\sqrt{2}}$ | $\frac{1}{2}$ | $\frac{1}{2}$ | 0 |
| $\sin x$ | 0 | $\frac{1}{\sqrt{2}}$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ | 1 |
| $\tan x$ | 0 | 1 | $\frac{1}{\sqrt{3}}$ | $\sqrt{3}$ |  |

# Définition-théorème (Propriétés des fonctions cosinus et sinus) 

- Fonction cosinus : La fonction cos est paire, $2 \pi$-périodique, de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$, et : $\cos ^{\prime}=-\sin$.
- Fonction sinus : La fonction sin est impaire, $2 \pi$-périodique, de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$, et : $\sin ^{\prime}=\cos$.

Pour tout $x \in \mathbb{R}: \quad|\sin x| \leqslant|x|$. En outre, $\frac{\sin x}{x} \underset{x \rightarrow 0}{\longrightarrow} 1$, autrement dit $\sin x \approx x$ pour $x$ proche de 0 .
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-40.jpeg)

Démonstration La limite $\frac{\sin x}{x} \underset{x \rightarrow 0}{\longrightarrow} 1$ n'est rien de plus que le nombre dérivé de la fonction sin en 0 .
Ensuite, la fonction sin est concave sur $[0, \pi]$ car sa dérivée $\cos y$ est décroissante, donc pour tout $x \in[0, \pi]$ : $|\sin x|=\sin x \leqslant \sin ^{\prime}(0) x+\sin 0=x=|x|$. A fortiori, pour tout $x \in[-\pi, 0]:|\sin x|=|\sin (-x)| \leqslant|-x|=|x|$. Enfin, l'inégalité est triviale pour $x>\pi$ et $x<\pi: \quad|\sin x| \leqslant 1 \leqslant \pi \leqslant|x|$.

Théorème (Formules d'addition et de produit du cosinus et du sinus) Pour tous $x, y \in \mathbb{R}$ :

$$
\begin{aligned}
& \sin (x+y)=\sin x \cos y+\cos x \sin y \\
& \sin (x-y)=\sin x \cos y-\cos x \sin y \\
& \cos (x+y)=\cos x \cos y-\sin x \sin y \\
& \cos (x-y)=\cos x \cos y+\sin x \sin y
\end{aligned} \quad \begin{aligned}
& \sin x \sin y=\frac{1}{2}(\cos (x-y)-\cos (x+y)) \\
& \sin x \cos y=\frac{1}{2}(\sin (x+y)+\sin (x-y)) \\
& \cos x \cos y=\frac{1}{2}(\cos (x+y)+\cos (x-y))
\end{aligned}
$$

Pour $x=y$, on parle de formules de duplication :

$$
\sin ^{2} x=\frac{1-\cos (2 x)}{2}, \quad \cos ^{2} x=\frac{1+\cos (2 x)}{2}
$$

$$
\sin (2 x)=2 \sin x \cos x \quad \text { et } \quad \cos (2 x)=2 \cos ^{2} x-1=1-2 \sin ^{2} x
$$

Les formules d'addition et de duplication doivent être connues par cœur - et ce même si les secondes découlent des premières. En revanche, vous devez juste savoir retrouver vite et bien les formules de produit, si possible de tête.

## Définition-théorème (Fonction tangente)

- Définition et régularité : On appelle fonction tangente la fonction $\tan =\frac{\sin }}{\cos }$ sur $]-\frac{\pi}{2}, \frac{\pi}{2}[]+\pi \mathbb{Z}$.

Impaire et $\pi$-périodique, tan est de classe $\mathscr{C}^{\infty}$ sur son ensemble de définition et :
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-41.jpeg)
$\tan ^{\prime}=1+\tan ^{2}=\frac{1}{\cos ^{2}}$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-42.jpeg)

- Résolution d'équations : Pour tous $x, y \in]-\frac{\pi}{2}, \frac{\pi}{2}[]+\pi \mathbb{Z}: \quad \tan x=\tan y \quad \Longleftrightarrow \quad x \equiv y[\pi]$.
- Formules d'addition et de duplication : Dès que chaque terme est bien défini :

$$
\tan (x+y)=\frac{\tan x+\tan y}{1-\tan x \tan y}, \quad \tan (x-y)=\frac{\tan x-\tan y}{1+\tan x \tan y} \quad \text { et } \quad \tan (2 x)=\frac{2 \tan x}{1-\tan ^{2} x}
$$

- Expression de $\cos x, \sin x$ et $\tan x$ en fonction de $\tan \frac{x}{2}$ : Pour tout $x \in]-\pi, \pi[+2 \pi \mathbb{Z}$, si on pose $t=\tan \frac{x}{2}$ :

$$
\cos x=\frac{1-t^{2}}{1+t^{2}}, \quad \sin x=\frac{2 t}{1+t^{2}} \quad \text { et } \quad \tan x=\frac{2 t}{1-t^{2}}
$$

La relation $\tan ^{2}=1+\tan ^{2}=\frac{1}{\cos ^{2}}$ ne sert pas tant à calculer $\tan ^{\prime}$ qu'à transformer $\cos$ en $\tan$ et vice versa. C'est comme ça qu'il faut la retenir $!$

Les expressions de $\cos x, \sin x$ et $\tan x$ en fonction de $\tan \frac{x}{2}$ ne sont pas à connaître par cœur, vous devez en revanche savoir les retrouver rapidement en cas de besoin.

# Démonstration 

- Définition : La tangente est définie là où le cosinus ne s'annule pas, i.e. sur $]-\frac{\pi}{2}, \frac{\pi}{2}[+\pi \mathbb{Z}$.
- Imparité : Pour tout $x \in]-\frac{\pi}{2}, \frac{\pi}{2}[+\pi \mathbb{Z}: \quad \tan (-x)=\frac{\sin (-x)}{\cos (-x)}=\frac{-\sin x}{\cos x}=-\tan x$.
- Périodicité : Pour tout $x \in]-\frac{\pi}{2}, \frac{\pi}{2}[+\pi \mathbb{Z}: \quad \tan (x+\pi)=\frac{\sin (x+\pi)}{\cos (x+\pi)}=\frac{-\sin x}{-\cos x}=\frac{\sin x}{\cos x}=\tan x$.

On comprend ici pourquoi la tangente est $\pi$-périodique alors que cosinus et sinus ne sont que $2 \pi$-périodiques.

- Dérivée : $\quad \tan ^{\prime}=\frac{\sin ^{\prime} \times \cos -\sin \times \cos ^{\prime}}{\cos ^{2}}=\frac{\cos ^{2}+\sin ^{2}}{\cos ^{2}}, \quad$ donc $\tan ^{\prime}=\frac{1}{\cos ^{2}}=1+\tan ^{2}$.
- Variations et limites : Par imparité et $\pi$-périodicité, une étude sur $\left[0, \frac{\pi}{2}[\right.$ suffit. La tangente y est strictement croissante car $\tan ^{\prime}=\frac{1}{\cos ^{2}}>0$. Enfin, $\sin x \xrightarrow[x \rightarrow \frac{\pi}{2}]{ } 1$ et $\cos x \xrightarrow[x \rightarrow \frac{\pi}{2}]{ } 0^{+}$, donc $\tan x \xrightarrow[x \rightarrow \frac{\pi}{2}]{ }+\infty$.
- Équation $\tan x=\tan y: \quad \tan x=\tan y \quad \Longleftrightarrow \quad \frac{\sin x}{\cos x}=\frac{\sin y}{\cos y} \quad \Longleftrightarrow \quad \sin x \cos y-\cos x \sin y=0$

$$
\Longleftrightarrow \quad \sin (x-y)=0 \quad \Longleftrightarrow \quad x-y \equiv 0[\pi] \quad \Longleftrightarrow \quad x \equiv y[\pi]
$$

- Formule $\tan (x+y):$

$$
\tan (x+y)=\frac{\sin (x+y)}{\cos (x+y)}=\frac{\sin x \cos y+\cos x \sin y}{\cos x \cos y-\sin x \sin y}=\frac{\cos x \cos y\left(\frac{\sin x}{\cos x}+\frac{\sin y}{\cos y}\right)}{\cos x \cos y\left(1-\frac{\sin x}{\cos x} \times \frac{\sin y}{\cos y}\right)}=\frac{\tan x+\tan y}{1-\tan x \tan y}
$$

- Expressions en fonction de $t=\tan \frac{x}{2}: \quad \tan x=\tan \left(2 \times \frac{x}{2}\right)=\frac{t+t}{1-t^{2}}=\frac{2 t}{1-t^{2}}$,

$$
\text { puis : } \quad \sin x=\sin \left(2 \times \frac{x}{2}\right)=2 \sin \frac{x}{2} \cos \frac{x}{2}=2 \tan \frac{x}{2} \cos ^{2} \frac{x}{2}=\frac{2 \tan \frac{x}{2}}{1+\tan ^{2} \frac{x}{2}}=\frac{2 t}{1+t^{2}}
$$

et enfin : $\quad \cos x=\frac{\sin x}{\tan x}=\frac{\frac{2 t}{1+t^{2}}}{\frac{2 t}{1-t^{2}}}=\frac{1-t^{2}}{1+t^{2}}$.

### 5.2 FonCTIONS ARCCOSINUS, ARCSINUS ET ARCTANGENTE

Périodiques, les fonctions cosinus, sinus et tangente ne sont pas injectives sur leurs ensembles de définition. Impossible de leur trouver une réciproque! Par exemple, l'équation $\cos x=\frac{1}{2}$ d'inconnue $x \in \mathbb{R}$ a plein de solutions, en l'occurrence tous les réels congrus à $\frac{\pi}{2}$ ou $-\frac{\pi}{2}$ modulo $2 \pi$, et aucun de ces antécédents de $\frac{1}{2}$ par la fonction cosinus n'est a priori meilleur que les autres. Cela dit, d'après le TVI strictement monotone :
— la restriction $\left.\cos \right|_{[0, \pi]}$ est bijective de $[0, \pi]$ sur $[-1,1]$,
— la restriction $\left.\sin \right|_{[-\frac{\pi}{2}, \frac{\pi}{2}]}$ est bijective de $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ sur $[-1,1]$,
— la restriction $\left.\tan \right|_{[-\frac{\pi}{2}, \frac{\pi}{2}[}$ est bijective de $]-\frac{\pi}{2}, \frac{\pi}{2}[$ sur $\mathbb{R}$.
L'équation $\cos x=\frac{1}{2}$ d'inconnue $x \in[0, \pi]$ ne possède à présent plus qu'une seule solution, à savoir $\frac{\pi}{3}$. En restreignant le champ des possibles, nous avons créé de l'injectivité. On aurait pu choisir d'autres domaines, mais ce choix arbitraire est désormais officiellement arrêté une fois pour toutes.

|  | $\cos$ | $\sin$ | $\tan$ |
| :--: | :--: | :--: | :--: |
| Domaine <br> privilégié | $[0, \pi]$ | $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ | $]-\frac{\pi}{2}, \frac{\pi}{2}[$ |

# Définition (Fonctions arccosinus, arcsinus et arctangente) 

- Arccosinus : $\left.\cos \right|_{[0, \pi]}$ est bijective de $[0, \pi]$ sur $[-1,1]$ et sa réciproque arccosinus est notée Arccos. Pour tout $x \in[-1,1]$, Arccos $x$ est l'unique réel $\theta$ de $[0, \pi]$ pour lequel $\cos \theta=x$.
- Arcsinus : $\left.\sin \right|_{[-\frac{\pi}{2}, \frac{\pi}{2}]}$ est bijective de $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ sur $[-1,1]$ et sa réciproque arcsinus est notée Arcsin. Pour tout $x \in[-1,1]$, Arcsin $x$ est l'unique réel $\theta$ de $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ pour lequel $\sin \theta=x$.
- Arctangente : $\left.\tan \right|_{]-\frac{\pi}{2}, \frac{\pi}{2}[$ est bijective de $\left.]-\frac{\pi}{2}, \frac{\pi}{2}\right[$ sur $\mathbb{R}$ et sa réciproque arctangente est notée Arctan. Pour tout $x \in \mathbb{R}$, Arctan $x$ est l'unique réel $\theta$ de $]-\frac{\pi}{2}, \frac{\pi}{2}[$ pour lequel $\tan \theta=x$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-43.jpeg)

| $x$ | -1 | $-\frac{\sqrt{3}}{2}$ | $-\frac{1}{\sqrt{2}}$ | $-\frac{1}{2}$ | 0 | $\frac{1}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{\sqrt{3}}{2}$ | 1 |
| :-- | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Arcsin $x$ | $-\frac{\pi}{2}$ | $-\frac{\pi}{3}$ | $-\frac{\pi}{4}$ | $-\frac{\pi}{6}$ | 0 | $\frac{\pi}{6}$ | $\frac{\pi}{4}$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |
| Arccos $x$ | $\pi$ | $\frac{5 \pi}{6}$ | $\frac{3 \pi}{4}$ | $\frac{2 \pi}{3}$ | $\frac{\pi}{2}$ | $\frac{\pi}{3}$ | $\frac{\pi}{4}$ | $\frac{\pi}{6}$ | 0 |
|  |  |  |  |  |  |  |  |  |  |


| $x$ | $-\infty$ | $-\sqrt{3}$ | -1 | $-\frac{1}{\sqrt{3}}$ | 0 | $\frac{1}{\sqrt{3}}$ | 1 | $\sqrt{3}$ | $+\infty$ |
| :-- | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| Arctan $x$ | $-\frac{\pi}{2}$ | $-\frac{\pi}{3}$ | $-\frac{\pi}{4}$ | $-\frac{\pi}{6}$ | 0 | $\frac{\pi}{6}$ | $\frac{\pi}{4}$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |

X Attention！ Arccos n'est pas la réciproque du cosinus, mais celle de $\cos _{[0, \pi]}$ et ça change tout. Cette mise en garde est détaillée ci-dessous dans le cas du cosinus, mais elle vaut aussi pour le sinus et la tangente.

- Pour tout $x \in[-1,1]$, Arccos $x$ est l'unique réel $\theta \in[0, \pi]$ pour lequel $\cos \theta=x$, donc $\cos \operatorname{Arccos} x=x$.
- En revanche, pour tout $x \in \mathbb{R}$, Arccos $\cos x$ est l'unique réel $\theta \in[0, \pi]$ pour lequel $\cos \theta=\cos x$. Ce n'est donc pas forcément $x$ ! La question importante, c'est : « $x$ appartient-il au domaine privilégié $[0, \pi]$, oui ou non?»
Par exemple : $\quad \operatorname{Arccos} \cos (2 \pi)=\operatorname{Arccos} 1=0 \neq 2 \pi$.
Vrai: $\forall x \in[-1,1], \cos \operatorname{Arccos} x=x . \quad$ Faux: $\forall x \times$. Arccos $\cos x=x . \quad$ Vrai: $\forall x \in[0, \pi]$, Arccos $\cos x=x$.

Exemple On veut résoudre l'équation $\cos x=\frac{1}{3}$ d'inconnue $x \in \mathbb{R}$. Pour tout $x \in \mathbb{R}$ :

$$
\cos x=\frac{1}{3} \quad \Longleftrightarrow \quad \cos x=\cos \operatorname{Arccos} \frac{1}{3} \quad \Longleftrightarrow \quad x \equiv \pm \operatorname{Arccos} \frac{1}{3}[2 \pi]
$$

L'ensemble des solutions cherché est donc la réunion $\left(\operatorname{Arccos} \frac{1}{3}+2 \pi \mathbb{Z}\right) \cup\left(-\operatorname{Arccos} \frac{1}{3}+2 \pi \mathbb{Z}\right)$.
Exemple $\quad \operatorname{Arccos} \cos \frac{20 \pi}{3}=\frac{2 \pi}{3} \quad$ et $\quad \operatorname{Arcsin} \sin \frac{20 \pi}{3}=\frac{\pi}{3}$.
Démonstration Dans les deux cas, on commence par placer $\frac{20 \pi}{3}$ sur le cercle trigonométrique ainsi que le domaine privilégié de la fonction sinus ou cosinus concernée.

- Arccosinus : $\frac{20 \pi}{3}$ appartient à $2 \pi$ près au domaine privilégié du cosinus : $\frac{20 \pi}{3} \in[0, \pi]+2 \pi \mathbb{Z}$. Il suffit donc d'ôter un certain nombre de fois $2 \pi$ et c'est fini.
- Arcsinus : $\frac{20 \pi}{3}$ n'appartient pas au domaine privilégié du sinus : $\frac{20 \pi}{3} \notin\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]+2 \pi \mathbb{Z}, \quad$ même à $2 \pi$ près. Nous pouvons cependant nous y ramener À SINUS CONSTANT grâce à la relation $\sin (\pi-x)=\sin x$. Par $2 \pi$-périodicité : $\sin \frac{20 \pi}{3}=\sin \frac{2 \pi}{3}$, puis $\sin \frac{20 \pi}{3}=\sin \left(\pi-\frac{2 \pi}{3}\right)=\sin \frac{\pi}{3}$, et bien sûr $\frac{\pi}{3} \in\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$.
![Figure](C:\Users\axelc\Documents\math-anki\ressources\mistralocr\images\img-44.jpeg)

Théorème (Lien entre les coordonnées cartésiennes et les coordonnées polaires) Soit $M$ un point de coordonnées cartésiennes $(x, y)$ et de coordonnées polaires $(r, \theta)$.
(i) $\left\{\begin{array}{l}x=r \cos \theta \\ y=r \sin \theta\end{array}\right.$ et $\quad r=\sqrt{x^{2}+y^{2}}$.
(ii) $\theta \equiv\left\{\begin{array}{ll}\operatorname{Arctan} \frac{y}{x}[2 \pi] & \text { si } x>0 \\ \pi+\operatorname{Arctan} \frac{y}{x}[2 \pi] & \text { si } x<0 .\end{array}\right.$

Démonstration C'est sous-entendu, mais on travaille bien sûr dans un repère orthonormal direct $(O, \vec{\imath}, \vec{\jmath})$.
(i) $\overrightarrow{O M}=x \vec{\imath}+y \vec{\jmath}=r(\cos \theta \vec{\imath}+\sin \theta \vec{\jmath})$, donc $x=r \cos \theta$ et $y=r \sin \theta$ par identification des coordonnées. En outre, $r=\|\overrightarrow{O M}\|=\sqrt{x^{2}+y^{2}}$.
(ii) Cas où $x>0: \theta-2 k \pi \in]-\frac{\pi}{2}, \frac{\pi}{2}[$ pour un certain $k \in \mathbb{Z}$, or $\tan (\theta-2 k \pi)=\tan \theta=\frac{r \sin \theta}{r \cos \theta}=\frac{y}{x}$, donc $\theta-2 k \pi=\operatorname{Arctan} \frac{y}{x}$, et enfin $\theta \equiv \operatorname{Arctan} \frac{y}{x}[2 \pi]$.
Cas où $x<0: \theta-2 k \pi \in] \frac{\pi}{2}, \frac{3 \pi}{2}[$ pour un certain $k \in \mathbb{Z}$, or $\tan (\theta-\pi-2 k \pi)=\tan \theta=\frac{y}{x}$ avec $\theta-2 k \pi-\pi \in]-\frac{\pi}{2}, \frac{\pi}{2}\left[\right.$, donc $\theta \equiv \pi+\operatorname{Arctan} \frac{y}{x}[2 \pi]$.

On a choisi d'exprimer $\theta$ comme une arctangente, mais on aurait pu l'exprimer comme un arccosinus ou un arcsinus, la stratégie est toujours la même. On place $M$ dans l'un des quatre quadrants que le repère choisi délimite, puis selon qu'on souhaite atteindre un arccosinus ou un arcsinus, on ramène $\theta$ dans le domaine privilégié adapté.

Exemple Avec les notations du théorème, faisons l'hypothèse que $x>0$ et $y<0$. On peut donc choisir $\theta$ dans $]-\frac{\pi}{2}, 0[$, mais comment l'exprimer comme un arccosinus ou un arcsinus?

- Arccosinus : $\theta$ n'appartient pas au domaine privilégié $[0, \pi]$, même à $2 \pi$ près, mais nous pouvons l'y ramener À COSINUS CONSTANT grâce à la relation $\cos (-x)=\cos x$. Précisément, $\cos (-\theta)=\cos \theta=\frac{x}{r}$ avec $-\theta \in[0, \pi]$, donc $-\theta=\operatorname{Arccos} \frac{x}{r}$, i.e. $\theta=-\operatorname{Arccos} \frac{x}{r}$.
- Arcsinus : $\theta$ appartient au domaine privilégié $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ et $\sin \theta=\frac{y}{r}$, donc $\theta=\operatorname{Arcsin} \frac{y}{r}$.


# - Théorème (Propriétés des fonctions arccosinus, arcsinus et arctangente) 

- Une relation mixte : Pour tout $x \in[-1,1]: \cos \operatorname{Arcsin} x=\sin \operatorname{Arccos} x=\sqrt{1-x^{2}}$.
- Arccosinus : Arccos est continue sur $[-1,1]$ et de classe $\mathscr{C}^{\infty}$ sur $]-1,1[$, mais pas dérivable en -1 et 1 . Pour tout $x \in]-1,1[$ :

$$
\operatorname{Arccos}^{\prime}(x)=-\frac{1}{\sqrt{1-x^{2}}}
$$

- Arcsinus : Arcsin est impaire et continue sur $[-1,1]$ et de classe $\mathscr{C}^{\infty}$ sur $]-1,1[$, mais pas dérivable en -1 et 1. Pour tout $x \in]-1,1[$ :

$$
\operatorname{Arcsin}^{\prime}(x)=\frac{1}{\sqrt{1-x^{2}}}
$$

- Arctangente : Arctan est impaire et de classe $\mathscr{C}^{\infty}$ sur $\mathbb{R}$. Pour tout $x \in \mathbb{R}: \operatorname{Arctan}^{\prime}(x)=\frac{1}{1+x^{2}}$.

La non-dérivabilité d'Arccos et Arcsin en $\pm 1$ s'explique bien géométriquement, les tangentes horizontales de sin et cos deviennent verticales quand on les symétrise par rapport à la droite d'équation $y=x$.

# Démonstration (Fonction arcsinus) 

- Continuité/imparité : La fonction $\sin \left|\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]\right.$ est bijective de $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ sur $[-1,1]$ et continue/impaire, donc d'après le théorème de continuité/imparité d'une réciproque, sa réciproque $\operatorname{Arcsin}=\left(\sin \left|\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]\right)^{-1}\right.$ est continue/impaire sur $[-1,1]$.
- Relation $\cos \operatorname{Arcsin} x$ : Pour tout $x \in[-1,1]: \quad \operatorname{Arcsin} x \in\left[-\frac{\pi}{2}, \frac{\pi}{2}\right], \quad$ donc $\cos \operatorname{Arcsin} x \geqslant 0$, donc :

$$
\cos \operatorname{Arcsin} x=|\cos \operatorname{Arcsin} x|=\sqrt{1-\sin ^{2} \operatorname{Arcsin} x}=\sqrt{1-x^{2}}
$$

- Dérivabilité et dérivée : La fonction $\sin \left[\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]\right.$ est bijective de $\left.]-\frac{\pi}{2}, \frac{\pi}{2}\right[$ sur $]-1,1\left[\right.$, de classe $\left.\mathscr{C}^{\infty}\right)$, et sa dérivée $\sin ^{\prime}=\cos$ ne s'annule pas sur $]-\frac{\pi}{2}, \frac{\pi}{2}[$, donc d'après le théorème de dérivabilité d'une réciproque, Arcsin est de classe $\mathscr{C}^{\infty}$ sur $]-1,1[$ et pour tout $x \in]-1,1[$ :

$$
\operatorname{Arcsin}^{\prime}(x)=\frac{1}{\sin ^{\prime} \circ \operatorname{Arcsin}(x)}=\frac{1}{\cos \operatorname{Arcsin} x}=\frac{1}{\sqrt{1-x^{2}}}
$$

Le théorème de dérivabilité ne nous dit rien de la dérivabilité d'Arcsin en $\pm 1 \operatorname{car} \cos ^{\prime}(0)=\cos ^{\prime}(\pi)=0$, mais on peut montrer qu'Arcsin n'est pas dérivable en ces points.

Démonstration (Fonction arctangente) Il s'agit là aussi essentiellement d'utiliser le théorème de dérivabilité/imparité d'une réciproque. La situation est cependant plus simple car $\tan ^{\prime}(x)=1+\tan ^{2} x \neq 0$ pour tout $x \in \mathbb{R}$. Pas de tangente horizontale sur le graphe de la fonction tangente, donc pas de problème de dérivabilité pour Arctan. Pour tout $x \in \mathbb{R}: \quad \operatorname{Arctan}^{\prime}(x)=\frac{1}{\tan ^{\prime} \circ \operatorname{Arctan}(x)}=\frac{1}{1+\tan ^{2} \operatorname{Arctan} x}=\frac{1}{1+x^{2}}$.

Exemple $\frac{3}{5}$ est l'unique solution de l'équation $\operatorname{Arcsin} x=\operatorname{Arccos} \frac{4}{5}$ d'inconnue $x \in[-1,1]$.
Démonstration Pour tous $x \in[-1,1]$ et $y \in\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]: \quad y=\operatorname{Arcsin} x \quad \Longleftrightarrow \quad x=\sin y \quad$ par définition de l'arcsinus, et attention, l'équivalence est vraie seulement si $y$ appartient à $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$. Ici, $\operatorname{Arccos} \frac{4}{5} \in\left[0, \frac{\pi}{2}\right]$ car $\frac{4}{5} \in[0,1]$, donc pour tout $x \in[-1,1]:$

$$
\operatorname{Arcsin} x=\operatorname{Arccos} \frac{4}{5} \quad \Longleftrightarrow \quad x=\sin \operatorname{Arccos} \frac{4}{5} \quad \Longleftrightarrow \quad x=\sqrt{1-\left(\frac{4}{5}\right)^{2}}=\frac{3}{5}
$$

Exemple Pour tout $x \in[-1,1]: \quad \operatorname{Arccos} x+\operatorname{Arcsin} x=\frac{\pi}{2}$.
Démonstration Il s'agit de montrer que la fonction $x \xrightarrow{f} \operatorname{Arccos} x+\operatorname{Arcsin} x$ est constante sur $[-1,1]$ de valeur $\frac{\pi}{2}$. Or cette fonction est dérivable sur l'intervalle ouvert $]-1,1[$ et sa dérivée est la fonction nulle, donc $f$ est constante. Quelle valeur? Nous pouvons la calculer en 0 par exemple : $\quad f(0)=\operatorname{Arccos} 0+\operatorname{Arcsin} 0=\frac{\pi}{2}+0=\frac{\pi}{2}$, et $f(1)$ et $f(-1)$ valent la même chose par continuité de $f$ sur l'intervalle fermé $[-1,1]$.

Exemple Pour tout $x>0: \quad \operatorname{Arctan} x+\operatorname{Arctan} \frac{1}{x}=\frac{\pi}{2} \quad$ et pour tout $x<0: \quad \operatorname{Arctan} x+\operatorname{Arctan} \frac{1}{x}=-\frac{\pi}{2}$.
Démonstration La fonction $x \xrightarrow{g} \operatorname{Arctan} x+\operatorname{Arctan} \frac{1}{x}$ est dérivable sur $\mathbb{R}^{*}$ et pour tout $x \in \mathbb{R}^{*}$ :

$$
g^{\prime}(x)=\frac{1}{1+x^{2}}+\left(-\frac{1}{x^{2}}\right) \times \frac{1}{1+\left(\frac{1}{x}\right)^{2}}=\frac{1}{1+x^{2}}-\frac{1}{1+x^{2}}=0
$$

Comme $\mathbb{R}^{*}=\rrbracket-\infty, 0[\cup] 0,+\infty[$ n'est pas un intervalle, on ne peut pas en déduire que $g$ est constante sur $\mathbb{R}^{*}$ tout entier, mais seulement qu'elle l'est sur $\mathbb{R}_{+}^{*}$ et $\mathbb{R}_{-}^{*}$ indépendamment. Quelles valeurs? Calculons $g(1)$ : $g(1)=2 \operatorname{Arctan} 1=2 \times \frac{\pi}{4}=\frac{\pi}{2} . \quad$ Pour la valeur de $g$ sur $\mathbb{R}_{-}^{*}$, remarquer simplement que $g$ est impaire.

Exemple On veut résoudre l'équation $\operatorname{Arccos} x=\operatorname{Arcsin} x$ d'inconnue $x \in[-1,1]$.
On a bien envie de passer au cosinus (ou au sinus) des deux côtés de l'équation, mais on perd l'équivalence en faisant cela car en toute généralité : $\cos x=\cos y \quad x=y, \quad$ autrement dit la fonction cosinus n'est pas injective sur $\mathbb{R}$. Elle l'est sur de plus petits domaines sur lesquels elle est strictement monotone, par exemple $[-\pi, 0],[0, \pi]$ ou $[\pi, 2 \pi]$.

C'est parti. Pour tout $x \in[-1,1]:$

$$
\begin{aligned}
& \operatorname{Arccos} x=\operatorname{Arcsin} x \quad \Longleftrightarrow \quad \cos \operatorname{Arccos} x=\cos \operatorname{Arcsin} x \text { et } \operatorname{Arcsin} x \in[0, \pi] \\
& \text { Cette équivalence } \star \text { est LE passage délicat, justifié plus loin. } \\
& \Longleftrightarrow \quad x=\sqrt{1-x^{2}} \text { et } x \in[0,1] \quad \text { après contemplation du graphe d'arcsinus } \\
& \Longleftrightarrow \quad x^{2}=1-x^{2} \text { et } x \in[0,1] \quad \Longleftrightarrow \quad x=\frac{1}{\sqrt{2}} .
\end{aligned}
$$

Justification de l'équivalence $\star$ : Cette équivalence est la difficulté principale de l'équation et on ne peut pas s'en tirer sans réfléchir. N'espérez pas «la méthode» qui vous évitera de réfléchir, il n'y en a pas.

- L'implication : $\quad \operatorname{Arccos} x=\operatorname{Arcsin} x \quad \Longrightarrow \quad \cos \operatorname{Arccos} x=\cos \operatorname{Arcsin} x \quad$ ne pose aucun problème.
- Le retour n'est possible que si $\operatorname{Arccos} x$ et $\operatorname{Arcsin} x$ appartiennent à un même domaine d'injectivité du cosinus. Ici, $\operatorname{Arccos} x$ appartient à $[0, \pi]$, mais $\operatorname{Arcsin} x$ appartient a priori à $\left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$ et non pas à $[0, \pi]$. En tout cas, l'implication suivante est correcte : $\cos \operatorname{Arccos} x=\cos \operatorname{Arcsin} x$ et $\operatorname{Arcsin} x \in[0, \pi] \quad \Longrightarrow \quad \operatorname{Arccos} x=\operatorname{Arcsin} x$.
- Mais l'implication corrigée : $\quad \operatorname{Arccos} x=\operatorname{Arcsin} x \quad \Longrightarrow \quad \cos \operatorname{Arccos} x=\cos \operatorname{Arcsin} x$ et $\operatorname{Arcsin} x \in[0, \pi]$ l'est-elle? C'est ce qu'il nous reste à comprendre. Et tout simplement, si $\operatorname{Arccos} x=\operatorname{Arcsin} x$, alors oui, $\operatorname{Arcsin} x=\operatorname{Arccos} x \in[0, \pi]$ car un arccosinus est toujours dans $[0, \pi]$.


# 6 TABLEAUX RÉCAPITULATIFS DES DÉRIVÉES USUELLES 

| Fonction | Dérivée |
| :--: | :--: |
| $\mathrm{e}^{x}$ | $\mathrm{e}^{x}$ |
| $\ln x$ | $\frac{1}{x}$ |
| $x^{\alpha}=\mathrm{e}^{\alpha \ln x}$ | $\alpha x^{\alpha-1}$ |
| $\operatorname{ch} x=\frac{\mathrm{e}^{x}-\mathrm{e}^{-x}}{2}$ | $\operatorname{sh} x$ |
| $\operatorname{sh} x=\frac{\mathrm{e}^{x}+\mathrm{e}^{-x}}{2}$ | $\operatorname{ch} x$ |
| $\operatorname{th} x=\frac{\operatorname{sh} x}{\operatorname{ch} x}$ | $1-\operatorname{th}^{2} x=\frac{1}{\operatorname{ch}^{2} x}$ |


| Fonction | Dérivée |
| :--: | :--: |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tan x=\frac{\sin x}{\cos x}$ | $1+\tan ^{2} x=\frac{1}{\cos ^{2} x}$ |
| $\operatorname{Arcsin} x$ | $\frac{1}{\sqrt{1-x^{2}}}$ |
| $\operatorname{Arccos} x$ | $-\frac{1}{\sqrt{1-x^{2}}}$ |
| $\operatorname{Arctan} x$ | $\frac{1}{1+x^{2}}$ |
