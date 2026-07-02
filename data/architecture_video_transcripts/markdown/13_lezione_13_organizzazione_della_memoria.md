# Lezione 13 - Organizzazione della memoria

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\Lezione 13 - Organizzazione della memoria.mp4`
- Durata: 02:03:24
- Trascrizione: `13_lezione_13_organizzazione_della_memoria.json`

## Argomenti probabili
- porte_logiche (411): and, or, nor, nand, sop
- memoria_bus (66): memoria, cache, indirizzo, ram
- registri_flip_flop (27): flip flop, registro, registri, propagazione
- clock_prestazioni (14): clock, tempo
- mips_assembly (11): registro, registri, sb

## Trascrizione

[00:00:30 - 00:00:32] Sottotitoli a cura di QTSS.
[00:01:00 - 00:01:02] Sottotitoli a cura di QTSS.
[00:01:30 - 00:01:32] Sottotitoli a cura di QTSS.
[00:02:00 - 00:02:02] Sottotitoli a cura di QTSS.
[00:02:30 - 00:02:32] Sottotitoli a cura di QTSS.
[00:03:00 - 00:03:02] Sottotitoli a cura di QTSS.
[00:03:30 - 00:03:32] Sottotitoli a cura di QTSS.
[00:04:00 - 00:04:02] Sottotitoli a cura di QTSS.
[00:04:30 - 00:04:32] Sottotitoli a cura di QTSS.
[00:05:00 - 00:05:18] Allora, continuiamo a vedere il livello della logica digitale, quindi stiamo vedendo circuiti sempre più complessi, mettendo insieme le varie porte che abbiamo visto, le porte elementari.
[00:05:18 - 00:05:38] Allora, se ricordate l'ultima lezione, allora abbiamo visto che una semplice memoria, in particolare un registro di memoria, lo potevamo costruire, diciamo, mettendo insieme, in base a quanti bit servivano.
[00:05:38 - 00:05:51] Quindi se dobbiamo fare il registro auto-bit, mettiamo insieme i flip-flops, che è l'unità di memorizzazione minima, che memorizza il singolo bit.
[00:05:52 - 00:06:20] Ad esempio in questa figura vediamo un possibile registro auto-bit, dove ad ogni bit da memorizzare, che sono questi indicati con i con zero, i con uno, i con due, in atto a destra la sarebbe i con tre, e così via, ogni bit da memorizzare è collegato, diciamo,
[00:06:20 - 00:06:36] in ingresso un flip-flop di tipo D, che, se vi ricordate, il flip-flop di tipo D, cosa fanno? Vanno a campionare il valore di ingresso e a memorizzarlo in che sono alimentati.
[00:06:36 - 00:07:03] Il campionamento del valore di ingresso di ogni flip-flop, diciamo, viene effettuato quando il flip-flop stesso viene abilitato, in questo caso sono dei flip-flops che vengono abilitate sul fronte di discesa,
[00:07:04 - 00:07:10] perché abbiamo il triangolo, quindi, l'abilizzazione sul fronte e il pallino, il fronte di discesa.
[00:07:12 - 00:07:25] In alto al destra abbiamo il segnale di clock, che vedete, abbiamo detto, piuttosto che essere inviato direttamente a flip-flop e utilizzare dei flip-flop abilitati sul fronte di salita,
[00:07:26 - 00:07:36] una tecnica è quella di inserire in mezzo invece un circuito ulteriore, che è un inverter in questo caso, e cosa fa?
[00:07:37 - 00:07:49] Che va a invertire il segnale di clock, quindi, quando il clock effettivo è sul fronte di salita, l'inverter mi genera un clock che invece sta sul fronte di discesa.
[00:07:49 - 00:08:01] Questo clock invertito va ad alimentare questi flip-flop che si abilitano sul fronte di discesa e quindi abbiamo che questi flip-flop si vanno ad abilitare,
[00:08:01 - 00:08:12] cioè che viene abilitata il campionamento dei segnali di ingresso, sul fronte di discesa del clock invertito, cioè sul fronte di salita del clock originale.
[00:08:12 - 00:08:41] A che serve? Questa cosa ne abbiamo parlato l'altro scorsa serve perché ponendo questo circuito di inverter mi fa anche da amplificatore del segnale di clock e quindi tipicamente potete trovare queste soluzioni di mettere dei buffer o degli inverter proprio per amplificare dei segnali che tipicamente vanno ad alimentare molti circuiti.
[00:08:43 - 00:09:04] Hanno la necessità di essere amplificati e una tecnica è quella di amplificare dei circuiti che possono essere dei buffer invertenti, invertitori, li vedremo dopo, che vanno appunto ad amplificare il segnale, a riportarlo a un livello un po' più alto.
[00:09:04 - 00:09:33] Nel momento in cui ovviamente si va a crescere con il numero di bit abbiamo letto i registri a 16 bit, si possono fare utilizzando due registri ad esempio 8 bit, quelli 64 con due registri a 16 o 4 8 e così via, però nel momento in cui però vanno a crescere di molto.
[00:09:35 - 00:09:47] Il numero di bit necessario per memorizzare la singola informazione, quindi in questo caso la singola informazione è una parola da 8 bit, una stringa di 8 bit.
[00:09:47 - 00:10:11] Se faccio il registro a 32 bit la singola informazione occuperà 32 bit, si parla di parola, cioè la stringa, la lunghezza delle informazioni che possono memorizzare, quindi se non registro a 32 bit la stringa è a 32 bit e quindi si parla di parola a 32 bit.
[00:10:12 - 00:10:39] In generale se mi sposto dal registro vado a considerare le memorie in generale, diciamo il numero di bit necessario possono crescere e diciamo i circuiti devono diciamo essere pensati in modo da, c'è l'organizzazione con cui vado a creare le memorie,
[00:10:39 - 00:11:00] devi mettere nel conto del fatto che comunque devo poter indirizzare le memorie, quindi poter accedere in maniera univoca alle singole parole e ovviamente l'organizzazione abbiamo detto varia volte quell'effettiva che si va a realizzare in pratica nella realtà tiene conto di problematiche anche diverse,
[00:11:00 - 00:11:15] cioè problematiche relative ai consumi a ridurre lo spazio occupato dal circuito e a ridurre il numero diciamo di pin necessari a collegarsi a questa memoria.
[00:11:15 - 00:11:44] Vediamo quindi un'organizzazione diversa un po' più complessa pensata appunto per realizzare memorie più grandi quindi diciamo con più bit dove questa per esempio è rappresentata in figura e un esempio di memoria composta da quattro possibili parole,
[00:11:45 - 00:12:13] possibili celle di memoria dove la singola cella, la singola parola a lunghezza di tre bit, tre bit perché vediamo vedete ci sono tre flip flop di che vanno a memorizzare i dati di input quindi tre bit abbiamo in input icon 0, icon 1 e con 2 quindi a questa memoria possiamo
[00:12:13 - 00:12:31] inviare un dato composto da tre bit per cercare di memorizzarlo e diciamo allo stesso memorizzarlo poi ovviamente memorizzarlo andrà memorizzato in una delle parole disponibili da cui nel caso diciamo di memorizzazione di un dato,
[00:12:31 - 00:13:00] questo andrà selezionato ovviamente, andrà indirizzata quale è la parola di interesse e allo stesso modo in uscita alla memoria i dati di output sono sempre i tre bit e sia quando si fa a effettuare una lettura in memoria vuol dire andare ad accedere innanzitutto alla parola di interesse quindi anche qua indirizzare nella memoria quale è la parola a cui si vuole accedere.
[00:13:02 - 00:13:27] Leggerla vuol dire portare in uscita della memoria, su questi icon 0, 1, 2, i tre bit corrispondenti al dato stesso che ovviamente sono collegati in qualche modo a le uscite che poi coincidono sempre con lo stato del flip flop di tutta la parola selezionata
[00:13:28 - 00:13:45] mentre ovviamente gli ingressi di prima quelli che vogliamo memorizzare vedete su coincidono vengono portati all'ingresso dei vari flip flops che compongono la parola.
[00:13:46 - 00:14:05] In questo circuito possiamo riconoscerlo, ci andiamo un po' più nel dettaglio, già da adesso vedete ci sono le classiche configurazioni del classico utilizzo delle porte and abilitanti che servono a, se ricordate,
[00:14:06 - 00:14:24] abilitare un certo percorso, quindi un segnale di ingresso che arriva su una porta abilitante quando la porta and è abilitata, quel segnale viene propagato in uscita, altrimenti la porta and forza e il valore nullo in uscita.
[00:14:24 - 00:14:53] Questa memoria, oltre ad avere i tre ingressi associati al dato di input che si vuole andare a memorizzare in memoria, ha ulteriori due ingressi che sono questo A1 e A0 che, se ci pensate bene, servono appunto a indicare alla memoria o meglio da indirizzare nella memoria la parola.
[00:14:54 - 00:15:23] Quindi, in qualche modo, sopra abbiamo i dati di input, questi dati di input vengono, diciamo, sono collegati a tutti gli ingressi di corrispondenti, cioè i con zero e collegato, vedete, ai vari ingressi della colonna di testa dei flip flops, quindi lo stesso bit di ingresso è collegato a tutta la colonna,
[00:15:24 - 00:15:36] quindi la memoria, i con uno alla colonna centrale dei flip flops e i con due alla prima colonna. Questo perché potenzialmente lo stesso segnale di ingresso può essere salvato in tutte le parole.
[00:15:36 - 00:15:37] Chi è che può va a decidere quale di questi flip flops deve essere abilitato e quindi deve andare a leggere il segnale di ingresso, ovviamente, il circuito che sta sulla sinistra, che in qualche modo è composto da una parte che indirizza, abbiamo detto, quale è la parola di interesse, quindi avrà lo scopo di andare a
[00:16:06 - 00:16:32] selezionare la riga di interesse, la riga di flip flop di interesse. D'altro canto poi c'è quella parte azzurra che andiamo a vedere nel dettaglio tra qualche slide invece che sono porte, diciamo, di scrittura, perché in qualche modo andranno ad abilitare appunto la scrittura dentro, diciamo,
[00:16:33 - 00:16:37] nella memoria del dato da memorizzare.
[00:16:40 - 00:16:52] Quindi c'è una parte di selezione, poi una parte che ci dice se le ho scrive e l'altro che appunto in magazzina, giusto?
[00:16:52 - 00:17:05] Sì, sì, adesso moriamo, ci vediamo con calma, se non sbaglio un pezzo l'ho avvolto, sì, ok, e diciamo, questa è la visione di insieme, ma scendiamo con calma nei vari parti.
[00:17:06 - 00:17:21] Già adesso possiamo riconoscere al volo la parte sinistra che è quella di indirizzamento, che ha la classica configurazione delle possibili combinazioni dei olori di A1 e A0, vedete?
[00:17:21 - 00:17:48] Perché sono collegati A1 e A0 o direttamente alla end inferiore, o diretto uno negato, al contrario l'altro diretto l'altro negato, entrambi negati sono le quattro possibili configurazioni dei valori della coppia A1 e A0 che in qualche modo mi va a attivare la end opportuna, però vediamolo con calma.
[00:17:51 - 00:18:06] Ovviamente anche questi che qua vediamo in fondo, diciamo, chips, elect, read, data, output, and able, sono ulteriori ingressi che vanno in qualche modo a definire il comportamento della memoria, ok?
[00:18:07 - 00:18:09] Vediamo con calma.
[00:18:10 - 00:18:27] Allora, questa memoria ha otto linee di input, perché sono, abbiamo detto, tre per i dati, due per l'indirizzamento e questi ulteriori tre di configurazione in fondo a sinistra.
[00:18:27 - 00:18:44] Quindi sono otto pin di input, diciamo, immaginatele tutto rinchiuso, diciamo, in un circuito integrato, che spone otto pin per gli input e tre di output, cioè tre per i dati, questi in fondo a destra.
[00:18:44 - 00:19:13] Ovviamente in base ai valori, diciamo, dell'indirizzo abbiamo detto che è abilitata la parola, viene selezionata in qualche modo la parola di interesse e poi quegli altri pin di configurazione vanno a definire se su quella parola che abbiamo selezionato con l'indirizzamento torno qui dobbiamo effettuare una lettura o una scrittura, come suggeriva il vostro collega.
[00:19:15 - 00:19:39] Questa è una configurazione, se avessimo utilizzato, diciamo, la stessa, quest'altra configurazione, questa era una memoria autobit che avevamo, diciamo,
[00:19:39 - 00:19:53] otto pin di ingresso, otto di uscita, il clear, avremmo avuto bisogno di venti pin.
[00:19:54 - 00:20:16] Mentre qui facendo, con questa configurazione, in cui abbiamo, torno qui vedete, quattro parole da tre bit, cioè questa è una memoria da 12 bit, non banalmente moltiplicando il numero di bit per riga,
[00:20:17 - 00:20:29] però nonostante abbiamo 12 bit, quindi una memoria maggiore della configurazione autobit che avevamo visto all'inizio, richiede soltanto appunto 13 bit,
[00:20:29 - 00:20:41] perché questa organizzazione è pensata per risparmiare il numero di bit, poi si presta anche, diciamo, a immaginare come si possa estendere facilmente,
[00:20:41 - 00:20:51] perché se vogliamo realizzare una memoria che ha una parola più lunga, quindi maggiori bit per la singola parola, vuol dire,
[00:20:51 - 00:20:58] banalmente aggiunge ulteriori colonne di questi flipflop di organizzati in questo modo.
[00:20:59 - 00:21:12] Se in questo modo, se invece vogliamo aumentare il numero di parole della memoria, vuol dire aggiungere ulteriori righe di questa organizzazione.
[00:21:13 - 00:21:25] In entrambi i casi, diciamo, questo approccio è scalabile, aggiungiamo componenti, li colleghiamo come abbiamo collegato queste, quindi, diciamo, dovrebbe essere facile immaginare come estenderla.
[00:21:30 - 00:21:32] Allora, vediamo come funziona.
[00:21:33 - 00:21:51] Ci davo prima il fatto della configurazione questa qui sulla destra, che sono l'indirizzamento. Qui abbiamo una memoria da quattro parole,
[00:21:52 - 00:22:07] i bit necessari a indirizzare una memoria si scelgono in base al numero di parole, quindi se io ho quattro parole mi servono almeno due bit per l'indirizzo, per l'indirizzamento.
[00:22:08 - 00:22:18] E quindi, a con uno e a con zero, sono appunto sufficienti, certamente sufficienti, ne è utile metterne ulteriori per indirizzare quattro parole,
[00:22:18 - 00:22:29] perché due alla seconda fa quattro e quindi le possibili combinazioni di questi due bit mi danno i quattro possibili valori a cui possiamo associare le singole parole in maniera univoca.
[00:22:30 - 00:22:38] E questo è il classico, diciamo, la classica implementazione che abbiamo già visto di quando facciamo un decodificatore.
[00:22:39 - 00:22:58] Il decodificatore, se vi ricordate, cosa fa in uscita abilita soltanto una porta e vale uno. Quindi, qui abbiamo quattro uscite, che sarebbero le uscite delle quattro end,
[00:22:59 - 00:23:12] che in base al valore della configurazione a con uno e a con zero, queste quattro ore end avranno un'unica end che vale uno, valore alto, tutte le altre, a valore basso.
[00:23:13 - 00:23:31] Quindi, in qualche modo, diciamo, poiché le uscite delle end, vedete, vanno ad alimentare poi le altre end ognuno associato.
[00:23:31 - 00:23:42] Per esempio, questa blu, la end della blu, va in qualche modo sul clock, cioè sul segnale di abilitazione della parola zero.
[00:23:43 - 00:23:49] Questa altra blu, sulla abilitazione della parola uno, e così via.
[00:23:49 - 00:24:06] Quindi, in base a quale di queste end viene abilitata dal circuito dei codificatori, si va a contribuire alla abilitazione della parola corrispondente.
[00:24:07 - 00:24:14] Ok, contribuire, perché adesso dobbiamo vedere gli altri contributi. Cosa fanno?
[00:24:19 - 00:24:38] No, dobbiamo raggiungere sempre qua. Ad esempio, qui nella parte azzurra, che sono le porte di scrittura.
[00:24:39 - 00:24:47] Porte di scrittura in tesso come scrittura nel flip flop, cioè alla fine sarebbe la lettura della parola.
[00:24:48 - 00:24:52] Cioè, non scusatemi, la memorizzazione dentro la parola del bit d'ingresso.
[00:24:53 - 00:25:04] E affinché, per esempio, se io voglio selezionare la parola zero e scriverci dentro la parola zero, quindi memorizzare il dato di input, cosa devo fare?
[00:25:04 - 00:25:20] Devo semplicemente collegare il dato di input agli ingressi zero, i1 e i2, e poi devo far arrivare il segnale di abilitazione sul clock della parola zero.
[00:25:20 - 00:25:27] Mentre, alle altre parole, il clock, il segnale di abilitazione deve essere sempre disabilitato.
[00:25:28 - 00:25:44] In questo modo, abilitando la memorizzazione solo nella parola selezionata dal decodificatore, quindi da i valori a1 e a0, andrò a scrivere dentro quella parola e soltanto in quella.
[00:25:44 - 00:26:03] Ok? Quindi, in fase di memorizzazione, a1 e a0 mi vanno a mandare il segnale di abilitazione soltanto e flip flop della parola indicata proprio dalla combinazione a1 a0.
[00:26:03 - 00:26:14] Questo altro valore che sale nelle porte, cioè che arriva nella end delle porte azzurre, che cos'è?
[00:26:14 - 00:26:21] E' questo chips select che, normalmente, in questo caso lo immaginiamo asto.
[00:26:21 - 00:26:32] Noi immaginiamo che ci sono più chips di memorizzazione, è stato, diciamo, selezionato questo, quindi nel nostro esempio è alto.
[00:26:33 - 00:26:41] Quando c'è quello che va a definire l'operazione poi, e invece questo read data.
[00:26:41 - 00:26:58] Per come è fatto, read data, vedete c'è l'invertitore, quindi quando il read data si abbassa,
[00:26:59 - 00:27:13] nella end questa qui, bianca, diciamo, con il chips select che lo possiamo immaginare sempre alto, perché stiamo selezionando questo chipset.
[00:27:13 - 00:27:20] In uscita, quindi, abbiamo un valore alto che arriva in queste porte di scrittura.
[00:27:20 - 00:27:35] Quindi, se, scusate, non devo leggere il dato, voglio scrivere il dato.
[00:27:35 - 00:27:38] Quindi read basso?
[00:27:38 - 00:27:47] Sì, read basso, quindi io voglio...
[00:27:48 - 00:27:50] E chips select sono alto?
[00:27:50 - 00:27:55] Chips select è sempre alto, perché in figura non ci sono altri chips select.
[00:27:55 - 00:28:05] Quindi immaginiamolo alto, io sto mandando i dati, immaginate che abbiamo più memorie che ricevano questi dati di input.
[00:28:05 - 00:28:16] Ovviamente io qua nella figura sono l'unica memoria, quindi se non è selezionato questo chips select, questa memoria ovviamente vincere o zero, non posso farci niente.
[00:28:17 - 00:28:27] Se ovviamente vogliamo scrivere in questa memoria chips select è alto, quindi dobbiamo vedere solo se read data mi dice se deve leggere o scrivere.
[00:28:27 - 00:28:41] Nel momento in cui ovviamente io voglio scrivere, read data è basso, viene invertito e quindi alla end questa bianca, subito dopo l'invertitore, quella che mette insieme chips select e read data esce uno, ok?
[00:28:42 - 00:28:48] E' abilita la selezione, cioè perché è in end?
[00:28:48 - 00:29:05] Sì, diciamo chips select alto e read data basso, come se fosse scrittura alta ovviamente, mi arriva il segnale alto a tutte queste end azurre in ingresso.
[00:29:05 - 00:29:17] Però le end azurre, le porte di scrittura oltre al segnale alto che viene dal chip select e da read data basso hanno anche l'indirizzamento in input.
[00:29:17 - 00:29:25] Ma solo una di quelle porte di scrittura avrà il segnale alto in base a quale è la parola di interesse.
[00:29:25 - 00:29:28] Vi trovate?
[00:29:28 - 00:29:30] Sì, sì.
[00:29:30 - 00:29:45] Quindi la parte di selezione della parola che è il nostro classico decodificatore mi va a selezionare solo la riga, solo la parola di interesse che diciamo solo la end di quella riga, la end azurra di quella riga.
[00:29:45 - 00:30:10] Se la end azurra di quella riga riceve in ingresso la selezione, in uscito ovviamente mi dà il valore alto che mi va ad abilitare tutti i flip flop di quella riga e quindi effettivamente ho il campionamento dei bit di ingresso corrispondente in ogni flip flop.
[00:30:15 - 00:30:21] Diamo se ho dimenticato qualcosa.
[00:30:21 - 00:30:31] Read data al valore alto quindi è la scrittura.
[00:30:32 - 00:30:40] Se invece devo fare la lettura, la lettura sarebbe il contrario.
[00:30:40 - 00:30:53] Legge dalla memoria, dobbiamo intendere, legge dalla memoria vuol dire portare un dato da una delle parole in uscita a questi valori, a questi bit 0, 1 o 2.
[00:30:53 - 00:31:01] Nel momento in cui il read data è alto, cosa succede?
[00:31:02 - 00:31:22] Che le porte di scrittura ricevono il negato quindi 0 va nella end, mi forza lo 0 a tutte le porte di scrittura e quindi questa parte di sinistra, la parte azurra, resta bassa.
[00:31:22 - 00:31:33] Quindi quando il read data è alto tutti i flip flop si trovano disabilitati quindi mantengono i loro valori.
[00:31:33 - 00:31:40] Dobbiamo quindi andare a esaminare invece questa parte in giù, la parte più bassa.
[00:31:41 - 00:31:58] Questa parte è sempre di abilitazione che ha un ulteriore pin, c'è l'ingresso output enable, ha il chip select e ha il read data, che però gli arriva non invertito, ma diretto.
[00:31:58 - 00:32:02] Quindi chip select abbiamo detto sempre è alto.
[00:32:02 - 00:32:08] Read data è alto, quindi questa volta voglio andare a legge dalla memoria.
[00:32:08 - 00:32:25] Output enable ovviamente se è abilitato l'output, quindi in ingresso questa end rossa, diciamo, riceve tre valori alti e ovviamente la end è alta, solo quando tutti gli ingressi sono alti.
[00:32:25 - 00:32:36] Quindi ho questo segnale di alto che arriva in ingresso a queste porte e poi ci ragioniamo.
[00:32:36 - 00:32:39] Nel frattempo andiamo a vedere la nostra configurazione.
[00:32:39 - 00:32:53] Allora l'output di ogni flip flop è collegato a, diciamo, queste porte end che vediamo tra le righe.
[00:32:54 - 00:33:04] Queste porte end, cosa fanno, ricevono anche loro come contributo di ingresso.
[00:33:04 - 00:33:18] Il segnale output del corrispondente, diciamo, flip flop, il valore Q per intenderci e ovviamente l'uscita della porta di selezione.
[00:33:19 - 00:33:35] Questo cosa vuol dire che soltanto la parola selezionata, quindi soltanto la porta di selezione abilitata, che ricordiamo, soltanto una per volte abilitata,
[00:33:35 - 00:33:49] che altre sono di vanno a zero, soltanto una mi andrà a abilitare queste porte end che fanno, mi portano il Q corrispondente alla riga, alla parola quindi selezionata,
[00:33:49 - 00:33:52] me lo porta in queste porte or finali.
[00:33:54 - 00:34:05] Come al solito, se vi ricordate la porta or, noi andiamo ad alimentare da più percorsi che possono contribuire al suo ingresso.
[00:34:06 - 00:34:19] Questi percorsi, quanti sono le parole quattro, quindi abbiamo che ogni porta or, vedete, riceve quattro ingressi, uno da ogni parola.
[00:34:19 - 00:34:39] Ovviamente dal bit, cioè abbiamo una porta or per ogni colonna, quindi questa porta or sulla sinistra, riceve l'ingresso, l'output di ogni flip flop alimentato dal bit i2, ok?
[00:34:40 - 00:34:52] E così via tutti gli altri, quindi alla fine, in base alla porta di selezione, viene abilitata solo una parola e solo lo stato di quella parola viene riportato in ingresso alla or.
[00:34:53 - 00:35:04] Ovviamente viene poi propagato in uscita, che ricordate, nella or basta che un ingresso è alto, anche l'uscita è alta.
[00:35:05 - 00:35:17] Questi, questi valori delle uscite delle porte or vengono riportate, ovviamente è alto, scusate mi, dipende dal valore di Q.
[00:35:18 - 00:35:33] Quindi il valore di Q arriva in ingresso alla or, solo il valore di Q della parola abilitata arriva alla or, mentre gli altri ingressi della or sono forzati a zero da queste porte.
[00:35:34 - 00:35:35] L'abilitazione è bianche.
[00:35:36 - 00:35:39] Che è la parte della selezione dell'indirizzo?
[00:35:40 - 00:35:51] Visto che solamente una sola indirizzo viene abilitata la volta, solamente quella parola passerà, le altre non passano, sono tutti zeri.
[00:35:52 - 00:35:58] Sì, poiché Q può essere zero o uno indifferente, Q arriva in ingresso alla or e si ritrova in uscita.
[00:35:58 - 00:36:18] Quindi sì, queste tre porte NAND che vediamo bianche in ogni riga, cioè all'uscita di ogni parola, sono abilitate dalla corrispondente porta di selezione della parola.
[00:36:19 - 00:36:35] Solo quindi una riga di queste tre porte bianche risulta abilitata e le altre avranno in ingresso zero, quindi forse erano a zero i loro Q, diciamo i loro contributi.
[00:36:36 - 00:36:43] Quindi alla or, l'unico valore che può essere diverso da zero è quella che porta il Q della parola di interesse.
[00:36:43 - 00:36:56] Però quello che da capire è che, diciamo, ogni porta a ora, quattro fili di ingresso, tre sono forzati a zero dalla selezione della parola.
[00:36:56 - 00:37:04] Quindi, diciamo, le parole non selezionate porteranno come contributo a questa orre il valore è zero.
[00:37:05 - 00:37:13] Le parole, invece, cioè la parola, l'unica parola selezionata porterà il suo contributo Q.
[00:37:13 - 00:37:19] Quindi in ingresso dobbiamo immaginare che abbiamo Q zero, zero, zero e questo per ogni colonna.
[00:37:20 - 00:37:33] E in uscita, quindi, all'ingresso di queste ulteriori porte, che vedete, sono una specie di invertitore, ma senza il pallino,
[00:37:33 - 00:37:46] e si chiamano buffer proprio perché non invertono, non la metto il pallino, non invertono, in ingresso si limita, ma riproporlo in uscita, quindi sono dei buffer.
[00:37:47 - 00:38:00] Questi buffer poi hanno questo segnale che viene da giù per indicare che sono, diciamo, abilitati da un segnale in ingresso che alla fine gli viene portato
[00:38:00 - 00:38:12] dall'output e nebo, cioè da questa porta rossa. Quindi questa porta rossa non fa altro che ad andare ad abilitare questi buffer che,
[00:38:12 - 00:38:17] una volta abilitati, replicano l'input e lo propagano in uscita.
[00:38:18 - 00:38:22] Non clicchicando il segnale, giustamente, perché?
[00:38:22 - 00:38:31] Sì, torniamo al discorso, ma c'è qualche slide in cui ripete queste cose che vi ho detto, però il concetto sia questo.
[00:38:31 - 00:38:42] Dimettere questi segnali da un lato per, diciamo, amplificare il segnale e portarlo, diciamo, a livello corretto in uscita.
[00:38:43 - 00:38:54] Questi buffer, diciamo, questi circuiti hanno questa parte di abilitazione governata dal output e nebo, perché?
[00:38:54 - 00:39:06] Perché nelle porte, diciamo, nelle memorie reali, qui non si vede da questa figura, ma nelle memorie reali, i segnali di input e output,
[00:39:06 - 00:39:11] tipicamente, sono condivisi nel senso che si trovano sulle stesse linee.
[00:39:11 - 00:39:18] Quindi la stessa linea, a volte, è utilizzata come input e a volte come output.
[00:39:20 - 00:39:30] Quindi, se non ci fossero, diciamo, questi buffer da abilitare, l'uscita delle output,
[00:39:30 - 00:39:40] delle porte orre, quindi, diciamo, l'uscita dei flip-flop andrebbero direttamente a collegarsi in ingresso ai flip-flop stessi.
[00:39:41 - 00:39:53] E per evitare, diciamo, questi momenti di coincidenza, diciamo, tra input e output, si aggiunge questa parte di abilitazione
[00:39:53 - 00:40:06] in modo da regolare il momento in cui i valori, poi, possono essere presentati in uscita.
[00:40:07 - 00:40:09] Vediamo se ho detto tutto.
[00:40:12 - 00:40:15] Ah, scusatevo il secondo, 10 secondi mi devo alzare un attimo.
[00:40:23 - 00:40:41] Eccomi, scusate.
[00:40:41 - 00:40:57] Quindi, come detto, le linee di indirect, che ovviamente qua sono solo due, perché abbiamo, stiamo ragionando con una parola, con una memoria di solo quattro parole.
[00:40:57 - 00:41:10] Se crescono, diciamo, se la memoria aumenta il larghezza, quindi aumenta la lunghezza della parola, ma il numero di parole resta quattro, continueranno a bastare due bit.
[00:41:11 - 00:41:16] Ok, quindi le linee di indirizzo aumentano solo se aumentano le parole da indirizzare.
[00:41:16 - 00:41:35] Allora, scrittura, vedete, abbiamo detto quando read data il valore basso, chip select abbiamo detto, noi immaginiamo sempre altro, perché stiamo ragionando su questo chip, con questo circuito di memoria.
[00:41:35 - 00:41:43] Nella realtà ci saranno più banchi di memoria, più circuiti di memoria, che ovviamente vanno selezionati anchissi.
[00:41:46 - 00:41:57] Che ovviamente se la memoria che stiamo analizzando avrà il chip select ha oltre un dire che alle altre, diciamo, verrà mandato il valore basso, cioè non verranno selezionate.
[00:41:57 - 00:42:07] Questo l'abbiamo detto, ha fatto dei buffer non invertenti. Qual è il problema?
[00:42:08 - 00:42:26] Avrei detto, perché altrimenti, se consideriamo che nella realtà le sesse linee dei dati vengono utilizzate, inoltre per l'input e inoltre per l'output, risulterebbe che le porte or di uscita della memoria
[00:42:27 - 00:42:46] se fossero collegate direttamente alla output, il chip di memoria cercherebbe di spedire appunto in output i dati anche durante la scrittura, vediamo perché, torniamo di qua.
[00:42:47 - 00:42:57] Perché durante la scrittura abbiamo detto, noi facciamo il campionamento dei valori di ingresso, perché demandiamo a D e questo che cosa fa?
[00:42:57 - 00:43:10] Si porta ovviamente il flip flop allo stato del valore D, lo memorizza, cioè il valore di Q assume quello del valore D che si sta cercando di memorizzare.
[00:43:11 - 00:43:26] E ovviamente se non ci fosse questa parte giù che mi va ad abilitare questi buffer, diciamo, se non avessi la possibilità di abilitare o meno questi circuiti,
[00:43:26 - 00:43:44] l'uscita delle porte or che anche quando vado a fare la scrittura mi porta in output, diciamo, in uscita alle porte or, i valori appena memorizzati, quindi il 0 e 1 e 2, in qualche modo io me li ritrovo subito,
[00:43:45 - 00:43:50] dopo ovviamente i tempi di propagazione in uscita alle porte or.
[00:43:51 - 00:44:05] Non devo però farle arrivare ai bit, diciamo, o 0 o 1 o 2, perché questi coincidono, diciamo, con le linee e quindi devo in qualche modo, quando si effetta la scrittura,
[00:44:05 - 00:44:20] output enable è basso in modo da andarmi a disabilitare questi buffer che così non andranno a propagare l'uscita delle porte or sulle linee dati.
[00:44:35 - 00:44:36] Chiaro questo concetto?
[00:44:40 - 00:44:41] Sì.
[00:44:45 - 00:45:01] Perché alla fine voi, come dire, sulle linee dati mettete il dato che volete memorizzare, però è importante che quasi sia staccato, perché all'uscita delle porte or, in quel caso penso che trovate il dato che si trova al momento,
[00:45:02 - 00:45:16] quello là che deve essere sostituito, lo trovate all'uscita delle porte or, quindi dovete staccare questo output enable e poi potete mandare sulle linee dati il dato che volete scrivere.
[00:45:16 - 00:45:34] E quindi per evitare interferenza, diciamo, imputte output durante queste fasi di modifica dei valori in memoria, tipicamente, diciamo, si usa questo approccio.
[00:45:35 - 00:45:53] Questo è il simbolo un po' più ingrandito, abbiamo detto non c'è il pallino, quindi un buffer e ha un secondo ingresso che questo ingresso di controllo che mi fa, appunto, mi permette di abilitare o meno il circuito.
[00:45:54 - 00:46:18] Quindi sono le buffer non invertenti e, come se suggeriva vostro collega, si introduce un appunto per ovviamente amplificare i segnali che stanno arrivando dalla memoria, che ovviamente qua su poche parole, diciamo, sembra superfluo,
[00:46:18 - 00:46:37] però immaginate una memoria con tantissime parole e quindi, diciamo, si sfrutta questa ulteriore proprietà del buffer non invertenti di amplificare, diciamo, il segnare.
[00:46:48 - 00:47:14] Ovviamente auto-potenable deve essere alto, read-data deve essere alto e cibeselect abbiamo supposto sempre che sia alto. Quando tutti e tre sono alto, i buffer invertenti ricevono il segnale alto e quindi replicano, diciamo, il segnale che erano l'ingresso, collegano effettivamente le uscite delle porte or alle linee dati e amplificano il segnale.
[00:47:18 - 00:47:43] Se, ovviamente, c'è il pallino, questa stessa configurazione, queste sono buffer invertenti che, di unica differenza rispetto all'inverter che abbiamo visto fino ad adesso, hanno questa linea di controllo per essere, diciamo, abilitati o meno, quindi sono circuiti comandati da un segnale di controllo.
[00:47:44 - 00:47:58] Se, diciamo, sono abilitati, questi circuiti si comportano come l'invertitore classico. Se non sono abilitati, sono circuiti aperto, quindi non collegano l'ingresso con l'uscita.
[00:47:58 - 00:48:23] Questa è la proprietà di amplificazione, abbiamo detto, entrambi i circuiti di controllo che abbiamo visto, quindi buffer invertenti e buffer non invertenti, vengono spesso utilizzati, vengono introdotti per permettere di amplificare il segnale.
[00:48:28 - 00:48:57] E come abbiamo visto prima, ad esempio, nel registro 8-bit, capita che vengono introdotti anche quando non necessari proprio per forzare, cioè viene cambiata la logica con cui funziona il circuito proprio per forzarne l'utilizzo, perché se utilizzo un invertitore o un buffer non invertente, posso usare l'amplificazione,
[00:48:58 - 00:48:59] dove è necessario.
[00:48:59 - 00:49:28] Sulla estensione ne abbiamo già parlato, quindi in questa organizzazione che abbiamo visto, penso sia facile immaginare come estenderla, abbiamo detto che possiamo estenderla sia aggiungendo bit alle singole parole, quindi fare parole più lunghe.
[00:49:29 - 00:49:35] Oppure aggiungere parole alla memoria aggiungendo ulteriori rig.
[00:49:35 - 00:49:58] E' un tipo di organizzazione che mi permette di risparmiare le linee, quindi il numero di pin, ma è anche facilmente escalabile, perché ha questa organizzazione matriciale in cui basta aggiungere colonne di flip-flop per aumentare il numero di bit delle parole o righe di flip-flop per aumentare il numero di parole.
[00:49:58 - 00:50:15] Posso fare ovviamente entrambe le cose, ovviamente la dimensione della memoria che è data dal numero di bit di ogni parola per il numero di parole aumenta in ogni caso.
[00:50:15 - 00:50:42] Anche per le memorie c'è una sorta di legge di Moron, che prevede che il numero di bit per i cipri raddoppi ogni 18 mesi, tipicamente la dimensione delle memorie aumenta,
[00:50:42 - 00:51:04] e allo stesso tempo diminuiscono i costi per realizzarle, anche se, diciamo, tipicamente le memorie più grandi hanno un costo per bit molto inferiore rispetto alle memorie più piccole, ma che sono più veloce.
[00:51:04 - 00:51:16] Non immaginate il confronto tra la RAM e la cache, tipicamente la memoria cache è piccola, ma veloce, mentre la memoria RAM è grande, ma un po' più lento.
[00:51:16 - 00:51:43] Qua c'è un esempio di cunicip di memoria effettiva, e come detto prima, una memoria io la posso realizzare andando a spingere, allargandola, facendo il numero di bit delle singole parole più grandi o il numero di parole.
[00:51:43 - 00:51:51] Ad esempio, qui abbiamo due memorie da 4 megabit, in cui hanno però un'organizzazione diversa.
[00:51:51 - 00:52:20] In una è stata realizzata con 512.000 parole da 8 bit. Nell'altro caso, invece, abbiamo 4096 k, quindi milioni alla fine, memorie da un bit.
[00:52:20 - 00:52:49] Per quanto riguarda i generali, qui nei simboli, vedete che alcuni, queste sono i bits, sono i bits, sono i bits, sono i bits, sono i bits, sono i bits, sono i bits, sono i bits.
[00:52:51 - 00:53:02] I pin che offrono questi chip, vedete che alcuni sono negati, hanno la negazione sotto, sono indicati in maniera diretta.
[00:53:02 - 00:53:23] Tipicamente, un segnale di abilitazione, se è scritto in maniera diretta, senza la negazione, vuol dire che asserisce inventione il circuito sul valore alto.
[00:53:23 - 00:53:36] Se invece, come in questo caso, sono negati, vuol dire che la sua abilitazione viene asserita sul valore basso.
[00:53:36 - 00:53:51] Ok, quindi, il concetto di asserire, un segnale di abilitazione, asseriscia, in essenzio espleta la sua azione,
[00:53:51 - 00:54:10] un segnale su valore alto, un segnale su valore basso, un segnale su valore alto, un segnale su valore basso.
[00:54:10 - 00:54:20] Quindi, cosa vuol dire qua nello specifico? Abbiamo questi tre segnali C, S, W, E, E, O, E, vedete, sono negati, come rasse e casso,
[00:54:20 - 00:54:30] vuol dire che abliterano, se andranno ad asserire il valore su quando sono bassi.
[00:54:30 - 00:54:48] Allora, questo tipo di memoria, questo qua che era fatto da 512, K parole, serve 2 alla 19 da 8-bit,
[00:54:48 - 00:55:01] quindi, immaginate con regalizzazione simile a quella di prima, in cui abbiamo, appunto, 512,000 righe e 8 colonne.
[00:55:01 - 00:55:12] Ah, il chip select che abbiamo visto anche prima, black and ebol, invece del read data, questo c'è il black and ebol e output the ebol,
[00:55:12 - 00:55:24] quindi, i tre segnali di controllo che abbiamo visto nell'organizzazione di prima. Semplicemente, invece, sono indicati negati, quindi, sono asseriti quando sono bassi.
[00:55:25 - 00:55:38] Quindi, per selezionare questo chipset, C, S deve essere posto al valore basso, se si vuole scrivere, black and ebol deve essere posto al valore basso,
[00:55:38 - 00:55:48] e se si vuole andare a leggere, output e ebol, o meglio, se si vuole abilitare l'output, valore basso.
[00:55:49 - 00:56:00] Quest'altra memoria, l'altro esempio, diciamo, segue un'organizzazione leggermente diversa.
[00:56:00 - 00:56:15] Ecco qua, che ha 4 milioni, 4.096 k parole, però non è organizzato, non è un'organizzazione leggermente diversa,
[00:56:15 - 00:56:30] e quindi, non sono 4.096 righe da un bit, ma hanno un'organizzazione matriciale, organizzata a 2048 per 2049,
[00:56:30 - 00:56:39] e, diciamo, ha questi segnali, che sono RAS e CAS, per andare a selezionare l'organizzazione di prima,
[00:56:39 - 00:56:56] ma hanno un'organizzazione matriciale, organizzata a 2048 per 2048 celle da un bit, e, diciamo, ha questi segnali, che sono RAS e CAS,
[00:56:56 - 00:57:06] per andare a selezionare la riga, diciamo, di interesse, e la colonna di interesse.
[00:57:07 - 00:57:17] Ma, beh, comunque, ma dov'è l'uscionante di particolare, da andare a approfondire, visto che manca poco tempo?
[00:57:19 - 00:57:28] Come al solito è giusto per dire che, rispetto all'organizzazione didattica, diciamo, che abbiamo visto prima, di quella matrice della memoria a 12-bit,
[00:57:29 - 00:57:42] poi, nell'area stava, quando si va a realizzare un chip di memoria effettivo, poi si possono fare, diciamo, considerazioni ingenieristiche diverse,
[00:57:42 - 00:57:50] che vanno a scegliere il numero di righe, il numero di colonna, in modo da, cioè, come organizzare la memoria.
[00:57:59 - 00:58:02] Ah, beh, mi fermo qui.
[00:58:06 - 00:58:13] Se non avete dubbi o domande, allora vi saluto, ci vediamo oggi o pomeriggio per un'altra lezione, ok?
[00:58:15 - 00:58:17] Grazie, prof, a dopo.
[00:58:17 - 00:58:18] Grazie, arrivederci.
[00:58:18 - 00:58:20] Grazie, arrivederci.
[00:58:20 - 00:58:22] Arrivederci più tardi.
[00:58:22 - 00:58:24] Arrivederci, prof.
[00:58:28 - 00:58:30] Arrivederci.
[00:58:58 - 00:59:01] Buon appetito.
[00:59:28 - 00:59:31] Buon appetito.
[00:59:58 - 01:00:01] Buon appetito.
[01:00:28 - 01:00:31] Buon appetito.
[01:00:58 - 01:01:01] Buon appetito.
[01:01:28 - 01:01:31] Buon appetito.
[01:01:58 - 01:02:00] Buon appetito.
[01:02:28 - 01:02:30] Buon appetito.
[01:02:58 - 01:03:00] Buon appetito.
[01:03:28 - 01:03:30] Buon appetito.
[01:03:58 - 01:04:00] Buon appetito.
[01:04:28 - 01:04:30] Buon appetito.
[01:04:58 - 01:05:00] Buon appetito.
[01:05:28 - 01:05:30] Buon appetito.
[01:05:58 - 01:06:00] Buon appetito.
[01:06:28 - 01:06:30] Buon appetito.
[01:06:58 - 01:07:00] Buon appetito.
[01:07:28 - 01:07:30] Buon appetito.
[01:07:58 - 01:08:00] Buon appetito.
[01:08:28 - 01:08:30] Buon appetito.
[01:08:58 - 01:09:00] Buon appetito.
[01:09:28 - 01:09:30] Buon appetito.
[01:09:58 - 01:10:00] Buon appetito.
[01:10:28 - 01:10:30] Buon appetito.
[01:10:58 - 01:11:00] Buon appetito.
[01:11:28 - 01:11:30] Buon appetito.
[01:11:58 - 01:12:00] Buon appetito.
[01:12:28 - 01:12:30] Buon appetito.
[01:12:58 - 01:13:00] Buon appetito.
[01:13:28 - 01:13:30] Buon appetito.
[01:13:58 - 01:14:00] Buon appetito.
[01:14:28 - 01:14:30] Buon appetito.
[01:14:58 - 01:15:00] Buon appetito.
[01:15:28 - 01:15:30] Buon appetito.
[01:15:58 - 01:16:00] Buon appetito.
[01:16:28 - 01:16:30] Buon appetito.
[01:16:58 - 01:17:00] Buon appetito.
[01:17:28 - 01:17:30] Buon appetito.
[01:17:58 - 01:18:00] Buon appetito.
[01:18:28 - 01:18:30] Buon appetito.
[01:18:58 - 01:19:00] Buon appetito.
[01:19:28 - 01:19:30] Buon appetito.
[01:19:58 - 01:20:00] Buon appetito.
[01:20:28 - 01:20:30] Buon appetito.
[01:20:58 - 01:21:00] Buon appetito.
[01:21:28 - 01:21:30] Buon appetito.
[01:21:58 - 01:22:00] Buon appetito.
[01:22:28 - 01:22:30] Buon appetito.
[01:22:58 - 01:23:00] Buon appetito.
[01:23:28 - 01:23:30] Buon appetito.
[01:23:58 - 01:24:00] Buon appetito.
[01:24:28 - 01:24:30] Buon appetito.
[01:24:58 - 01:25:00] Buon appetito.
[01:25:28 - 01:25:30] Buon appetito.
[01:25:58 - 01:26:00] Buon appetito.
[01:26:28 - 01:26:30] Buon appetito.
[01:26:58 - 01:27:00] Buon appetito.
[01:27:28 - 01:27:30] Buon appetito.
[01:27:58 - 01:28:00] Buon appetito.
[01:28:28 - 01:28:30] Buon appetito.
[01:28:58 - 01:29:00] Buon appetito.
[01:29:28 - 01:29:30] Buon appetito.
[01:29:58 - 01:30:00] Buon appetito.
[01:30:28 - 01:30:30] Buon appetito.
[01:30:58 - 01:31:00] Buon appetito.
[01:31:28 - 01:31:30] Buon appetito.
[01:31:58 - 01:32:00] Buon appetito.
[01:32:28 - 01:32:30] Buon appetito.
[01:32:58 - 01:33:00] Buon appetito.
[01:33:28 - 01:33:30] Buon appetito.
[01:33:58 - 01:34:00] Buon appetito.
[01:34:28 - 01:34:30] Buon appetito.
[01:34:58 - 01:35:00] Buon appetito.
[01:35:28 - 01:35:30] Buon appetito.
[01:35:58 - 01:36:00] Buon appetito.
[01:36:28 - 01:36:30] Buon appetito.
[01:36:58 - 01:37:00] Buon appetito.
[01:37:28 - 01:37:30] Buon appetito.
[01:37:58 - 01:38:00] Buon appetito.
[01:38:28 - 01:38:30] Buon appetito.
[01:38:58 - 01:39:00] Buon appetito.
[01:39:28 - 01:39:30] Buon appetito.
[01:39:58 - 01:40:00] Buon appetito.
[01:40:28 - 01:40:30] Buon appetito.
[01:40:58 - 01:41:00] Buon appetito.
[01:41:28 - 01:41:30] Buon appetito.
[01:41:58 - 01:42:00] Buon appetito.
[01:42:28 - 01:42:30] Buon appetito.
[01:42:58 - 01:43:00] Buon appetito.
[01:43:28 - 01:43:30] Buon appetito.
[01:43:58 - 01:44:00] Buon appetito.
[01:44:28 - 01:44:30] Buon appetito.
[01:44:58 - 01:45:00] Buon appetito.
[01:45:28 - 01:45:30] Buon appetito.
[01:45:58 - 01:46:00] Buon appetito.
[01:46:28 - 01:46:30] Buon appetito.
[01:46:58 - 01:47:00] Buon appetito.
[01:47:28 - 01:47:30] Buon appetito.
[01:47:58 - 01:48:00] Buon appetito.
[01:48:28 - 01:48:30] Buon appetito.
[01:48:58 - 01:49:00] Buon appetito.
[01:49:28 - 01:49:30] Buon appetito.
[01:49:58 - 01:50:00] Buon appetito.
[01:50:28 - 01:50:30] Buon appetito.
[01:50:58 - 01:51:00] Buon appetito.
[01:51:28 - 01:51:30] Buon appetito.
[01:51:58 - 01:52:00] Buon appetito.
[01:52:28 - 01:52:30] Buon appetito.
[01:52:58 - 01:53:00] Buon appetito.
[01:53:28 - 01:53:30] Buon appetito.
[01:53:58 - 01:54:00] Buon appetito.
[01:54:28 - 01:54:30] Buon appetito.
[01:54:58 - 01:55:00] Buon appetito.
[01:55:28 - 01:55:30] Buon appetito.
[01:55:58 - 01:56:00] Buon appetito.
[01:56:28 - 01:56:30] Buon appetito.
[01:56:58 - 01:57:00] Buon appetito.
[01:57:28 - 01:57:30] Buon appetito.
[01:57:58 - 01:58:00] Buon appetito.
[01:58:28 - 01:58:30] Buon appetito.
[01:58:58 - 01:59:00] Buon appetito.
[01:59:28 - 01:59:30] Buon appetito.
[01:59:58 - 02:00:00] Buon appetito.
[02:00:28 - 02:00:30] Buon appetito.
[02:00:58 - 02:01:00] Buon appetito.
[02:01:28 - 02:01:30] Buon appetito.
[02:01:58 - 02:02:00] Buon appetito.
[02:02:28 - 02:02:30] Buon appetito.
[02:02:58 - 02:03:00] Buon appetito.
