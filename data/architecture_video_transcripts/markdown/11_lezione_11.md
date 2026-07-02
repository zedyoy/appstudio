# lezione 11

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\lezione 11.mp4`
- Durata: 00:47:02
- Trascrizione: `11_lezione_11.json`

## Argomenti probabili
- porte_logiche (260): and, or, not, nor, nand, sop
- clock_prestazioni (42): clock, tempo
- memoria_bus (28): memoria, temporizzazione, ram
- microarchitettura (11): mic, alu, controllo
- registri_flip_flop (10): flip flop, latch, registro, propagazione

## Trascrizione

[00:00:00 - 00:00:02] Sottotitoli a cura di QTSS.
[00:00:30 - 00:00:32] Sottotitoli a cura di QTSS.
[00:01:00 - 00:01:02] Sottotitoli a cura di QTSS.
[00:01:30 - 00:01:32] Sottotitoli a cura di QTSS.
[00:02:00 - 00:02:02] Sottotitoli a cura di QTSS.
[00:02:30 - 00:02:32] Sottotitoli a cura di QTSS.
[00:03:00 - 00:03:02] Sottotitoli a cura di QTSS.
[00:03:30 - 00:03:32] Sottotitoli a cura di QTSS.
[00:04:00 - 00:04:02] Sottotitoli a cura di QTSS.
[00:04:30 - 00:04:32] Sottotitoli a cura di QTSS.
[00:05:00 - 00:05:02] Sottotitoli a cura di QTSS.
[00:05:30 - 00:05:38] Tra i vari circuiti sequenziali,
[00:05:38 - 00:05:44] questa ecce ne vediamo quello fondamentale, il LEX,
[00:05:44 - 00:05:48] in particolare il LEX SR,
[00:05:48 - 00:05:54] che è il primo elemento di memoria che andiamo a vedere,
[00:05:54 - 00:05:56] proprio perché, come dire,
[00:05:56 - 00:06:00] essendo un circuito che dipende
[00:06:00 - 00:06:03] dallo stato del circuito stesso,
[00:06:03 - 00:06:08] in qualche modo vuol dire che
[00:06:08 - 00:06:16] c'è una memoria dello stato che possiamo andare a
[00:06:16 - 00:06:22] avere nel circuito, quindi c'è qualcosa che possiamo andare a memorizzare.
[00:06:22 - 00:06:26] Questo che vedete è, diciamo, il simbolo del...
[00:06:26 - 00:06:30] schematicamente, diciamo, come l'indicato un LEX SR,
[00:06:30 - 00:06:40] in cui vediamo già, adesso, che è un circuito che ha due input S ed R,
[00:06:40 - 00:06:45] che li chiamano, diciamo, l'uso che se ne fa di questi int,
[00:06:45 - 00:06:50] dove S sta per 7 per settare, diciamo, lo stato a 1,
[00:06:50 - 00:06:57] e R sta per reset per invece settare lo stato a 0.
[00:06:57 - 00:07:01] Le uscite, qui chiamate Q e Q negato,
[00:07:01 - 00:07:07] nell'ECSR l'uscita Q indica anche,
[00:07:07 - 00:07:11] cioè coincide con lo stato stesso del sistema,
[00:07:11 - 00:07:16] e l'uscita Q negata è sempre, diciamo, la versione negata
[00:07:16 - 00:07:18] dell'altra uscita, quindi abbiamo due uscite,
[00:07:18 - 00:07:23] caratterizzata, fatte che una è la negazione dell'altra.
[00:07:23 - 00:07:34] LEX, diciamo, questo qui che andiamo a vedere, è asincrono.
[00:07:34 - 00:07:38] È in grado di, diciamo, mantenere uno stato,
[00:07:38 - 00:07:42] in questo caso, quindi il valore di Q, ad esempio,
[00:07:42 - 00:07:45] senza dimenticare che è proprio conegato, ovviamente,
[00:07:45 - 00:07:52] è la negazione, mantiene il suo stato a un certo in grado di mantenere
[00:07:52 - 00:07:56] un certo valore del suo stato al 0 o a 1,
[00:07:56 - 00:08:02] finché, diciamo, manteniamo una certa configurazione degli ingressi.
[00:08:02 - 00:08:06] Cambiando la configurazione degli ingressi è possibile, diciamo,
[00:08:06 - 00:08:09] cambiare lo stato del sistema,
[00:08:09 - 00:08:12] e per questo, diciamo, questo è un elemento di memoria,
[00:08:12 - 00:08:15] perché lo possiamo sfruttare, appunto,
[00:08:15 - 00:08:21] memorizzare un'informazione nel circuito, nel LEX,
[00:08:21 - 00:08:24] il fatto che memorizziamo un'informazione che memorizziamo
[00:08:24 - 00:08:29] ovviamente è quella minima o 0 o 1.
[00:08:29 - 00:08:31] Memorizzare 1, nel LEX,
[00:08:31 - 00:08:36] cioè che, diciamo, manteniamo lo stato posto a 1,
[00:08:37 - 00:08:39] finché il circuito, diciamo, è alimentato,
[00:08:39 - 00:08:44] e finché non cambiamo la configurazione degli ingressi.
[00:08:45 - 00:08:49] Si dice che questo elemento, il LEX, è distabile,
[00:08:49 - 00:08:54] perché, come vedremo tra un poco, fa i vari possibili, diciamo,
[00:08:54 - 00:08:57] tra le vari possibili configurazioni degli ingressi,
[00:08:57 - 00:09:00] che sono quattro, ovviamente, perché sono due ingressi,
[00:09:00 - 00:09:02] le possibili combinazioni sono quattro,
[00:09:03 - 00:09:08] esistono due stati in cui riesce a stabilizzarsi,
[00:09:08 - 00:09:12] perciò è distabile, perché ha due stati stabili
[00:09:12 - 00:09:18] in cui si porta, diciamo, si può portare il LEX
[00:09:18 - 00:09:20] e li può mantenere.
[00:09:23 - 00:09:27] Quali sono, ovviamente, lo stato in cui memorizza il valore 1
[00:09:27 - 00:09:31] e lo stato in cui memorizza il valore 0?
[00:09:33 - 00:09:39] L'altro elemento di memoria che andremo a vedere
[00:09:39 - 00:09:43] è il flip-flop, che però vedremo,
[00:09:43 - 00:09:46] alla fine si basa sempre su il LEX,
[00:09:48 - 00:09:52] però la differenza del flip-flop,
[00:09:52 - 00:09:56] scusatemi, è che non è asincrono, ma è sincrono.
[00:09:56 - 00:10:00] Quindi, flip-flop e LEX, sono due circuiti sequenziali
[00:10:00 - 00:10:04] che permettono di memorizzare un'informazione,
[00:10:04 - 00:10:07] hanno due stati stabili,
[00:10:07 - 00:10:10] hanno due uscite di godù nel complemento dell'altra,
[00:10:10 - 00:10:12] e la differenza è che il LEX è asincrono,
[00:10:12 - 00:10:16] mentre il flip-flop, in qualche modo, è sincronizzabile,
[00:10:16 - 00:10:19] rispetto a un ulteriore segnale di in-input,
[00:10:19 - 00:10:23] vedete, infatti adesso sono tre in-input,
[00:10:23 - 00:10:25] però, diciamo, il terzo non viene visto come in-input,
[00:10:25 - 00:10:29] ma viene visto come segnale di sincronizzazione,
[00:10:29 - 00:10:32] che può essere tipicamente un croco,
[00:10:32 - 00:10:34] o comunque un segnale, in generale,
[00:10:34 - 00:10:41] che abilita, sincronizza la memorizzazione del circuito.
[00:10:43 - 00:10:46] Quindi, due tre metri di memoria fondamentali sono LEX,
[00:10:46 - 00:10:48] e flip-flop, perché però vedremo,
[00:10:48 - 00:10:50] si riconducono alla stessa tipologia di circuito,
[00:10:50 - 00:10:52] che è quella del LEX SR.
[00:10:52 - 00:11:02] Allora, un LEX SR, che quindi è un elemento di memoria asincrono,
[00:11:02 - 00:11:06] che è arretizzato da due input senza clock,
[00:11:06 - 00:11:08] quindi è asincrono,
[00:11:10 - 00:11:13] e due uscite di una e il complemento dell'altra
[00:11:13 - 00:11:17] può essere, diciamo, implementato da questo circuito,
[00:11:18 - 00:11:21] in cui abbiamo due porte NOR,
[00:11:22 - 00:11:26] collegati, diciamo, in una sorta di retroazione reciproca,
[00:11:26 - 00:11:29] in cui vediamo che l'uscita, vediamo,
[00:11:29 - 00:11:33] il set va nella porta NOR,
[00:11:34 - 00:11:37] e insieme, in ingresso a questa porta NOR superiore,
[00:11:37 - 00:11:40] va anche l'uscita dell'altra porta NOR,
[00:11:40 - 00:11:43] che è alimentata dal reset,
[00:11:44 - 00:11:48] e dall'uscita della porta NOR superiore,
[00:11:48 - 00:11:50] quindi sopra abbiamo Q negato,
[00:11:50 - 00:11:52] giù abbiamo Q,
[00:11:52 - 00:11:55] e quindi, in ingresso alla porta NOR superiore,
[00:11:55 - 00:11:57] abbiamo S e Q.
[00:11:58 - 00:12:00] All'ingresso della porta,
[00:12:00 - 00:12:02] inferiore, la porta NOR inferiore,
[00:12:02 - 00:12:04] abbiamo invece
[00:12:06 - 00:12:08] R e Q negato.
[00:12:15 - 00:12:18] Vediamo come si funziona,
[00:12:18 - 00:12:20] cosa può succedere.
[00:12:20 - 00:12:23] Allora, immaginiamo di porre
[00:12:23 - 00:12:27] il ingresso a queste porte NOR,
[00:12:27 - 00:12:29] così collegate,
[00:12:29 - 00:12:32] insegnare, c'è la configurazione di ingresso 00,
[00:12:32 - 00:12:34] quindi, S e Q,
[00:12:34 - 00:12:36] le due segnali di ingresso li poniamo
[00:12:36 - 00:12:38] al zero.
[00:12:41 - 00:12:43] Cosa succede?
[00:12:44 - 00:12:47] Ok, scusatemi.
[00:12:54 - 00:12:57] Guardiamo, ad esempio, l'altro sinistro,
[00:12:57 - 00:12:59] la porta NOR superiore,
[00:12:59 - 00:13:02] io ho 00,
[00:13:05 - 00:13:07] e come uscita
[00:13:08 - 00:13:10] di Q, diciamo,
[00:13:10 - 00:13:13] è un stato a cui tende la lecce,
[00:13:13 - 00:13:15] e quelle di evere Q
[00:13:15 - 00:13:17] uguale a zero, e ovviamente
[00:13:17 - 00:13:19] Q negato uguale a uno.
[00:13:19 - 00:13:21] Questo è uno stato stabile,
[00:13:21 - 00:13:23] ovviamente noi dobbiamo immaginare che,
[00:13:23 - 00:13:25] ovviamente,
[00:13:25 - 00:13:27] i segnali in qualche modo
[00:13:27 - 00:13:29] si propagano, e quindi
[00:13:29 - 00:13:31] l'uscita di una NOR
[00:13:31 - 00:13:33] rientra nell'altra NOR,
[00:13:33 - 00:13:35] che ovviamente potremmo avere che
[00:13:35 - 00:13:37] le uscite iniziano a cambiare
[00:13:37 - 00:13:39] e a saltellare.
[00:13:39 - 00:13:41] Però questo non avviene
[00:13:41 - 00:13:43] nel caso in cui io ho
[00:13:43 - 00:13:46] S ed R uguale a zero,
[00:13:46 - 00:13:48] nel senso che
[00:13:48 - 00:13:50] ci può essere
[00:13:50 - 00:13:52] un cambiamento
[00:13:52 - 00:13:54] dei segnali,
[00:13:54 - 00:13:56] però a un certo punto
[00:13:56 - 00:13:58] raggiungono questa configurazione
[00:13:58 - 00:14:00] e si stabilizzano,
[00:14:00 - 00:14:02] cambia più.
[00:14:02 - 00:14:04] Perché? Perché se
[00:14:04 - 00:14:06] Q,
[00:14:06 - 00:14:08] infatti, diciamo che Q
[00:14:08 - 00:14:10] vale a zero,
[00:14:10 - 00:14:12] arriva
[00:14:12 - 00:14:14] la configurazione
[00:14:14 - 00:14:16] S uguale a zero,
[00:14:16 - 00:14:18] e succede che ovviamente
[00:14:18 - 00:14:20] la NOR zero a zero
[00:14:20 - 00:14:22] fa zero negato a uno,
[00:14:22 - 00:14:24] uno
[00:14:24 - 00:14:26] va in retroazione con R,
[00:14:26 - 00:14:28] vince rispetto a R,
[00:14:28 - 00:14:30] e quindi
[00:14:30 - 00:14:32] negata viene zero.
[00:14:32 - 00:14:34] Quindi se Q
[00:14:34 - 00:14:36] vale a zero,
[00:14:36 - 00:14:38] la configurazione
[00:14:38 - 00:14:40] in ingresso
[00:14:40 - 00:14:42] mantiene questi valori,
[00:14:42 - 00:14:44] che non li fa cambiare.
[00:14:44 - 00:14:46] Ma mantiene
[00:14:46 - 00:14:48] uno stato,
[00:14:48 - 00:14:50] però in questo caso qui
[00:14:50 - 00:14:52] non lo sappiamo.
[00:14:52 - 00:14:54] No, no, io sto facendo
[00:14:54 - 00:14:56] ripotesi, se Q vale a zero,
[00:14:56 - 00:14:58] quando arriva
[00:14:58 - 00:15:00] la configurazione zero a zero,
[00:15:00 - 00:15:02] resta Q vale a zero, non c'è
[00:15:03 - 00:15:05] ok.
[00:15:07 - 00:15:09] Se invece
[00:15:09 - 00:15:11] Q vale o zero a uno,
[00:15:11 - 00:15:13] nel momento in cui arriva la configurazione
[00:15:13 - 00:15:15] zero a zero,
[00:15:15 - 00:15:17] Q vale a zero o vale a uno, prima
[00:15:17 - 00:15:19] dico. Ok, lo stato,
[00:15:19 - 00:15:21] sto dicendo,
[00:15:21 - 00:15:23] qualunque sia lo stato, che sia
[00:15:23 - 00:15:25] o Q vale a zero o Q vale a uno,
[00:15:25 - 00:15:27] quando arriva la
[00:15:27 - 00:15:29] configurazione zero a zero,
[00:15:29 - 00:15:31] che succede?
[00:15:32 - 00:15:34] Nel primo caso,
[00:15:34 - 00:15:36] resta così e non cambia.
[00:15:37 - 00:15:39] Nel secondo caso,
[00:15:39 - 00:15:41] quindi quello di destra,
[00:15:41 - 00:15:43] io ipotigio che Q vale a uno,
[00:15:43 - 00:15:45] arriva s uguale a zero,
[00:15:45 - 00:15:47] r uguale a zero in ingresso.
[00:15:47 - 00:15:49] Ok, la nor
[00:15:49 - 00:15:51] superiore fa
[00:15:51 - 00:15:53] zero or
[00:15:53 - 00:15:55] uno, che fa uno negato
[00:15:55 - 00:15:57] zero, quindi
[00:15:57 - 00:15:59] in cui negato mi mette
[00:15:59 - 00:16:01] zero.
[00:16:01 - 00:16:03] Se questo zero, dopo un po'
[00:16:03 - 00:16:05] arriva, diciamo,
[00:16:05 - 00:16:07] alla nor
[00:16:07 - 00:16:09] inferiore,
[00:16:09 - 00:16:11] zero o zero,
[00:16:11 - 00:16:13] la nor da
[00:16:13 - 00:16:15] uno in uscita.
[00:16:17 - 00:16:19] Ok.
[00:16:21 - 00:16:23] Se questo uno
[00:16:23 - 00:16:25] non cambia, quindi è sempre lo stesso.
[00:16:25 - 00:16:27] Ok, quindi, in entrambi casi,
[00:16:27 - 00:16:29] sia che c'è zero, sia che c'è
[00:16:29 - 00:16:31] il fatto che io porto
[00:16:31 - 00:16:33] zero o zero in ingresso,
[00:16:33 - 00:16:35] mi lascia lo stesso
[00:16:35 - 00:16:37] stato, non mi altera il signal.
[00:16:37 - 00:16:39] Se non ti trovi che ho detto
[00:16:39 - 00:16:41] che imponiamo a zero,
[00:16:41 - 00:16:43] mi sono confuso, scusami.
[00:16:47 - 00:16:49] Ti trovi, quindi, in entrambi casi,
[00:16:49 - 00:16:51] il fatto che arriva zero a zero in ingresso
[00:16:51 - 00:16:53] non causa alterazione
[00:16:55 - 00:16:57] dello stato
[00:16:57 - 00:16:59] e lo lascia in variato.
[00:17:01 - 00:17:03] Ti trovi?
[00:17:03 - 00:17:05] Sì, sì, sì.
[00:17:05 - 00:17:07] Si mi trovo che
[00:17:07 - 00:17:09] è zero, mantiene lo stato.
[00:17:13 - 00:17:15] Diferentemente, quando invece uno
[00:17:15 - 00:17:17] uno che è proprio instabile,
[00:17:17 - 00:17:19] quindi è impossibile
[00:17:19 - 00:17:21] come
[00:17:21 - 00:17:23] come situazione, cioè
[00:17:23 - 00:17:25] non è
[00:17:25 - 00:17:27] definita la
[00:17:27 - 00:17:29] configurazione.
[00:17:31 - 00:17:33] Quindi,
[00:17:33 - 00:17:35] sia lo stato zero, che lo stato uno,
[00:17:35 - 00:17:37] quindi sono stabili
[00:17:37 - 00:17:39] quando S è zero,
[00:17:39 - 00:17:41] R è male zero.
[00:17:41 - 00:17:43] Quindi, cosa voglio dire? Che qua basta
[00:17:43 - 00:17:45] mettergli a massa S, R
[00:17:45 - 00:17:47] e il valore memorizzato
[00:17:47 - 00:17:49] nel lecce per mani che è alimentato
[00:17:49 - 00:17:51] il circuito.
[00:17:51 - 00:17:53] Per questo è un elemento
[00:17:53 - 00:17:55] di memoria.
[00:18:01 - 00:18:03] Ovviamente, non posso
[00:18:03 - 00:18:05] avere
[00:18:05 - 00:18:07] q zero e q negato
[00:18:07 - 00:18:09] uguale a zero,
[00:18:11 - 00:18:13] mentre
[00:18:13 - 00:18:15] q zero e q negato
[00:18:17 - 00:18:19] uguale a uno.
[00:18:19 - 00:18:21] Questo sempre impotizzando
[00:18:21 - 00:18:23] S, R uguale a zero.
[00:18:23 - 00:18:25] Ok?
[00:18:25 - 00:18:27] È impossibile
[00:18:27 - 00:18:29] perché forse sarebbe
[00:18:29 - 00:18:31] gli input a zero e a uno
[00:18:31 - 00:18:33] producendo zero e uno come
[00:18:33 - 00:18:35] come altro.
[00:18:35 - 00:18:37] Quindi, nell'ipotesi che io do S
[00:18:37 - 00:18:39] ed R uguale a zero,
[00:18:39 - 00:18:41] le combinazioni di
[00:18:41 - 00:18:43] stati che si possono verificare
[00:18:43 - 00:18:45] o meglio, quelli
[00:18:45 - 00:18:47] tra i quattro possibili
[00:18:47 - 00:18:49] in casi sono 0, 1
[00:18:49 - 00:18:51] o 0 di riesco a mantenere.
[00:18:51 - 00:18:53] Sono stati
[00:18:53 - 00:18:55] 0, 0 e i stabi
[00:18:55 - 00:18:57] quindi cambia
[00:18:57 - 00:18:59] e passo direttamente
[00:18:59 - 00:19:01] ad un altro
[00:19:01 - 00:19:03] e quell'altro è impossibile.
[00:19:03 - 00:19:05] Vediamo, invece,
[00:19:05 - 00:19:07] nel caso in cui
[00:19:07 - 00:19:09] S uguale a uno
[00:19:09 - 00:19:11] R uguale a zero.
[00:19:13 - 00:19:15] In questo caso
[00:19:17 - 00:19:19] S, quando S uguale a uno
[00:19:19 - 00:19:21] ovviamente vince
[00:19:21 - 00:19:23] qualunque sia il valore di Q
[00:19:23 - 00:19:25] perché volendo R
[00:19:25 - 00:19:27] vince
[00:19:27 - 00:19:29] poi c'è la negazione
[00:19:29 - 00:19:31] e viene zero.
[00:19:31 - 00:19:33] Quindi, S uguale a uno
[00:19:33 - 00:19:35] mi forza q negato a zero.
[00:19:37 - 00:19:39] R vale zero.
[00:19:39 - 00:19:41] 0, 0 negato
[00:19:41 - 00:19:43] fa 1.
[00:19:43 - 00:19:45] Quindi, qualunque
[00:19:45 - 00:19:47] chi ha lo stato attuale
[00:19:47 - 00:19:49] se S
[00:19:49 - 00:19:51] cioè se arriva la configurazione 1 o 0
[00:19:51 - 00:19:53] in ingresso
[00:19:53 - 00:19:55] oppure sta a uno
[00:19:55 - 00:19:57] oppure se sta a zero si porta a uno.
[00:20:03 - 00:20:05] Ci c'è Versa
[00:20:05 - 00:20:07] però funziona allo stesso mondo
[00:20:07 - 00:20:09] però al contrario se
[00:20:09 - 00:20:11] R ad essere 1
[00:20:11 - 00:20:13] e S uguale a zero
[00:20:13 - 00:20:15] o che vince 1
[00:20:15 - 00:20:17] nella nor
[00:20:17 - 00:20:19] inferiore
[00:20:19 - 00:20:21] quindi Q viene forzata a S0
[00:20:23 - 00:20:25] Q
[00:20:25 - 00:20:26] una volta che si
[00:20:26 - 00:20:27] propaga
[00:20:27 - 00:20:29] alla nor superiore
[00:20:29 - 00:20:31] viene S0
[00:20:31 - 00:20:33] Q uguale a zero
[00:20:33 - 00:20:35] quindi in alcun negato si porta a uno
[00:20:35 - 00:20:37] come si può diventa uno
[00:20:37 - 00:20:39] ora sta a uno o si porta a uno
[00:20:39 - 00:20:41] e quindi
[00:20:43 - 00:20:45] quando S uguale a zero
[00:20:45 - 00:20:47] ed R uguale a uno
[00:20:47 - 00:20:49] o Q
[00:20:49 - 00:20:51] era già a zero
[00:20:51 - 00:20:53] e resta a zero
[00:20:53 - 00:20:55] o Q se era a uno
[00:20:55 - 00:20:57] si porta a zero
[00:20:57 - 00:20:59] quindi per questo
[00:20:59 - 00:21:01] questa configurazione S0
[00:21:01 - 00:21:03] e R1 è il reset
[00:21:03 - 00:21:05] dell'H
[00:21:05 - 00:21:07] nel senso che il reset a zero è in uscita
[00:21:07 - 00:21:09] mentre se S uguale a uno
[00:21:09 - 00:21:11] ed R uguale a zero è il set
[00:21:11 - 00:21:13] dell'action
[00:21:13 - 00:21:15] nel senso che me lo porta
[00:21:15 - 00:21:17] a uno
[00:21:17 - 00:21:19] in uscita
[00:21:19 - 00:21:21] quindi o già si trova
[00:21:21 - 00:21:23] in quella situazione
[00:21:23 - 00:21:25] o la raggiunge e si stabilizza
[00:21:29 - 00:21:31] questa configurazione
[00:21:31 - 00:21:33] non viene permessa
[00:21:33 - 00:21:35] perché porterebbe
[00:21:35 - 00:21:37] continuamente tra i questati
[00:21:39 - 00:21:41] e quindi tipicamente gli unici ingressi per me
[00:21:41 - 00:21:43] si sono 0 1
[00:21:43 - 00:21:45] 1 0 e 0 0
[00:21:45 - 00:21:47] 0 0
[00:21:47 - 00:21:49] dobbiamo concentraci
[00:21:49 - 00:21:51] su questa figura
[00:21:51 - 00:21:53] le 0 0 mi mantiene allo stato attuale
[00:21:53 - 00:21:55] se è 0 resta a 0
[00:21:55 - 00:21:57] se è 1 resta a 1
[00:21:59 - 00:22:01] se 1 0
[00:22:01 - 00:22:03] me lo pone a 1
[00:22:03 - 00:22:05] me lo pone a 0
[00:22:05 - 00:22:07] questa configurazione semplicemente
[00:22:07 - 00:22:09] non è permessa
[00:22:11 - 00:22:13] quindi se vado a fare la tabella di verità
[00:22:13 - 00:22:15] la posso fare così
[00:22:15 - 00:22:17] 0 0
[00:22:17 - 00:22:19] dove l'uscita è lo stato
[00:22:19 - 00:22:21] T1
[00:22:21 - 00:22:23] nel senso dopo che i segnali
[00:22:23 - 00:22:25] immagino che
[00:22:25 - 00:22:27] all'istante T arriva
[00:22:27 - 00:22:29] una certa configurazione
[00:22:29 - 00:22:31] di S ed R
[00:22:31 - 00:22:33] all'istante T1
[00:22:39 - 00:22:41] lo stato sarà lo stesso
[00:22:41 - 00:22:43] di quello precedente
[00:22:43 - 00:22:45] se in ingresso c'ho 0 0
[00:22:45 - 00:22:47] quindi 0 0 in ingresso
[00:22:47 - 00:22:49] in uscita lo stato successivo
[00:22:49 - 00:22:51] sarà lo stesso attuale
[00:22:51 - 00:22:53] 0 1 va a 0
[00:22:53 - 00:22:55] 1 0 va a 1
[00:22:55 - 00:22:57] 1 1 semplicemente
[00:22:57 - 00:22:59] viene non permesso
[00:22:59 - 00:23:01] perché viene iniziato in un stato
[00:23:01 - 00:23:03] indeterminato
[00:23:03 - 00:23:05] non è quello che mi interessa
[00:23:05 - 00:23:07] mi serve qualcosa che memorizzi
[00:23:07 - 00:23:09] lo stato
[00:23:09 - 00:23:11] quindi tipicamente
[00:23:11 - 00:23:13] questi dispositivi, il lecce
[00:23:13 - 00:23:15] e come quando vedremo il flip flop
[00:23:15 - 00:23:17] o meglio quando introdurremo un segnale di abilitazione
[00:23:17 - 00:23:19] e disinclinizzazione
[00:23:21 - 00:23:23] cosa fanno
[00:23:23 - 00:23:25] come funziona
[00:23:25 - 00:23:27] funziona con l'idea che
[00:23:27 - 00:23:29] come il set
[00:23:29 - 00:23:31] o il reset
[00:23:31 - 00:23:33] del dispositivo
[00:23:33 - 00:23:35] di memoria e circuito di memoria
[00:23:35 - 00:23:37] e poi subito e dopo si porta
[00:23:37 - 00:23:39] all'ingresso 0 0
[00:23:39 - 00:23:41] in modo che
[00:23:41 - 00:23:43] o se è setato a 0 o 1
[00:23:43 - 00:23:45] poi si porta al memorizzarlo stato
[00:23:45 - 00:23:47] qui
[00:23:55 - 00:23:57] la descrizione del circuito
[00:23:57 - 00:23:59] come automa di mur
[00:24:01 - 00:24:03] o meglio come automa
[00:24:03 - 00:24:05] e si mette risatto che
[00:24:05 - 00:24:07] come tipologia di automa
[00:24:07 - 00:24:09] una automa di mur
[00:24:09 - 00:24:11] perché dipende l'uscita
[00:24:11 - 00:24:13] soltanto alla fine
[00:24:13 - 00:24:15] dallo stato
[00:24:17 - 00:24:19] lo stato
[00:24:19 - 00:24:21] e dipende dagli ingressi ovviamente
[00:24:21 - 00:24:23] ma l'uscita non è funzione
[00:24:23 - 00:24:25] più degli ingressi messo dello stato
[00:24:25 - 00:24:27] e per definizione diciamo
[00:24:27 - 00:24:29] mentre l'automa di mili
[00:24:29 - 00:24:31] cioè l'uscita è funzione
[00:24:31 - 00:24:33] sia dell'ingresso che dello stato
[00:24:33 - 00:24:35] se in un'automa
[00:24:35 - 00:24:37] l'uscita è solo funzione dello stato
[00:24:37 - 00:24:39] se dice che è una toma di mur
[00:24:39 - 00:24:41] e qua sono riportate da bella
[00:24:41 - 00:24:43] grafo di transizione dello stato
[00:24:43 - 00:24:45] in cui
[00:24:45 - 00:24:47] vediamo
[00:24:47 - 00:24:49] gli stati possibili sono 2
[00:24:49 - 00:24:51] q al e 0 e q al e 1
[00:24:51 - 00:24:53] e cosa può succedere
[00:24:53 - 00:24:55] l'abbiamo già detto semplicemente
[00:24:55 - 00:24:57] qua è rappresentato come
[00:24:57 - 00:24:59] grafo di transizione
[00:24:59 - 00:25:01] abbiamo che se arriva
[00:25:01 - 00:25:03] nella coppia di ingressi 0 0
[00:25:03 - 00:25:05] io resto
[00:25:05 - 00:25:07] in q al e 0
[00:25:07 - 00:25:09] ma lo stesso se mi trova in q al e 1
[00:25:09 - 00:25:11] e arriva la combinazione degli ingressi 0 0
[00:25:11 - 00:25:13] presto
[00:25:13 - 00:25:15] in q al e 1
[00:25:15 - 00:25:17] giusto per ricordarvi
[00:25:17 - 00:25:19] come funziona quindi nei nodi
[00:25:19 - 00:25:21] o la rappresentazione degli stati
[00:25:21 - 00:25:23] negli archi
[00:25:23 - 00:25:25] o diciamo
[00:25:25 - 00:25:27] in quale stato vado a finire
[00:25:27 - 00:25:29] quando arrivano a certa combinazione
[00:25:29 - 00:25:31] degli ingressi riportata sull'arco
[00:25:31 - 00:25:33] quindi
[00:25:33 - 00:25:35] ad esempio
[00:25:35 - 00:25:37] quest'arco tra q 0 e q 1
[00:25:37 - 00:25:39] mi rappresenta
[00:25:39 - 00:25:41] il fatto che
[00:25:41 - 00:25:43] se arriva 1 o 0
[00:25:43 - 00:25:45] e mi trovo in q al e 0
[00:25:45 - 00:25:47] mi sposto nello stato
[00:25:47 - 00:25:49] q al e 1
[00:25:49 - 00:25:51] e quindi
[00:25:51 - 00:25:53] la combinazione 0 0
[00:25:53 - 00:25:55] mi fa rimanere nello stato sia che
[00:25:55 - 00:25:57] sto di qua sia che sto da quest'arco
[00:25:57 - 00:25:59] là
[00:25:59 - 00:26:01] ovviamente se sto in q al e 0
[00:26:01 - 00:26:03] e mi arriva il reset
[00:26:03 - 00:26:05] resto
[00:26:05 - 00:26:07] q al e 0 quindi quest'arco
[00:26:07 - 00:26:09] condiviso tra queste due configurazioni
[00:26:09 - 00:26:11] per risparmare
[00:26:11 - 00:26:13] invece di fare due acchi
[00:26:13 - 00:26:15] c'è uno solo
[00:26:15 - 00:26:17] però è chiaro che valetto
[00:26:17 - 00:26:19] sia sopra che sotto
[00:26:19 - 00:26:21] quindi
[00:26:21 - 00:26:23] 0 0 mi fa rimanere in q al e 0
[00:26:23 - 00:26:25] 0 1 mi fa rimanere
[00:26:25 - 00:26:27] in q al e 0
[00:26:27 - 00:26:29] se invece mi trovo in q al e 1
[00:26:29 - 00:26:31] 0 0 resto in q al e 1
[00:26:31 - 00:26:33] 1 o 0 mi fa
[00:26:33 - 00:26:35] rimanere in q al e 0
[00:26:35 - 00:26:37] se mi trovo in q al e 1
[00:26:37 - 00:26:39] io l'unico modo per cambiare
[00:26:39 - 00:26:41] stato è che mi arrivi
[00:26:41 - 00:26:43] 0 1
[00:26:43 - 00:26:45] questo arco dice
[00:26:45 - 00:26:47] se mi trovo in q al e 0
[00:26:47 - 00:26:49] l'unico modo per cambiare stato
[00:26:49 - 00:26:51] è che mi arrivi
[00:26:51 - 00:26:53] q al e 0
[00:26:55 - 00:26:57] di nuovo questa
[00:26:57 - 00:26:59] la transizione
[00:26:59 - 00:27:01] è rappresentata
[00:27:01 - 00:27:03] in tabella
[00:27:03 - 00:27:05] la tabella di verità
[00:27:05 - 00:27:07] in cui vado a fare la funzione
[00:27:07 - 00:27:09] q t più 1
[00:27:09 - 00:27:11] sempre inteso
[00:27:11 - 00:27:13] come stato successivo
[00:27:13 - 00:27:15] in cui mi porto
[00:27:15 - 00:27:17] rappresento le stesse informazioni
[00:27:17 - 00:27:19] se sto in 0
[00:27:19 - 00:27:21] resto in 0
[00:27:21 - 00:27:23] con la coppia a 0 0 in ingresso
[00:27:23 - 00:27:25] se sto in 0 resto in 0
[00:27:25 - 00:27:27] resto in 1
[00:27:27 - 00:27:29] se invece mi arriva il reset
[00:27:29 - 00:27:31] vado in 0 a prescindere
[00:27:31 - 00:27:33] che mi trovi in 0 o che mi trovi in 1
[00:27:33 - 00:27:35] se mi arriva il set
[00:27:35 - 00:27:37] 1 o 0
[00:27:37 - 00:27:39] vado in 1 a prescindere
[00:27:39 - 00:27:41] che mi trovi in 0 o che mi trovi in 1
[00:27:41 - 00:27:43] ovviamente le ultime due diche
[00:27:43 - 00:27:45] non devono essere permette
[00:27:45 - 00:27:47] quindi lo stato successivo sarebbe
[00:27:47 - 00:27:49] indeterminato
[00:27:49 - 00:27:51] non le guardiamo
[00:27:51 - 00:27:53] muoviamo tra qualche slide
[00:27:53 - 00:27:55] delle soluzioni
[00:27:55 - 00:27:57] che impediscono
[00:27:57 - 00:27:59] questa configurazione
[00:27:59 - 00:28:01] di s uguale 1 r uguale 1
[00:28:05 - 00:28:07] questo sempre
[00:28:07 - 00:28:09] dell'ambito degli automi
[00:28:09 - 00:28:11] le transizioni si possono rappresentare
[00:28:11 - 00:28:13] non solo come un grafito
[00:28:13 - 00:28:15] ma anche tramite una tabella
[00:28:15 - 00:28:17] ma per di nuovo
[00:28:17 - 00:28:19] le informazioni sono sempre le stesse
[00:28:19 - 00:28:21] in questo caso
[00:28:21 - 00:28:23] una tabella di transizione dello stato
[00:28:23 - 00:28:25] abbiamo sulle righe i possibili stati
[00:28:25 - 00:28:27] e sulle colonne
[00:28:27 - 00:28:29] i possibili configurazioni
[00:28:29 - 00:28:31] degli input
[00:28:31 - 00:28:33] e di nuovo come lo leggo
[00:28:33 - 00:28:35] qui la presè entro
[00:28:35 - 00:28:37] se mi trovo in 0 e arriva
[00:28:37 - 00:28:39] questa configurazione degli input
[00:28:39 - 00:28:41] in quale stato vado a finire in 0
[00:28:41 - 00:28:43] se arriva 0 1
[00:28:43 - 00:28:45] vado in 0
[00:28:45 - 00:28:47] se arriva 1 o 0 vado in 1
[00:28:47 - 00:28:49] e così di anche per
[00:28:49 - 00:28:51] la seconda artigia
[00:28:53 - 00:28:55] quindi il lecce
[00:28:55 - 00:28:57] è un'automa di murro
[00:28:59 - 00:29:01] la presenza degli stati
[00:29:01 - 00:29:03] le leggiamo semplicemente
[00:29:03 - 00:29:05] o la tabella o il grafo
[00:29:05 - 00:29:07] niente di particolare
[00:29:09 - 00:29:11] allora
[00:29:11 - 00:29:13] quello il lecce esserre
[00:29:13 - 00:29:15] a sincrono da cui partiamo
[00:29:15 - 00:29:17] quindi le altre tipologie di circuiti
[00:29:17 - 00:29:19] che però
[00:29:19 - 00:29:21] riprendono sempre la stessa modalità
[00:29:21 - 00:29:23] di funzionamento
[00:29:23 - 00:29:25] ad esempio il lecce esserre
[00:29:25 - 00:29:27] temporizzato
[00:29:27 - 00:29:29] cosa fa?
[00:29:29 - 00:29:31] introduce vedete
[00:29:31 - 00:29:33] perché non so
[00:29:33 - 00:29:35] come?
[00:29:35 - 00:29:37] non mi è nemmeno
[00:29:37 - 00:29:39] fatto nessuna domanda
[00:29:39 - 00:29:41] ho detto le due cose
[00:29:45 - 00:29:47] fate attenzione a non attivare
[00:29:47 - 00:29:49] il microfono involontariamente
[00:29:49 - 00:29:51] allora dicevo
[00:29:51 - 00:29:53] guardate qua
[00:29:53 - 00:29:55] il lecce temporizzato si basa
[00:29:55 - 00:29:57] su un segnale
[00:29:57 - 00:29:59] esterno
[00:29:59 - 00:30:01] il clock
[00:30:01 - 00:30:03] per temporizzare
[00:30:03 - 00:30:05] il momento in cui devono avvenire
[00:30:05 - 00:30:07] questi cambiamenti di stato
[00:30:07 - 00:30:09] quindi
[00:30:09 - 00:30:11] l'idea è quella di non
[00:30:11 - 00:30:13] farli cambiare
[00:30:13 - 00:30:15] mentre
[00:30:15 - 00:30:17] il lecce
[00:30:17 - 00:30:19] l'essere
[00:30:19 - 00:30:21] cosa succede?
[00:30:21 - 00:30:23] appena cambiano i valori
[00:30:23 - 00:30:25] di esserre
[00:30:25 - 00:30:27] di conseguenza
[00:30:27 - 00:30:29] a meno del tempo di propagazione
[00:30:29 - 00:30:31] dei segnali avviene il cambiamento di stato
[00:30:31 - 00:30:33] se invece
[00:30:33 - 00:30:35] si vuole introdurre
[00:30:35 - 00:30:37] un tollo
[00:30:37 - 00:30:39] sul cambiamento di stato a dire ok
[00:30:39 - 00:30:41] in conto è che io metto
[00:30:41 - 00:30:43] ci faccio la commutazione del segnale ingresso
[00:30:43 - 00:30:45] però aspettiamo un attimo il cambiamento
[00:30:45 - 00:30:47] lo voglio synchronizzare
[00:30:47 - 00:30:49] voglio temporizzare
[00:30:49 - 00:30:51] per fare questo controllo
[00:30:51 - 00:30:53] bisogna mettere qualcosa in mezzo
[00:30:55 - 00:30:57] e lo facciamo
[00:30:57 - 00:30:59] tramite
[00:30:59 - 00:31:01] le solite end di abilitazione
[00:31:01 - 00:31:03] che abbiamo visto anche le volte scorse
[00:31:03 - 00:31:05] in cui diciamo che
[00:31:05 - 00:31:07] ma io voglio un segnale
[00:31:07 - 00:31:09] quindi
[00:31:09 - 00:31:11] s e dr io li porto al valore
[00:31:11 - 00:31:13] del nuovo
[00:31:13 - 00:31:15] stato che vorrei
[00:31:15 - 00:31:17] s 1 r
[00:31:17 - 00:31:19] 0 però non vanno
[00:31:19 - 00:31:21] ancora a imporre
[00:31:21 - 00:31:23] l'informazione
[00:31:23 - 00:31:25] il cambiamento di stato desiderato
[00:31:25 - 00:31:27] non vanno ancora a comandare
[00:31:27 - 00:31:29] l'essere che
[00:31:29 - 00:31:31] lo troviamo qua sulla testa
[00:31:31 - 00:31:33] finché il clock non dicio
[00:31:33 - 00:31:35] che adesso si può
[00:31:35 - 00:31:37] andare a valutare
[00:31:37 - 00:31:39] s r
[00:31:41 - 00:31:43] perché ovviamente il clock
[00:31:43 - 00:31:45] alimentando queste due end
[00:31:45 - 00:31:47] che mascherano
[00:31:47 - 00:31:49] s r al lecce
[00:31:49 - 00:31:51] che succede che ad esempio
[00:31:51 - 00:31:53] finché il clock è basso
[00:31:53 - 00:31:55] o il segnale di abilitazione
[00:31:55 - 00:31:57] è basso
[00:31:57 - 00:31:59] le end vengono
[00:31:59 - 00:32:01] nel praleggiere vanno a
[00:32:01 - 00:32:03] mandare 0 in uscita
[00:32:03 - 00:32:05] qualunque sia il valore di s r
[00:32:05 - 00:32:07] e se il clock è basso
[00:32:07 - 00:32:09] mi forza il valore
[00:32:09 - 00:32:11] 0 in ingresso al lecce
[00:32:11 - 00:32:13] ma noi abbiamo detto che
[00:32:13 - 00:32:15] 0 0 per il lecce
[00:32:15 - 00:32:17] vuol dire stai fermo, mantieni
[00:32:17 - 00:32:19] lo stato che hai e aspetta
[00:32:21 - 00:32:23] ti accormuta a livello
[00:32:23 - 00:32:25] questo qui?
[00:32:25 - 00:32:27] si per come disegnato
[00:32:29 - 00:32:31] però non andiamo
[00:32:31 - 00:32:33] a vedere
[00:32:33 - 00:32:35] che qualche altra modifica successiva
[00:32:35 - 00:32:37] però è importante capire che
[00:32:37 - 00:32:39] come commuti il segnale
[00:32:41 - 00:32:43] l'informazione di quello che volevo dire
[00:32:43 - 00:32:45] è che
[00:32:45 - 00:32:47] usando queste due end di abilitazione
[00:32:47 - 00:32:49] io sto dicendo
[00:32:49 - 00:32:51] i valori di s r vengono
[00:32:51 - 00:32:53] valutati
[00:32:53 - 00:32:55] secondo i tempi dettati
[00:32:55 - 00:32:57] dal segnale di abilitazione o comunque dal clock
[00:32:57 - 00:32:59] in questo senso
[00:32:59 - 00:33:01] mi sono sbagliato
[00:33:01 - 00:33:03] mi sono confuso con l'altra configurazione
[00:33:03 - 00:33:05] che è abilitato
[00:33:05 - 00:33:07] a tempo
[00:33:09 - 00:33:11] cioè l'altra
[00:33:11 - 00:33:13] era l'altra configurazione
[00:33:15 - 00:33:17] poi vediamo come si può
[00:33:17 - 00:33:19] fare con dell'impulso
[00:33:19 - 00:33:21] senza impulso
[00:33:21 - 00:33:23] al livello però è importante capire il concetto
[00:33:23 - 00:33:25] di andare a temporizzare
[00:33:25 - 00:33:27] a dare
[00:33:27 - 00:33:29] l'abilitazione
[00:33:29 - 00:33:31] a l'ex tramite queste
[00:33:31 - 00:33:33] porte di abilitazione
[00:33:33 - 00:33:35] le due end
[00:33:35 - 00:33:37] che forzano
[00:33:37 - 00:33:39] il segnale 00
[00:33:39 - 00:33:41] finché non arriva qualcosa che abilita
[00:33:41 - 00:33:43] la valutazione
[00:33:43 - 00:33:45] poi questa qualcosa vediamo si può fare in diversi modi
[00:33:45 - 00:33:47] come suggerivi tu
[00:33:47 - 00:33:49] però è importante capire l'idea che c'è dietro
[00:33:49 - 00:33:51] dalle porte
[00:33:51 - 00:33:53] il suo fatto di mettere le porte di abilitazione
[00:33:57 - 00:33:59] c'è così si dà il tempo
[00:33:59 - 00:34:01] di propagazione del segnale
[00:34:01 - 00:34:03] che non fa
[00:34:05 - 00:34:07] e non c'è il giochino
[00:34:07 - 00:34:09] dell'istabilità del segnale
[00:34:11 - 00:34:13] tipicamente più immaginati comunque
[00:34:13 - 00:34:15] che queste lo stiamo ragionando su
[00:34:15 - 00:34:17] un latch che è una memoria
[00:34:17 - 00:34:19] cioè a un bit no immaginate
[00:34:19 - 00:34:21] sempre la stringa di bit
[00:34:21 - 00:34:23] poi è costruito il registro
[00:34:23 - 00:34:25] e vuoi dare
[00:34:25 - 00:34:27] o comunque ci sono
[00:34:27 - 00:34:29] più segnali abilitate allora tu
[00:34:29 - 00:34:31] tipicamente si fa
[00:34:31 - 00:34:33] in modo che
[00:34:33 - 00:34:35] i segnali si potessero
[00:34:35 - 00:34:37] te lo desiderato
[00:34:37 - 00:34:39] e solo a quel punto si manda il cock
[00:34:39 - 00:34:41] per tutto
[00:34:41 - 00:34:43] che li va a sincronizzare
[00:34:43 - 00:34:45] da questo punto di vista
[00:34:45 - 00:34:47] quindi qui sono semplicemente
[00:34:47 - 00:34:49] tutto quello che vi ho già accennato
[00:34:49 - 00:34:51] quindi in questo caso
[00:34:51 - 00:34:53] il livello del clock finché il livello
[00:34:53 - 00:34:55] è basso
[00:34:55 - 00:34:57] le end forzate
[00:34:57 - 00:34:59] sono forzate ad avere zero in uscita
[00:34:59 - 00:35:01] livello basso in uscita
[00:35:01 - 00:35:03] la configurazione è 00
[00:35:03 - 00:35:05] per mezzo
[00:35:05 - 00:35:07] vuol dire mantieni lo stato
[00:35:07 - 00:35:09] e quindi s e r
[00:35:09 - 00:35:11] non vengono valutate praticamente
[00:35:11 - 00:35:13] finché il clock è basso
[00:35:13 - 00:35:15] quando il clock
[00:35:15 - 00:35:17] è altro
[00:35:17 - 00:35:19] che di nuovo può essere anche
[00:35:19 - 00:35:21] un segnale di abilitazione
[00:35:21 - 00:35:23] ovviamente nella end
[00:35:23 - 00:35:25] l'uno
[00:35:25 - 00:35:27] il valore alto del clock
[00:35:27 - 00:35:29] viene ignorato
[00:35:29 - 00:35:31] non contribuisce
[00:35:31 - 00:35:33] vengono valutati s e r
[00:35:33 - 00:35:35] quindi all'uscita delle end
[00:35:35 - 00:35:37] quando il clock
[00:35:37 - 00:35:39] è alto passano effettivamente
[00:35:39 - 00:35:41] i veri valori di s e r
[00:35:41 - 00:35:43] quelli desiderati quindi
[00:35:43 - 00:35:45] è in questo momento soltanto
[00:35:45 - 00:35:47] che avviene all set
[00:35:47 - 00:35:49] o il reset
[00:35:51 - 00:35:53] testa però un problema
[00:35:53 - 00:35:55] che è quello di s e r
[00:35:55 - 00:35:57] vuole 1
[00:35:57 - 00:35:59] quindi abbiamo
[00:35:59 - 00:36:01] diciamo in qualche modo
[00:36:01 - 00:36:03] introdotto un miglioramento
[00:36:03 - 00:36:05] con la temporizzazione
[00:36:05 - 00:36:07] testa però il problema
[00:36:07 - 00:36:09] che ci dobbiamo preoccupare
[00:36:09 - 00:36:11] di evitare di
[00:36:11 - 00:36:13] mandare questi due segnali
[00:36:13 - 00:36:15] che però sono ancora diciamo
[00:36:15 - 00:36:17] possibili
[00:36:21 - 00:36:23] ma per questo abbiamo detto
[00:36:23 - 00:36:25] quando lo serve
[00:36:25 - 00:36:27] quando ha necessità
[00:36:27 - 00:36:29] di sincronizzare
[00:36:29 - 00:36:31] il dispositivo
[00:36:31 - 00:36:33] il dispositivo che praticamente
[00:36:33 - 00:36:35] hanno tempistiche diverse
[00:36:35 - 00:36:37] hanno velocità diverse
[00:36:37 - 00:36:39] con il clock
[00:36:39 - 00:36:41] possiamo sincronizzarti
[00:36:41 - 00:36:43] quello che voglio far più vedere
[00:36:43 - 00:36:45] è il latch
[00:36:45 - 00:36:47] di temporizzato
[00:36:47 - 00:36:49] che cosa fa
[00:36:49 - 00:36:51] va a risolvere
[00:36:51 - 00:36:53] la problematica
[00:36:53 - 00:36:55] della configurazione
[00:36:55 - 00:36:57] s e r uguale 1
[00:36:57 - 00:36:59] e come funziona
[00:36:59 - 00:37:01] semplicemente va ad aggiungere
[00:37:01 - 00:37:03] un unico
[00:37:03 - 00:37:05] cioè va
[00:37:05 - 00:37:07] a ridurre
[00:37:07 - 00:37:09] segnali ingresso a uno solo
[00:37:11 - 00:37:13] in questo modo
[00:37:13 - 00:37:15] per come è configurato
[00:37:15 - 00:37:17] segnali ingresso a uno solo
[00:37:17 - 00:37:19] e di
[00:37:19 - 00:37:21] si prende il circuito di prima
[00:37:21 - 00:37:23] si aggiunge però
[00:37:23 - 00:37:25] si elimina praticamente
[00:37:25 - 00:37:27] il reset e viene collegato
[00:37:27 - 00:37:29] con questa notte
[00:37:29 - 00:37:31] perché a noi non ci interessa
[00:37:31 - 00:37:33] abbiamo detto solo
[00:37:33 - 00:37:35] tornando adesso al latch
[00:37:35 - 00:37:37] temporizzato
[00:37:37 - 00:37:39] a noi basta che
[00:37:39 - 00:37:41] ci interesse non solo le configurazioni
[00:37:41 - 00:37:43] 1 0 e 0 1
[00:37:43 - 00:37:45] perché la configurazione
[00:37:45 - 00:37:47] s e r uguale 0
[00:37:47 - 00:37:49] la fine non la mandiamo più
[00:37:49 - 00:37:51] nel latch temporizzato
[00:37:51 - 00:37:53] basta usare il segnale di
[00:37:53 - 00:37:55] abilitazione basso
[00:37:55 - 00:37:57] quindi finché
[00:37:57 - 00:37:59] il clock basso
[00:37:59 - 00:38:01] finché
[00:38:01 - 00:38:03] segnale di abilitazione basso
[00:38:03 - 00:38:05] semplicemente il latch mantiene tutto il stato
[00:38:05 - 00:38:07] quindi ci siamo ridotti
[00:38:07 - 00:38:09] a queste configurazioni
[00:38:09 - 00:38:11] interesse 1 0 e 0 1
[00:38:11 - 00:38:13] e questa cosa viene spinta
[00:38:13 - 00:38:15] ancora di più
[00:38:15 - 00:38:17] nelle cd in cui dico che allora se mi servono
[00:38:17 - 00:38:19] solo queste due configurazioni
[00:38:19 - 00:38:21] uso
[00:38:21 - 00:38:23] un unico segnale visto che
[00:38:23 - 00:38:25] l'altro segnale di ingresso
[00:38:25 - 00:38:27] è la negazione
[00:38:27 - 00:38:29] che a me mi serve solo o 1 o 0 o 0 o 1
[00:38:29 - 00:38:31] uso solo il segnale di
[00:38:31 - 00:38:33] di ingresso
[00:38:33 - 00:38:35] in cui dico se di uguale 1
[00:38:35 - 00:38:37] file set
[00:38:37 - 00:38:39] del circuito lo poniamo 1
[00:38:39 - 00:38:41] se di uguale 0
[00:38:41 - 00:38:43] file set
[00:38:43 - 00:38:45] del circuito a 0
[00:38:45 - 00:38:47] questa cosa come funziona
[00:38:47 - 00:38:49] finalmente collegando il d
[00:38:49 - 00:38:51] a entrambi le porte and di prima
[00:38:51 - 00:38:53] però giù vedete si manda
[00:38:53 - 00:38:55] la versione negata di d
[00:38:55 - 00:38:57] ok
[00:38:57 - 00:38:59] questo cosa comporta che
[00:38:59 - 00:39:01] qua abbiamo sempre segnale di temporizzazione
[00:39:01 - 00:39:03] segnale di temporizzazione che
[00:39:03 - 00:39:05] come prima
[00:39:05 - 00:39:07] finché basso
[00:39:07 - 00:39:09] dice al circuito ignora d
[00:39:09 - 00:39:11] e mantieni lo stato
[00:39:11 - 00:39:13] perché?
[00:39:13 - 00:39:15] perché se il segnale è basso all'uscita
[00:39:15 - 00:39:17] delle end c'è 0 o 0
[00:39:17 - 00:39:19] 0 o 0
[00:39:19 - 00:39:21] nell'ecce sr che sta
[00:39:21 - 00:39:23] nell'estrema destra diciamo del circuito
[00:39:23 - 00:39:25] vuol dire mantieni lo stato
[00:39:25 - 00:39:27] fin qua ci siamo
[00:39:27 - 00:39:29] quando d uguale 1
[00:39:29 - 00:39:31] vuol dire
[00:39:31 - 00:39:33] mandare nell'ecce temporizzato
[00:39:33 - 00:39:35] 1 o 0
[00:39:35 - 00:39:37] e cioè mandare 1 o 0
[00:39:37 - 00:39:39] nell'ecce sr
[00:39:39 - 00:39:41] ovviamente ha messo che il clock si up
[00:39:41 - 00:39:43] se invece d
[00:39:43 - 00:39:45] è uguale 0
[00:39:45 - 00:39:47] vuol dire che
[00:39:47 - 00:39:49] all'ingresso delle end
[00:39:49 - 00:39:51] arriva 0 o 1
[00:39:51 - 00:39:53] perché c'è la porta negata
[00:39:53 - 00:39:55] c'è la notte giù
[00:39:55 - 00:39:57] quindi
[00:39:57 - 00:39:59] con il ecce temporizzato
[00:39:59 - 00:40:01] eliminiamo
[00:40:01 - 00:40:03] la cortezza di dover
[00:40:03 - 00:40:05] controllare che sr non vadano a 1
[00:40:05 - 00:40:07] perché per definizione
[00:40:07 - 00:40:09] cioè per come costruire questo circuito
[00:40:09 - 00:40:11] non si verifica
[00:40:11 - 00:40:13] mai non si può
[00:40:13 - 00:40:15] più verificare il caso
[00:40:15 - 00:40:17] sr uguale 1
[00:40:17 - 00:40:19] trovate?
[00:40:25 - 00:40:27] se si semplifica pure la tabella della verità
[00:40:27 - 00:40:29] in questo caso
[00:40:29 - 00:40:31] eccentro che abbiamo ridotto
[00:40:31 - 00:40:33] gli ingressi e adesso non abbiamo uno solo
[00:40:35 - 00:40:37] diciamo abbiamo complicato
[00:40:37 - 00:40:39] e ingrandito il circuito
[00:40:39 - 00:40:41] però ne gioviamo
[00:40:41 - 00:40:43] in possibilità di temporizzazione
[00:40:43 - 00:40:45] e
[00:40:45 - 00:40:47] riduciamo il problema
[00:40:47 - 00:40:49] a monte il fatto di dover evitare
[00:40:49 - 00:40:51] che si verifichi la configurazione degli ingressi
[00:40:51 - 00:40:53] qua è impossibile perché abbiamo un unico ingresso
[00:40:53 - 00:40:55] quindi
[00:40:55 - 00:40:57] se vale 0 va bene, se vale 1 va bene
[00:40:57 - 00:40:59] basta non ci sono casi
[00:40:59 - 00:41:01] da evitare
[00:41:01 - 00:41:03] e se non è più vero
[00:41:03 - 00:41:05] cioè che abbiamo sempre questi due ingressi
[00:41:05 - 00:41:07] uno che è il segnale di clock
[00:41:07 - 00:41:09] e l'altro che è
[00:41:09 - 00:41:11] segnale di
[00:41:11 - 00:41:13] quindi che lo potremmo
[00:41:13 - 00:41:15] potrebbero essere queste due
[00:41:15 - 00:41:17] c'è 3 compilurazioni
[00:41:17 - 00:41:19] a due e giù
[00:41:19 - 00:41:21] il clock che
[00:41:21 - 00:41:23] rimane
[00:41:23 - 00:41:25] certe non cambia
[00:41:25 - 00:41:27] alla fine quando il clock è giù
[00:41:27 - 00:41:29] mi forza 0 0
[00:41:29 - 00:41:31] quando il clock è su
[00:41:31 - 00:41:33] semplicemente mi fa passare di
[00:41:33 - 00:41:35] fa funzionare il circuito
[00:41:35 - 00:41:37] sì
[00:41:37 - 00:41:39] il circuito comunque resta in funzione
[00:41:39 - 00:41:41] perché mi mantiene lo stato
[00:41:43 - 00:41:45] il clock serve solo
[00:41:45 - 00:41:47] da interruttore per di
[00:41:47 - 00:41:49] lo fa passare o non lo fa passare
[00:41:51 - 00:41:53] quando non lo fa passare
[00:41:53 - 00:41:55] mi manda 0 0 in ingresso
[00:41:55 - 00:41:57] al lec
[00:41:57 - 00:41:59] diciamo su semplici
[00:42:03 - 00:42:05] è giusto per capire
[00:42:05 - 00:42:07] qual è il senso di fare
[00:42:07 - 00:42:09] queste modifiche
[00:42:09 - 00:42:11] di introdurre queste modifiche
[00:42:11 - 00:42:13] che problemi si vogliono andare a risolvere
[00:42:13 - 00:42:15] rispetto al lec sr
[00:42:15 - 00:42:17] diciamo di pastenza
[00:42:19 - 00:42:21] quindi
[00:42:21 - 00:42:23] lec sr
[00:42:23 - 00:42:25] e sr
[00:42:27 - 00:42:29] e lec sr
[00:42:29 - 00:42:31] temporizzato
[00:42:31 - 00:42:33] si può fare la temporizzazione
[00:42:33 - 00:42:35] anche sul
[00:42:35 - 00:42:37] sr
[00:42:37 - 00:42:39] introduciamo poi lec d
[00:42:39 - 00:42:41] per evitare questa problemata
[00:42:41 - 00:42:43] qui sono ripetute le cose
[00:42:43 - 00:42:45] che vi accendono prima
[00:42:45 - 00:42:47] 0 0 mi forza
[00:42:47 - 00:42:49] il mantenimento dello stato
[00:42:49 - 00:42:51] o comunque mi garantisci
[00:42:51 - 00:42:53] il mantenimento dello stato
[00:42:53 - 00:42:55] quando il clock è basso
[00:42:55 - 00:42:57] o comunque quando il segnale di
[00:42:57 - 00:42:59] abilitazione è basso
[00:42:59 - 00:43:01] se è alto mi fa passare di
[00:43:01 - 00:43:03] e poi ovviamente di uguale 1
[00:43:03 - 00:43:05] coinciderà
[00:43:05 - 00:43:07] con il set del lec
[00:43:07 - 00:43:09] di uguale 0 coinciderà con il reset
[00:43:09 - 00:43:11] del lec
[00:43:21 - 00:43:23] e qua parla di
[00:43:23 - 00:43:25] di cambiamento
[00:43:25 - 00:43:27] nel senso che ovviamente
[00:43:27 - 00:43:29] quando il clock è alto
[00:43:29 - 00:43:31] mi fa passare di
[00:43:31 - 00:43:33] che ovviamente in questo caso
[00:43:33 - 00:43:35] coincide con il
[00:43:35 - 00:43:37] valore di di proprio quello che vado a memorizzare
[00:43:37 - 00:43:39] non è più un set e un reset
[00:43:39 - 00:43:41] se guardo il circuito dall'estero
[00:43:41 - 00:43:43] senza focalizzarmi sulla parte di lec
[00:43:43 - 00:43:45] io se di uguale 1
[00:43:45 - 00:43:47] vado a memorizzare effettivamente di
[00:43:47 - 00:43:49] se di uguale 0
[00:43:49 - 00:43:51] vado a memorizzare effettivamente
[00:43:51 - 00:43:53] 0 quindi adesso costruito
[00:43:53 - 00:43:55] non un circuito che si può
[00:43:55 - 00:43:57] settare per settare ma il circuito
[00:43:57 - 00:43:59] effettivamente di memoria
[00:43:59 - 00:44:01] si permette di
[00:44:01 - 00:44:03] salvare il valore di di
[00:44:03 - 00:44:05] quindi immaginiamo che
[00:44:05 - 00:44:07] di sia un segnale che proviene
[00:44:07 - 00:44:09] da un altro lato del nostro
[00:44:09 - 00:44:11] calcolatore se io lo voglio memorizzare
[00:44:11 - 00:44:13] mi basta mandare
[00:44:13 - 00:44:15] abilitazione
[00:44:15 - 00:44:17] a questo registro
[00:44:17 - 00:44:19] di memoria di
[00:44:19 - 00:44:21] di che effettivamente mi prende
[00:44:21 - 00:44:23] il valore di di e me lo memorizza
[00:44:33 - 00:44:35] beh queste sono qualche considerazione
[00:44:35 - 00:44:37] su quanti transistor
[00:44:37 - 00:44:39] possono o sono
[00:44:39 - 00:44:41] tipicamente coinvolti
[00:44:41 - 00:44:43] ma è stato che noi in una lezione
[00:44:43 - 00:44:45] è una possibile implementazione
[00:44:45 - 00:44:47] di una porta
[00:44:47 - 00:44:49] con i transistor
[00:44:49 - 00:44:51] però poi
[00:44:51 - 00:44:53] diciamo ci sono versioni più o meno
[00:44:53 - 00:44:55] ottimizzate che certano di ridurre
[00:44:55 - 00:44:57] il numero del transistor
[00:44:57 - 00:44:59] come vedete si parla di una decina
[00:44:59 - 00:45:01] di transistor
[00:45:01 - 00:45:03] coinvolti
[00:45:09 - 00:45:11] e che dire
[00:45:11 - 00:45:13] questo è un elemento di memoria
[00:45:13 - 00:45:15] che mantiene lo stato
[00:45:15 - 00:45:17] abbiamo detto quindi mantenere
[00:45:17 - 00:45:19] l'informazione finché alimentato
[00:45:19 - 00:45:21] quindi l'informazione
[00:45:21 - 00:45:23] diciamo non deve essere
[00:45:23 - 00:45:25] aggiornata
[00:45:25 - 00:45:27] nel tempo
[00:45:27 - 00:45:29] tutta l'affatti
[00:45:29 - 00:45:31] della storia
[00:45:39 - 00:45:41] ci sono invece altri elementi di memoria
[00:45:43 - 00:45:45] nel calcolatore non banalmente la memoria RAM
[00:45:45 - 00:45:47] ovviamente è molto più
[00:45:47 - 00:45:49] evoluta di quello che stiamo vedendo
[00:45:49 - 00:45:51] in questo momento che però sono
[00:45:51 - 00:45:53] elementi che invece richiedono
[00:45:53 - 00:45:55] il refresh
[00:45:55 - 00:45:57] l'informazione
[00:45:57 - 00:45:59] anche se il circuito è alimentato
[00:45:59 - 00:46:01] diciamo può decadere
[00:46:01 - 00:46:03] quindi richiede
[00:46:03 - 00:46:05] l'aggiornamento continuo
[00:46:07 - 00:46:09] mentre il leccidic abbiamo visto
[00:46:09 - 00:46:11] adesso cioè finché alimentato
[00:46:11 - 00:46:13] resta l'informazione
[00:46:13 - 00:46:15] non è basata
[00:46:15 - 00:46:17] ad esempio un capacitore
[00:46:17 - 00:46:19] che decade
[00:46:19 - 00:46:21] una ferma
[00:46:23 - 00:46:25] domande sono queste cose
[00:46:25 - 00:46:27] qualche dubbio
[00:46:35 - 00:46:37] vabbè allora se non ci sono domande
[00:46:37 - 00:46:39] vi libero e vi auguro
[00:46:39 - 00:46:41] una buona serata
[00:46:41 - 00:46:43] alla prossima
[00:46:43 - 00:46:45] buona serata a lei
[00:46:45 - 00:46:47] buona serata
[00:46:47 - 00:46:49] buona serata
