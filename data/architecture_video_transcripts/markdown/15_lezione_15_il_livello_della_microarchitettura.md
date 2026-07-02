# Lezione 15 - Il livello della microarchitettura

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\Lezione 15 - Il livello della microarchitettura.mp4`
- Durata: 00:45:18
- Trascrizione: `15_lezione_15_il_livello_della_microarchitettura.json`

## Argomenti probabili
- porte_logiche (198): and, or, not, nand, sop
- memoria_bus (131): memoria, bus, indirizzo, temporizzazione, ram, rom
- microarchitettura (100): microarchitettura, mic, alu, controllo
- registri_flip_flop (67): registro, registri, propagazione
- mips_assembly (65): registro, registri

## Trascrizione

[00:00:00 - 00:00:20] Poi abbiamo l'instruzione di aspo di vero che è unica, ma poi viene implementata a
[00:00:20 - 00:00:26] il livello di microarchitettura da più microestruzioni che vengono eseguite come se fosse un bel
[00:00:26 - 00:00:37] proprio programma che utilizza microestruzioni più fini.
[00:00:37 - 00:00:47] Allora per vedere un esempio di come funziona l'implementazione di un'instruzione di
[00:00:47 - 00:00:55] livello ISA, la generemo su un ridotto set di istruzioni, quindi consideriamo come
[00:00:55 - 00:01:02] il livello ISA che vogliamo implementare in questa microarchitettura, un sott'insieme
[00:01:02 - 00:01:09] della Java Virtual Machine che contiene solo istruzioni che lavorano su interi, indicato
[00:01:09 - 00:01:19] con la Java Virtual Machine. Anche se è molto piccolo come insieme ISA, come di a livello
[00:01:19 - 00:01:25] didattico c'è utile per vedere effettivamente come un'instruzione di livello ISA può essere
[00:01:25 - 00:01:33] implementata nell'architettura con questa logica di spezzettar, da scompore questa
[00:01:33 - 00:01:40] macroestruzione di livello ISA in microestruzioni da eseguire come se fosse un programma che
[00:01:40 - 00:01:52] appunto prende il nome appunto di microprogrammazione proprio per come viene implementata l'esecuzione
[00:01:52 - 00:02:01] di questa istruzione. Quindi non abbiamo un mette indiretto tra istruzione ISA e circuito
[00:02:01 - 00:02:17] che la implementa. Abbiamo invece il su... che viene, come dire, decodificata, scomposta
[00:02:17 - 00:02:25] in microoperazioni che poi possono essere implementate attraverso l'architettura, attraverso
[00:02:25 - 00:02:34] i circuiti. Quello che ci serve però è un circuito in più, un programma in più che
[00:02:34 - 00:02:40] è come software che va a interpretare e seguire queste microestruzioni e c'è quello che
[00:02:40 - 00:02:47] si chiama appunto un microprogramma che, come dire, ad ogni ciclo del clock finché
[00:02:47 - 00:02:54] il computer, il calcolatore, è alimentato questo microprogramma che quindi è sulla
[00:02:54 - 00:03:00] da un livello ISA, ma è una scelta architetturale, è un'implementazione del livello sottostante
[00:03:00 - 00:03:07] della microartitettura, esiste appunto un microprogramma in una ROM, ovviamente, che
[00:03:07 - 00:03:16] ad ogni ciclo di clock va a vedere quale è la prossima esruzione da eseguire, la preleva,
[00:03:16 - 00:03:23] la decodifica, capisce se ci sono delle operazioni da effettuare, quali sono le operazioni da
[00:03:23 - 00:03:28] effettuare e gli eseguire. Quindi, come si avessimo in un linguaggio da alto livello,
[00:03:28 - 00:03:34] un loop continuo, un foro, un ciclo in esecuzione che va a spolgere delle operazioni.
[00:03:34 - 00:03:45] Quindi quando l'esecuzione delle esruzioni svolta tramite il microprogrammazione si
[00:03:45 - 00:03:52] intende questo, che la singola esruzione di livello ISA non ha una sua, diciamo, implementazione
[00:03:52 - 00:03:59] diretta circuitale, ma viene gestita come se fosse appunto un microprogramma livello più
[00:03:59 - 00:04:08] basso che la va a interpretare, a decodificare e a eseguire. Abbiamo quindi un microprogramma
[00:04:08 - 00:04:16] appunto memorizzato in una ROM che esegue queste esruzioni basilari ciclicamente che
[00:04:16 - 00:04:23] nessuno oppure vai a leggere, lo vediamo più avanti, qualche esempio, è leggere, diciamo,
[00:04:23 - 00:04:28] un registro del processore dove è indicato qual è la vostra esruzione di eseguire,
[00:04:28 - 00:04:33] ovviamente immaginate se è un processore che segue un'estruzione alla volta, deve capire
[00:04:33 - 00:04:41] quale deve eseguire. Quindi questo microgramma, frenamente in eseguzione, va a leggere in
[00:04:41 - 00:04:48] dirizzo della vostra esruzione di eseguire, noi ci troviamo in un modello di Bicontorman in cui
[00:04:48 - 00:04:57] i programmi, i dati risiedono il memoria, quindi pregavare la vostra esruzione da eseguire
[00:04:57 - 00:05:02] vuol dire, anche alla legge, dalla memoria, qual è l'estruzione da eseguire, la si prelleva,
[00:05:02 - 00:05:07] poi può essere dalla cresce oppure direttamente dalla memoria, comunque la si prelleva dalla
[00:05:07 - 00:05:16] memoria e poi c'è la fase del codifica nel senso che in base a l'estruzione che si è prelevata
[00:05:16 - 00:05:22] si fa vedere, il tipo di istruzione del codificare l'estruzione vuol dire capire qual è l'estruzione
[00:05:22 - 00:05:29] tra quelle supportate, tra quelle possibili, se l'estruzione richiede degli operandi dove si
[00:05:29 - 00:05:35] trovano questi operandi se stanno stessi sui registri del processore o se l'operante risiede
[00:05:35 - 00:05:41] il memore anch'esso e quindi mi ha prima di poter eseguire l'operazione e andare a
[00:05:41 - 00:05:46] recuperare questa informazione, ovviamente se si recupera l'informazione dalla memoria potete
[00:05:46 - 00:05:53] immaginare che difficilmente riuscirò a eseguire l'operazione nel singolo ciclo di clock no,
[00:05:53 - 00:06:02] perché abbiamo visto la tolto prelievo dalla memoria, occupa più cicli e quindi una volta
[00:06:02 - 00:06:10] che termina questo recupero degli operandi per quelle istruzioni che ne necessitano che
[00:06:10 - 00:06:16] ne hanno bisogno, allora finalmente si può eseguire l'estruzione, l'estruzione produrrà,
[00:06:16 - 00:06:21] cioè l'esecuzione produrrà degli autobot, l'esecuzione, immaginiamo che venga sempre
[00:06:21 - 00:06:27] fatta tramite l'alu, ovviamente l'alu, se vi ricordate avevo detto più volte, che comunque è
[00:06:27 - 00:06:34] unirretà logica o ritmetica che supporta diverse tipologie di operazioni, si effettuano
[00:06:34 - 00:06:40] queste operazioni tramite l'alu, prendere al suo tempo, eseguire, cioè produrrà un
[00:06:40 - 00:06:46] autobot, questo autoboi dovrà essere salvato da qualche parte, quindi vedete, stiamo come
[00:06:46 - 00:06:54] dire eseguire la singola istruzione, vuol dire svolgere un programma composto da più micro
[00:06:54 - 00:07:04] operazioni, da più micro istruzioni. Questo ciclo, il classico ciclo del processore,
[00:07:04 - 00:07:12] ripeto, è per memente in funzione, in eseguzione, finché la macchina è alimentata, il computer
[00:07:12 - 00:07:19] è alimentato, il processore fa questo ciclo, le fasi principali sono fetch, cioè recupera
[00:07:19 - 00:07:30] istruzione, decodifica, esegui. La fase di operando, cioè recupero degli operandi,
[00:07:30 - 00:07:37] diciamolo opzionale, dipende dalla particolare istruzione, quindi sicuro c'è fetch, decodifica
[00:07:37 - 00:07:43] istruzione, se l'istruzione, la micro, c'è l'istruzione da eseguire che lo richiede,
[00:07:43 - 00:07:47] sì, si potrà avere fetch, decodifica, recupero, operandi e poi eseguzione.
[00:07:47 - 00:08:04] Come tutti i programmi, anche questo microprogramma lavorerà su delle variabili che memorizzano
[00:08:04 - 00:08:11] e tengono costantemente, diciamo, lo stato della istruzione, lo stato del microprogramma
[00:08:11 - 00:08:18] che si sta eseguendo, no, delle microestruzioni. Ovviamente queste variabili tipicamente saranno
[00:08:18 - 00:08:25] associate ai corrispondenti registri del processore, quindi avremo, ad esempio, il
[00:08:25 - 00:08:32] program counter, che è il registro che memorizza, diciamo, l'istro indirizzo della prossima
[00:08:32 - 00:08:40] istruzione da eseguire, avremo il registro in cui viene memorizzata l'istruzione da
[00:08:40 - 00:08:47] eseguire, l'extraction register e così via. Quindi, varie registri che compongono o
[00:08:47 - 00:08:55] meglio che sono coinvolti nell'eseguizione di questo microprogramma rappresentano lo
[00:08:55 - 00:08:58] stato del microprogramma stesso, cioè dell'eseguizione stessa.
[00:08:58 - 00:09:08] Vedremo, nelle prossime slide, durante queste eseguzioni di questo microprogramma, tutti
[00:09:08 - 00:09:19] registri coinvolti, l'ALU, diciamo, in questo ciclo, quindi recupero dell'istruzione,
[00:09:19 - 00:09:27] memorizzazione nei registri opportuni, i registri coinvolti che possono contenere operandi,
[00:09:27 - 00:09:35] che possono contenere risultati delle operazioni, l'ALU o così dire, costituiscono quello
[00:09:35 - 00:09:42] che si chiama il datapad, cioè l'insieme dei registri coinvolti appunto in questo ciclo
[00:09:42 - 00:09:55] continuo l'eseguizione delle strutti. Ad esempio, qui ho parlato nello specifico
[00:09:55 - 00:10:02] le istruzioni che vedremo, sono molto semplici, sono tipicamente in colge identificativo
[00:10:02 - 00:10:11] l'opcode che identifica univocamente la particolare istruzione ISA da eseguire e per
[00:10:11 - 00:10:17] lo più si hanno degli operandi, avranno, la Giopparte non c'è un operando, alcune
[00:10:17 - 00:10:23] c'è l'ALU e così via, quindi sono molto molto semplici.
[00:10:23 - 00:10:42] Attenzione, non attivare il microfono involontariamente. Allora, come è detto, si chiama Fetch
[00:10:42 - 00:10:51] Decode, l'eseguizione e il ciclo, ed è, diciamo, il modo in cui la nostra musica
[00:10:51 - 00:10:58] d'artitettura andrà, va, diciamo, a implementare le istruzioni di livello ISA. Ok? Questo ciclo
[00:10:58 - 00:11:06] che vedremo, queste operazioni, queste microoperazioni che vedremo, è sempre come il livello di
[00:11:06 - 00:11:12] microartitettura implementa il livello ISA. A livello ISA, se mi senti in livello superiore,
[00:11:12 - 00:11:19] dove sono definite le istruzioni supportate dalla macchina, la…
[00:11:20 - 00:11:21] ovviamente se non ci sono…
[00:11:21 - 00:11:28] …ciò che avviene a livello superiore non è visto, diciamo, è trasparente, questo non è
[00:11:28 - 00:11:35] completamente vero perché per ottinizzare certe cose è bene che il livello superiore
[00:11:35 - 00:11:42] sapeva come funziona il livello inferiore, però immaginiamolo a questo punto di vista,
[00:11:42 - 00:11:47] al senso che il livello ISA è un interfaccio a livello inferiore di microarchitettura,
[00:11:47 - 00:11:51] decidiamo come implementare quell'intervaccia con le istruzioni di livello ISA.
[00:11:51 - 00:12:01] Allora, qui da TAPAT, che accennava prima, abbiamo detto che insieme dei registri coinvolti
[00:12:01 - 00:12:10] nell'eseguizione delle microprogramma, abbiamo detto che ci sono vari registri che ho menzionato
[00:12:11 - 00:12:19] prima ci sono tanti altri, c'è l'ALU e poi c'è, diciamo, ci sono i bassi interni
[00:12:19 - 00:12:29] a processore che permettono ai registri di inviare i propri valori all'ALU e il bass che
[00:12:29 - 00:12:37] dall'ALU permette di inviare i risultati dell'ALU ai registri stessi. Vediamo adesso nello schema
[00:12:37 - 00:12:44] che non questi registri possono scrivere o possono essere scritti dall'ALU, però immaginate
[00:12:44 - 00:12:58] che questi collegamenti appunto costituiscono il TAPAT. Anche questo, essendo sempre al livello
[00:12:58 - 00:13:04] di microarchitettura, viene TAPAT, diciamo, viene progettato tipicamente tenendo volto
[00:13:04 - 00:13:17] delle istruzioni che si vuole implementare, quindi, che sono i registri che devono costituire
[00:13:17 - 00:13:24] il TAPAT. La tipologia di collegamenti tradiesi sono sempre, diciamo, scelte progettuali della
[00:13:24 - 00:13:32] microarchitettura in funzione delle istruzioni, sa che si vogliono implementare. Vediamo,
[00:13:32 - 00:13:41] ecco la quale la figura. Vedete, qua abbiamo alcuni registri in evidenza, il program
[00:13:41 - 00:13:52] counter, il memory address register, lo stack pointer e così via. Poi, quando vedremo qualche
[00:13:52 - 00:13:59] esempio, analizzeremo il dettaglio cosa fa ogni registro. Quello che da tenere a mente e notare
[00:13:59 - 00:14:10] al momento è che qui abbiamo l'ALU, vedete, i registri, quelli che possono scrivere sull'ALU,
[00:14:10 - 00:14:17] o meglio, quelli che possono, diciamo, inviare il proprio dato all'ALU, lo possono fare attraverso
[00:14:17 - 00:14:27] il bus B. Quindi abbiamo un bus a cui accedono alcuni registri che possono scrivere sul bus B,
[00:14:27 - 00:14:38] ovviamente, il dato che viene scritto sul bus B poi viene propagato fino all'ingresso B dell'ALU.
[00:14:39 - 00:14:48] Ovviamente, soltanto uno di questi registri sarà abilitato a scrivere sul bus B e quello
[00:14:48 - 00:14:54] sarà il valore del registro, diciamo, che vogliamo che coinvolto in un'operazione sull'ALU.
[00:14:57 - 00:15:02] L'ALU, se vi ricordate, abbiamo detto, può intettuare diverse operazioni.
[00:15:04 - 00:15:13] Questa faccetta sulla sinistra dell'ALU con la lineetta obbligua si intende che sono 6 linee,
[00:15:14 - 00:15:19] per, diciamo, per ridurre lo spazio ne è indicata una sola, ma sono 6 linee che sono
[00:15:19 - 00:15:27] le 6 linee di controllo dell'ALU e con l'obbligano, diciamo, l'operazione richiesta all'ALU.
[00:15:29 - 00:15:37] Poi abbiamo il bit n e 0 che sono dei bit, queste linee squaso la destra dell'ALU che
[00:15:37 - 00:15:40] prendono valore in base al risultato dell'operazione.
[00:15:40 - 00:15:54] L'autocut dell'ALU, vedete, va a finire in un registro shifter che ha due linee di controllo
[00:15:56 - 00:16:08] che può, diciamo, o meno shiftare il risultato o meglio lo shifter e registro che, diciamo,
[00:16:08 - 00:16:16] il valore che riceve in ingresso può riproporlo in uscita, shiftato di un bit o due,
[00:16:18 - 00:16:26] o meglio, un bit a sinistra o a destra, può fare lo shift o di tutta la stringa o solo
[00:16:27 - 00:16:33] del secondo byte della stringa, comunque, diciamo, la particolare ecologia di shifter
[00:16:33 - 00:16:44] è definita da segnale di controllo, dei segnali di controllo, o può banalmente riproporre
[00:16:44 - 00:16:52] l'ingresso senza shiftarlo. Il segnale, diciamo, in uscita dallo shifter, il valore,
[00:16:52 - 00:17:02] vedete, va a finire sul bus, sul bus C. Il bus C, diciamo, il dato che l'ALU scrive
[00:17:02 - 00:17:12] sul bus C può essere letto da alcuni registri, quelli che hanno la freccetta nera, vedete,
[00:17:12 - 00:17:21] in ingresso. Allora, ovviamente, sul bus B può scrivere un solo registro di quelli,
[00:17:21 - 00:17:29] diciamo, registro alla volta di quelli che possono scrivere sul bus B e solo l'ALU legge
[00:17:29 - 00:17:41] dal bus B. Sul bus C, invece, solo l'ALU scrive, mentre tutti i registri che possono,
[00:17:41 - 00:17:47] diciamo, leggere dal bus C eventualmente possono anche leggere in parallelo, ok? Non
[00:17:47 - 00:17:52] c'è un problema. Solo sulla scrittura c'è il vincolo che un registro alla volta deve
[00:17:52 - 00:17:59] scrivere, invece la lettura può essere fatta in parallelo. Queste freccettine che vedete
[00:17:59 - 00:18:07] sotto i registri, quella nera e quella bianca, sono di nuovo segnali di controllo per abilitare
[00:18:07 - 00:18:18] o meno la scrittura sul bus B, le freccette bianche e la lettura sul bus dal bus C delle
[00:18:18 - 00:18:34] freccette nere. E ovviamente ogni, diciamo, microestuzione implementata dalla nostra microarchivettura
[00:18:34 - 00:18:42] produrrà, diciamo, un'atterazione in qualche modo, un coinvolgimento di questi registri,
[00:18:42 - 00:18:50] cioè del datapart, ok? Per questo il datapart viene progettato in base all'estuzione che bisogna
[00:18:50 - 00:18:58] implementare, perciò poi ogni istruzione, ogni microestuzione del, o meglio, ogni istruzione
[00:18:58 - 00:19:04] del livello ISA viene implementata attraverso microestuzioni che vanno ad alterare questo
[00:19:04 - 00:19:15] datapart. Invece il livello H, che non ho menzionato ancora, e vedete un registro in cui è possibile
[00:19:15 - 00:19:26] scrivere sempre tanto il bus C e il registro in cui bisogna inserire i valori che si vogliono
[00:19:26 - 00:19:37] utilizzare per alimentare l'ingresso A dell'ALU. Questo cosa vuol dire che, come dire, un vincolo
[00:19:37 - 00:19:43] di questa implementazione, per come è stata progettata, progettato questo datapart in figura,
[00:19:44 - 00:19:52] abbiamo che tutti registri, cioè vari registri, possono scrivere, possono enviare un valore
[00:19:52 - 00:20:04] sull'operando B, diciamo l'ingresso B dell'ALU, ma sull'ingresso a solo il registro H può scrivere.
[00:20:05 - 00:20:11] Questo cosa vuol dire che se bisogna fare un'operazione, una microestuzione, diciamo,
[00:20:11 - 00:20:25] che deve essere eseguita ed è alterata dall'ALU, se questa istruzione non ha un unico operando,
[00:20:26 - 00:20:35] posso, diciamo, immediatamente farlo nell'unico ciclo di clock, ha belito quel registro che
[00:20:35 - 00:20:45] contiene l'operando, lo mando sul bus B, arriva all'ALU e svolgo l'operazione. Se invece bisogna
[00:20:46 - 00:20:55] effettuare un'operazione che coinvolge due operandi, non posso farlo mai, diciamo, in un unico
[00:20:55 - 00:21:04] ciclo, perché il primo ciclo lo devo perdere per inviare il dato sull'operando a, quindi,
[00:21:04 - 00:21:12] per arrivare ad H, per arrivare ad A o meglio, devo inviare, immaginate che l'operando sta
[00:21:12 - 00:21:18] tra, cioè i valori che voglio utilizzare, lo fa la somma, ad esempio, tra due registri, devo prendere
[00:21:18 - 00:21:28] uno di questi registri, lo mando sul bus B, attraverso l'ALU e poi dall'ALU arrivo ad H, solo
[00:21:28 - 00:21:37] in questo momento posso, come dire, mandarlo in A, ok? Quindi, perdo un primo ciclo per
[00:21:37 - 00:21:43] mandare l'operando in H e poi, al secondo ciclo, l'altro operando, lo prendo dall'altro registro
[00:21:43 - 00:21:51] e quindi riesco a fare l'operazione su AB. Ok, per come è progettata questo datapet o questo
[00:21:51 - 00:22:01] vincolo, che le operazioni che coinvolgono due operandi richiedono sempre il passaggio di un valore
[00:22:01 - 00:22:07] attraverso l'ALU soltanto per fare il giro, ok, per arrivare ad H.
[00:22:14 - 00:22:23] L'ALU l'abbiamo vista altre volte e svolge diverse operazioni, ha i segnali di controllo che determinano
[00:22:23 - 00:22:32] l'operazione d'effettuare, vediamo nelle lezioni scorse c'è altri segnali per abilitare i valori,
[00:22:32 - 00:22:41] per invertirli e così via. Vedete qua, ad esempio, riportato rispetto ai segnali e i valori di controllo,
[00:22:41 - 00:22:52] quale è la funzione che si va a implementare e quindi replicare AB, fare la somma di AB,
[00:22:52 - 00:23:06] incrementa AB più uno e così via, quindi operazione aritmetiche oppure logiche AB, AB oppure la
[00:23:06 - 00:23:19] negazione di un operando e così via. Questa è la cosa che vi dicevo prima, poiché l'ingresso
[00:23:19 - 00:23:26] all'importo sinistro, diciamo, dell'ALU e collegato al registro H, dobbiamo sempre passare attraverso
[00:23:26 - 00:23:42] l'ALU e allo shifter per rendiare un valore in AB. Lo shifter dicevo anche esso delle linee di controllo
[00:23:42 - 00:23:55] per effettuare alcune operazioni, nello specifico può eseguire lo scorrimento logico di un byte,
[00:23:55 - 00:24:04] quindi non un bit, sln8, oppure il classico scorrimento a destra, per esempio, di un bit.
[00:24:11 - 00:24:18] Allora, nelle operazioni che vedremo, che avvengono, diciamo, lungo questo data path,
[00:24:18 - 00:24:29] dobbiamo tenere presente che seguono, diciamo, come al solito la temporizzazione del clock,
[00:24:29 - 00:24:36] però non è che avvengono, diciamo, le operazioni solo sul fronte di salita o sul fronte di scesa,
[00:24:36 - 00:24:47] ma sono degli intervalli di tempo all'interno del ciclo, secondo cui tipicamente la lettura
[00:24:47 - 00:24:58] dai registri avviene all'inizio del ciclo, mentre la scrittura avviene verso la fine del ciclo,
[00:24:58 - 00:25:05] in modo che, al ciclo successivo, i valori nei registri siano già disponibili.
[00:25:13 - 00:25:19] E questa cosa, diciamo, ci sfruttano i ritardi nella propagazione, diciamo, designale,
[00:25:20 - 00:25:39] considerando un ciclo di questo dico, in cui inizia, vedete, sul fronte di scesa, abbiamo un primo intervallo delta2
[00:25:40 - 00:25:47] in cui vengono impostati i segnali di controllo del data path.
[00:25:52 - 00:25:59] Dopo un delta v, che è il tempo, diciamo, massimo necessario affinché i segnali siano stati inviati
[00:25:59 - 00:26:09] e siano stabili, segnali di controllo, si ha l'impostazione di H e del bus B.
[00:26:12 - 00:26:26] Dopo un altro intervallo, questo, diciamo, delta X, i valori sono stabili sul bus B e su H,
[00:26:26 - 00:26:36] e quindi può di dato, dal bus B, attraversare l'alu e lo shifter, quindi viene effettuata l'operazione.
[00:26:37 - 00:26:44] E, di nuovo, in questo terzo intervallo, siamo sempre nel livello basso, vedete, del ciclo,
[00:26:45 - 00:26:51] e stiamo vedendo i segnali come si propagano e fanno il giro nel data path.
[00:26:52 - 00:27:04] Abbiamo impostato le linee di controllo del data path, abbiamo impostato scritto, diciamo, sul bus B, chi doveva scrivere.
[00:27:10 - 00:27:18] Poi viene effettuata l'operazione configurata per l'alu e, dopo un certo intervallo delta Y,
[00:27:18 - 00:27:31] non si assicura che il dato sia, diciamo, il risultato dell'alu sia stato prodotto e che abbia attraversato anche lo shifter.
[00:27:34 - 00:27:44] Bus B, questo qua sempre, è quello di destra, no? Quindi abbiamo impostato i registri, abbiamo abilitato, tra i vari registri, uno che deve scrivere sul bus B.
[00:27:45 - 00:27:51] Nel delta X avviene questa scrittura, diciamo, il valore di un registro che ne è portato dal bus B.
[00:27:52 - 00:28:05] In delta Y, i valori del bus B, diciamo, che costituiscono l'input destro dell'alu passano attraverso l'alu e attraverso il shifter,
[00:28:06 - 00:28:07] ovviamente seguendo l'operazione.
[00:28:07 - 00:28:26] Nell'ultimo intervallo, cosa manca, il risultato prodotto dall'alu deve essere portato in ingresso al registro o ai registri che devono leggere dal bus, quindi abbiamo terminato il ciclo.
[00:28:26 - 00:28:43] Il dato parte dai registri, dal bus B arriva all'alu, termina esce fuori dall'alu, ritorna attraverso il bus C nei registri opposto a cui devono leggere.
[00:28:43 - 00:28:56] Ovviamente la cosa funziona perché i segnali, diciamo, non sono istantani, ma hanno delle tagli di propagazione che seguono questo ordine.
[00:28:57 - 00:29:03] Come al soldo il progettista, diciamo, deve garantire degli intervalli in cui le cose devono arvenire.
[00:29:13 - 00:29:40] Quando c'è il fronte di salita del clock, abbiamo detto il ciclo deve essere terminato, quindi i valori presenti nel bus C vengono, diciamo, letti da registri abilitati.
[00:29:44 - 00:29:50] In modo che al prossimo fronte di discesa si potrà ricominciare.
[00:29:51 - 00:30:07] Ok, quindi il fronte di discesa cominciano le operazioni, cominciano il ciclo del clock, tutte le operazioni del datapart, diciamo, si segnali, diciamo, attraverso il datapart,
[00:30:07 - 00:30:23] e diventano stabili sul bus C entro la fine, diciamo, entro il prossimo fronte di salita e al fronte di salita, diciamo, il dato viene letto nei registri opportuni, vengono abilitati i registri che devono leggere.
[00:30:23 - 00:30:48] Ovviamente il progettista, diciamo, chi realizza questa microarchitettura deve garantire che la somma di questi tempi, di questi delta, deve, diciamo, terminare in tempo prima che arriva il prossimo ciclo, prima del prossimo fronte di salita.
[00:30:49 - 00:31:00] In modo che quando scatta il comando ai registri C di legge, i registri di legge dal bus C i dati devono essere, i segnali devono essere già stabili.
[00:31:01 - 00:31:08] L'autunto dell'Alo e dello shifter deve essere già prodotto e essere stabile sul bus C.
[00:31:08 - 00:31:26] Abbiamo detto che i registri visualizzati, diciamo, in alto erano quelli dedicati alle operazioni verso la memoria.
[00:31:27 - 00:31:40] Ce ne sono diversi perché il mar, il indirizzo, cioè il registro che contiene, l'indirizzo di memoria a cui si vuole accedere.
[00:31:41 - 00:31:53] E, ovviamente, vedete, viene letto dalla memoria, diciamo, la freccia bianca uscente verso la memoria.
[00:31:54 - 00:32:08] Il registro MDR, invece il memoria data register, viene utilizzato, cioè contiene il dato effettivo che si vuole andare a o a scrivere in memoria o che viene letto dalla memoria.
[00:32:09 - 00:32:14] E per questo può essere sia scritto che letto dalla memoria.
[00:32:15 - 00:32:19] Quindi, in mar mettiamo l'indirizzo sempre.
[00:32:20 - 00:32:30] Se questo indirizzo è l'indirizzo di una cera di memoria che vogliamo leggere, in MDR andrà a finire la parola della memoria, diciamo, indirizzata da mar.
[00:32:31 - 00:32:46] Se invece in mar mettiamo l'indirizzo di una parola di memoria che vogliamo scrivere, in MDR dobbiamo mettere il dato che vogliamo scrivere in memoria all'indirizzo puntato, cioè indicato da mar.
[00:32:47 - 00:32:57] E, diciamo, mar e MDR sono come borti nella lettura e scrittura di dati dalla memoria o verso la memoria.
[00:33:00 - 00:33:10] Il programcante, invece, è PC, abbiamo detto, contiene l'indirizzo della prossima istruzione da eseguire.
[00:33:11 - 00:33:28] Tipicamente le memorie, anche se hanno parole di 32-bit, quindi di 4-byte, quindi memorie più grandi di un byte, tipicamente però sono indirizzate sul singolo byte.
[00:33:29 - 00:33:43] E l'istruzione, il programcante indica l'indirizzo della memoria, come indirizzo, diciamo, non indica l'indirizzo della memoria, ma l'indirizzo di byte.
[00:33:43 - 00:33:54] Quindi, tipicamente, il programcante legge byte alla volta, legge solo i byte, diciamo, di tutta la parola, ok?
[00:33:54 - 00:34:01] Cioè, come dire, come indirizzo e indicizzata a byte la memoria, ok?
[00:34:01 - 00:34:10] Mentre il mar va molti di byte in base a quante è grande la parola, il programcante va di byte in byte.
[00:34:13 - 00:34:30] È proprio perché quando poi si va a leggere dalla memoria l'istruzione, l'istruzione che stiamo utilizzando, su cui stiamo ragionando, sono di, hanno la dimensione di un byte.
[00:34:31 - 00:34:36] Per questo Wolfgang Counter ha la granularità di un byte.
[00:34:36 - 00:34:54] L'MBR, che il registo doveva andare a finire l'istruzione da eseguire, lo vediamo visualizzato così, perché tipicamente lo si fa comunque, che ne so, a 32-bit, saranno questi quattro registri a 32-bit.
[00:34:54 - 00:35:15] Però, a noi l'istruzione abbiamo detto è di un byte, però non è che si va a leggere un byte, perché tanto la parola è 32-bit, i circuiti di lettura, diciamo, sono, leggono l'intera parola, è solo che quella di interesse è solo il primo byte, ok?
[00:35:15 - 00:35:24] Perciò è visualizzata così, l'MBR è il byte meno significativo della parola che si è letta dalla memoria.
[00:35:24 - 00:35:49] E i segnali di controllo li abbiamo detto sono queste frecette nere e bianche, che semplicemente vanno ad abilitare, con il solito discorso che abbiamo visto, delle porte di abilitazione, in modo che soltanto un registro possa scrivere sul bus lì,
[00:35:49 - 00:35:58] e le frecette nere vanno invece a abilitare uno o più registri, se questi devono leggere dal bus c.
[00:35:58 - 00:36:22] Quindi, ovviamente per effettuare delle operazioni di memoria abbiamo detto che, se per caso devo fare una scrittura, non abbiamo visto una scorsa volta, un esempio di temporizzazione di una lettura dalla memoria,
[00:36:22 - 00:36:41] se devo fare una scrittura, devo prima mettere il dato su MDR, poi devo mettere l'indirizzo sul MAR e successivamente inviare quei segnali di lettura alla memoria,
[00:36:41 - 00:36:51] quindi di memoria quest, il read, asseriti in maniera diretta o negata, in base a come sono fatti i circuiti.
[00:36:52 - 00:37:07] Allora, ricordiamo sempre MAR e MDR per leggere scrivere dati, PC ed MBR invece per prelevare istruzioni di livello ISA da eseguire.
[00:37:07 - 00:37:36] Sempre su questa differenza tra MAR e program counter, che sono entrambi registri che contengono indirizzi della memoria, abbiamo detto il MAR lavora sulle parole, quindi c'è punta alla prima parola,
[00:37:36 - 00:37:57] la seconda parola e così via. Quindi, se le parole abbiamo detto, facciamo un esempio che sono a 32 bit e le memorie però lavorano comunque su un indice di byte, quindi la prima parola della memoria
[00:37:57 - 00:38:18] sarà composta dai byte di indice 0 1 2 3, la seconda parola dai byte di indice 4 5 6 7. Preferimento alla parola 2, non vuol dire alla seconda parola, ma sarebbe la terza parola,
[00:38:18 - 00:38:39] perché sempre inteso parte da 0, quindi la terza parola è quella che va appunto dal byte 8 9 10 11. Ok? Quindi, se nel MAR c'è scritto 2, è inteso come indirizzo della seconda parola
[00:38:39 - 00:39:05] e cioè in MDR viene messo, mettiamo che stiamo facendo la lettura, in MDR finiranno i byte 8 11 della memoria. Nel caso del program counter invece il valore che ci troviamo, abbiamo detto far riferimento ai byte, quindi se trovo lo stesso valore 2 anche nel program counter, non è la seconda parola, ma è il secondo byte.
[00:39:06 - 00:39:25] Secondo byte vuol dire che dalla memoria voglio leggere, no il secondo byte, scusate il byte 2, cioè il terzo byte, devo leggere quindi il terzo byte che ha posizione e indice 2, perché 0 il primo, 1 il secondo, 2 il terzo.
[00:39:26 - 00:39:52] Leggo questo, questo andrà a finire nell'MBR, che però è di 8 bit a livello logico, lavoriamo solo sui primi 8 bit del registro, il registro ne ha 32, però lo si fa da 32, perché in altre operazioni può essere utile, è utilizzato all'MBR tutti i 32 bit
[00:39:53 - 00:40:10] e quindi diciamo perciò non lo si fa a 1 byte, lo si fa a 32 bit, poi logicamente, a livello logico intendo, quando si fa il prelievo delle istruzioni invece, si vanno a interpretare sui primi 8 bit, perché le istruzioni sono composte da 1 byte.
[00:40:11 - 00:40:37] Ovviamente nasce un problema di conversione tra dell'indirizzo tra MAR e PC o viceversa, nel senso che il problema è del MAR, il MAR lavora su indirizzi di parola, però abbiamo detto che la memoria invece effettivamente lavora su indirizzi di byte.
[00:40:38 - 00:40:48] E quindi se nel MAR c'è scritto un indirizzo di parola, io poi per capire quali byte devo andare a leggere dalla memoria, devo in qualche modo convertirlo.
[00:40:52 - 00:41:03] E questa conversione la si fa nel momento in cui si va a spostare il valore indicato dal MAR sul bassi indirizzi, il bassi indirizzi è quello che deve leggere la memoria.
[00:41:04 - 00:41:21] Ok, come se dicesse, nel processore, nel data path ho un valore, quando lo vedo devo comunicare alla memoria gli comunico un altro valore, un valore che la memoria può capire, la memoria può capire i valori indicizzati sui byte.
[00:41:22 - 00:41:47] E lo devo convertire, quindi abbiamo detto, sempre nell'esempio che ho una parola di 4 byte, se nel MAR ho scritto 2 abbiamo detto, sto puntando il byte 8, quindi devo passare, devo convertire questo valore 2 nel MAR in un valore 8 che devo andare a mettere nel bassi indirizzi.
[00:41:48 - 00:41:57] Se invece nel MAR c'è 3, terza parola comincerà al byte 12, ok?
[00:41:58 - 00:42:18] Quindi quello che devo fare mi serve in qualcosa, un circuito o un'operazione, qualcosa che mi va a moltiplicare per 4 il valore memorizzato nel MAR.
[00:42:19 - 00:42:26] In questo passaggio dal MAR al bassi indirizzi devo moltiplicare per 4 il valore del MAR.
[00:42:26 - 00:42:54] Questa cosa non la si fa con un circuito apposito, ma la si fa sfruttando, il fatto che la moltiplicazione per 4 in binario coincide con lo shift a sinistra di un bit se si vuole fare per 2, di due bit se si vuole fare per 4.
[00:42:56 - 00:43:09] Ok, quindi 1 in binario se lo shift di due bit a sinistra diventa 1, 0, 0 che vuol dire 4 e questo vale in generale.
[00:43:09 - 00:43:17] Quindi quando si fa uno shift a sinistra si fa una moltiplicazione per 2, quando si fa uno shift a destra si fa una divisione per 2.
[00:43:17 - 00:43:27] A me serve fare in questo caso una moltiplicazione per 4, quindi devo fare uno shift a sinistra.
[00:43:27 - 00:43:41] Questa cosa la si fa non mettendo uno shift, ma semplicemente collegando il MAR al bassi indirizzi in maniera shiftata.
[00:43:42 - 00:43:48] Quindi sopra abbiamo il MAR, vedete?
[00:43:48 - 00:44:06] Il collegamento tra le linee del registro MAR al bassi indirizzi avviene shiftando il bit di due, proprio collegandoli shiftati di due e ponendo a 0 i primi due, quelli meno significativi.
[00:44:12 - 00:44:15] È chiaro?
[00:44:23 - 00:44:27] Grazie, dubbi su queste cose che stiamo volendo oggi, domande?
[00:44:31 - 00:44:33] No, però ok.
[00:44:33 - 00:44:53] Va bene, allora se non ci sono domande o osservazioni ho terminato, qui c'è riferimento al agrofo del libro che affronta questi argomenti, se le volete approfondire o rivedere.
[00:44:53 - 00:45:01] E allora vi saluto, vi auguro buon pranzo, buona giornata e alla prossima.
[00:45:01 - 00:45:05] Grazie, alla prossima.
