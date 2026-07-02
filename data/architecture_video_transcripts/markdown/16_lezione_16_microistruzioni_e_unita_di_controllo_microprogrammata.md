# Lezione 16 - Microistruzioni e Unità di controllo microprogrammata

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\Lezione 16 - Microistruzioni e Unità di controllo microprogrammata.mp4`
- Durata: 00:54:06
- Trascrizione: `16_lezione_16_microistruzioni_e_unita_di_controllo_microprogrammata.json`

## Argomenti probabili
- porte_logiche (202): and, or, not, nor, nand
- microarchitettura (159): microarchitettura, microistruzione, mic, datapath, alu, controllo
- memoria_bus (92): memoria, bus, indirizzo, temporizzazione, ram, rom
- mips_assembly (71): registro, registri, sb
- registri_flip_flop (66): registro, registri

## Trascrizione

[00:00:00 - 00:00:02] Sottotitoli a cura di QTSS.
[00:00:30 - 00:00:32] Sottotitoli a cura di QTSS.
[00:01:00 - 00:01:02] Sottotitoli a cura di QTSS.
[00:01:30 - 00:01:32] Buongiorno, mi sentite?
[00:02:00 - 00:02:02] Buongiorno.
[00:02:30 - 00:02:53] Allora, in questa lezione continuiamo a vedere una microarchitettura che stanno vedendo, da Atapath che abbiamo introdotto nella scorsa lezione.
[00:02:53 - 00:03:04] Abbiamo detto una microarchitettura pensata per implementare l'estruzione di livello ISA, quindi livello superiore di nostro interesse.
[00:03:04 - 00:03:22] Abbiamo detto ci concentriamo su un ristretto set della Java Virtual Machine che è composto da un insieme di istruzioni ISA che operano sui interi.
[00:03:23 - 00:03:33] Abbiamo letto che il livello della microarchitettura si progetta e si implementa allo scopo di implementare le istruzioni di livello ISA definite.
[00:03:34 - 00:03:44] Questa è la microarchitettura o meglio, il datapath che abbiamo visto la volta scorsa.
[00:03:44 - 00:03:51] Adesso andiamo a esploderlo, aggiungere elementi che non abbiamo ancora parlato.
[00:03:51 - 00:04:09] Abbiamo detto in questa microarchitettura stiamo ragionando sul fatto che le istruzioni di livello ISA che dobbiamo supportare non sono implementate a livello hardware direttamente.
[00:04:09 - 00:04:35] Non abbiamo un circuito dedicato ad ogni istruzione, ma abbiamo invece un circuito, un microprogramma che risiede imunarom, in grado di elaborare e, o meglio, interpretare le istruzioni di livello ISA per decomporre in microistruzioni
[00:04:36 - 00:04:44] da andare a eseguire queste, sì, a livello hardware per realizzare, appunto, queste istruzioni di livello ISA.
[00:04:44 - 00:05:12] Quindi stiamo immaginando il fatto che ogni istruzione prelevata dalla memoria, diciamo, di istruzione di livello ISA che deve essere eseguita dalla nostra architettura, in qualche modo viene interpretata come se fosse un programma, un linguaggio, un programma di esecuzione che circuitamente va ad interpretare le istruzioni e capire le operazioni di effettuare, le microoperazioni di effettuare.
[00:05:13 - 00:05:15] E li va a andare a eseguire.
[00:05:18 - 00:05:28] Quindi, la volta che abbiamo trovato le microistruzioni, queste microstruzioni poi si vanno a realizzare, a implementare in effetti le operazioni sull'hardware.
[00:05:28 - 00:05:43] Cioè, nello suo specifico vanno a impattare il data, vanno a regolare quali registri devono essere utilizzati, quali dati devono essere spostati dai registri all'alua o dall'alua viceversa dei registri.
[00:05:44 - 00:05:56] Quindi, sono le singole microestruzioni che vengono effettivamente eseguite, microestruzioni che insieme, nel loro insieme, vanno a realizzare una particolare istruzione ISA.
[00:05:57 - 00:06:23] Per fare ciò abbiamo un micro programma, un micro sequenziatore, un programma diciamo scritto in hardware in questa ROM che va sempre effettuare cilicamente le 3 operazioni fondamentali che abbiamo detto sono il fetch, cioè il recupero dell'estruzione dalla memoria, la interpretazione, il decode.
[00:06:24 - 00:06:46] Poi, a seconda della particolare istruzione che si deve andare a eseguire, se necessario bisogna recuperare degli operandi, una volta che tutto è pronto si procede all'eseguzione dell'istruzione e quindi si ricomincia in questo cibo.
[00:06:47 - 00:07:04] Queste microestruzioni che vanno a implementare le istruzioni del livello ISA devono essere in grado di comandare il datapad, comandare il datapad vuol dire agire sui segnali di controllo del datapad.
[00:07:04 - 00:07:15] Abbiamo visto questa figura l'autorscorsa, abbiamo detto che in questa architettura che stiamo immaginando, che stiamo descrivendo, abbiamo due basse fondamentali.
[00:07:16 - 00:07:38] Uno è il bus B che alimenta uno degli input dell'ALU e su questo bus B possono scrivere alcuni registri e poi abbiamo l'altro bus, bus C, su cui invece va a finire, diciamo l'output dell'ALU eventualmente sciftato.
[00:07:39 - 00:07:45] I dati che arrivano su bus C possono essere poi letti da uno o più registri.
[00:07:52 - 00:08:04] Quali sono i registri che sono autorizzati a leggere dal bus C? Qual è l'unico registro che è autorizzato a scrivere bus B?
[00:08:04 - 00:08:25] Vengono configurati da questi segnali di controllo, queste frecette indicate in figura, dove abbiamo le frecette bianche indicano delle linee di abilitazione del registro a scrivere sul bus B.
[00:08:25 - 00:08:32] Le frecette nere invece indicano delle linee di abilitazione dei registri a leggere dal bus C.
[00:08:33 - 00:08:39] Altri segnali di controllo abbiamo detto ci sono per l'ALU e per lo shifter, sono 8.
[00:08:40 - 00:08:55] E quindi diciamo tutte queste configurazioni di queste linee di controllo che vanno a definire quale registro deve scrivere, quali registri devono leggere, che operazione deve effettuare l'ALU,
[00:08:55 - 00:09:07] se deve essere o meno sciftato il risultato dell'ALU, così via, devono, dipendono diciamo dalla particolare microestruzione che dobbiamo andare a eseguire.
[00:09:07 - 00:09:13] Quindi è un'informazione che deve essere codificata nella microestruzione stessa.
[00:09:15 - 00:09:25] Quindi andiamo adesso a vedere come può essere una struttura, come può essere organizzata una microestruzione.
[00:09:26 - 00:09:36] Per questa particolare microarchitettura che stiamo descrivendo ogni microestruzione richiede 36 bit in totale.
[00:09:39 - 00:09:44] Vediamo che informazioni ci sono, che informazioni sono codificate in questi 36 bit.
[00:09:44 - 00:10:09] Allora abbiamo detto, i segnali di controllo, perdonatevi, i segnali di controllo per abilitare i registri sono 9, per il bus C, 9 per il bus B.
[00:10:10 - 00:10:19] E siamo a 18, diciamo, bit che servirebbero, che dobbiamo andare a configurare.
[00:10:20 - 00:10:26] Poi l'ALU e l'USCIFTER sono 6 e 2 a 8, quindi altri 8 segnali servono.
[00:10:27 - 00:10:40] Poi da qui non sono evidenziati, ma occorrono due segnali per indicare alla memoria di leggere o scrivere attraverso il MARL MDR.
[00:10:41 - 00:10:52] I segnali che abbiamo visto quando abbiamo soddiato, diciamo, la lettura e la temporizzazione della lettura di un dato dalla memoria.
[00:10:53 - 00:11:01] E poi un segnale per indicare il prelievo dalla memoria attraverso invece il PROGUN COUNTER LMDR.
[00:11:02 - 00:11:12] Ricordo che MARL MDR, diciamo, è la coppia di registri come morti nel prelievo o nella scrittura di un dato dalla memoria,
[00:11:13 - 00:11:21] mentre il PROGUN COUNTER LMDR sono la coppia di registri come morti nel prelievo di un'istruzione dalla memoria.
[00:11:21 - 00:11:43] Siamo quindi arrivati a 9.9.18.8.26.29 segnali che, diciamo, devo configurare per poter utilizzare il dato,
[00:11:44 - 00:11:51] per decidere quale registro scrive in B, cosa deve fare l'ALU e quali registri leggono da C.
[00:11:51 - 00:12:07] Abbiamo detto che più registri possono leggere da C, ok, ma soltanto registro può scrivere in D.
[00:12:07 - 00:12:17] Questa cosa può essere utilizzata per ridurre, diciamo, i numeri segnali necessari.
[00:12:20 - 00:12:31] Perché? Perché ci sono solo 9 possibili registri che possono guidare il busbG, che possono scrivere sul busbG.
[00:12:32 - 00:12:41] Questa informazione invece di prevedere dentro l'istruzione, vogliamo arrivare a capire quanti bit ci servono nella microistruzione
[00:12:42 - 00:12:58] per codificare chi deve scrivere nel busbG. Quindi alcuni bit della microistruzione li devo destinare, riservare, per codificare questa informazione.
[00:12:58 - 00:13:13] Ora, io potrei semplicemente fare 9 bit per un bit per ogni registro con valore 01 e quindi occupare 9 bit nella microistruzione, il formato della microistruzione.
[00:13:14 - 00:13:34] Però per risparmiare questa parte la posso andare a codificare, invece di esprimerla direttamente con 9 bit posso usare 4 bit in cui vado a codificare un numero e ad ogni numero associo uno dei 9 possibili valori.
[00:13:34 - 00:13:49] Ovviamente per rappresentare 9 possibili valori 3 bit non mi bastano ma ne servono 4. Avrei ulteriori 7 valori ancora che potrei codificare però non li utilizzo nello specifico.
[00:13:49 - 00:14:18] Ora, oltre a questi bit per configurare i segnali di controllo dobbiamo mettere ulteriori informazioni, perché nel formato della microistruzione oltre a scrivere cosa deve fare questa microistruzione,
[00:14:19 - 00:14:38] cosa deve fare, abbiamo detto, lo si evince, lo si determina dalla configurazione di questi segnali di controllo, ulteriori informazioni che sono presenti saranno il campo della prossima microistruzione.
[00:14:39 - 00:14:54] Ok, quindi mentre l'instruzione di livello ISA, l'indirizzo della prossima istruzione di livello ISA da eseguire, io lo memorizzo nel Pro-Can-Counter e non nelle istruzioni stesse.
[00:14:55 - 00:15:06] Nelle microistruzioni invece stesso nella microistruzione ci scrivo anche quale è l'indirizzo della prossima microistruzione da eseguire.
[00:15:07 - 00:15:26] Questo lo posso fare perché tanto queste sono diciamo microprogrammi noti definiti quando viene progettata la macchina e quindi ad ogni microestruzione che compone diciamo un certo microprogramma e il microprogramma implementa una certa istruzione ISA,
[00:15:26 - 00:15:38] io lego tra di loro le microestruzioni della stessa istruzione ISA aggiungendoci il puntatore alla prossima microestruzione da eseguire.
[00:15:39 - 00:16:03] In più però lascio la possibilità di effettuare un sasto, diciamo, un momento di decisione tramite un ulteriore bit, che siano questi indicati con GEM, che sta in giangere di GEM, proprio per dire io ti metto l'indirizzo della prossima microestruzione,
[00:16:03 - 00:16:18] ma nel caso in cui GEM assuma certi valori posso cambiare questo next address in modo da saltare a un'altra microestruzione invece di quella codificata nelle istruzioni stesse.
[00:16:19 - 00:16:36] Quindi arriviamo a 36 bit, perché? Perché abbiamo che questo next address, diciamo, questo diciamo è formato di tutta la microestruzione a 36 bit,
[00:16:37 - 00:16:50] e abbiamo i primi 9 bit, quelli più significativi, sono l'indirizzo della prossima microestruzione che deve essere eseguita, se non ci sono salti, ok?
[00:16:51 - 00:17:06] Poi abbiamo 3 bit, questi GEM, che sono 3 bit, che possono determinare un salto a una microestruzione diversa, nel caso si veniscano certe situazioni,
[00:17:07 - 00:17:28] e poi abbiamo i bit di controllo che abbiamo visto prima, quindi gli 8 bit dell'aluplo shifter, i 9 bit che vanno a specificare i registri che possono leggere dal BASC
[00:17:29 - 00:17:46] e i 3 bit, questi GEM sono quelli che identificano l'operazione della memoria, non l'abbiamo detto prima, non erano indicati nella figura, ma ci sono, sono i classici scrivi, leggi o fetch recupera istruzione,
[00:17:46 - 00:18:00] vanno a determinare se l'operazione di lettura, se bisogna fare, diciamo, l'operazione di lettura o scrittura dalla memoria, o di fetch, che vi ricorda invece il prelievo dell'istruzione, secondo l'indirizzo del program count.
[00:18:01 - 00:18:28] Poi abbiamo i 4 bit che vi accendiamo prima, che codificano quale registro può scrivere sul BASC B, capiamo perché, come dire, si è potuto fare questo risparmio di bit da 9,
[00:18:28 - 00:18:47] che sono i registri che possono scrivere sul BASC B a 4, abbiamo detto perché io posso risparmiare, utilizzando una codifica diretta, come per esempio nel determinare quali registri possono scrivere da cibi,
[00:18:48 - 00:19:13] sono 9 bit dedicati, un bit per ogni registro, il registro H, il registro TOS, così via, no? Perché invece chi deve scrivere sul BASC B si è fatta questa restrezione, o mai si è fatto questo risparmio? Ho detto in altri termini, e perché questo risparmio non si fa anche sui registri che devono leggere dal BASC?
[00:19:14 - 00:19:38] Questa cosa dipende dal fatto che sul BASC B può scrivere soltanto un registro alla volta, quindi io devo identificare solo un valore, non posso, diciamo, abilitare più registri e quindi semplicemente faccio una codifica in cui ad ogni valore codificato,
[00:19:38 - 00:19:45] negli primi 4 bit meno significativi ad ogni valore codificato assucio un singolo registro.
[00:19:46 - 00:20:08] Invece chi può leggere dal BASC questa cosa non si può fare? Perché io voglio poter abilitare o un singolo registro e gli altri lascio a 0, oppure quel registro insieme ad altri?
[00:20:08 - 00:20:35] Quindi un registro non posso associare un unico valore ad un registro, ma un singolo registro può essere coinvolto in più valori, può andare a leggere da solo o insieme ad altri registri, quindi per avere il potere espessivo di poter dire uno più registri possono leggere dal BASC sono costetto a dedicare un bit ad ogni registro.
[00:20:38 - 00:21:07] E quindi i 29 bit di controllo scendono a 24, sono smaglio, più i 3 bit di gem e i 9 bit del next address arriviamo ai 36 bit minimi necessari per, diciamo, il formato della micro istruzione di questa architettura.
[00:21:08 - 00:21:29] Quando a livello ardo, diciamo, viene selezionata una micro istruzione vedendo ogni bit di questa stringa di 36 bit, si configura il data path e possono avvenire l'operazione.
[00:21:29 - 00:21:54] Poi, come abbiamo accennato, abbiamo visto anche la volta scorsa, i dati fluiscono attraverso il data, fatta seguendo la sincronizzazione del clock e, in particolare, seguendo, diciamo, i sottocicli all'interno del clock.
[00:21:54 - 00:22:13] Quindi, in una parte iniziale, dopo il fronte di discesa del clock, come vediamo, questa cosa viene ripetuta nelle prossime slide, diciamo, al fronte di discesa del clock partono le operazioni di esecuzione di una singola micro istruzione.
[00:22:13 - 00:22:25] E allora, nella parte iniziale, vengono abilitati il registro scrivere sul bus B. Poi, dopo un certo intervallo, il dato aggiunge all'ALU.
[00:22:25 - 00:22:54] Dopo un certo intervallo, l'ALU effette le operazioni, dopo un certo intervallo di tempo ulteriore, l'output dell'ALU aggiunge al bus C, finché, diciamo, tutto questo deve essere garantito che deve essere fatto in tempo, prima che avviene il fronte di salita del clock, perché al fronte di salita del clock i registri leggono dal bus C e quindi si può ricominciare,
[00:22:54 - 00:22:59] all'esecuzione di una nuova micro istruzione con il prossimo fronte di discesa.
[00:22:59 - 00:23:28] E questo microprogramma, che qua è indicato conseguenze all'alizzatore, diciamo, abbiamo detto è in una ROM e ha il compito di far avanzare, diciamo, passo passo queste operazioni, che sono le microoperazioni necessarie per eseguire la singola istruzione ISA.
[00:23:29 - 00:23:51] Ok, quindi ad ogni cilio di questo microprogramma bisogna, al giornale postato dei segnali di controllo, recuperare, diciamo, la microistruzione da eseguire e eseguirla.
[00:23:51 - 00:24:20] Aggiungendo ulteriori dettagli alla nostra microarchitettura, che qui abbiamo indicato con mic 1, abbiamo che non solo, quindi abbiamo il datapad che è l'insieme dei registri coinvolti in questo ciclo di eseguzione, diciamo, a livello ISA, dell'istruzione a livello ISA, ma poi abbiamo una memoria di controllo che contiene una ROM.
[00:24:21 - 00:24:36] Quindi abbiamo, diciamo, che contiene il microprogramma da eseguire, cioè le microestruzioni che vanno a implementare l'istruzione di livello ISA.
[00:24:37 - 00:24:58] Qui sulla destra abbiamo il formato, diciamo, dalla microistruzione che abbiamo visto prima, dunque abbiamo, vedete, indirizzo della prossima istruzione, la parte jump, poi gli otto bit che determina il comportamento dell'ALU e dello shifter,
[00:24:59 - 00:25:21] abbiamo poi bit che comandano i registri che possono leggere da BUS C e poi abbiamo i quattro bit che codificano, prima c'è la parte M che determina cosa può essere fatto in memoria, quindi se una lettura, se una scrittura o se un fetch,
[00:25:21 - 00:25:35] poi abbiamo l'ultima parte, quindi c'è la B, la parte meno significativa, che è quella che va a codificare chi può leggere nel BUS B.
[00:25:36 - 00:25:52] Ovviamente, formazione codificata, vedete, mentre i bit della parte C della microestruzione sono collegati direttamente ai segnali, cioè sono essi stessi dei segnali che vanno ad abitare i registri che possono leggere,
[00:25:53 - 00:26:09] la parte del BUS B invece deve essere decodificata, perché abbiamo quattro bit che devono essere trasformati in un'informazione sul nove bit, poi abbiamo quei set bit in più che non ci servono, non li utilizziamo,
[00:26:10 - 00:26:28] colleghiamo solo i primi nove bit che vanno ad alimentare, che vanno ad abilitare i registri che possono scrivere sul BUS B, quando in base al valore che è memorizzato nella parte B della microestruzione,
[00:26:29 - 00:26:46] abbiamo che questo essere un decodificatore, soltanto una linea di output sarà abilitata, le astri saranno a zero, e quella, diciamo, il registro collegato su quella linea sarà quello autorizzato a scrivere sul BUS B.
[00:26:47 - 00:27:09] La parte di jump invece, che sono quelli tre bit, vedete, sono collegati all'output di n e z dell'alu, che sono dei bit che vengono impostati in base a risultato, diciamo, dell'operazione effettuata dall'alu,
[00:27:09 - 00:27:38] che indicano se il risultato dell'alu è negativo o è zero. In base, diciamo, al valore di jump, vedete, va a controllare questo circuito che non fa stro che riproporre, diciamo, o meno, il valore di n,
[00:27:39 - 00:28:02] e z qui in modo che vada ad alterare la prossima istruzione, la prossima microestruzione, scusatevi, quindi la prossima microestruzione normalmente sarà a DR, cioè quella indicata nella istruzione della microestruzione corrente, abbiamo l'indirizzo della prossima microestruzione.
[00:28:02 - 00:28:18] Questo è un indirizzo della prossima microestruzione, quindi non punta alla memoria, ma punta alla memoria ROM che contiene le microestruzioni possibili, infatti, vedete, punta alla memoria stessa.
[00:28:19 - 00:28:44] Questo indirizzo della prossima microestruzione può essere alterato, in genere, solo il bit più significativo di questo indirizzo, quando n o z hanno determinati valori e quando il valore di j della microestruzione determina questo salto.
[00:28:44 - 00:29:12] Quindi vedete, questo è tutto a livello hardware, tutto collegato con fili che vanno ad abilitare i registri opportuni, con il circuito dei codificatori, la lua e così di allo shifter, tutti i circuiti che abbiamo visto durante il corso, quindi stiamo mettendo insieme per realizzare questa microarchitettura.
[00:29:15 - 00:29:27] Che, ripeto, è sempre in qualche modo progettata e implementata pensando alle istruzioni lisa da dover supportare, da dover implementare.
[00:29:27 - 00:29:52] Questa memoria, riportata nell'esempio, contiene 512 parole di 36 bit, ovviamente se il formato della microestruzione è 36 bit, la dimensione della parola di questa memoria di controllo è 36 bit anch'essa.
[00:29:52 - 00:30:08] Questo è un limite, ovviamente ci sono 512 parole, quindi insieme ai programmi che possiamo memorizzare, non può superare le 512 microestruzioni.
[00:30:08 - 00:30:37] L'ho accennato già prima la gestione delle microestruzioni, dei microprogrammi in questa memoria roma, diferece da come vengono gestiti i microprogrammi e le istruzioni di livello isa.
[00:30:38 - 00:31:07] Perché nei programmi classici, le istruzioni isa tipicamente sono memorizzate in maniera consecutive e poi abbiamo il program counter che non fa altro che incrementarsi in modo da puntare sempre alla prossima istruzione che incende spesso.
[00:31:08 - 00:31:37] In questi microprogrammi, invece, richiedono maggiore flessibilità, perché devono essere, diciamo, i più brevi possibili, le sequenze, e quindi abbiamo detto ogni microestruzione indica esplicitamente dove si trova la successiva, che però può trovarsi in qualunque, diciamo, zona della memoria di controllo.
[00:31:39 - 00:31:42] E proprio per questo si porta presso l'indirizzo.
[00:31:42 - 00:32:04] Anche qua, a livello di microprogramma, abbiamo una sorta di micro program counter, che è quello che abbiamo indicato qui con MPC.
[00:32:04 - 00:32:28] Quindi, noi abbiamo questi 9-bit che indicano l'indirizzo della prossima istruzione, abbiamo detto è alimentato dalla DR e quindi MPC tipicamente assume il valore indicato dai 9-bit più significativi della microestruzione corrente, a meno che non venga alterato dalla parte jump.
[00:32:29 - 00:32:46] Abbiamo dei registri anche nella microestructure register, dove viene memorizzata la microestruzione corrente, che questo qui è esplicitato, il miso, vedete?
[00:32:46 - 00:33:15] E quindi, diciamo, c'è una distinzione tra i registri, diciamo, di livello ISA, sono quelli che tipicamente vengono visti da chi scrive l'estruzione di livello ISA, mentre la microarchitettura, queste microestruzioni che invece sono un'implementazione delle istruzioni di livello ISA,
[00:33:16 - 00:33:33] ovviamente non sono visibili, cioè non è chi al programmatore di usare l'estruzione di livello ISA, no, opera su questi micro registri, questi micro registri sono soltanto di visibilità e utilizzo del livello di microarchitettura.
[00:33:33 - 00:33:51] Allora, abbiamo detto, come abbiamo visto, i segnali di registromir vanno ad alimentare la nostra architettura di controllo.
[00:33:52 - 00:34:15] Abbiamo detto, quindi, il next address va ad alimentare l'MPC, gem invece va ad abilitare o meno l'utilizzo del bit di N, Z o compare, diciamo, del...
[00:34:16 - 00:34:44] No, questo è l'MPC, che altra quindi il valore del micro approach and counter, gli 8 bit dell'alu collegati ai segnali di controllo dell'alu e dello shift, questi sono i 9 bit che vanno ad abilitare i corrispondenti registri che possono leggere dal Bass C,
[00:34:44 - 00:34:58] questi sono i 3 bit che determinano la tipologia di operazione d'effettuare verso la memoria o dalla memoria e poi 4 bit che codificano come o meglio quale registro può scrivere sul Bass B.
[00:34:59 - 00:35:20] Allora, l'Occernato prima è il fatto che queste le secuzioni, diciamo, di ogni istruzione segue la sincronizzazione del clock e si parla di sottocigli del data,
[00:35:20 - 00:35:37] parte che sono sottocigli, cioè sottointervalli rispetto al clock e in questa rappresentazione sono tutte le operazioni che vedete partono dal fronte di discesa del clock e devono terminare entro il fronte di salita.
[00:35:38 - 00:36:01] Questo perché? Perché ovviamente al fronte di salita ci sarà la lettura dei registri dei valori del Bass C e quindi il dato deve essere venuto sul Bass C ed essere stabile in tempo affinché possa essere letto.
[00:36:02 - 00:36:21] Il dato che deve essere che sarà scritto sul Bass C comincia a formarsi sul fronte di discesa del clock quando i segnali presenti nell'amico istruzione, quindi nel registro Mir, vengono utilizzati per impostare i datapads.
[00:36:22 - 00:36:46] Quindi si vanno a impostare tutte le cose che abbiamo detto prima, l'abilitazione del registro che deve scrivere subì, l'abilitazione dei registri che dovranno leggere, dopo, non subito, l'impostazione dell'ALU, dello shifter e così via.
[00:36:47 - 00:37:11] In particolare abbiamo che il primo sottointerval, cioè il primo sottociclo del datapad si chiama Delta V, abbiamo che i segnali diciamo di controllo si propagano, cioè arrivano ai registri, ai circuiti e determinano il loro comportamento.
[00:37:11 - 00:37:35] Quando poi si verifica il secondo ciclo, che è questo Delta X, il secondo sottociclo del datapad, i segnali ormai sono impostati, quindi cominciano a fluire i dati, quali dati?
[00:37:35 - 00:38:00] Il registro abilitato a scrivere subì, il dato dal registro giunge sub basb, e in questo stesso momento un'eventuale abilitazione del registro H determina che il valore diciamo...
[00:38:05 - 00:38:33] ...del basc viene inserito in H. Successivamente l'ALU è pronta, quindi nel intervallo del sottociclo Delta Y, all'inizio di Delta Y, diciamo, i dati sul basb ed eventualmente sul registro H sono pronti per essere utilizzati.
[00:38:35 - 00:38:47] Durante l'intervallo Delta Y, l'ALU e lo shifter effettano le loro operazioni così come sono state configurate dei segnali della microestruzione in esame.
[00:38:48 - 00:39:02] E al termine di Delta Y, il dato, cioè la microarchivatura è progettata in modo che l'autobot dello shifter è stabile e può essere utilizzato.
[00:39:03 - 00:39:17] Viene utilizzato nel sottociclo Delta Z dove i valori, diciamo, raggiungono il basc e diventano stabili.
[00:39:17 - 00:39:46] Questa cosa di stabilizzare i valori prodotti dallo shifter sul basc deve avvenire entro il fronte di salita del clock, perché al fronte di salita del clock, diciamo, in base ai segnali impostati prima, i registri abilitati a leggere dal basc leggeranno.
[00:39:48 - 00:39:53] E quindi si chiude, diciamo, il ciclo del Delta PATH.
[00:39:53 - 00:40:22] Abbiamo detto che durante Delta Y è l'ALU che effetto le operazioni ed è in questo sottociclon del Delta PATH che vengono impostati anche i valori di n e di z, che sono singoli bit in autobot dell'ALU che segnalano il sottociclo.
[00:40:23 - 00:40:30] La negatività o il valore zero, diciamo, del risultato prodotto dall'ALU.
[00:40:30 - 00:40:59] Nel quarto ciclo abbiamo detto che il risultato dell'ALU si propaga ai bus e il risultato, diciamo, dei bit di valori n e z si propagano ai flip-flop n e z, che stanno qui.
[00:41:00 - 00:41:27] Vedete, questi valori di n e z vengono memorizzati in questi due flip-flop n, che sono i flip-flop n e poi vengono, diciamo, abilitati che confluiscono, diciamo, in questo bit alto, che in base al valore di j,
[00:41:27 - 00:41:34] può generare che viene posto a 1 il bit più significativo dell'MFPC.
[00:41:34 - 00:42:03] Allora, il valore di jam, che questo registro da tre bit, abbiamo detto che permette di alsterare il valore di negro progancante dell'MFPC.
[00:42:03 - 00:42:23] Allora, se jam vale 0000, quindi abbiamo uno zero in ogni uno dei tre bit che compongono jam, semplicemente non viene alterato l'MFPC, che è semplicemente quello indicato dal next address.
[00:42:23 - 00:42:45] Se invece uno dei tre bit jam vale 1, bisogna allora calcolare, verificare se il valore next address memorizzato in MFPC deve essere alterato.
[00:42:46 - 00:43:03] Allora, se jam n e jam z sono pari a 1, questi cosa fanno?
[00:43:04 - 00:43:18] Semplicemente abilitano l'utilizzo dei flip-flop corrispondenti n e z per impostare il valore più significativo di MFPC.
[00:43:19 - 00:43:34] Quindi basta che uno dei due è alto o se lo sono entrambi, e allora il bit più significativo dell'MFPC viene posto a 1, perché sono collegati così semplicemente, vedete?
[00:43:35 - 00:43:50] Questo bit tasto, cioè questo è l'unico segnale che in genere vale 0, ma se jam z o jam n vale 1, passa il valore nel flip-flop.
[00:43:50 - 00:44:00] Passa il valore nel flip-flop, vuol dire che se n o z valgono 1, viene portato questo 1, vedete, al bit più significativo di MFPC.
[00:44:00 - 00:44:29] Quindi alla fine viene implementata una funzione da questa circuiteria così che dice semplicemente che il bit più significativo di MFPC è pari o al bit più significativo di MFPC.
[00:44:30 - 00:44:48] All'ambito il bit più significativo di next address oppure a 1 se jam n e n valgono 1 oppure se jam z vale 1 e z vale 1.
[00:44:48 - 00:45:01] Quindi come al solito essendo una OR, basta che uno di questi valori è alto e il valore più significativo dell'MFPC vale 1.
[00:45:02 - 00:45:19] Quindi alla fine l'MFPC può assumere solo due valori possibili, cioè il next address così come o il next address alterato nel bit più significativo, posto a 1.
[00:45:20 - 00:45:32] Quindi la prossima microstruzione o il next address o il next address alterato nel bit più significativo di MFPC.
[00:45:33 - 00:45:43] Perché mettiamo questi flip-flop? Perché memorizzano, diciamo, i valori di n z.
[00:45:44 - 00:46:03] Questo è perché per come abbiamo temporizzato le operazioni secondo il clock, dopo il fronte di salita del clock, diciamo, il bus B non viene più alimentato.
[00:46:04 - 00:46:14] Non è più necessario, diciamo, perché già è stato utilizzato il valore che c'era nel bus B.
[00:46:14 - 00:46:28] E quindi, diciamo, il valore ingresso al lalo può essere alterato, può differire da quello precedente nel momento in cui non viene più alimentato.
[00:46:28 - 00:46:53] Quindi i valori di n z in attuta al lalo potrebbero cambiare e quindi memorizzando i valori ottenuti dei flip-flop n e z è possibile, appunto, renderli stabili in modo da poter utilizzare per calcolare il valore di MFPC.
[00:46:53 - 00:46:59] Questo, diciamo, indipendentemente da quello che sta facendo lalo nel frattempo.
[00:47:02 - 00:47:06] Allora, vediamo un esempio.
[00:47:06 - 00:47:19] Abbiamo che la microestruzione che stiamo seguendo in questo momento, quindi quella che abbiamo nel registro mir, si trova all'indirizzo della memoria di controllo 0.75.
[00:47:19 - 00:47:27] E ha come next address 0.92, vedete? 0.92 nei 9 bit più significativi.
[00:47:27 - 00:47:34] Jam vale 0.01, quindi jam z è impostata a 1.
[00:47:38 - 00:47:47] Questo vuol dire che l'indirizzo della prossima istruzione o sarà 0.92 o sarà 192.
[00:47:47 - 00:48:03] Quindi sono due possibili, le microestruzioni dove s'alterà, diciamo, il microprogramma e quale delle due verrà effettivamente scelta come prossima microestruzione dipende dal valore di z,
[00:48:03 - 00:48:09] che ovviamente è impostato dall'isecuzione dell'istruzione 0.75.
[00:48:09 - 00:48:25] Quindi in base a quello che viene durante questa esecuzione lalo produrrà uno z che vale 0.01, se z vale 0 si salterà a 0.92, se invece vale 1 si salterà a 0.192.
[00:48:25 - 00:48:44] Sono rappresentati in essa decimale per semplificare, ovviamente dovete raggiungare, sui 9 bit alterando il bit più significativo si passa da 92 a 192.
[00:48:44 - 00:49:13] C'è anche jump mpc e quando viene abilitato permette di usare gli 8 bit dell'MBR combinati con gli 8 bit di mpc.
[00:49:14 - 00:49:39] Questa è una cosa che può essere utilizzata per memorizzare codici operativi che stanno nelle MBR e quindi il valore che stanno nelle MBR è levata a stirare l'MPC.
[00:49:40 - 00:49:46] E' basso con questo ho concluso.
[00:49:46 - 00:49:53] Sono domande?
[00:49:53 - 00:49:57] Dubbi?
[00:49:57 - 00:50:15] Ok allora se non avete domande io vi saluto e ci vediamo dopo più tardi per la prossima lezione.
[00:50:15 - 00:50:25] Grazie.
[00:50:25 - 00:50:26] Grazie.
[00:50:45 - 00:50:48] Buon appetito.
[00:51:15 - 00:51:18] Buon appetito.
[00:51:45 - 00:51:48] Buon appetito.
[00:52:15 - 00:52:18] Buon appetito.
[00:52:45 - 00:52:48] Buon appetito.
[00:53:15 - 00:53:18] Buon appetito.
[00:53:45 - 00:53:48] Buon appetito.
