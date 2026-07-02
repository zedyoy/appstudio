# lezione5

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\lezione5.mp4`
- Durata: 00:58:03
- Trascrizione: `05_lezione5.json`

## Argomenti probabili
- porte_logiche (503): and, or, not, nor, nand, xor, boole, sop
- memoria_bus (16): memoria, bus, ram
- conversioni (13): binario, base
- microarchitettura (8): microarchitettura, mic, alu
- mips_assembly (3): registro, sb, addi

## Trascrizione

[00:00:00 - 00:00:02] Ok, grazie.
[00:00:04 - 00:00:07] Giusto un minuto o due e comincio.
[00:00:30 - 00:00:32] Buon appetito.
[00:01:00 - 00:01:02] Buon appetito.
[00:01:30 - 00:01:55] Allora in questa lezione cominciamo a vedere un po' la posta.
[00:01:55 - 00:02:07] Allora in questa lezione cominciamo a vedere la parte, la logica digitale, inseriamo a vedere le porte logiche,
[00:02:07 - 00:02:19] leggiamo i concetti su cui si baseranno poi la postazione dei circuiti più complessi che vedremo nelle prossime lezioni.
[00:02:19 - 00:02:29] Allora, vi ricordate quando abbiamo visto che un Calcolatore tipicamente viene realizzato e progettato come una macchina a livelli di complessità,
[00:02:29 - 00:02:45] estrazione sempre diversa, quindi dal livello più basso che questo appunto della logica digitale fino a salire verso i livelli più alti del linguaggio di programmazione?
[00:02:45 - 00:03:00] Abbiamo detto che i livelli più vicini a quelli alla realizzazione effettiva del Calcolatore sono appunto il livello 0 e il livello 1.
[00:03:00 - 00:03:17] E diciamo ogni macchina, ogni livello di estrazione, abbiamo detto come una macchina visuale che in qualche modo ha visibilità di quello che offre il livello inferiore,
[00:03:17 - 00:03:37] però non sa come viene implementato il livello inferiore, descrive i programmi meglio le istruzioni che deve seguire secondo il linguaggio del suo livello e quello che deve fare è tradurlo nel linguaggio della macchina inferiore
[00:03:37 - 00:03:58] per raggiungere poi all'ultimo livello effettivamente all'esecuzione dell'estruzione. L'ultimo livello c'è il primo, in questo caso il livello 0 arrivano poi all'estruzione vera che è come vengono poi realizzate e eseguiti direttamente dai circuiti digitali.
[00:03:58 - 00:04:25] Questo livello quindi è il livello della logica digitale dove abbiamo una combinazione di dispositivi elettronici che chiameremo porte logiche o gate, poi come effettivamente una porta logica viene implementata, vedremo giusto un esempio di implementazione,
[00:04:25 - 00:04:50] restiamo a livello di porta logica, capiamo qual è il funzionamento in una porta logica in senso che output produce in corrispondenza di determinati input, però poi non lo scenderemo a livello dei transistor effettivamente, lo vedremo giusto in una slide come esempio come curiosità,
[00:04:50 - 00:05:07] però restiamo a livello di porta logica digitale, c'è il livello più basso che vedremo. Poi c'è il livello 1 indicato come livello 1 che sarà il livello della microarchitettura su cui ci concentreremo su questo corso,
[00:05:08 - 00:05:31] che la parte principale che vediamo quasi i livelli che approfondiamo maggiormente in questo corso sono il livello 0 e il livello 1, il livello 0 è appunto questo delle porte digitali su cui ragioneremo per capire come vengono costruiti i circuiti elettronici fondamentali,
[00:05:32 - 00:05:56] tipo una memoria, un registro, un addizionatore e così via. Nel livello 1 invece che vedremo si chiama livello della microarchitettura vedremo come questi componenti fondamentali che vediamo nel livello 0 vengono utilizzati per costruire il bus, il datapad, l'alu e così via.
[00:05:57 - 00:06:06] Quindi diciamo queste sono le parti fondamentali su cui poi i mattoancini diciamo che poi vengono utilizzati per costruire i calcolatori.
[00:06:07 - 00:06:27] Allora in generale un circuito digitale lo possiamo vedere ovviamente come un circuito elettronico in cui abbiamo già detto che parliamo di circuito digitale e assumiamo che la cifra a cui facciamo riferimento è la cifra binaria.
[00:06:28 - 00:06:36] Quindi un circuito digitale in circuito che dicevuto in ingresso una combinazione di valori produce delle uscite.
[00:06:37 - 00:06:43] Nel momento in cui diciamo che la logica digitale su cui andiamo a ragionare è quella binaria,
[00:06:44 - 00:06:54] vuol dire che le combinazioni possibili degli ingressi sono le combinazioni dei valori 0 e 1 che si possono realizzare diciamo in base al numero degli ingressi del circuito.
[00:06:55 - 00:07:05] Quindi se un circuito digitale ha un unico ingresso potete già immaginare che ovviamente i possibili valori sono semplicemente 2, 0 e 1.
[00:07:05 - 00:07:18] Se sono due ingressi possiamo fare le combinazioni possibili di questi due ingressi, 0 e 1 per ogni ingresso vuol dire quattro possibili coppie di combinazioni e così via.
[00:07:18 - 00:07:35] Quindi un vantaggio che tornerà spesso che sfrutteremo per ragionare circuito digitale è fatto che le combinazioni possibili degli ingressi, quindi anche delle uscite sono finite,
[00:07:35 - 00:08:01] possiamo calcolare quanti possibili ingressi possiamo avere e quindi assegnando ogni possibile ingresso quale il valore di uscita possiamo semplicemente elencando le combinazioni, le coppie o meglio le tuple in generale di ingressi e uscite possiamo descrivere in maniera completa diciamo un circuito digitale.
[00:08:02 - 00:08:20] Ci torneremo questo che diciamo un circuito o vedremo tra qualche slide una funzione buleana quindi la possiamo descrivere non soltanto attraverso una formula o un'espressione come siamo abituate con le funzioni normali,
[00:08:20 - 00:08:38] ma sfruttando questa proprietà che il numero degli ingressi e il numero di possibili loro sono finiti, un modo per descrivere un circuito digitale o una funzione buleana è quello di enunciare semplicemente tutte le possibili combinazioni.
[00:08:39 - 00:09:06] Generale, se il circuito digitale generico ovviamente avrà n ingressi, ovviamente può cambiare da 1 a un numero entero n e può avere una o più uscite, questo slide è indignato con m le possibili uscite del circuito,
[00:09:07 - 00:09:27] ovviamente ogni singola uscita di un circuito digitale è tipicamente una funzione degli ingressi, quindi se ho m ingressi avrò m funzioni che descrivono le uscite, sempre funzioni degli ingressi.
[00:09:28 - 00:09:45] Queste funzioni che vanno a lavorare su variabili che abbiamo detto assumono soltanto il valore 0 1 e quindi possiamo definire variabili buleane sono quindi funzioni di variabili buleane, sono funzioni buleane, si dico, ti chiamano.
[00:09:46 - 00:10:03] Una funzione buleana e quindi una generica funzione che ha come dominio l'insieme delle possibili combinazioni 0 e 1 in base ovviamente alla cardinalità di quanti ingressi hanno, questo insieme 0 1 con cardinalità n
[00:10:03 - 00:10:32] fa appunto di ferimento che se c'è un ingresso sarà insieme 0 1, se ci sono due ingressi il dominio sarà l'insieme delle coppie che posso costruire sull'insieme 0 1, quindi 0 0, 0 1, 1 0, 1 1 e così via, se ho 3 ingressi il dominio sarà l'insieme delle triple che posso costruire con i valori 0 1, quindi 0 0 0.
[00:10:34 - 00:10:45] Il codominio invece della singola funzione buleana è sempre l'insieme 0 1, cioè il valore di una funzione o è 0 o è 1.
[00:10:45 - 00:11:14] Su questo mondo diciamo delle variabili buleane si define poi l'algebra buleana o l'algebra di bull che descrive appunto le proprietà diciamo delle variabili buleane e delle funzioni buleane.
[00:11:15 - 00:11:40] L'algebra buleana è stata sviluppata da Giorgio Bull, come un concetto più ampio, non è relativo diciamo un concetto dei circuiti ovviamente, ma era un concetto relativo alla logica e il ragionamento logico-matematico in cui si basava su un'algebra che può essere definita ogni qual voto.
[00:11:40 - 00:12:07] Tutta c'è una proposizione che può essere vera o falsa, cioè un concetto di origine buleana direi in generale binaria nel caso nostro che nell'algebra di bull quindi come abbiamo visto prima vale in generale il concetto che le funzioni buleane hanno uno più variabili di input,
[00:12:07 - 00:12:26] ma in uscita hanno sempre un solo valore che può essere buleano o binario, se preferite, cioè può essere o zero o uno, nel nostro caso in generale in un algebra di bull, una funzione buleana può avere un valore vero o falso o falso o alto o basso e così via.
[00:12:26 - 00:12:55] L'idea di questa, cioè la grande proprietà che sfrutteremo, che si sfrutta in generale delle funzioni buleane è questa che vi accennavo prima, cioè il fatto che i possibili valori degli ingressi sia un insieme finito e non è come per esempio in una funzione reale ovviamente noi abbiamo che l'insieme del domino sono i numeri reali,
[00:12:56 - 00:13:12] e possono assumere infiniti valori, infinite combinazioni, quindi una funzione reale, tipicamente noi siamo abituati a definirla tramite una formula, una funzione effettiva delle variabili reali di x, di z, y e così via.
[00:13:12 - 00:13:37] Nel caso buleano ovviamente possiamo sempre scrivere una funzione informalgebrica, cioè da tramite un'espressione di variabili buleane, però possiamo in vaniera equivalente definire una funzione semplicemente elencando tutte le possibili combinazioni di ingresse e uscite perché sono un insieme finito.
[00:13:42 - 00:14:11] E questo questo concetto è un modo per definire una funzione quello di descrivere la sua tabella di verità si chiama, quindi una funzione buleana di n variabili in generale può essere o espressa tramite una forma algebrica, un'espressione, una funzione delle variabili oppure elencando le possibili combinazioni di ingresso
[00:14:11 - 00:14:36] e assegnando ad ogni combinazione degli ingressi l'uscita, cioè il valore di uscita. Questo elenco esastivo di tutte le possibili combinazioni degli ingressi con assegnato il valore di uscita per ogni combinazione si chiama tabella di verità, quindi una funzione buleana è sempre definita o essere sempre definita tramite la sua tabella di verità.
[00:14:36 - 00:15:05] In questo esempio che vedete nella slide abbiamo una funzione buleana di tre variabili, quindi indicate con vi 1, vi 2, vi 3 che sono variabili buleane, costruire la sua tabella di verità vuol dire andarsi a scrivere mananmente tutte le possibili combinazioni che possiamo trovare, combinazioni ovviamente distinte, di queste variabili andando a cambiare appunto i possibili valori.
[00:15:06 - 00:15:23] Quindi abbiamo che una prima combinazione, un primo, diciamo, punto del dominio di questa funzione di esempio sarà la tripletta, la tripla 0, 0, 0, un altro punto sarà 0, 0, 1, un altro punto sarà 0, 1, 0, cioè tutte le possibili combinazioni dei tre ingressi.
[00:15:24 - 00:15:47] E noi sappiamo benissimo che se abbiamo tre bit a disposizione o in questo caso tre variabili a disposizione, le possibili valori binari che posso costruire su tre variabili o tre bit come siamo abituati a ragionare sono due elevato al numero di valori.
[00:15:48 - 00:16:09] Questo concetto qui lo vado ad usare dicendo che le righe della tabella di verità, il numero di righe della tabella di verità è pari a 2 alla n dove è nel numero di ingressi o meglio del numero delle variabili di ingresso della funzione, funzione qui nell'esempio a tre variabili di ingresso quindi avremo otto righe.
[00:16:10 - 00:16:28] Fatto ciò bisogna poi definire quanto vale la funzione in uscita, in questo esempio quando ingresso o la configurazione 0, 0, 0, in uscita la funzione è alta o vale 1.
[00:16:29 - 00:16:34] 0, 0, 1 vale 1, 0, 1, 0 vale 0, 0, 1, 1 vale 0 e così via.
[00:16:36 - 00:16:54] Quindi vi trovate che il numero di funzioni booleane che posso costruire su tre variabili booleane ovviamente non è unico posso costruire più funzioni ma non è infinito.
[00:16:54 - 00:16:59] Anche quello è un valore che posso calcolare.
[00:16:59 - 00:17:19] Tra le tante funzioni o meglio tra le varie funzioni che esistono su tre variabili booleane la specifica funzione che sto definendo, che sto assegnando a questo esempio è quella in cui vado a dire i valori della F.
[00:17:19 - 00:17:35] Ovviamente questo esempio è ricordato con una funzione ma se io uno di queste uscite, la cambio per esempio invece di avere il valore alto quando vale 0, 0, metto 0 sto cambiando un'altra funzione, quella è una funzione diversa.
[00:17:35 - 00:17:54] La funzione che dà 0 quando in ingresso c'ho 0, 0, 0 e quindi ogni possibile asseniazione della colonna F mi darà una funzione booleana diversa sempre su tre variabili ma diversa da quella precedente.
[00:17:55 - 00:18:06] E ovviamente nel momento in cui scegliamo quanto vale F per ogni riga stiamo definendo una particolare funzione di tre variabili booleane tra le possibili che esistono.
[00:18:07 - 00:18:24] E ovviamente se vi faccio la domanda quante funzioni posso costruire possiamo sempre applicare il ragionamento di prima.
[00:18:24 - 00:18:36] Abbiamo detto che noi sappiamo calcolare le possibili combinazioni binarie su N bit a disposizione, su N variabili a disposizione.
[00:18:36 - 00:18:45] Il ragionamento che prima abbiamo fatto in cui abbiamo detto quante righe ci sono, lo calcoliamo facendo 2 alla N dove N è il numero di variabili di ingresso.
[00:18:46 - 00:19:05] In questo esempio viene 8, lo possiamo applicare nuovamente nel momento in cui vi chiedo quante funzioni invece posso costruire diverse su queste tre variabili dovete ragionare sul numero di righe.
[00:19:05 - 00:19:27] Perché abbiamo detto ogni volta che cambio un valore della colonna F identifica una funzione diversa e quindi il numero di funzioni booleane su tre variabili sarà pari alle combinazioni possibili distinte che riesco a costruire su 8 righe, su 8 bit diciamo.
[00:19:28 - 00:19:43] E quindi anche in questo caso sarà 2 elevato al numero di manopole che ho a disposizione, quindi in questo caso sarà 2 elevato alla 8.
[00:19:44 - 00:20:03] Quindi su tre variabili di booleane esistono due alla 8 possibili funzioni booleane di nuovo, non è un numero infinito come nelle funzioni reali,
[00:20:03 - 00:20:19] è un numero finito che posso calcolare facendo appunto 2 elevato al numero di righe, ma il numero di righe noi sappiamo che è 2 alla N quindi sarebbe 2 elevato a 2 alla N.
[00:20:20 - 00:20:45] E quindi ricordatevi questo concetto fondamentale nelle funzioni booleane del mondo binario appunto o booleano, se vogliamo vedere in generale ancora, il numero di funzioni è finito, il numero di valori di ingresso, il numero di punti del dominio di una funzione è un numero finito,
[00:20:45 - 00:21:00] e quindi essendo finito, essendo finito semplicemente indicando in ogni punto del dominio qual è il valore assunto della funzione, possiamo definire in maniera chiara e completa la funzione.
[00:21:00 - 00:21:10] Ecco qui la formula di cui vi parlavo prima, 2 elevato a 2 alla N.
[00:21:10 - 00:21:39] Ad esempio, se noi abbiamo qui un'unica variabile di ingresso che qui è indicata con x1 o se preferite un bit di ingresso, le funzioni definibili su un'unico bit, su un'unica variabile booleana,
[00:21:41 - 00:21:56] quante sono, abbiamo detto che poiché abbiamo un'unico bit, i possibili valori di questo bit, diciamo di questa variabile di ingresso, sono 2 o 0 o 1.
[00:21:57 - 00:22:04] Quindi, vuol dire che la tabella di verità di una funzione booleana a una variabile di ingresso avrà solo due righe.
[00:22:05 - 00:22:23] Le possibili funzioni booleane a un bit di ingresso sono 2 elevato a numero di righe, quindi 4 quali sono semplicemente le possibili combinazioni su due righe.
[00:22:24 - 00:22:37] E sono queste che vedete qua riportate, cioè noi con x1 e la variabile di ingresso, poi come funzione possiamo avere la funzione che viene chiamata set 0, quella che assegna 0 a tutti gli ingressi.
[00:22:38 - 00:22:46] Oppure un'altra funzione a una variabile booleana, come adesso, diciamo, siamo definiti.
[00:22:46 - 00:23:08] Dicevo, un'altra funzione è la funzione che viene chiamata buffer, che è la funzione che semplicemente replica l'ingresso.
[00:23:09 - 00:23:21] Un'altra funzione è la funzione not che invece inverte l'ingresso, vedete, quando è 0 l'ingresso l'uscite è 1, quando è 1 l'ingresso l'uscite è 0.
[00:23:22 - 00:23:29] Ultima funzione che viene chiamata funzione set 1, quella che assegna 1, indipendentemente dall'ingresso.
[00:23:30 - 00:23:42] Ecco qua, con questa tabella o espresso, diciamo, ho definito tutte le funzioni booleane possibili a un ingresso.
[00:23:43 - 00:23:48] Cioè, sono rappresentate in maniera sintetica, ma queste sono quattro tabelle di verità.
[00:23:49 - 00:23:52] E ogni tabella definiscemera una particolare funzione booleana.
[00:23:54 - 00:24:03] Ovviamente questo discorso può essere esteso in generale, mi riporto gesso quelli più importanti, più importanti,
[00:24:03 - 00:24:15] da cui poi derivano le porte logiche, che spesso sono funzioni, le porte che vedremo sono basate o con ingresso o su due ingressi.
[00:24:16 - 00:24:31] In questa slide sono riportate le possibili funzioni che possiamo definire, non sono tutte, ma sono le funzioni
[00:24:31 - 00:24:34] che poi andremo a richiamare nelle porte logiche.
[00:24:36 - 00:24:39] Vediamo le sono, quindi, due ingressi, in questo caso.
[00:24:39 - 00:24:52] Due ingressi vuol dire quattro righe nella tabella di verità, e in effetti sono le possibili combinazioni di x1, x2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1.
[00:24:52 - 00:25:03] Ok? Poi dobbiamo andare a specificare in ogni una di queste righe, in ogni configurazione degli ingressi, quanto vale l'uscita.
[00:25:03 - 00:25:10] E ogni possibile specifica che andiamo a mettere in uscita ci definirà una particolare funzione.
[00:25:11 - 00:25:19] Quelle più importanti su cui torneremo, quando analizzeremo le porte logiche, sono la funzione end.
[00:25:19 - 00:25:23] La funzione end fa l'end logico tra gli ingressi.
[00:25:24 - 00:25:41] End logico vuol dire che il valore di uscita è vero e alto quando, soltanto quando entrambi gli ingressi sono alti.
[00:25:42 - 00:25:53] In tutti gli altri casi è 0, e in effetti vedete 0, 0, 0, 0, 0, 1, 0, 0, vale 1, solo quando entrambi sono 1.
[00:25:55 - 00:26:07] La funzione or, invece, vale 1, ogni qualvolta almeno un ingresso vale 1.
[00:26:08 - 00:26:15] E quindi, di conseguenza, varrà a 0, solo quando entrambi gli ingressi valgono 0.
[00:26:17 - 00:26:24] Queste funzioni poi sono facilmente estendibili, diciamo, al caso di più ingressi, perché questo vale in generale.
[00:26:24 - 00:26:33] La end è vera solo quando tutti gli ingressi sono veri, e la or è falsa quando tutti gli ingressi sono falsi.
[00:26:33 - 00:26:48] La funzione end, invece, è la funzione che inverte la end, come se fosse not end per ricordarvi il nome,
[00:26:48 - 00:26:55] e in effetti vedete la end ha i valori invertiti rispetto alla end.
[00:26:56 - 00:27:02] Quindi, dove la end vale 0, la end vale 1, dove la end vale 1, la end vale 0.
[00:27:03 - 00:27:09] In maniera simile abbiamo la nor, che inverte la or.
[00:27:10 - 00:27:15] Vedete, dove la or è 0, la nor vale 1, dove la or vale 1, la nor vale 0.
[00:27:16 - 00:27:25] Poi abbiamo la xor, dove questa x sta per esclusivo, or esclusivo.
[00:27:25 - 00:27:27] Qual è la differenza?
[00:27:27 - 00:27:38] Dovete soltanto ricordare che, mentre la or è alta quando almeno un ingresso è alto,
[00:27:38 - 00:27:50] l'axor è alta quando soltanto un ingresso è alto e non quando più di un ingresso è alto.
[00:27:50 - 00:27:56] Quindi cambia il valore che uno une ingresso l'axor vale 0.
[00:27:56 - 00:28:02] Vedete l'axor vale uno solo quando in maniera esclusiva un ingresso è alto,
[00:28:02 - 00:28:09] ma se più ingressi sono alti l'axor vale 0, mentre la or è alta.
[00:28:10 - 00:28:14] L'axor, invece, è semplicemente la negazione dell'axor,
[00:28:14 - 00:28:19] e in effetti quando l'axor è 0, l'axor è 1 e così via.
[00:28:21 - 00:28:26] Ripeto, le funzioni possibili sono due alla quarta, quindi 16.
[00:28:26 - 00:28:32] Qua sono riportate solo 6, perché sono quelle che andremo a richiamare nelle porte logiche.
[00:28:34 - 00:28:42] Appunto vediamo le porte logiche sono dispositivi elettronici, quindi circuiti,
[00:28:42 - 00:28:49] che vanno, vedete, a implementare una specifica funzione buleana,
[00:28:49 - 00:28:52] ad esempio quelle che abbiamo visto prima.
[00:28:52 - 00:28:58] La notte, che ricordate una funzione di una variabile di ingresso,
[00:28:58 - 00:29:04] la n della or, invece, sono funzioni di due variabili di ingresso, ok?
[00:29:05 - 00:29:12] Poi, come sono implementate il braccianato prima, le porte vedremo qualche esempio,
[00:29:12 - 00:29:17] ma giusto per curiosità, non ci torneremo ulteriormente.
[00:29:18 - 00:29:25] Allora, le porte logiche fondamentali vengono tipicamente indicate con dei simboli,
[00:29:25 - 00:29:33] più o meno standard, che, diciamo, identificano la tipologia di porta.
[00:29:33 - 00:29:39] Quindi, tipicamente, quando vedrete un circuito in cui sono rappresentate le porte logiche,
[00:29:39 - 00:29:45] dovrete imparare a riconoscirele in base al simbolografico.
[00:29:46 - 00:29:52] Simbolografico, che appunto sono i due triangoli per queste funzioni di una variabile.
[00:29:52 - 00:29:59] Ricordate il buffer, semplicemente ripete il valore che riceve l'ingresso, lo ripete in uscita.
[00:29:59 - 00:30:04] Se c'è il pallino, invece, pensate sempre che c'è un'inversione.
[00:30:04 - 00:30:09] Quindi, un buffer col pallino sarebbe una notte.
[00:30:09 - 00:30:16] Cioè, in uscita non troverete l'ingresso, ma lo troverete invertito.
[00:30:16 - 00:30:22] Ricordando l'informazione sul pallino, sarà facile, diciamo, più o meno identificare le porte.
[00:30:22 - 00:30:30] Allora, la end a questo simbolografico in cui vedete la parte sinistra è una linea retta
[00:30:30 - 00:30:33] e poi c'è questa parte curpa sulla destra.
[00:30:33 - 00:30:40] Vedete, c'è due ingressi con queste lineette in uscita, invece, ha un'unica lineetta, quindi, diciamo, un'unica uscita.
[00:30:40 - 00:30:45] Se una end ha un pallino, allora è una end.
[00:30:46 - 00:30:51] L'axor, invece, ha questa forma un po' a triangolo curvato, diciamo,
[00:30:51 - 00:30:56] vedete se è la parte sinistra che le parte destra sono incurvate.
[00:30:56 - 00:31:00] Però ha sempre la cartessica di avere due ingressi, un'uscita.
[00:31:00 - 00:31:03] Se c'è il pallino, è una nor.
[00:31:04 - 00:31:10] L'axor, vedete, rispetto alla orra, ha questa doppia curva sulla sinistra
[00:31:10 - 00:31:15] e ovviamente se c'è il pallino, è una x nor, cioè è negata.
[00:31:20 - 00:31:27] Allora, abbiamo visto varie porte che implementano varie funzioni,
[00:31:27 - 00:31:31] però le porte veramente fondamentali,
[00:31:31 - 00:31:38] fondamentali nel senso che sono, diciamo, quelle strettamente necessarie
[00:31:38 - 00:31:43] per rappresentare le varie funzioni guleane, sono soltanto tre.
[00:31:45 - 00:31:52] Si dice che, ad esempio, le porte NAND, o meglio, scusami,
[00:31:52 - 00:31:59] rispetto a quello che voglio dire, le funzioni fondamentali sono tre,
[00:31:59 - 00:32:01] le funzioni fondamentali.
[00:32:01 - 00:32:05] A livello di funzione sono la NND, la ORRA e la NOT.
[00:32:05 - 00:32:10] Perché pure quando abbiamo visto, diciamo, le varie funzioni,
[00:32:10 - 00:32:18] le possiamo scrivere come combinazione di queste funzioni guleane fondamentali.
[00:32:18 - 00:32:24] Quindi se io riesco a trovare delle porte logiche che mi implementano
[00:32:24 - 00:32:29] queste funzioni guleane fondamentali, cioè la NND, la ORRA e la NOT,
[00:32:29 - 00:32:34] allora posso realizzare anche tutte le altre funzioni.
[00:32:34 - 00:32:39] Quindi le funzioni guleane fondamentali sono tre, NND o ORRA e NOT.
[00:32:40 - 00:32:50] Una porta logica, o si dice completa, se io con questa porta logica riesco
[00:32:50 - 00:32:54] a implementare queste tre funzioni fondamentali, perché poi tutto il resto
[00:32:54 - 00:32:57] riesco a realizzarlo di conseguenza.
[00:32:57 - 00:33:04] E una porta logica fondamentale, cioè completa, è la porta NAND.
[00:33:05 - 00:33:09] C'è un refuso sulla slide.
[00:33:09 - 00:33:11] Certo.
[00:33:11 - 00:33:14] C'è scritto ORRA e invece è una NND.
[00:33:17 - 00:33:20] C'è scritto ORRA e invece è una NND.
[00:33:20 - 00:33:26] C'è sotto circuiti, cioè NOT AND e poi ORRA.
[00:33:26 - 00:33:28] Quella è una NND, se non erro.
[00:33:28 - 00:33:30] No, deve essere una ORRA.
[00:33:30 - 00:33:39] Infatti il concetto è che con le porte NAND io riesco a implementare
[00:33:39 - 00:33:44] una NOT, una NND e una ORRA usando solo una NND.
[00:33:44 - 00:33:48] Per questo si definitione completa la porta NAND.
[00:33:48 - 00:33:52] Perché vedi, gli unici simboli grafici che vedi sono porte NAND.
[00:33:52 - 00:33:54] Ti trovi?
[00:33:55 - 00:34:01] Se usando il porte NAND, il tuo dubbio è che in questa non ti sembra una ORRA.
[00:34:01 - 00:34:05] No, no è vero, è vero, perché c'è A negato, B negato.
[00:34:05 - 00:34:11] Poi fai una NND tra i due negati e poi neghi tutto quanto.
[00:34:12 - 00:34:17] Perfetto.
[00:34:17 - 00:34:24] Altro concetto fondamentale che non so se ci sono in questo slide,
[00:34:24 - 00:34:29] in qualche lezione futura, è che abbiamo detto che una funzione buleana
[00:34:29 - 00:34:36] si definitione in maniera completa ed esastiva tramite la sua tabella di verità.
[00:34:36 - 00:34:38] Ok.
[00:34:38 - 00:34:47] Questo concetto può essere utilizzato per confrontare funzioni buleane o circuiti digitali.
[00:34:47 - 00:34:54] Cosa voglio dire? Che se questa rappresentazione, tu mi è sembrato che lo facessi pensando
[00:34:54 - 00:35:00] ad demorgan, algeplicamente, volevi dimostrare che questa è una ORRA, no?
[00:35:00 - 00:35:04] E' fatto bene se hai pensato così.
[00:35:04 - 00:35:10] Altro modo, per farli in maniera più semplice, è dire prova a fare la tabella di verità di questo circuito.
[00:35:10 - 00:35:15] E vedi se esce lo stesso output di una ORRA.
[00:35:15 - 00:35:20] Se due circuiti hanno lo stesso output, diciamo, sono equivalenti.
[00:35:20 - 00:35:27] Quindi se questo circuito effettivamente mi dà che in uscita ho il valore basso
[00:35:27 - 00:35:34] solo quando ai bisogni bassi e alto in tutti gli altri casi allora è una ORRA.
[00:35:34 - 00:35:38] Quindi se non sbagliono, dovrebbe essere corretto che è una ORRA.
[00:35:38 - 00:35:46] Non è corretto. È una cosa, come ha detto, demorgan, che con le negazioni che negava tutto quanto
[00:35:46 - 00:35:50] con la fine, anche l'operatore.
[00:35:50 - 00:35:55] Sì, sì, quello tu puoi dimostrare, diciamo, l'equivalenza tra due circuiti o tra due funzioni
[00:35:55 - 00:35:59] o tra olgeplicamente, come hai provato a fare tu con demorgan, oppure semplicemente
[00:35:59 - 00:36:03] confrontando le tabelle di verità.
[00:36:03 - 00:36:10] Quindi, tornando a noi, se proprio perché io usando solo porte NAND riesco a implementare
[00:36:10 - 00:36:16] una NOT, una AND e una ORRA, non ho bisogno di indagar ulteriormente.
[00:36:16 - 00:36:21] Posso dire che le NAND sono complete perché tutte le altre funzioni sono combinazioni
[00:36:21 - 00:36:28] di AND o RAND NOT, se io implementato queste tre, posso fare tutto solo usando NAND,
[00:36:28 - 00:36:31] che è questo il concetto.
[00:36:31 - 00:36:38] E a parte le NAND, anche la porta NOR, gode di questa proprietà, e anche qua,
[00:36:38 - 00:36:45] vedi, solo usando porte NOR posso implementare una NOT, una AND e una ORRA,
[00:36:45 - 00:36:52] quindi riesco a ottenere la completezza e quindi posso implementare qualunque circuito
[00:36:52 - 00:36:56] logico usando solo NOR.
[00:37:01 - 00:37:08] Qui c'è un esempio di implementazione effettiva, poi, a livello di transistor, di una porta
[00:37:08 - 00:37:17] NOT, in cui vedete, questo è il simbolo del transistor, abbiamo che quando l'attenzione,
[00:37:17 - 00:37:26] diciamo, in ingresso, a VCC pensatelo come un'alimentazione fissa, a cui sono sottoposti
[00:37:26 - 00:37:33] i circuiti per mantenere, diciamo, i loro valori, è l'attenzione di alimentazione
[00:37:33 - 00:37:38] e poi abbiamo delle tensioni di ingresso e di uscita, VIN è l'ingresso e VOUT dove
[00:37:38 - 00:37:41] viene misurata l'uscita.
[00:37:41 - 00:37:46] Quando l'attenzione di ingresso, questo è come funziona il transistor, quando l'ingresso
[00:37:46 - 00:37:54] alla base, sopra un certo valore di soglia, il transistor si comporta come un circuito
[00:37:54 - 00:37:57] usso tra collettore e dimettitore.
[00:37:57 - 00:38:05] Quindi, quando l'attenzione in ingresso è bassa, invece, bassa vuol dire al di sotto
[00:38:05 - 00:38:11] della tensione di soglia del transistor, invece si comporta come un circuito aperto.
[00:38:11 - 00:38:13] Questo cosa vuol dire?
[00:38:13 - 00:38:21] Che quando in ingresso ho una tensione di alimentazione bassa, il circuito tra collettore
[00:38:21 - 00:38:29] e dimettitore è aperto e quindi in uscita io avrò una tensione diversa da zero,
[00:38:29 - 00:38:38] una tensione alta che, diciamo, è alimentata da VCC.
[00:38:38 - 00:38:44] Ok, avrò la caduta di tensione sulla resistenza, quello che è, però ho una tensione alta.
[00:38:44 - 00:38:51] Quando invece, quindi, il tensione di ingresso viva con i, bassa, tensione di uscita alta.
[00:38:51 - 00:38:57] Quando invece la tensione di ingresso è alta, quindi che supera la tensione di soglia,
[00:38:57 - 00:39:03] vuol dire che il transistor si inizia a comportare come un circuito chiuso,
[00:39:03 - 00:39:10] il circuito è chiuso e quindi è come se in uscita, quindi io vengo, viene posto a massa,
[00:39:10 - 00:39:15] perché il dimettitore è a massa, la tensione di uscita di out tende a zero.
[00:39:15 - 00:39:20] E quindi una tensione di ingresso alta è una tensione di uscita bassa
[00:39:20 - 00:39:25] e quindi effettivamente questo implementa una porta notte.
[00:39:25 - 00:39:37] Sempre ragionando su come funziona il transistor,
[00:39:37 - 00:39:42] vediamo questa è una possibile implementazione di una porta NAND.
[00:39:42 - 00:39:49] E, ovviamente, se io riesco a implementare una porta NAND per la completezza delle porte NAND,
[00:39:49 - 00:39:53] posso replicare questa implementazione ogni qual volta,
[00:39:53 - 00:39:57] cioè per implementare tutte le altre porte che mi servono.
[00:39:57 - 00:40:05] Vediamo, porta NAND è una porta a due ingressi, infatti qua ho due transistor in serie
[00:40:05 - 00:40:10] con le due tensioni di ingresso alla base del transistor,
[00:40:10 - 00:40:16] che nella figura sono indicate come V1 e V2, mentre nella tabella di verità sono indicate come X1 e X2,
[00:40:16 - 00:40:19] però, diciamo, ci capiamo.
[00:40:19 - 00:40:27] E, ovviamente, vediamo, quando X1 e X2 sono zero, quindi le due tensioni alla base del transistor sono basse,
[00:40:27 - 00:40:34] vuol dire che entrambi si comportano da circuito aperto e quindi in uscita un valore alto.
[00:40:34 - 00:40:41] Valore alto la NAND effettivamente è alta.
[00:40:41 - 00:40:48] Quando invece uno dei due X1 e X2 sono alti, ma l'altro è basso,
[00:40:48 - 00:40:52] cosa succede? Che uno si comporta da circuito chiuso,
[00:40:52 - 00:40:59] ma ci sarà sempre uno dei due, almeno uno dei due, che si comporta da circuito aperto.
[00:40:59 - 00:41:07] E, ovviamente, io per far abbassare la tensione di uscita ho bisogno che tutti si comportino da circuito chiuso,
[00:41:07 - 00:41:11] altrimenti non riesco a mandare di auto a massa.
[00:41:11 - 00:41:20] E quindi ci troviamo, spero che la NAND, cioè l'uscita di questo circuito, diciamo,
[00:41:20 - 00:41:25] sarà sempre alta, a meno che tutte le tensioni siano alte,
[00:41:25 - 00:41:34] solo in quel caso riesco a mandarla a zero e questo è proprio la tabella di verità, il comportamento di una NAND.
[00:41:35 - 00:41:40] Quindi una NAND, un molo per implementarla penso anche a più ingressi
[00:41:40 - 00:41:47] e quello di mettere i vari ingressi con dei transistor in serie tra di loro.
[00:41:51 - 00:41:55] Se invece voglio fare la NOR, vedete cambia un po' la configurazione,
[00:41:55 - 00:42:02] non ho più una serie di transistor, ma ho un parallelo, cioè ho del transistor in parallelo tra loro.
[00:42:03 - 00:42:08] E, ragionando sempre sul fatto di circuito chiuso, circuito aperto in base a V9V2,
[00:42:08 - 00:42:12] potete già immaginare che questo circuito, realizzato così,
[00:42:12 - 00:42:16] pensate anche se ci possono più ingressi, il comportamento dovrebbe essere simile.
[00:42:16 - 00:42:24] In cui abbiamo che il circuito è sempre o meglio, va sempre a zero,
[00:42:24 - 00:42:29] ogni qual volta c'è almeno una tensione alta in ingresso,
[00:42:29 - 00:42:41] perché in un parallelo di circuito abbiamo che, basta che un ramo del parallelo diventa circuito chiuso,
[00:42:41 - 00:42:48] tutto il parallelo viene visto come circuito chiuso e quindi va a zero via out.
[00:42:51 - 00:42:55] Cioè basta che si apre o meglio, che si crea una strada
[00:42:55 - 00:43:03] sul ramo del parallelo che porta a massa la via out, cioè la corrente si va di là e quindi la via out va a zero.
[00:43:04 - 00:43:11] L'unico modo per avere la tensione alta è che tutti i transistor si comportino da circuito aperto,
[00:43:11 - 00:43:20] quindi tutte le tensioni devono essere basse e in effetti questo è proprio il comportamento di una NOR,
[00:43:20 - 00:43:24] che è sempre bassa tra nel caso in cui ingressi valgono tutti i zero.
[00:43:25 - 00:43:30] E quindi ci dovremo trovare che questo circuito implementa una NOR.
[00:43:37 - 00:43:45] Ora, ragionare sull'equivalenza tra circuiti, sul fatto che io posso usare o portenand o portenor,
[00:43:46 - 00:43:53] può complicare da un punto di vista logico perché devo lavorare con l'enand e con l'enor
[00:43:53 - 00:44:01] quando poi posso lavorare con l'end e con l'or e diciamo si vanno poi a fare ragionamenti
[00:44:01 - 00:44:06] sulla complessità implementativa, cioè quanti transistor ci servono.
[00:44:07 - 00:44:16] Noi abbiamo visto in queste semplici implementazioni che le porte che si realizzano sono effettivamente,
[00:44:16 - 00:44:22] cioè che si realizzano così facilmente alla fine, abbiamo fatto dei transessori in seri o dei transessori in parallelo,
[00:44:22 - 00:44:32] ci realizzano delle NAND e delle NOR, quindi è la semplicità del circuito che ci porta a realizzare la NAND e la NOR.
[00:44:32 - 00:44:40] Perché se invece volessi realizzare, se non c'è l'esempio, se volessi realizzare una NAND e una OR,
[00:44:40 - 00:44:48] devo aggiungere un altro transistor, quindi per risparmiare effettivamente il numero di circuiti utilizzati
[00:44:48 - 00:44:56] per implementare le porte logiche, e tipicamente si preferisce prende andare a implementare la NAND e la NOR,
[00:44:56 - 00:45:04] perché tanto abbiamo visto che sono forte e complete, quindi da punto di vista di questa cosa è un circuitale,
[00:45:04 - 00:45:07] ma è più semplice da realizzare.
[00:45:12 - 00:45:21] Qualche considerazioni sui transistor, che è la tecnologia CMOS domina ancora nei calcolatori,
[00:45:22 - 00:45:31] però qua vado veloce, abbiamo parlato prima di rappresentazione algebrica, cosa sarebbe, potete immaginare ovviamente,
[00:45:31 - 00:45:38] cosa può essere, vediamo velocemente, allora la tabela di verità abbiamo detto specifica completamente la funzione,
[00:45:38 - 00:45:45] perché banalmente elenca tutti i punti del dominio e del codominio, diciamo, della funzione,
[00:45:46 - 00:45:55] ovviamente è facile ragionare con le tabele di verità finché si testa in pochi, con un piccolo numero di variabili ingressi,
[00:45:55 - 00:46:04] no, tipicamente noi ragioneremo sempre con funzioni 2, 3, 4 variabili, perché è facile costruire la tabela di verità,
[00:46:04 - 00:46:12] però potete immaginare che se dovete fare una funzione a 8 variabili ingresso, a 16 così via diventa complicato,
[00:46:12 - 00:46:19] e quindi, sì, in quel caso è meglio usare notazioni alternative, equivalenti, ma più sintetiche,
[00:46:19 - 00:46:27] ad esempio la notazione algebrica, in cui andiamo a indicare come facciamo la funzione reale,
[00:46:27 - 00:46:37] cioè la funzione andiamo a indicare come espressione delle variabili, quindi gli ingressi andiamo ad adizionare o a moltiplicare,
[00:46:37 - 00:46:45] ovviamente avremo una notazione signale a quella classica che siamo abituati,
[00:46:45 - 00:46:55] però dobbiamo sempre ricordare che quando stiamo parlando di adizione o moltiplicazione in senso aritmetico, ma in senso buleano.
[00:46:58 - 00:47:06] Allora, come si rappresentano? Allora, l'end buleana, tra due variabili, lo andremo a rappresentare come moltiplicazione,
[00:47:07 - 00:47:15] la orro come somma, e la notta la possiamo trovare rappresentata o come una lineetta sopra le variabili,
[00:47:15 - 00:47:22] o come un trattino, diciamo, che precede la prefissa, diciamo, che precede la variabile.
[00:47:24 - 00:47:33] Ovviamente tutto ciò funziona finché noi possiamo dire che, diciamo, una funzione buleana, diciamo,
[00:47:33 - 00:47:46] è rappresentabile sempre da un'espressione algebrica e ogni funzione buleana, vedremo, può essere descritta come orro,
[00:47:46 - 00:47:54] quindi come somma delle combinazioni in cui la funzione è vera.
[00:47:54 - 00:48:04] Cosa vuole dire questo? Guardiamo un attimo alla tabella di verità riportata nella figura, che riguarda le due funzioni end-end.
[00:48:04 - 00:48:14] Allora, un modo semplice, immediato, che vale sempre per trovare l'espressione algebrica di una funzione buleana,
[00:48:14 - 00:48:25] è quella di, vedete, andare a scrivere la funzione come sommatoria delle combinazioni in cui,
[00:48:25 - 00:48:30] delle combinazioni degli ingressi in cui la funzione assume valore alto.
[00:48:30 - 00:48:40] Quindi nel caso della end, che ha valore alto solo in una riga, avremo soltanto una combinazione degli ingressi.
[00:48:40 - 00:48:54] Quali ingressi sono x2? Come si prendono questi ingressi? Gli ingressi vanno presi direttamente quando valgono 1,
[00:48:54 - 00:49:04] e nel caso della end, vedete, valgono 1, ovviamente, x1 vale 1, x2 vale 1, vi vado a scrivere così come sono x1 per x2.
[00:49:05 - 00:49:11] E ho finito, perché la end non ha altre righe in cui vale 1, e ovviamente questo è un caso banale,
[00:49:11 - 00:49:16] perché per definizione abbiamo detto che la end si scrive come prodotto degli ingressi.
[00:49:16 - 00:49:23] Se osserviamo la end, invece, possiamo vedere le varie situazioni che possono capitare,
[00:49:24 - 00:49:32] perché l'espressione algebrica della end abbiamo detto come qualunque funzione si calcola,
[00:49:32 - 00:49:37] si scrive o meglio come sommatoria delle combinazioni in cui vale 1,
[00:49:37 - 00:49:45] ovviamente nella end, vedete, ha tre righe in cui vale 1, quindi dobbiamo fare la somma di tre valori.
[00:49:45 - 00:49:51] Questi valori si chiamano min termini, come si calcolano, come si scrivono,
[00:49:51 - 00:49:58] abbiamo detto si scrivono prendendo tutte le variabili di ingresso moltiplicate tra loro
[00:49:58 - 00:50:08] e prese in forma negata se l'ingresso corrispondente vale 0, in forma diretta se l'ingresso corrispondente vale 1.
[00:50:08 - 00:50:15] Questo è semplicemente una tecnica per scrivere rapidamente la forma algebrica di una funzione.
[00:50:16 - 00:50:20] Quindi, volendolo fare per la end, partiamo dalla prima riga.
[00:50:20 - 00:50:27] Prima riga vale 1, quindi la devo prendere, la devo considerare nella forma algebrica.
[00:50:27 - 00:50:38] Il min termine della prima riga è dato dal prodotto di x1 preso negato perché x1 vale 0 in questa prima riga,
[00:50:38 - 00:50:44] per x2 preso anche x1 negato perché vale 0 anche x2,
[00:50:44 - 00:50:50] e in effetti vedete nella forma algebrica ho scritto x1 negato per x2 negato.
[00:50:50 - 00:50:54] Questo è il primo min termine della funzione.
[00:50:55 - 00:51:06] Più, ci sono altri min termini, sì, il secondo min termine, scusate, è quello associato alla seconda riga
[00:51:06 - 00:51:12] ed è dato dalla combinazione degli ingressi prendendo x1,
[00:51:12 - 00:51:19] no, qua sono invertiti perché x1, lo devo prendere negato, è stato dopo,
[00:51:20 - 00:51:29] allora il secondo min termine scritto a sinistra sarebbe la terza riga, x1 preso direttamente x2 negato,
[00:51:29 - 00:51:35] più x1 negato, che è la seconda riga, per x2.
[00:51:35 - 00:51:41] Quindi, qua, volendo giustare la slide, andremo a lo scritti in maniera invertita,
[00:51:41 - 00:51:44] però ovviamente essendo una somma non cambia niente.
[00:51:44 - 00:51:53] E' importante che dovete capire che in termini sono prodotti delle variabili di ingresso,
[00:51:53 - 00:52:02] dove le singole variabili le vado a prendere in maniera negata o diretta in base al valore in cui si presenta, diciamo,
[00:52:02 - 00:52:05] dentro la tabella di verità.
[00:52:06 - 00:52:17] In generale possiamo scrivere sempre che una funzione generica tn variabili i è pari,
[00:52:17 - 00:52:21] vedete, questo è semplicemente una generalizzazione, vedete, nella NAND,
[00:52:21 - 00:52:27] vi ho scritto che la sommatoria dei min termini ovviamente questo vale per la NAND su due variabili,
[00:52:27 - 00:52:33] ma in generale con una funzione buleana posso scrivere che la sua forma algedica
[00:52:33 - 00:52:40] può essere trovata facendo la sommatoria su m, dove m è il numero delle righe,
[00:52:40 - 00:52:55] dei prodotti, i prodotti, se io ho n ingressi, questo sarà una produttoria su n delle variabili di ingresso x.
[00:52:55 - 00:53:00] Ok, quindi questo è scritto in maniera più generale possibile,
[00:53:00 - 00:53:14] dove questo x star abbiamo detto che si chiama min termine, si calcola andando a mettere insieme tutte le variabili di ingresso
[00:53:15 - 00:53:29] o direttamente o negate, quindi il singolo x star, diciamo, sarà scelto nell'insieme x iesimo g esimo diretto
[00:53:29 - 00:53:36] oppure x iesimo g esimo negato, in base a quale riga sto considerando, stiamo considerando.
[00:53:37 - 00:53:47] Questo modo di scrivere una funzione come somma dei min termini si chiama forma canonica,
[00:53:47 - 00:53:56] ne esistono due di forma canonica, questa forma canonica si chiama somma di prodotti,
[00:53:57 - 00:54:05] forma sop, sarebbe sum of product, somma di prodotti in inglese semplicemente,
[00:54:05 - 00:54:11] e permette appunto di scrivere facilmente, vedete questa altra funzione, questa funzione m,
[00:54:11 - 00:54:20] funzione boleana di tre ingressi, scritta in forma algebrica o meglio scritta nella sua forma canonica
[00:54:20 - 00:54:27] come somma dei min termini, si vanno a considerare le righe pare a uno, qua sono quattro uno,
[00:54:27 - 00:54:35] quindi quattro righe, il primo uno, cioè quello della quarta riga, sarà a negato bc, il secondo uno
[00:54:35 - 00:54:45] sarà a b negato c, poi viene a bc negato e poi a bc. Sommando questi min termini, io ottengo
[00:54:45 - 00:54:55] una forma algebrica che è la forma canonica della funzione, e ovviamente questo funziona
[00:54:55 - 00:55:01] perché perché soltando le somme, io devo descrivere come vale la funzione, sto dicendo
[00:55:01 - 00:55:12] la funzione vale uno, mi basta fare la or o meglio la somma delle configurazioni in cui vale uno,
[00:55:12 - 00:55:23] in tutti gli altri casi parla a zero. Poi qui è riportato un esempio di nuovo immediato,
[00:55:23 - 00:55:31] quello più semplice per, più semplice ma non più efficace ovviamente, quello che poi effettivamente
[00:55:31 - 00:55:38] si va a utilizzare, perché poi diciamo, senza considerare quante porte stiamo utilizzando,
[00:55:38 - 00:55:45] non le paghiamo, le mettiamo tutte così come vengono e diciamo un modo molto semplice
[00:55:45 - 00:55:55] è quello di implementare un circuito seguendo la sua forma canonica e quindi devo fare questa m
[00:55:55 - 00:56:03] è la somma di quattro min termini e quindi metto in uscita una bella ora quattro ingressi che vado
[00:56:03 - 00:56:10] da alimentare con quattro end dove le quattro end mi vanno a calcolare i min termini.
[00:56:10 - 00:56:16] I quattro end, cioè questi min termini sono fatti da tre elementi quindi saranno quattro
[00:56:16 - 00:56:25] end da tre ingressi e i tre ingressi li vado a collegare ad abici oppure ad abici legato
[00:56:25 - 00:56:31] in base a quello che mi serve. Quindi devo fare il primo min termine è a negato bc e in effetti
[00:56:31 - 00:56:38] vedete il filo, il primo filo è collegato ad a negato, il secondo a b e il terzo a c e così via
[00:56:38 - 00:56:46] le altre. Quindi qua senza preoccuparmi di come ottimizzare diciamo l'implementazione,
[00:56:46 - 00:56:52] un modo molto semplice per disegnare l'implementazione di un circuito è quello di collegare i vari
[00:56:52 - 00:57:00] ingressi a delle porte notte che mi vanno a generare ingressi negati quindi ho tre ingressi
[00:57:00 - 00:57:08] da cui genero sei fili a bc presi diretti a negato bc negato presi in maniera negata.
[00:57:08 - 00:57:16] Questi sei fili poi vado a utilizzati per alimentare quattro porte end da tre ingressi
[00:57:16 - 00:57:32] le cui uscite vado a mandare nella or finale ok dovrei aver finito ci sono dubbi domande
[00:57:32 - 00:57:45] tutto chiaro? Tutto chiaro si prof. Ok allora prima che scatta la chiusura
[00:57:45 - 00:57:52] vi saluto e ci vediamo la prossima lezione. Grazie buongiorno. Grazie.
