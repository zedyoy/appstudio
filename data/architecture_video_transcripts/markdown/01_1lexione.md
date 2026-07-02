# 1lexione

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\1lexione.mp4`
- Durata: 00:53:19
- Trascrizione: `01_1lexione.json`

## Argomenti probabili
- porte_logiche (352): and, or, not, nor, nand, sop
- conversioni (29): binario, conversione, base, virgola
- memoria_bus (16): memoria, bus, ram
- mips_assembly (14): registro, sb, addi
- registri_flip_flop (5): flip flop, registro

## Trascrizione

[00:00:00 - 00:00:19] Allora, oggi cominciamo a vedere qualche concetto relativo alla codifica binaria, vedremo
[00:00:19 - 00:00:28] il colgice binario, le metriche fondamentali che abbiamo utilizzate quando si ha a che
[00:00:28 - 00:00:34] fare col colgice binario e vedremo il concetto di numeri a precisione finita.
[00:00:34 - 00:00:46] Allora, come già sapete immagino, le codiche binarie, in generale nei calcolatori digitali
[00:00:46 - 00:00:52] basati sul colgice binario, l'unità base delle informazioni, cioè l'unità base con
[00:00:52 - 00:00:56] cui vengono presentate le informazioni, è il bit.
[00:00:57 - 00:01:04] E come suggerisceomo la parola binario può assumere solo due valori possibili, in
[00:01:04 - 00:01:07] particolare il valore zero e il valore uno.
[00:01:07 - 00:01:19] Il bit rappresenta la più semplice unità informativa che è possibile codificare in binario e è fondamentale
[00:01:19 - 00:01:28] ovviamente per costruire circuiti e sistemi in grado di memorizzare i dati e poi per realizzare
[00:01:28 - 00:01:29] i calcolatori.
[00:01:29 - 00:01:40] Tipicamente, quando si parla di calcolatori digitali, si sottentende in genere che si parla
[00:01:40 - 00:01:50] di bit della codifica binaria, però in generale digitale vuol dire soltanto che la codifica è basata
[00:01:50 - 00:01:57] su valori discreti, però facciamo questa assunzione che quando parliamo di digitale intendiamo su
[00:01:57 - 00:01:58] il bit.
[00:01:58 - 00:02:05] Cioè su un numero di cifre finite, però due ovviamente nel nostro caso.
[00:02:05 - 00:02:14] Allora, una prima cosa da analizzare è perché mai diciamo i calcolatori di elettronici si basano
[00:02:14 - 00:02:16] su questa codifica, sulla codifica binaria.
[00:02:16 - 00:02:43] Scusate, perché se si usa la codifica binaria, risulta semplificata la codifica stessa,
[00:02:43 - 00:02:47] la formalizzazione delle informazioni in binario.
[00:02:47 - 00:02:57] Questo perché la codifica risulta più facile, diciamo, creare lo specifico relativamente
[00:02:57 - 00:03:06] ai dispositivi di memoria, ai circuiti di memoria, risulta più facile realizzare dispositivi
[00:03:06 - 00:03:10] in grado di memorizzare l'informazione caratterizzata soltanto dal bit.
[00:03:10 - 00:03:20] Qui, nell'esempio, è schematizzato un classico, diciamo, flip flop che è l'unità di memorizzazione
[00:03:20 - 00:03:23] minimale per memorizzare appunto un bit.
[00:03:23 - 00:03:30] Qual è la difficoltà principale che bisogna affrontare quando si deve creare un dispositivo
[00:03:30 - 00:03:39] di memorizzazione, è quella di memorizzare i dati in modo che siano poi facilmente distinguibili,
[00:03:39 - 00:03:49] cioè quando si va a progettare e a realizzare il dispositivo che in genere si basa su entità
[00:03:49 - 00:04:00] fisica, tipo la corrente o la tensione, su stati fisici, creare un dispositivo che deve
[00:04:00 - 00:04:06] memorizzare un'informazione, vuol dire che il dispositivo che si va a realizzare deve
[00:04:06 - 00:04:13] essere in grado non solo di mantenere informazione, ma deve anche mantenere corrente in modo
[00:04:13 - 00:04:22] che eventuali errori che possono verificarsi soprattutto in tendezze di questo tipo, tipo
[00:04:22 - 00:04:33] uno sbalzo di tensione, che poi in qualche modo alterare momentaneamente i valori elettronici
[00:04:33 - 00:04:40] su un circuito, ovviamente si auspica che questi sbalzi non vadano poi a inficiare l'informazione
[00:04:40 - 00:04:49] memorizzata, ci sia quindi una sorta di tolleranza, entro cui gli errori siano tollerati e si
[00:04:49 - 00:04:59] vede che se l'informazione è binaria è più facile creare una tolleranza o meglio
[00:04:59 - 00:05:06] che sia una tolleranza maggiore, si può avere una tolleranza maggiore a questo tipo di errori,
[00:05:06 - 00:05:13] proprio perché gli stati possibili che bisogna realizzare e mantenere sono minimi, sono soltanto
[00:05:13 - 00:05:25] due. Questo da un punto di vista fisico di realizzazione, poi da un punto di vista più
[00:05:25 - 00:05:35] di alto livello, il fatto che risulta spesso facile o comunque immediato andare a immaginare
[00:05:35 - 00:05:44] le informazioni come binaria, tante informazioni si sposano facilmente a una modellazione
[00:05:44 - 00:05:52] binaria. Il fatto che dico prima della tensione elettrica in un circuito è facile pensare
[00:05:52 - 00:05:59] a un'informazione di presenza e assenza di tensione, alla polarità ad esempio negativa
[00:05:59 - 00:06:08] o positiva di un magnete, un intuitore che può essere acceso o spento. Dovendo appresentare
[00:06:08 - 00:06:16] solo due stati, questi due stati dal punto di vista fisico quando deve realizzare un circuito
[00:06:16 - 00:06:23] viene facile immaginare delle possibili soluzioni per realizzare questi due stati. Avere invece
[00:06:23 - 00:06:30] una codifica non binaria ma a più cifre necessiterebbe ovviamente più stati, dispositivi
[00:06:30 - 00:06:37] quindi elettronici in grado di rappresentare e mantenere più stati fisici a cui associare
[00:06:37 - 00:06:46] le informazioni che si vogliono rappresentare. Per capire meglio questo concetto immaginiamo
[00:06:46 - 00:06:53] che la soluzione fisica che voglio utilizzare per realizzare questo mio dispositivo di
[00:06:53 - 00:07:06] memoria è la tensione. Qui ho un circuito su cui applico una tensione e immaginiamo che
[00:07:06 - 00:07:15] nel mio circuito io sono in grado di gestire tensioni che vagliano da 0 e 5 volt. Ora questo
[00:07:15 - 00:07:23] è un limite fisico che io in questo momento sto fissando. La capacità del dispositivo,
[00:07:23 - 00:07:30] il range di tensioni che può gestire il dispositivo è fissato quindi è un intervallo che dipende
[00:07:30 - 00:07:34] alla particolare soluzione che sto usando per realizzare il circuito ma è comunque un
[00:07:34 - 00:07:43] input. Io ho a disposizione un range di tensioni che vada da 0 a 5 volt. Ora cosa ci posso
[00:07:43 - 00:07:49] fare o meglio? Cosa potrei fare con un circuito di questo tipo? Mi potrei inventare diversi
[00:07:49 - 00:07:56] modi per rappresentare le informazioni. Io sempre questo range di tensioni ho a disposizione
[00:07:56 - 00:08:06] e ovviamente se ho la necessità di rappresentare più valori cosa succede? Che io devo suddividere
[00:08:06 - 00:08:13] le tensioni per questi valori. Cosa voglio dire? Se io ho nella parte sinistra di questa
[00:08:13 - 00:08:25] immagine, vedete, devo rappresentare 5 valori, 5 stati possibili, quindi 0, 1, 2, 3, 4. Una
[00:08:25 - 00:08:33] soluzione è quella di dire che io ho il mio range di tensioni lo suddivido in 5 intervalli e quando
[00:08:33 - 00:08:42] una tensione ricade in uno di questi 5 intervalli io definisco diciamo il valore informativo associato
[00:08:42 - 00:08:50] al circuito. Se lo stesso circuito invece lo devo usare per rappresentare solo due
[00:08:50 - 00:08:57] informazioni come avvene nel caso B, la parte di destra, vedete, ovviamente io devo rappresentare
[00:08:57 - 00:09:05] solo due valori, 0, 1, posso suddividere il range possibile del 0 a 5 in due intervalli
[00:09:05 - 00:09:13] e associare ogni intervallo a un valore di informazione. Cosa cambia? Nei due casi. Nel
[00:09:13 - 00:09:20] primo caso ovviamente, cioè in entrambi casi cosa cambia, cambia la dimensione dell'intervallo che
[00:09:20 - 00:09:28] associo al singolo valore informativo. Questo impatta significativamente direttamente sulla
[00:09:28 - 00:09:40] tolleranza associata al valore informativo perché nel caso in cui io, se si dovesse verificare
[00:09:40 - 00:09:49] ad esempio uno sbalzo di tensione di 0,5V o comunque di una certa attenzione, cosa può
[00:09:49 - 00:09:56] succedere? Che se nel secondo caso vedete che l'intervallo di tensione è da 0,2V quindi io
[00:09:56 - 00:10:07] ho un range di 2,5V, posso immaginare, posso sperare che uno sbalzo che va da 0,5V fino a 1,25V
[00:10:08 - 00:10:13] mi fa rimanere nello stesso intervallo perché è quella la cosa significativa che può
[00:10:13 - 00:10:20] succedere. Se uno sbalzo di tensione che mi fa alterare la tensione effettiva ai capi del circuito
[00:10:20 - 00:10:27] rientra comunque nell'intervallo associato all'informazione, allora io riesco ad assorbire
[00:10:27 - 00:10:36] l'errore. Il circuito, credo, se memorizzava o se voleva memorizzare l'informazione 0, continua
[00:10:36 - 00:10:43] a memorizzare l'informazione 0, questo vale anche se invece era l'informazione 1, no? Nell'altro
[00:10:43 - 00:10:52] caso invece nella figura di sinistra dove c'è indicato con A vedete, gli intervalli sono più
[00:10:52 - 00:11:00] piccoli quindi come dire è più grande la probabilità, il rischio che un eventuale spostamento della
[00:11:00 - 00:11:10] tensione dovuta a uno sbalzo giammo della tensione mi faccia ricadere il valore che io volevo
[00:11:10 - 00:11:17] memorizzare in un intervallo diverso. Cosa vuol dire che nel momento in cui il sistema va a
[00:11:17 - 00:11:25] misurare che tensione c'è ai capi del circuito si trova una tensione diversa, non fa niente se
[00:11:25 - 00:11:30] è diversa ma diventa un problema se la tensione misurata non solo è diversa ma ricade nell'intervallo
[00:11:30 - 00:11:38] diverso quindi io che ne so ho memorizzato o volevo memorizzare l'informazione 0, un problema
[00:11:38 - 00:11:45] circuitale mi fa vedere una tensione che invece è 1,5 volte, 1,5 volte associato all'informazione 1
[00:11:45 - 00:11:52] e quindi in quel momento io mi trovo un'informazione errata rispetto a quella che doveva esserci.
[00:11:52 - 00:12:00] Da qui spero si possa capire perché il fatto di avere minori stati da rappresentare quindi
[00:12:00 - 00:12:10] una codifica binaria aumenta la la tolleranza diciamo e guasti perché perché posso usare
[00:12:10 - 00:12:18] meglio al meglio diciamo il rege di tensioni disponibili quindi minori sono gli stati
[00:12:18 - 00:12:26] informativi da rappresentare con la grandezza fisica maggiore sarà la tolleranza con cui io
[00:12:26 - 00:12:34] riesco a rappresentarlo o meglio la robustezza scusate con cui riesco a rappresentar proprio
[00:12:34 - 00:12:43] perché meno stati mi permette di usare diciamo in maniera più eh più larga possibile i valori
[00:12:43 - 00:12:50] possibili più stati invece perché i valori possibili sono sempre quelli se io aumento gli
[00:12:50 - 00:12:55] stati informativi che voglio rappresentare quindi se invece di una codifica binaria
[00:12:55 - 00:13:03] una codifica a otto cifre o a più cifre mi si fanno sempre i piccoli intervalli
[00:13:03 - 00:13:11] della tensione in questo caso e quindi ovviamente più sono piccoli gli intervalli più appena si
[00:13:11 - 00:13:16] muove la tensione eh salto da un intervallo a un altro e quindi si creano eh problemi
[00:13:16 - 00:13:29] quindi da punto di vista diciamo eh dei dei numero di valori necessari per rappresentare le
[00:13:29 - 00:13:37] informazioni il sistema binario è più efficiente proprio perché si basa su una
[00:13:37 - 00:13:45] minore separazione necessaria tra i valori eh adiacenti questo aumenta la fidabilità del
[00:13:45 - 00:13:50] circuito la fidabilità della memorizzazione eh delle informazioni tramite il circuito
[00:13:50 - 00:14:01] elettronico quale il il limite ovviamente si fa sempre a perdere qualcosa no quando si fa
[00:14:01 - 00:14:10] una una scelta ecco ovviamente avere solo due cifre cioè solo due valori possibili per
[00:14:11 - 00:14:18] l'informazione minimale mi aumenta la fidabilità diciamo del del circuito la realizzazione del
[00:14:18 - 00:14:29] circuito mi semplifica la realizzazione del circuito però poi quando vado a rappresentare
[00:14:29 - 00:14:36] le informazioni tipicamente eh diciamo le stringe intese come numero di di picc necessari
[00:14:36 - 00:14:41] per rappresentare la stessa informazione ovviamente cresce molto di più immaginate
[00:14:41 - 00:14:49] eh un numero che in decimale si coscrive manualmente con una cifra se io lo vado a rappresentare
[00:14:49 - 00:14:55] invece in binario mi servono eh possibile quindi eh aumentano le stringe di bit necessari
[00:14:55 - 00:15:01] per rappresentare la stessa informazione però dal punto di vista fisico mi conviene farlo diciamo
[00:15:01 - 00:15:10] binario allora il codice binario quando in genere quando si parla di codifica si può
[00:15:10 - 00:15:17] identificare se lo definire l'alfabeto l'alfabeto di una codifica non è altro che l'insieme
[00:15:17 - 00:15:24] dei simboli disponibili per la codifica quindi il caso della codifica binaria l'alfabeto è composto
[00:15:24 - 00:15:34] lo soltanto due eh insieme cioè due elementi scusatemi zero e uno e la cardinalità ovviamente
[00:15:34 - 00:15:44] è due si parla di stringa di bit anticipavo non è altro che la sequenza di eh simboli
[00:15:44 - 00:15:52] che viene eh usata diciamo per rappresentare un'informazione tipicamente le stringe di bit
[00:15:52 - 00:16:01] sono eh raggruppate per un valore tipico che è otto e ogni otto bit si chiamano spengono
[00:16:01 - 00:16:07] identificati in genere con un byte quindi ricordate questa equivalenza fondamentale un byte sono
[00:16:07 - 00:16:18] otto bit e viceversa beh otto bit sono un byte altra conseguenza della scelta di rappresentare
[00:16:18 - 00:16:25] le informazioni tramite il codice binario è il fatto che i calcolatori digitali basati
[00:16:25 - 00:16:34] sulla codifica binaria sono calcolatori che hanno una precisione finita e determinata questo
[00:16:34 - 00:16:39] dipende dal fatto che i numeri sono memorizzate con parole codice parole codice quindi con
[00:16:39 - 00:16:48] eh string di bit che hanno una lunghezza retissata analmente se in un registro di memoria lo facciamo
[00:16:48 - 00:16:55] viene realizzato diciamo con otto bit ovviamente io non posso rappresentare tutti i numeri
[00:16:55 - 00:17:02] possibili ma sceglierò una tecnica di codifica che mi permette di rappresentare alcune informazioni
[00:17:02 - 00:17:09] su otto bit questo vuol dire che quando poi andiamo a svolgere delle elaborazioni sui
[00:17:09 - 00:17:16] numeri o svelovi informazioni ci ho non toglie che il risultato dovrà sempre scontrarsi sul fatto
[00:17:16 - 00:17:25] che il numero di bit a disposizione non è infinito è finito e questo ovviamente andrà a impattare
[00:17:25 - 00:17:34] su sui risultati se siano o meno rappresentabili. Tecnicamente fissato il numero di bit a
[00:17:34 - 00:17:43] disposizione possiamo sempre calcolare il numero di eh informazioni rappresentabili quindi se sono
[00:17:44 - 00:17:52] un un bit banalmente un bit inteso come un registro in grado di memorizzare un bit su un bit
[00:17:52 - 00:17:58] ovviamente noi rappresentiamo possiamo rappresentare due valori possibili abbiamo detto o zero e uno
[00:17:58 - 00:18:06] zero e uno sono due paroli codice possibili la parola codice che a lunghezza uno zero è la
[00:18:06 - 00:18:16] lunghezza è la parola codice che a lunghezza uno e vale uno ok se invece ho due bit a disposizione
[00:18:16 - 00:18:25] di questo indicando con l se ho due bit ovviamente io tutte le possibili combinazioni non sono
[00:18:25 - 00:18:30] infinite ma sono limitate se ho due bit a disposizione faccio tutte le combinazioni in quell'ogni
[00:18:30 - 00:18:39] bit associo o zero o uno otterrò alla fine quattro possibili configurazioni che sono zero
[00:18:39 - 00:18:46] o zero zero uno uno zero uno uno quindi sono quattro possibili configurazioni dette anche
[00:18:46 - 00:18:52] quattro possibili parole codice dove ogni parola codice ha la lunghezza pare al numero di bit
[00:18:52 - 00:19:00] disponibile cioè due quindi nel caso di l ora due quindi un ad esempio registro composto due bit
[00:19:00 - 00:19:07] il numero di parole codice possibili sono quattro hanno tutte valore di meglio di lunghezza due in
[00:19:07 - 00:19:16] generale fissato l la lunghezza della stringa di bit ad esempio il numero di bit disponibili in
[00:19:16 - 00:19:23] registro di memoria il numero di valori rappresentabili è pari a due l che sono appunto
[00:19:23 - 00:19:31] le possibili combinazioni di bit su l bit a disposizione e sono le configurazioni di bit
[00:19:31 - 00:19:42] possibili dette anche le parole codice qui sono riportate le configurazioni che vi accennavo
[00:19:42 - 00:19:52] prima quindi nel caso di due bit a disposizione quattro bit a disposizione o tre bit a disposizione
[00:19:52 - 00:20:02] le parole codice possibili costruibili in un sistema a un bit a due o tre bit vedi che sono note e
[00:20:02 - 00:20:12] fissate e sono limitate ovviamente quindi due bit scusate me un bit due alla uno fa due e le
[00:20:12 - 00:20:20] parole sono 0 1 due bit due alla seconda fa quattro le parole codice sono 00001101 si ha
[00:20:20 - 00:20:29] tre bit a disposizione due alla terza fa otto e queste sono le combinazioni ovviamente l ordine
[00:20:29 - 00:20:35] nello scritte io in questo ordine quello che è importante è capire che le parole codice
[00:20:35 - 00:20:42] possibili si ottengono alternando vedete da la combinazione dei possibili valori quindi
[00:20:42 - 00:20:50] o sono tutti 0 o sono tutti 0 tra ne uno che vale 1 uno al centro uno a sinistro scrivete
[00:20:50 - 00:20:57] tutte le possibili e ottenete quante ne sono ricordatevi però che quante ne sono in tutto
[00:20:57 - 00:21:09] lo sapete ed è definito da due elevato al numero di bit questo è il caso di quattro bit due alla
[00:21:09 - 00:21:21] quarta fa sedici e qua sono elencate se invece vogliamo ragionare al contrario cioè invece
[00:21:21 - 00:21:28] di fissare il numero di bit a disposizione conosciamo quante informazioni vorremmo codificare
[00:21:28 - 00:21:39] abbiamo un insieme di valori in generale delle informazioni v1 v2 vm che sono dei valori che
[00:21:39 - 00:21:48] io voglio codificare in binario quindi se vi chiedo dati m possibili valori da codificare
[00:21:48 - 00:21:58] valori che diciamo caratterizzano un'informazione che vogliamo codificare quanti bit servono per
[00:21:58 - 00:22:07] codificare questi m valori in maniera diciamo un'ivoca ovviamente cerchiamo una codifica
[00:22:07 - 00:22:13] che permette di codificare l'informazione in binario e passare con l'operazione inversa
[00:22:13 - 00:22:26] dal binario all'informazione stessa bisogna utilizzare la formula inversa abbiamo detto prima
[00:22:26 - 00:22:35] che era il numero di parole codice era due alla l se invece ragiono al contrario possiamo dire
[00:22:35 - 00:22:50] che se m è il numero di valori che voglio codificare no logaritmo base 2 di m bit ovviamente questo
[00:22:50 - 00:22:57] minimo questo almeno che sto sottolineando vuol dire il fatto che ovviamente non è detto che il
[00:22:57 - 00:23:04] numero di bit sia perfettamente o meglio sia perfettamente utilizzato no se io devo rappresentare
[00:23:04 - 00:23:12] un'informazione caratterizzata da quattro valori ovviamente è facile dire logaritmo base 2 di
[00:23:12 - 00:23:19] 4 viene due mi servono due bit due alla due fa 4 e quindi utilizzo tutte le possibili parole
[00:23:19 - 00:23:25] codice però può anche succedere che il numero di valori che voglio codificare non sia un
[00:23:25 - 00:23:33] pultipolo di due ad esempio devo codificare cinque informazioni sei informazioni in questo caso
[00:23:33 - 00:23:44] logaritmo in base 2 mi fa avere il numero minimo nel senso che per rappresentare 5 valori 6 valori
[00:23:44 - 00:23:54] mi servono 3 bit per rappresentare in maniera onivoca 5 valori 6 valori ovviamente io su 3 bit
[00:23:55 - 00:24:02] abbiamo 8 possibili parole codice però se devo codificare solo 5 valori 6 valori
[00:24:02 - 00:24:08] vorrà dire che due parole codice possono non utilizzarle non mi servono però mi servono
[00:24:08 - 00:24:20] comunque i 3 bit per codificare l'informazione quando sia una stringa di bit quindi una
[00:24:20 - 00:24:28] sequenza di o meglio una parola codice composta da una sequenza di bit tipicamente si può
[00:24:28 - 00:24:41] identificare il bit più significativo e il bit meno significativo il bit meno significativo e il bit
[00:24:41 - 00:24:52] più a destra il bit più significativo invece quello più a sinistra se ragioniamo un attimo su
[00:24:52 - 00:25:04] come funziona il sistema numerico decimale sarà facile diciamo ricordare e capire questa questa
[00:25:04 - 00:25:13] definizione perché come avviene nel sistema decimale i numeri le cifre o meglio hanno ovviamente
[00:25:13 - 00:25:20] un valore diverso in base a come vengono posizionati se parla appunto di sistemi numerici posizionali
[00:25:20 - 00:25:33] in cui la cifra 3 ha valore dell'unità 3 se lo posizioniamo come prima cifra a destra
[00:25:34 - 00:25:39] mentre se la posizioniamo nella posizione del decine avrà valore 30 se la posizioniamo
[00:25:39 - 00:25:49] nella posizione delle centinaio avrà valore 300 e così via quindi il peso il valore di una cifra
[00:25:49 - 00:26:01] dipende è pesato in base alla posizione e come è suggerito nella nella figura vedete il peso così
[00:26:01 - 00:26:13] come nel sistema decimale è 10 alla 0 10 alla 1 12 così via crescere anche nel sistema nella
[00:26:13 - 00:26:20] codifica binaria diciamo il peso delle cifre cresce andando verso sinistra quindi la cifra
[00:26:20 - 00:26:27] diciamo più a sinistra della stringa sarà quello più significativo proprio perché ha peso maggiore
[00:26:27 - 00:26:34] quando si può calcolare diciamo il valore rappresentato dice versa quello meno significativo
[00:26:34 - 00:26:46] e il bit più a destra quello che ha peso 0 allora vediamo tipicamente quali sono le unità
[00:26:46 - 00:26:55] metriche che possiamo incontrare nella nella informazione rappresentate in binario allora ci
[00:26:55 - 00:27:03] sono le diciamo delle unità metriche che tipicamente richiamano in qualche modo quelle
[00:27:03 - 00:27:10] che già conosciamo nel sistema internazionale in cui vedete abbiamo
[00:27:10 - 00:27:23] i kilo mega giga terra esa mili micro nano pico atto e così via che richiamano allo
[00:27:23 - 00:27:36] stesso modo il sistema internazionale appunto delle potenze del 10 e quindi ad esempio un kilo
[00:27:36 - 00:27:46] sarà 10 alla terza un mega sarà 10 alla 6 e così via tipicamente le maiuscole indicano
[00:27:46 - 00:27:56] delle dei multipli mentre le minuscole sono i sottomultibili poi se a volte troviamo la
[00:27:56 - 00:28:09] b maiuscola si intende bite quindi kb vuol dire ad esempio un kb da per un kilo bite mentre se
[00:28:09 - 00:28:22] b minuscola un kilo b a un meglio uno kb minuscolo indica un kilo bit ad esempio quindi un
[00:28:22 - 00:28:30] alien di comunicazione a un m maiuscolo bps vuol dire che è un alien di comunicazione
[00:28:30 - 00:28:43] che trasmette a 10 alla 6a perché m sarebbe mega bps sta per bit per secondo e un altro
[00:28:43 - 00:28:52] esempio un clock a 100 ps vuol dire pico secondi quindi è un t con i 10 alla meno 10 secondi
[00:28:52 - 00:29:04] questo diciamo per le linea di quando si parla di linee di trasmissione quindi quanti bit si
[00:29:04 - 00:29:16] vengono spediti sulla rete il clock la frequenza e così via quando invece c'è a che fare con
[00:29:16 - 00:29:22] per esempio le memorie dei dischi la memoriera me così via quindi le memoritazioni dei dati
[00:29:22 - 00:29:33] cambia l'interpretazione che si dà alle sigle kb me b e così via questo perché perché
[00:29:33 - 00:29:44] tipicamente queste diciamo queste ditamente che vengono hanno sempre i simboli simili a quelli
[00:29:44 - 00:29:51] del sistema internazionale però i valori effettivi non rispecchiano effettivamente le
[00:29:51 - 00:30:00] potenze del 10 come abbiamo visto ma invece si va per analogia quindi se io ho una memoria a un
[00:30:00 - 00:30:11] mb si sta parlando di un megabyte però questi megabyte se li vado a convertire non sono un
[00:30:11 - 00:30:18] milione di bite come sarebbe il sistema internazionale o come abbiamo visto prima per le
[00:30:18 - 00:30:25] linee di trasmissione ma nel caso delle delle memorie si va per analogia quindi un mega dovrebbe
[00:30:25 - 00:30:33] essere un milione ma in realtà è due alla 20 e circa un milione quindi per questo viene
[00:30:33 - 00:30:41] chiamato viene indicato con mega però non è precisamente 10 alla 6 quindi ricordiamoci
[00:30:41 - 00:30:53] che nelle memorie le unità di metri che seguono le potenze di due con valori che diciamo si avvicinano
[00:30:53 - 00:30:58] ai valori del sistema internazionale ma sono invece vedete due alla 10 ma due alla 20 e
[00:30:58 - 00:31:05] prima due alla 30 e così via poi la conversione da bite a bit ovviamente semplicemente moltiplicare
[00:31:05 - 00:31:12] per otto il valore di bite oppure dividere per otto i valori di bit per arrivare ai bite
[00:31:12 - 00:31:21] ovviamente come potete immaginare da soli questa situazione crea delle ambiquità perché a volte
[00:31:21 - 00:31:27] può essere non chiaro se la conversione debba seguire quanto visto diciamo nell'ambito delle
[00:31:27 - 00:31:37] linee di comunicazione o quanto visto invece nell'ambito delle memorie superare questa ambiquità
[00:31:37 - 00:31:50] sono state proposte ulteriori unità metri che in cui si è deciso che nel momento in cui si
[00:31:50 - 00:32:01] parla di kilo bite megabyte gigabyte diciamo i valori che abbiamo visto finora si per analogia
[00:32:01 - 00:32:07] si va diciamo col sistema metrico si va con l'interpretazione classica quindi potenza del
[00:32:07 - 00:32:14] 10 per indicare invece le unità metri che basate sulla potenza del due si usa invece
[00:32:14 - 00:32:24] queste altre unità metri che il che bibite medibite gb bite e bibite così via quindi diciamo
[00:32:24 - 00:32:34] standardizzate esistono le unità metri che permettono di specificare a quale tipologia di
[00:32:34 - 00:32:42] interpretazione si vuole vedere se vuole intendere quindi se io scrivo kilo bite non deve essere
[00:32:42 - 00:32:51] ambiguo sono 10 alla terza però succede che nella realtà anche se diciamo queste nuove unità
[00:32:51 - 00:32:58] di metri che sono state definite standardizzate spesso diciamo non vengono utilizzate si continua a
[00:32:58 - 00:33:06] usare l'interpretazione pre pre standard diciamo in cui si usa questa interpretazione usando
[00:33:06 - 00:33:14] questi simboli e quindi diciamo mantenendo questa ambiguità per capire diciamo come deve essere
[00:33:14 - 00:33:22] interpretata la cosa dovete analizzare di cosa si sta parlando se se memorie o se linee di
[00:33:22 - 00:33:33] comunicazione quindi dice le cose che vi ho accennato prima allora torniamo un attimo sul
[00:33:33 - 00:33:41] concetto di numero a precisione finita questo abbiamo detto terrio dal fatto che in un
[00:33:41 - 00:33:48] colcolatore ovviamente la coditica binaria io non è che la posso studiare e analizzare
[00:33:48 - 00:33:56] la potenza teorico per nel senso che se mi serve un bit in più ce l'ho metto e vado avanti no in
[00:33:56 - 00:34:06] un colcolatore reale ovviamente il numero di bit è fissato e non è infinito e questo comporta che
[00:34:06 - 00:34:16] la ritmetica non segue sempre le le proprietà della ritmetica classica ma può diciamo alcune
[00:34:16 - 00:34:23] proprietà che vagano nella ritmetica classica possono non essere più valide la ritmetica a
[00:34:23 - 00:34:30] precisione finita proprio perché è influenzata dal fatto che le valori informazioni rappresentabili su
[00:34:30 - 00:34:38] il bit a disposizione nel momento in cui vado a elaborare l'informazione vado a fare dei calcoli
[00:34:38 - 00:34:45] delle espressioni può succedere che durante i calcoli o il risultato finale possa non essere più
[00:34:45 - 00:34:52] rappresentabile questo mi crea un problema quindi la ritmetica a precisione finita è una
[00:34:52 - 00:34:58] carteristia dei calcolatori ed è imposto dal bincolo che abbiamo sulla rappresentazione sul bit a
[00:34:58 - 00:35:08] disposizione per capire questo concetto lo consideriamo di avere un colcolatore ad esempio una
[00:35:08 - 00:35:18] calcolatrice che opera soltanto su tre cifre cifre decimali per semplificare senza virgola senza segno
[00:35:18 - 00:35:28] una semplicissima calcolatrice in cui possiamo scrivere numeri fino a tre cifre se io se abbiamo
[00:35:28 - 00:35:34] soltanto tre cifre a disposizione vuol dire che noi possiamo scrivere su questa calcolatrice il numero
[00:35:34 - 00:35:46] 0 1 2 così via fino a 999 questo diciamo il numero più grande che possiamo scrivere abbiamo
[00:35:46 - 00:35:54] tre o meglio mille valori possibili che riusciamo a codificare su queste tre cifre decimali e
[00:35:54 - 00:36:01] ovviamente non possiamo rappresentare i numeri più grandi di 299 non possiamo rappresentare i
[00:36:01 - 00:36:09] numeri negativi non possiamo rappresentare frazioni numeri reali con la virgola diciamo
[00:36:09 - 00:36:19] nei numeri irrazionali ok quindi stiamo imponendo dei vincoli che derivano dal fatto stesso che
[00:36:19 - 00:36:30] il calcolatore ha soltanto un numero fissato di cifre a disposizione quindi non solo non
[00:36:30 - 00:36:40] posso rappresentare questi valori limitati diciamo dal numero del bit ma poi può essere che quando
[00:36:40 - 00:36:48] vado a fare dei calcoli delle operazioni succede che io eccedo i limiti oppure ottengo un risultato
[00:36:48 - 00:36:55] che non è rappresentabile e quindi dobbiamo sempre tener presente il fatto che se due valori o più
[00:36:55 - 00:37:03] valori siano singolarmente rappresentabili nel nostro calcolatore non è detto che un'operazione
[00:37:03 - 00:37:10] soddiesi sia ancora rappresentabile e questa è una limitazione intrinserica dal fatto che la
[00:37:10 - 00:37:20] memoria è finita e limitata e questo infliccie poi sulla ritmetica reale sulla ritmetica del
[00:37:20 - 00:37:31] calcolatore la cosa più immediata è che le operazioni ritmetiche che normalmente sono chiuse
[00:37:31 - 00:37:42] non lo sono più nei numeri è precisione finita ad esempio nei numeri interi teorici diciamo
[00:37:42 - 00:37:50] risattiamo che l'insieme chiuso rispetto alla lezione la sottrazione la molti applicazione questo
[00:37:50 - 00:37:55] vuol dire insieme chiuso vuol dire che se io prendo due numeri interi e faccio la somma il
[00:37:55 - 00:38:02] risultato è un numero intero lo stesso vale per la sottrazione e per la molti applicazione già
[00:38:02 - 00:38:09] sulla divisione sappiamo che non è chiusa perché il risultato di una divisione può essere un numero
[00:38:09 - 00:38:17] che non è più intero. Nei numeri a precisione finita però non sono neanche chiuse rispetto
[00:38:17 - 00:38:24] a l'operazione fondamentale all'addizione alla sottrazione quindi teoricamente se io vado a
[00:38:24 - 00:38:33] codificare in binario i numeri interi non posso più basarmi sul fatto che se faccio la somma di
[00:38:33 - 00:38:42] due numeri interi il risultato sia un numero un numero intero nel sistema di codifica e diventa
[00:38:42 - 00:38:49] tutto vincolato rispetto al sistema di codifica che sto utilizzando se assolta dipende dal numero
[00:38:49 - 00:39:00] di bit a disposizione. Le errori dovuti alla non chiusura delle operazioni si chiamano
[00:39:00 - 00:39:06] di overflow e underflow, tipicamente quando io faccio la somma di due numeri in un calcolatore
[00:39:06 - 00:39:13] il risultato non è più rappresentabile perché se io ottengo un valore che teoricamente è più
[00:39:13 - 00:39:18] grande del massimo olore rappresentabile non lo posso rappresentare lo si parla di errore di
[00:39:18 - 00:39:24] overflow. Invece si parla di errore di underflow quando il risultato di un'operazione è troppo
[00:39:24 - 00:39:32] piccolo per essere rappresentato oppure se viene approssimato a un valore diverso. L'approssimazione
[00:39:32 - 00:39:42] più nella codifica dei valori reali se restiamo nell'amido dei sistemi dei numeri interi si
[00:39:42 - 00:39:47] parlano di soltanto troppo piccolo ad esempio ottengo un valore più piccolo del più piccolo
[00:39:47 - 00:39:54] numero rappresentabile e allora c'è un errore di underflow. Se fosse tipo tre a diviso due no?
[00:39:54 - 00:40:05] Tre a diviso due è semplicemente che l'auto è un valore che non è rappresentabile e quindi viene
[00:40:05 - 00:40:14] approssimato a quello più vicino. Guarda un esempio dopo. Overflow e underflow nell'ambito
[00:40:14 - 00:40:22] dei numeri interi si intende semplicemente se io ho un calculatore a tre cifre 600 è rappresentabile
[00:40:22 - 00:40:28] su tre cifre però se faccio 600 più 600 in teoria fa 1200 mi servirebbero quattro cifre ma io
[00:40:28 - 00:40:37] non ce l'ho questa cifra e quindi in overflow. L'overflow è quando supero l'esco fuori del
[00:40:37 - 00:40:46] intervallo fuori scala. L'overflow invece è sotto ok. La cosa che dicevi tu,
[00:40:46 - 00:40:54] 7 diviso 2, 3,5 non vado fuori semplicemente risultato diciamo non è un intero tipicamente
[00:40:54 - 00:41:02] viene approssimato. Non è rappresentabile. E ho lo rappresento con il numero intero più vicino.
[00:41:02 - 00:41:20] Questo avviene tipicamente. Non ho la vera per dire nell'ambito dei sistemi reali o meglio
[00:41:20 - 00:41:27] in questa calcolatrice il valore finale risultato sarebbe o tre o quattro perché non può rappresentare
[00:41:27 - 00:41:37] tre virgola qualcosa. Però in questo caso si traduce in un errore del calcolo che dipende dalla
[00:41:37 - 00:41:46] codifica utilizzata quindi avere tre bit in tutto implica soltanto che risultato delle operazioni
[00:41:46 - 00:41:55] hanno un errore fino a 0,5 perché so che se c'è un valore con la virgola viene approssimato all'intero
[00:41:55 - 00:42:04] più vicino quindi il massimo errore sarà 0,5. Sì però non viene segnalato errore tipicamente
[00:42:04 - 00:42:16] esce il risultato però è sbagliato risultato per chi viene approssimato invece quando proprio
[00:42:16 - 00:42:23] esci fuori sotto o sopra dall'intervallo di rappresentazione segnano l'overflow o di underflow.
[00:42:25 - 00:42:35] Ovviamente a parte la chiusura questo vale anche per le proprietà algibiche perché ovviamente
[00:42:35 - 00:42:44] la classica legge associativa o distributiva possono non più valere nel momento in cui
[00:42:44 - 00:42:52] andiamo a fare le operazioni perché in un sistema diciamo con una calcolatrice,
[00:42:52 - 00:43:00] diciamo che c'è un esempio migliore non c'è, immagina una, sembra una calcolatrice a 3 cife
[00:43:00 - 00:43:14] che tu devi fare 600 meno 400 più 600. Ovviamente noi sappiamo che nell'aritmetica generale
[00:43:14 - 00:43:20] l'ordine delle operazioni non cambia io posso fare prima la somma e poi dopo la sottrazione
[00:43:20 - 00:43:30] o viceversa invece in un'aritmetica a precisione finita l'ordine può alterare significativamente
[00:43:30 - 00:43:38] il risultato perché se io devo fare 600 meno 400 più 600 se faccio prima la sottrazione quindi
[00:43:38 - 00:43:46] faccio 600 meno 400 viene 200 più 600 800 800 lo posso rappresentare quindi il problema non si
[00:43:46 - 00:43:52] pone ma se ho inverto l'ordine e faccio prima 600 più 600 non arriverò mai a fare meno 200
[00:43:52 - 00:44:04] perché il risultato intermedio mi causa overflow e quindi diciamo come qua è riportato no a più
[00:44:04 - 00:44:11] b meno c è la stessa cosa di a più b meno c no con la proprietà associativa però questo in
[00:44:11 - 00:44:20] teoria ma nel sistema a precisione finita uno può casoare overflow e l'altro no e lo stesso vale per
[00:44:20 - 00:44:26] la distribuzione cioè per la legge distributiva in questo caso potevano essere ai b 600 valorizzate
[00:44:26 - 00:44:36] a 600 l'altro la c era 400 nel primo caso andava in overflow nel secondo caso l'esempio che ho fatto
[00:44:36 - 00:44:44] prima è invertito quindi il primo va in overflow il secondo no e quindi bisogna sempre generalmente
[00:44:44 - 00:44:51] a volte uno non ci pensa e vede solo il risultato finale cioè tipicamente in un caso reale capita
[00:44:51 - 00:44:57] a volte che si verificano gli errori perché durante le operazioni di un carcolo con complesso
[00:44:57 - 00:45:03] un'approssimazione come dire si può propagare così tanto da far confondere poi un numero e lo fa
[00:45:03 - 00:45:11] diventare zero o altro se un numero diventa zero non perché è veramente zero ma è stato semplicemente
[00:45:11 - 00:45:18] approssimato a zero poi ti trovi che ti esce una divisione per zero che ti manda in eccezione tutto
[00:45:18 - 00:45:25] il programma quando poi tu dicevi ma come teoricamente non esiste zero non dovevo uscire e quindi bisogna
[00:45:25 - 00:45:32] stare attenti a queste cose quindi pensare non saltando risultato finale ma anche risultati
[00:45:32 - 00:45:37] intermelli possono causare problemi possono causare underflow o overflow e così via
[00:45:46 - 00:45:51] e quindi va bene i calcolatori possono poter risultati errati semplicemente perché sono
[00:45:51 - 00:45:57] vincolati dal numero di cifre a disposizione dei numeri di bit a disposizione
[00:45:57 - 00:46:08] è possibile diciamo costruire hardware dedicato a rilevare eventuali errori di overflow però
[00:46:08 - 00:46:16] diciamo ci sono limitazioni intrinsiche della ritematica finita che caratterizzai i i calcolatori
[00:46:19 - 00:46:24] e con questo finito qua ci sono i riferimenti al libro sempre che sta
[00:46:24 - 00:46:27] sul sito online
[00:46:31 - 00:46:40] e nintra se ci sono domande dubbi professore io avrei una domanda se possibile non ho capito la
[00:46:40 - 00:46:49] parte iniziale quella con il circuito con i valori del voltaggio divisi con il massimo di
[00:46:49 - 00:46:57] 15 volte se può un attimo riassumare questa parte è quasi possibile certo qui l'idea che
[00:46:57 - 00:47:06] voglio far capire che diciamo un vantaggio del perché i calcolatori o più semplicemente un
[00:47:06 - 00:47:15] dispositivo elettronico di memorizzazione di informazioni diciamo è più affidabile se si
[00:47:15 - 00:47:23] basa su una codifica binaria piuttosto che su una codifica a 5 cifre o a più cifre perché perché
[00:47:23 - 00:47:30] se io devo rappresentare uso la codifica binaria la codifica mi nascendiamo banalmente al singolo
[00:47:30 - 00:47:36] bit la mia informazione un bit devo costruire un dispositivo di memoria in grado di memorizzare
[00:47:36 - 00:47:45] il valore di un bit ora è piuttosto dire bit un simbolo devo memorizzare no ora se questo
[00:47:45 - 00:47:53] simbolo può assumere soltanto due valori a disposizione io posso scegliere e posso scegliere
[00:47:53 - 00:48:00] come dire diverse tecnologie per fare tecnologie scusa mi intendo diversi grandi posso costruire
[00:48:00 - 00:48:06] un dispositivo che utilizza diverse grandezze fisiche per rappresentare l'informazione c'erano
[00:48:06 - 00:48:14] qua gli esempi non posso usare un circuito elettrico tolgo o metto tensione oppure con le
[00:48:14 - 00:48:23] soldi attenzione da 0 a 5 vale 1 o da 5 a 2 vale da 5 a 10 scusa mi vale un altro valore oppure
[00:48:23 - 00:48:29] posso usare un magnete che mi dà una polarità positiva per indicare un'informazione o negativa
[00:48:29 - 00:48:38] un'altra informazione c'è scelgo una grandezza fisica su cui costruire il mio dispositivo di
[00:48:38 - 00:48:44] memorizzazione e cerco di usare gli stati possibili della grandezza fisica per memorizzare
[00:48:45 - 00:48:51] nel caso di dispositivo basato sulla tensione io cosa ciò o sono in grado di costruire
[00:48:51 - 00:49:01] un dispositivo che mi mantiene una tensione tra 0 e 5 volt ok ora se io voglio rappresentare oggi
[00:49:01 - 00:49:10] piove oggi non piove posso fare che se mantengo il circuito tra 0 e 2,5 volt vuol dire che sto
[00:49:10 - 00:49:18] salvando l'informazione non piove se invece mantengo una tensione da 2,5 volt a 5 volt voglio
[00:49:18 - 00:49:24] rappresentare l'informazione piove quindi una suddivisione progettuale sto dicendo ho una
[00:49:24 - 00:49:31] grandezza fisica la sfrutto per rappresentare due valori possibili due stati possibili che
[00:49:31 - 00:49:40] banalizzando sarebbe tensione bassa tensione alta ok quindi soltanto due due valori precisi e
[00:49:40 - 00:49:49] distinti invece che vedo che si poteva dare dall'informazione più informazioni oltre a
[00:49:49 - 00:49:56] 0 e 1 tramite il livello delle tensioni no aspetta però non ho finito questa prima soluzione
[00:49:56 - 00:50:04] questa prima soluzione è l'utilizzo del circuito per rappresentare solo due stati possibili cioè
[00:50:04 - 00:50:11] un'informazione caratterizzata da due volodi possibili ok se invece voglio rappresentare
[00:50:12 - 00:50:23] oggi c'è il sole c'è c'è una nuvola sta piovendo sta nevicando sta grandinando sono
[00:50:23 - 00:50:30] cinque valori possibili della mia descrizione del tempo dei oggi del medio di oggi ok quindi
[00:50:30 - 00:50:39] le informazioni possibili non sono più due ma sono cinque se io voglio costruire un dispositivo
[00:50:39 - 00:50:45] che sempre con quei cinque volte mi deve rappresentare cinque possibili valori distinti
[00:50:45 - 00:50:51] ovviamente quello che posso fare avere una tensione bassa una tensione un po più alta
[00:50:51 - 00:50:57] una tensione media devo andarmi a definire in che modo le mie tensioni possibili le vado
[00:50:57 - 00:51:04] ad associare alle informazioni e quindi posso dire che ne so da 0 a 1 volta c'è bella giornata da
[00:51:05 - 00:51:11] un volta a due volte voglio rappresentare nuvoloso da due a tre volte quindi più
[00:51:11 - 00:51:18] aumento le capose che voglio rappresentare su quei cinque volte a disposizione più mi devo
[00:51:18 - 00:51:29] restringere gli intervalli di tensione ti trovi? Si e ovviamente costringermi ad avere che l'informazione
[00:51:29 - 00:51:37] minima a cinque valori possibili mi costringe a restringere gli intervalli di rappresentazione
[00:51:37 - 00:51:44] un intervallo di rappresentazione più piccolo è un intervallo che soffre più facilmente
[00:51:44 - 00:51:53] degli errori dovuti agli sbalzi di tensione perché appena mi arriva uno sbalzo di tensione
[00:51:53 - 00:51:59] può darsi che io casco in un intervallo diverso e quindi l'informazione rappresentata non è più
[00:51:59 - 00:52:05] quella teorica ma è un'altra non so se ho spiegato meglio quello che volevo dire. Perfettamente
[00:52:05 - 00:52:11] no no perfettamente ho capito perfettamente e quindi avere un sistema in cui l'informazione
[00:52:11 - 00:52:20] minima ha il minor numero possibile di stati diversi che ovviamente è meno di due non riesco a fare
[00:52:20 - 00:52:27] mi permette di realizzare sistemi di memorizzazione più affidabili e quindi per questo ci si è
[00:52:27 - 00:52:34] buttato cioè si è seguito la codifica binaria proprio perché dal punto di vista elettronico
[00:52:34 - 00:52:40] dei circuiti sono più affidabili in questo modo perché il range di grandezza fisica utilizzata
[00:52:40 - 00:52:47] vi è sfruttato meglio dal punto di vista della robustezza ai guasti da tolleranza ai guasti.
[00:52:47 - 00:52:52] Sì chiaro grazie mille. Di niente.
[00:52:57 - 00:53:08] Ok se non ci sono altre domande allora vi saluto e ci vediamo alla prossima lezione.
[00:53:08 - 00:53:17] Grazie buonasera buonasera buonasera. Grazie buonasera.
