# Lezione 18 - Riduzione della lunghezza del percorso di esecuzione

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\Lezione 18 - Riduzione della lunghezza del percorso di esecuzione.mp4`
- Durata: 00:43:46
- Trascrizione: `18_lezione_18_riduzione_della_lunghezza_del_percorso_di_esecuzione.json`

## Argomenti probabili
- porte_logiche (135): and, or, nand
- microarchitettura (86): microarchitettura, mic, alu, controllo
- clock_prestazioni (58): clock, ciclo, frequenza, prestazioni, tempo
- memoria_bus (48): memoria, bus, indirizzo, ram, rom
- mips_assembly (32): registro, registri, sb

## Trascrizione

[00:00:00 - 00:00:19] Con qui vengono eseguite le istruzioni e vediamo alcune possibili soluzioni che possano
[00:00:19 - 00:00:28] appunto migliorare o, diciamo, ridurre i tempi con cui vengono eseguite l'estruzione.
[00:00:28 - 00:00:40] Allora, abbiamo detto più volte che, ovviamente, quando dobbiamo progettare qualcosa, quindi
[00:00:40 - 00:00:48] anche per la microarchitettura che va a implementare, diciamo, l'estruzione di livello isa, bisogna
[00:00:48 - 00:00:53] sempre scegliere, diciamo, una soluzione che in qualche modo è una soluzione di compromesso
[00:00:53 - 00:01:05] tra varie esigenze, tra cui le esigenze di cui bisogna ter condutili veramente sono ovviamente
[00:01:05 - 00:01:12] la velocità di eseguzione che accennavo prima, però anche i costi per realizzare l'architettura,
[00:01:12 - 00:01:21] la fittabilità, la facilità poi con cui può essere utilizzata, il consumo energetico
[00:01:21 - 00:01:26] e poi anche le dimensioni fisiche che abbiamo detto varie volte che nell'ambito dei circuiti
[00:01:26 - 00:01:36] integrati si parla di occupazione proprio di area di superficie e quindi scegliere delle
[00:01:36 - 00:01:43] soluzioni che richiedono l'implementazione di opportuni circuiti bisogna poi tenere
[00:01:43 - 00:01:49] conto, non solo del costo di realizzazione ma anche poi dello spazio che è aggiuntivo
[00:01:49 - 00:02:01] richiesto nel circuito, nel processo. Allora, gli approcci che venono tipicamente perseguiti
[00:02:01 - 00:02:07] per aumentare la velocità abbiamo accennati anche altre volte, sono ovviamente quello
[00:02:07 - 00:02:15] più immediato, potrebbe essere quello di, diciamo, intervenire sui cicli di clock, quindi
[00:02:15 - 00:02:26] o malamente aumentare la frequenza del clock, questo che mente comporta altre problematiche,
[00:02:26 - 00:02:35] oppure cercare di ridurre il numero di micro istruzioni necessari per implementare una
[00:02:35 - 00:02:44] istruzione isa, cioè ridurre il numero di cicli di clock necessari appunto per eseguire
[00:02:44 - 00:02:50] una istruzione isa. Ricordato, abbiamo detto più volte che con quella microarchitettura
[00:02:50 - 00:02:59] che abbiamo studiato con quel datapad della microarchitettura c'erano diverse problematiche,
[00:02:59 - 00:03:08] ovunque necessità banalmente per mettere un operando, un secondo operando nell'aluo eravamo costretti
[00:03:08 - 00:03:19] a perdere un ciclo di clock solo per caricare l'operando in H. E quindi trovare delle strategie
[00:03:19 - 00:03:25] che invece possano ridurre il numero di cicli di clock necessari per implementare una singola
[00:03:25 - 00:03:31] istruzione, ovviamente impatto sulla velocità di eseguzione dell'istruzione stessa che non ci
[00:03:31 - 00:03:42] metterà più, che ne so, quattro cicli, ma ne metterà tre e così via. Aumentare la frequenza
[00:03:42 - 00:03:55] di clock vuol dire ovviamente ridurre, semplificare la durata del ciclo di clock, oppure cercare
[00:03:55 - 00:04:06] una soluzione basata sul parallelismo, ad esempio architetture superscalari in grado di effettuare
[00:04:06 - 00:04:21] più operazione, più istruzioni contemporaneamente. Quindi ovviamente tra le varie soluzioni possibili,
[00:04:21 - 00:04:28] come detto prima, quando si fa una scelta e si persegue una strategia tra una di queste,
[00:04:28 - 00:04:34] per esempio, su cui stiamo ragionando, abbiamo detto da una parte andrò a guadagnare, da
[00:04:34 - 00:04:44] l'altra andrò a perdere, sarà sempre una scelta di compremesso e quindi dobbiamo, bisogna
[00:04:44 - 00:04:52] il progettista, diciamo, dovete nel punto e deve scegliere una soluzione bilanciando, diciamo,
[00:04:52 - 00:04:58] da una parte i costi per realizzare un'architettura e introdurre nuovi circuiti che permettono
[00:04:58 - 00:05:05] di effettuare una esecuzione in parallelo di, se non delle istruzioni, di alcuni stage,
[00:05:05 - 00:05:14] di alcune fasi, diciamo, delle esecuzioni del ciclo, il ciclo intendo quello là generale,
[00:05:14 - 00:05:30] il fetch, decode, execute e diciamo non sempre, ovviamente, possibile investire su più soluzioni,
[00:05:30 - 00:05:42] ma bisogna scegliere, appunto, qualcosa di compremesso. Allora, abbiamo detto che il data path
[00:05:42 - 00:05:50] per come è fatto, per come viene progettata la micro-architettura, in patta, diciamo,
[00:05:50 - 00:05:59] sul numero di operazioni necessari per svolgere, per implementare una istruzione isa e in qualche
[00:05:59 - 00:06:05] modo in patta, quindi la progettazione stessa, l'architettura pensata, in patta su il numero
[00:06:05 - 00:06:15] di cicli necessari per seguire l'estruzione. Il fatto che un'estruzione isa richieda due
[00:06:15 - 00:06:20] o più cicli di clock è figlio proprio di come abbiamo organizzati, di come sono state
[00:06:20 - 00:06:29] organizzati i registri, le bus che abbiamo previsto e tecnici dal path, ok? E questo,
[00:06:29 - 00:06:36] perché? Perché comunque, diciamo, il data path abbiamo detto, insieme delle registri,
[00:06:36 - 00:06:44] diciamo, l'insieme delle circuiti, delle unità che sono coinvolte nel flusso di esecuzione
[00:06:44 - 00:06:54] dell'istruzione, ovviamente più unità sono coinvolte, più è lungo il percorso del data
[00:06:54 - 00:07:04] path, più saranno, diciamo, necessari i cicli di clock per seguire l'estruzione. Quindi,
[00:07:04 - 00:07:12] una cosa su cui si può andare a investire per ridurre il numero di cicli di clock, quindi
[00:07:12 - 00:07:21] per aumentare la velocità di esecuzione dell'estruzione è quello di cercare di accorciare
[00:07:21 - 00:07:30] la lunghezza di questo percorso. Il fatto che, ripeto, per come abbiamo fatto quella
[00:07:30 - 00:07:42] micrarchitettura micuno, bisogna passare per l'alu per mettere un operando in ACA e poi
[00:07:42 - 00:07:51] prendere l'altro operando da un altro registro potrei, diciamo, ridurre o meglio evitare
[00:07:51 - 00:07:57] questa inutile passaggio nell'alu, ma prevedere, per esempio, un'architettura leggermente
[00:07:57 - 00:08:03] diversa, introducendo nuovi componenti che permettono di caricare gli operandi nello
[00:08:03 - 00:08:10] stesso ciclo di clock, questo ovviamente richiede poi un'aggiunta di hardware delicato. Quindi,
[00:08:10 - 00:08:16] se da una parte voglio risparmiare hardware, mi complico poi l'utilizzo, se lo voglio semplificare
[00:08:16 - 00:08:28] l'utilizzo, a volte sono costretto ad aggiungere componenti all'architettura. Malalmente il
[00:08:28 - 00:08:36] fatto che noi sappiamo che il program counter può essere o meglio debba essere incrementato
[00:08:36 - 00:08:43] ad ogni ciclo in modo da puntare al byte successivo rispetto a quello, diciamo, letto nel ciclo
[00:08:43 - 00:08:53] precedente, se, diciamo, questo incremento non lo faccio passando dall'alu, ma prevedo
[00:08:53 - 00:09:00] che è un circuito dedicato che fa solo l'incremento per il program counter, ovviamente posso risparmiare
[00:09:00 - 00:09:16] tempo, semplicemente ovviamente devo pagare contro hardware aggiuntivo, scusate. Tuttavia,
[00:09:16 - 00:09:27] quando si incrementa il program counter poi bisogna comunque svolgere l'operazione, diciamo,
[00:09:27 - 00:09:37] di lettura, però l'esecuzione dell'estruzione non può essere anticipata, ma ho solo, diciamo,
[00:09:37 - 00:09:52] effettuato l'incremento evitando di occupare l'alu. Quindi, diciamo, il solo aggiungere
[00:09:52 - 00:10:03] un circuito che mi incrementa il program counter impatta relativamente poco, nel senso che comunque mi servirebbe
[00:10:03 - 00:10:16] qualche soluzione in più per ottenere un risparmio più significativo. E, diciamo, una delle tecniche più
[00:10:16 - 00:10:24] significative, da punto di vista di quanto riesce ad accelerare il prelievo delle istruzioni, quello appunto, come
[00:10:24 - 00:10:42] ci chiamavamo prima, di andare a sovrapporre l'esecuzione di alcune istruzioni. Ad esempio, il modo che,
[00:10:42 - 00:10:54] mentre un'unità del datapad effettua un'operazione, potrei far partire un'altra operazione con un'altra
[00:10:54 - 00:11:09] unità. Ad esempio, avere un'unità che va a prelevare autonomamente senza passare dal datapad, senza impegnare
[00:11:09 - 00:11:21] il processore, il dato puntato dal program counter, mi potrebbe, diciamo, risparmiare il vero circuito.
[00:11:21 - 00:11:35] Attenzione, amicofono. Come accennavo prima, nell'ambito dei circuiti integrati, però non bisogna tenere
[00:11:35 - 00:11:44] il conto solo dei costi per aggiungere hardware, nel senso di costi di realizzazione, ma bisogna anche tenere il conto
[00:11:44 - 00:11:55] dello spazio, perché noi, in circuito integrato, ovviamente, nemmeno ammettere diverse circuiti e quindi
[00:11:55 - 00:12:08] andarne ad aggiungere ulteriori, mi riduce, diciamo, la distanza tra i tracercuti presenti. Si parla
[00:12:08 - 00:12:19] di proprietà terriera di un cipro, riferendosi proprio all'aria richiesta dal circuito, isolata proprio
[00:12:19 - 00:12:28] in acri picoacri, ovviamente, perché sono piccolissime le dimensioni, però l'unità di misura richiama
[00:12:28 - 00:12:40] appunto a quella della terra. Questo perché ormai circuiti integrati ne contengono talmente tanti,
[00:12:40 - 00:12:51] quindi più che contare quanti ce ne sono, si ragiona su quale è lo spazio fisico che occupano, cioè quale è l'aria fisica
[00:12:51 - 00:13:07] effettivamente occupata dal circuito integrato. Un'altra cosa su cui a volte ci abbiamo già ragionato è il sommatore,
[00:13:07 - 00:13:25] il fatto che esistono diverse modi per implementare un circuito sommatore. C'è fatto capire che a volte la soluzione
[00:13:25 - 00:13:34] didattica che si studia per capire come funziona un circuito è diversa da quella che effettivamente viene
[00:13:34 - 00:13:43] implementata perché poi nell'implementazione, nella realizzazione fisica ci sono esigenze diverse e qui sono stati studiati
[00:13:43 - 00:13:53] ad esempio per il sommatore ma anche per tante altre tipologie di circuiti, implementazioni che cercassano di ottimizzare
[00:13:53 - 00:14:04] o la velocità di esecuzione o lo spazio occupato. Dificamente il sommatore che entra in gioco come potete immaginare una moltitudine
[00:14:04 - 00:14:17] di istruzioni e di operazioni, si è cercato di realizzarlo sempre quanto più veloce possibile proprio perché impatta
[00:14:17 - 00:14:24] la proprietà terriera. Quindi come costo che bisogna sostenere per ridurre i tempi per aumentare quindi la velocità di esecuzione
[00:14:24 - 00:14:35] spesso è proprio il fatto che la velocità di esecuzione, quindi la velocità di esecuzione,
[00:14:35 - 00:14:47] ok quindi come costo che bisogna sostenere per ridurre i tempi per aumentare quindi la velocità di esecuzione spesso è proprio il fatto
[00:14:47 - 00:14:57] che bisogna perdere in proprietà terriera, cioè il circuito diventa più esteso, più grande, occupano superficie maggiore.
[00:14:57 - 00:15:10] Abbiamo parlato del fatto che del clock, che ovviamente aumentare la velocità del clock, aumentare la frequenza del clock,
[00:15:10 - 00:15:23] vi permette di aumentare il numero di istruzioni che riesco a seguire al secondo però ovviamente potete immaginare che ci sono diverse problematiche
[00:15:24 - 00:15:40] che vengono impattate diciamo dall'aumentare dalla frequenza e quindi piuttosto che aumentare soltanto la frequenza del clock
[00:15:40 - 00:15:56] nel ganni si è investito, si è studiato come aumentare invece il parallelismo, cercare di creare architetture in grado di seguire più compiti in parallelo
[00:15:56 - 00:16:12] ovviamente il parallelismo può essere utilizzato per quelle operazioni che sono in qualche modo parallelizzabili, ci sono istruzioni o comunque parti
[00:16:12 - 00:16:28] di istruzioni che sono intrinsicamente seriali e quindi non possono essere parallelizzate nel senso che una fase, una parte di un'istruzione o un'istruzione intera per essere eseguito
[00:16:28 - 00:16:39] per cui rattende l'input prodotto dalla nostra istruzione, in questo caso c'è una dipendenza e quindi da questo punto di vista sono intrinsicamente seriali
[00:16:39 - 00:16:57] se si riescono a individuare parti, fasi o istruzioni che sono parallelizzabili nel senso che non dipendono dall'altra allora si può prevedere una strategia di eseguzione in parallelo dell'hardware
[00:16:57 - 00:17:12] che effetti delle operazioni in parallelo e quindi anche in questo caso aumentare in qualche modo la velocità di eseguzione
[00:17:12 - 00:17:33] un'altra cosa su cui abbiamo già parlato, se vi ricordate quando abbiamo visto il formato delle microestruzioni della nostra architettura
[00:17:33 - 00:17:52] avevamo detto che per ridurre il numero di bit dell'instruzione, con la lunghezza delle microestruzioni, l'informazione su quale registro fosse abilitato,
[00:17:52 - 00:18:11] su quale registro possiamo abilitare per scrivere sul bus V, avevamo detto che utilizzavamo una strategia di codifica in cui invece di rappresentare i 9 bit per ogni registro che può scrivere
[00:18:11 - 00:18:27] utilizzavamo soltanto 4 codificando l'informazione su quale fosse il registro, ovviamente questo risparmio di bit necessario a memorizzare le istruzioni e a gestile
[00:18:28 - 00:18:39] da come svantaggio il fatto che devo aggiungere un componente ulteriore, un hardware ulteriore per la decodifica di questa informazione
[00:18:39 - 00:18:54] mentre invece le informazioni su registro che possono leggere dal bus C avevamo detto che sono semplicemente collegati i bit ai segnali di abilitazione, quindi non c'è l'hardware aggiuntivo
[00:18:55 - 00:19:12] in questo caso invece c'è bisogno di aggiungere un hardware di decodifica che mi va a occupare spazio ulteriore nel circuito, ma mi introduce anche un rallentamento che è il tempo appunto di decodifica dell'informazione
[00:19:13 - 00:19:35] e quindi diciamo in questo caso il ritardo diciamo introdotto dal circuito di decodifica impatta appunto anche sul quanto deve essere lungo il ciclo di clock
[00:19:35 - 00:19:56] quindi come al solito bilanciamento di nuovo tra velocità e costi, risparmiare invece abbiamo detto invece di 9 bit ne usiamo 4 quindi risparmiamo 5 bit per ogni parola, per ogni micro istruzione
[00:19:56 - 00:20:14] quindi parola della memoria di controllo che vi ricordo della memoria ROM dove memorizzano memorizzate le micro istruzioni che implementano le istruzioni ISA della Integger Java Virtual Machine
[00:20:14 - 00:20:42] che abbiamo su cui abbiamo costruito la nostra micro architettura, questo risparmio ovviamente lo andiamo a spendere in un rallentamento del clock perché dobbiamo aspettare che il circuito di decodifica termini le sue operazioni quindi anche se si potesse ridurre ulteriormente la duranza del clock quindi aumentarle alla frequenza poi ovviamente c'è un limite
[00:20:45 - 00:20:50] oltre che non possiamo andare perché abbiamo aggiunto questo circuito di decodifica
[00:20:52 - 00:21:09] quindi tipicamente se si vuole invece realizzare un sistema che va che massimizza la velocità dobbiamo, cioè una cosa su cui possiamo investire è quello di eliminare ove possibile appunto i circuiti di decodifica
[00:21:10 - 00:21:22] ciò comporta di conseguenza aumentare componenti hardware per gestire ad esempio in questo caso tutti nove bit piuttosto che soltanto quattro
[00:21:23 - 00:21:29] quindi in questo esempio diciamo aumentiamo la velocità
[00:21:31 - 00:21:33] ma aumentano anche i costi
[00:21:36 - 00:21:47] i costi per realizzare questa circuiteria in più, se vogliamo risparmiare bit, risparmiare memoria la velocità si riduce però
[00:21:47 - 00:22:01] allora vediamo qualche strategia per ridurre, aumentare la velocità basata invece sull'ottimizzazione del microcodice
[00:22:02 - 00:22:07] rivediamo quindi di nuovo la nostra microarchitettura
[00:22:15 - 00:22:23] che diciamo era pensata per ridurre al minimo i componenti hardware quindi pochi registri
[00:22:24 - 00:22:34] plalo molto semplice replicata 32 volte perché abbiamo letto in questi registri su una 32 bit
[00:22:37 - 00:22:46] con la memoria di controllo abbiamo letto per memorizzare le micro istruzioni che era 512 parole da 36 bit
[00:22:47 - 00:22:55] e poi i segnali di abilitazione dei registri più i segnali di controllo di alu e shifter
[00:22:56 - 00:23:04] abbiamo visto che questa scelta diciamo di risparmiare mettendo soltanto H in grado di scrivere su A
[00:23:05 - 00:23:14] ci comporta questa perdida di tempo ogni qualvolta dobbiamo effettuare un'operazione su due registri
[00:23:14 - 00:23:21] perché dobbiamo spendere un ciclo vedete per copiare un valore da un registro in H
[00:23:21 - 00:23:29] e un altro ciclo poi per caricare gli operanti l'input A e B dell'alu
[00:23:29 - 00:23:39] abbiamo detto per migliorare la velocità quello che possiamo fare c'è quello di cercare di ridurre la lunghezza
[00:23:39 - 00:23:53] dell'alu. Abbiamo detto per migliorare la velocità quello che possiamo fare tra le
[00:23:53 - 00:23:58] varie cose è quello di cercare di ridurre la lunghezza del percorso di esecuzione.
[00:23:58 - 00:24:08] Abbiamo anche detto che per migliorare la velocità stesso siamo costretti ad aggiungere componenti
[00:24:08 - 00:24:17] adder aggiuntivi nello specifico se ragioniamo su questa architettura di micuno possiamo
[00:24:17 - 00:24:28] introdurre, potremmo migliorare la velocità introdurendo basse diversi registri ulteriori o
[00:24:28 - 00:24:37] funzionali specializzate. Ad esempio che accendavo prima il fatto che se io aggiungo una
[00:24:37 - 00:24:45] unità che fa il fetch dalla memoria del byte diciamo indicato dal program counter senza
[00:24:45 - 00:24:52] quindi impegnare il processore posso farlo in parallelo mentre faccio altre quindi risparmiare
[00:24:52 - 00:25:03] cicli di clock riducendo appunto la lunghezza del percorso. Partiamo da quello più facile che
[00:25:03 - 00:25:14] invece è senza spendere costo senza comprare o introdurre diciamo nuovi componenti hardware
[00:25:14 - 00:25:23] la prima cosa che possiamo fare in quanto diciamo programmatore diciamo sviluppatore
[00:25:23 - 00:25:34] e pensare a livello di software di codice cioè le implementazioni che abbiamo visto la vostra
[00:25:34 - 00:25:43] scorsa cioè i micro programmi che implementano il livello isa se diciamo ragioniamo se possiamo in
[00:25:43 - 00:25:51] qualche modo migliorare le implementazioni del micro codice, le implementazioni del micro
[00:25:51 - 00:26:00] programma in modo da ridurre ove possibile ripeto dipende caso per caso se possibile anticipare
[00:26:00 - 00:26:09] qualche micro istruzione in modo da ridurre in qualche modo i cicli di clock del micro
[00:26:09 - 00:26:18] programma. Se un micro programma che sempre ripeto l'implementazione di un istruzione isa richiede
[00:26:18 - 00:26:28] 5 cicli di clock però ragionando su come avviene l'esecuzione delle micro istruzioni se riesco a
[00:26:28 - 00:26:34] trovare un modo per cui in castro meglio o diversamente diciamo nei micro istruzioni se
[00:26:34 - 00:26:43] riesco a ridurre da 5 a 4 cicli di clock necessari per eseguire completare quel micro programma
[00:26:43 - 00:26:51] allora in patto cioè riduco il tempo necessario per eseguire quelle istruzioni isa passo
[00:26:51 - 00:26:58] dall'istruzione isa che dura 5 cicli di clock a una che ne dure invece 4 senza introdurre
[00:26:58 - 00:27:06] hardware senza spendere soldi semplicemente ragionando e ottimizzando il micro codice.
[00:27:07 - 00:27:18] Vediamo un esempio in particolare di questa strategia e sicuramente per come le abbiamo
[00:27:18 - 00:27:25] visti diciamo la volta scorsa possiamo andare a ragionare sul micro istruzione main 1 che
[00:27:25 - 00:27:35] se vi ricordate era la micro istruzione che veniva diciamo incruosa in ogni micro programma
[00:27:35 - 00:27:45] perché ogni micro programma aveva l'onere di andare a incrementare il program counter e recuperla
[00:27:45 - 00:27:57] la prossima istruzione isa da eseguire in modo che ad ogni nuovo ciclo di clock
[00:27:57 - 00:28:07] come diciamo al ciclo di clock quando si passa alla prossima istruzione il byte il byte indicato
[00:28:07 - 00:28:15] dal program canto è forse già stato recuperato cioè la fase di fetch deve essere effettuata
[00:28:15 - 00:28:22] al termine di ogni micro programma così all'inizio del micro programma successivo che vuol dire
[00:28:22 - 00:28:28] all'inizio della eseguzione della prossima istruzione in mbr troviamo già l'opcode
[00:28:28 - 00:28:41] della istruzione da eseguire che sarebbe la riferimento nella memoria di controllo
[00:28:41 - 00:28:50] della micro istruzione che inizia il micro programma della nuova istruzione da eseguire quindi
[00:28:50 - 00:29:02] se questa continuo diciamo micro programma o meglio scusate in questa continuamica istruzione
[00:29:02 - 00:29:15] riesco in qualche modo a anticiparla in alcuni micro programmi può essere vantaggioso ragioniamo
[00:29:15 - 00:29:24] ad esempio su istruzione isa pop sozione isa pop sarebbe l'estrazione dell'elemento che si
[00:29:24 - 00:29:35] trova in cima allo stack e come riportato nella slide vedete un istruzione di livello isa che
[00:29:35 - 00:29:41] è stata viene o meglio viene implementata sulla microarchitettura che abbiamo considerato da
[00:29:41 - 00:29:49] questo micro programma micro programma che richiedete quattro cicli di croc cosa fa nella
[00:29:49 - 00:30:01] prima microstruzione assegna all'indirizzo a registro mar e assegna a registro sp che
[00:30:01 - 00:30:09] lo stack pointer che cosa il valore precedente perché adesso viene letto
[00:30:09 - 00:30:20] quello attuale quando si fa la pop quindi il puntatore allo stack deve essere decrementato
[00:30:20 - 00:30:34] e poiché il registro tos è il registro in cui è presente il valore che si trova in cima
[00:30:34 - 00:30:43] allo stack poiché se più è cambiato deve essere aggiornato il tos quindi si aggiorni
[00:30:43 - 00:30:55] sp si fa la lettura e si mette in tos mdr che il registro dove c'è il dato letto dalla memoria
[00:30:55 - 00:31:06] fatto ciò avendo finito diciamo le operazioni che caratterizzano la pop c'è sempre il go to
[00:31:06 - 00:31:13] min 1 che l'amicrostruzione che fa il ciclo di cui parlavo prima cioè incremento è proprio
[00:31:13 - 00:31:26] un counter fa la fetch in modo che in mbr viene inserito o meglio in modo che in mbr verrà
[00:31:26 - 00:31:47] inserito il nuovo valore e salta appunto ad mbr ora osserviamo che nel ciclo 2 dov'era questo
[00:31:47 - 00:31:59] qua in pop 2 poiché c'è stata la rid in pop 1 lo sta facendo niente sta solo attendendo che il
[00:31:59 - 00:32:08] dato venga recuperato dalla memoria quindi qua abbiamo un buco in cui possiamo inserire delle
[00:32:08 - 00:32:23] istruzioni qual delle micro istruzioni da effettuare e possiamo che cosa anticipare la
[00:32:23 - 00:32:38] parte di min 1 che l'incremento e il fetch un pop 2 quindi possiamo incrementare incremento
[00:32:38 - 00:32:48] nella richiesta dalla memoria del del opcode diciamo successivo il byte successivo così quando
[00:32:48 - 00:32:59] arrivo in pop 3 o scappare la segnazione che facevo anche prima invece di dire vai a min 1 dove
[00:32:59 - 00:33:08] poi devo fare quella micro istruzione solita dico soltanto vai direttamente a mbr perché in mbr
[00:33:08 - 00:33:14] adesso c'è il valore che è stato diciamo richiesto nel micro ciclo nella c'è nella
[00:33:14 - 00:33:25] micro istruzione precedente questa piccolissima modifica che diciamo a sfruttato un momento diciamo
[00:33:25 - 00:33:34] un ciclo in cui il micro programma non stava facendo niente mi permette di ridurre diciamo a
[00:33:34 - 00:33:45] 3 cicli a 3 micro istruzioni diciamo i cicli necessari per seguire l'instruzione pop quindi
[00:33:45 - 00:33:56] il struzione pop di suo passa da 4 cicli a 3 cicli e quindi diciamo o una una aumenta diciamo
[00:33:56 - 00:34:10] della velocità dell'esecuzione dell'estruzione di tipo pop quindi prima strategia che si può
[00:34:10 - 00:34:19] perseguire è questo unire cito di interpretazione alla fine delle sequenze di ogni micro codice
[00:34:19 - 00:34:31] mi permette di passare vedete da 4 a 3 pop 3 viene diciamo impattato in maniera marginale perché
[00:34:31 - 00:34:37] comunque faceva un salto invece di farlo a me ne lo fa a delle vierne quello che faccio e diciamo
[00:34:37 - 00:34:51] sfruttare meglio il pop 2 in cui lo facciamo integrativamente vediamo invece ora una soluzione
[00:34:51 - 00:35:03] in cui diciamo aumento posso aumentare la velocità di esecuzione posso meglio ancora ridurre la
[00:35:03 - 00:35:12] lunghezza del percorso di esecuzione del data pot spendendo soldi diciamo in acquistare
[00:35:12 - 00:35:19] il progettario diciamo un componente diverso cambiare quindi l'architettura ovviamente
[00:35:19 - 00:35:30] nell'ottimitazione del micro codice io non cambio l'architettura ma nella se invece diciamo sono
[00:35:30 - 00:35:38] disposto ad acquistare componenti aggiuntivi un problema che posso immediatamente risolvere che
[00:35:38 - 00:35:45] impatta molto diciamo la velocità di questa microchitettura è il fatto di passare da
[00:35:45 - 00:35:58] un'architettura a 2 bass a un'architettura diversa a 3 bass che diciamo non mi costringa a passare
[00:35:58 - 00:36:13] sempre per h quando devo operare su quando devo usare l'alu con due input potrei fare ad
[00:36:13 - 00:36:20] esempio questa architettura in cui ovviamente il terzo bass che devo che potrei inserire che
[00:36:20 - 00:36:34] potrei inserire diciamo mi serve per collegare i registri non solo al bass b ma anche al bass a in
[00:36:34 - 00:36:43] questo modo ogni registro che erano nove se non sbaglio che poteva scrivere su bass b e quindi
[00:36:43 - 00:36:51] inviare un dato in input all'alu se devo fare una versione tra due registri con questa nuova
[00:36:51 - 00:37:01] architettura io nello stesso ciclo di clock vedete ho un segnale aggiuntivo per ogni registro quindi
[00:37:01 - 00:37:11] i segnali di abilitazione passano da abilitazione sulla scrittura verso l'alu prima erano nove
[00:37:11 - 00:37:15] perché potremmo uno scrivere solo sul bass b ovviamente adesso aggiungendo un secondo bass
[00:37:15 - 00:37:25] il terzo basso totale per un secondo bass in input all'alu intendo che questo bass a ovviamente
[00:37:25 - 00:37:36] adesso o per ogni registro due segnali di abilitazione per la possibile scrittura sul bass a o sul bass b
[00:37:36 - 00:37:50] e quindi nello stesso ciclo abilitando i registri di interesse carico diciamo arrivo in come in
[00:37:50 - 00:37:57] input all'alu entrambi gli argomenti non ho più bisogno di fare il giro per caricare l'altro
[00:37:57 - 00:38:06] input ovviamente ho bisogno di aggiungere un basso ulteriore il collegamento a questo
[00:38:06 - 00:38:16] basso di tutti i registri più i segnali di abilitazione di questi registri quindi aggiungendo
[00:38:16 - 00:38:26] diciamo circuiteria più ovviamente mi impatterà poi sul formato delle microstruzioni il che mi
[00:38:26 - 00:38:36] fa aumentare la grandezza del del mir il micro istraccion registre mi fa aumentare la memoria
[00:38:36 - 00:38:51] di controllo e così via però diciamo questi costi aggiuntivi questi circuiti aggiuntivi mi garantiscono
[00:38:51 - 00:39:12] però un significativo aumento della velocità ovviamente cambia l'implementazione delle
[00:39:12 - 00:39:23] istruzioni isa che richiedono diciamo di operare su due valori perché ricordiamo sempre l'implementazione
[00:39:23 - 00:39:32] cioè i micro programmi sono direttamente dipendenti collegati all'architettura alla
[00:39:32 - 00:39:38] microarchitettura progettata nel momento in cui cambio la microarchitettura ne faccio una tre bassi
[00:39:39 - 00:39:52] vediamo in questa istruzione di velo isa la ilode prima ero costetto vedete a passare per h quindi
[00:39:52 - 00:40:04] primo ciclo lo perdevo a caricare in h il valore di lv poi andavo a fare delle operazioni la
[00:40:04 - 00:40:16] summa diciamo tra il valore che ho caricato in h quindi lv e mbr userebbe l mbr intero unsigned
[00:40:16 - 00:40:28] l mbr vi ricordo il circuito cioè il registro dove finisce il bite preso dalla come si fa la
[00:40:28 - 00:40:39] fetch però è un registro a 32 bit di cui tipicamente si utilizza soltanto il primo bite ma viene
[00:40:39 - 00:40:45] comunque realizzato a 32 bit perché in alcuni casi come in questo caso può essere utile utilizzarlo
[00:40:45 - 00:40:54] tutto ma viene utilizzato tipicamente unsigned cioè quindi senza abbandare il bit di segno
[00:40:54 - 00:41:04] torniamo a noi quindi faccio io devo fare questa operazione di somma tra mbr e quindi mbr preso
[00:41:04 - 00:41:14] interamente a 32 bit più il valore di h per mettere il valore dell indirizzo di interesse in
[00:41:14 - 00:41:29] mar e poi lanciare la rit ovviamente nel momento in cui io ho un terzo bass questo passaggio in h e
[00:41:29 - 00:41:40] poi effettuare la somma in ilod 2 me lo posso risparmiare e posso implementare la ilod direttamente
[00:41:40 - 00:41:49] scrivendo mar uguale mbr u più lv adesso lo posso scrivere posso effettuare operazioni
[00:41:49 - 00:41:56] dirette tra i registri perché i registri sono collegati a entrambi gli input della dell alu
[00:41:56 - 00:42:09] questo diciamo mi permette ovviamente di passare da tre sei cicli per implementare il odd nella
[00:42:09 - 00:42:18] archivettura micuno in cinque cicli per implementare la ilod in questa archivettura a tre bass
[00:42:23 - 00:42:30] quindi oltre a cercare di ottimizzare il colge per anticipare istruzioni nei ritagli di tempo
[00:42:30 - 00:42:39] quando il micro programma è in attesa altro scelta diciamo che impatta significativamente
[00:42:39 - 00:42:51] quella da aggiungere un terzo bass mi riduce diciamo il cicli necessario ad esempio per per l'ai lod
[00:42:51 - 00:43:02] ed è appunto una seconda tecnica diciamo per migliorare le prestazioni
[00:43:12 - 00:43:14] domande dubbi
[00:43:22 - 00:43:29] va bella cazzo se non ci sono domande io vi saluto alla prossima
[00:43:35 - 00:43:35] per i dirci
