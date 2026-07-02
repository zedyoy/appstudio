# Lezione 12 - Flip-Flop e Registri

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\Lezione 12 - Flip-Flop e Registri.mp4`
- Durata: 00:45:42
- Trascrizione: `12_lezione_12_flip_flop_e_registri.json`

## Argomenti probabili
- porte_logiche (224): and, or, nand, sop
- registri_flip_flop (46): flip flop, latch, registro, registri, propagazione
- clock_prestazioni (39): clock, ciclo, tempo
- mips_assembly (25): registro, registri
- memoria_bus (19): memoria, ram

## Trascrizione

[00:00:00 - 00:00:15] Lecce e Frippleflop, diciamo, è la modalità di attivazione, cioè in che modo, diciamo,
[00:00:15 - 00:00:24] lo stato del circuito si va ad aggiornare, nei lecce, il cambiamento, la modifica, diciamo,
[00:00:24 - 00:00:35] la lettura, diciamo, dell'input viene in maniera asincrona, quindi non appena arriva
[00:00:35 - 00:00:40] in input una configurazione di ingressi SR viene valutata manualmente.
[00:00:40 - 00:00:49] Mi ricordo che la configurazione, cioè le configurazioni di interesse sono 00 per
[00:00:49 - 00:01:01] mantenere lo stato corrente, 00 per settare lo stato a 1, 01 per impostare lo stato a
[00:01:01 - 00:01:08] 0, invece la configurazione 01, abbiamo detto, non viene utilizzata, deve essere evitata.
[00:01:08 - 00:01:22] Nel caso di Frippleflop, invece, il circuito, diciamo, è sincrono, nel senso che il momento
[00:01:22 - 00:01:31] in cui si va a vedere la configurazione all'ingresso, quindi, come abbiamo visto anche l'olta scorsa
[00:01:31 - 00:01:39] collecce, in momento in cui viene abilitato l'ingresso per andarlo a valutare, può essere,
[00:01:39 - 00:01:49] diciamo, regolarizzato, sincronizzato, scusatemi, da un segnale e Frippleflop prevede proprio
[00:01:49 - 00:01:58] che ci sia un segnale apposito per la sincronizzazione e il simbolo, vedete, riporta questo triangolino
[00:01:58 - 00:02:04] fino a questo terzo segnale che è il segnale di sincronizzazione, che adesso andiamo a
[00:02:04 - 00:02:14] vedere, diciamo, in che modo avviene, appunto, la sincronizzazione, l'abilitazione del circuito.
[00:02:14 - 00:02:20] Abbiamo visto l'olta scorsa che con l'ecce pure potevamo fare il l'ecce temporizzato, il l'ecce di in
[00:02:20 - 00:02:29] cui avevamo, introducevamo appunto un segnale che abilitava il circuito a livello, però invece
[00:02:29 - 00:02:41] il Frippleflop triplicamente è su un fronte del segnale, però adesso li vediamo con calma.
[00:02:41 - 00:02:54] Diciamo che dal simbolo, questo simbolo schematico che vediamo ci può dare già un'indicazione
[00:02:54 - 00:03:01] sulla modalità di sincronizzazione sia a livello, se sul fronte di salita, sul fronte di discesse e così
[00:03:01 - 00:03:10] via, però vedete, si basano sempre sulle ecce di base, diciamo, sulle SR che abbiamo visto
[00:03:10 - 00:03:16] l'olta scorsa, su cui poi si vanno a costruire o a meglio, si vanno a integrare ulteriori porte,
[00:03:16 - 00:03:21] ulteriori circuiti per realizzare le diverse tipologie che stiamo vedendo.
[00:03:21 - 00:03:33] Allora, il Frippleflop abbiamo detto, si caratterizza per il fatto di dover essere abilitato da un segnale,
[00:03:33 - 00:03:44] non a livello, ma su che, diciamo, ma lavora su, su, su, o il fronte di salita o il fronte di discesse,
[00:03:44 - 00:03:52] in generale lavora su un segnale che è di tipo in pulsì, ognuno su un impulso che deve essere mandato
[00:03:52 - 00:04:02] al circuito, con l'idea di abilitare brevemente, in un tempo molto ridotto il circuito, in modo da
[00:04:02 - 00:04:13] campionare l'ingresso, da andare a memorizzare, da andare a valutare, e poi subito disabilitare il circuito stesso.
[00:04:13 - 00:04:22] Quindi vediamo adesso come si può realizzare, diciamo, un impulso.
[00:04:22 - 00:04:32] L'impulso si può realizzare con questa implementazione che vedete in figura, in che modo.
[00:04:32 - 00:04:42] Allora, questo semplicemente è un segnale che, il segnale A, vedete, viene mandato in ingresso a questa porta end,
[00:04:42 - 00:04:50] la solita porta dei abilitazioni che serve in genere per abilitare un percorso o un circuito,
[00:04:50 - 00:04:59] però vedete, l'ingresso A viene portato nell'ingresso C in maniera diretta,
[00:04:59 - 00:05:07] mentre l'ingresso B passa per un invertitore. Questo cosa comporta che,
[00:05:07 - 00:05:14] vando a vedere nella realtà, abbiamo detto che le porte introducono sugli tardi,
[00:05:14 - 00:05:29] dovute dire che è il segnale che si propaga dall'ingresso all'uscita e quindi la presenza o la propagazione di un segnale
[00:05:29 - 00:05:38] non è istantanea, ma impiega un certo intervallo di tempo, che può essere piccolo quanto si vuole, ma non è nullo.
[00:05:39 - 00:05:41] Il segnale viene sfalzato.
[00:05:41 - 00:05:51] Sì, diciamo che nei momenti in cui, per esempio, da A passa da 0 a 1, ok, quindi A è alto,
[00:05:51 - 00:05:53] C è alto.
[00:05:53 - 00:06:00] Da B c'è uno sfalzamento rispetto a C.
[00:06:00 - 00:06:08] Sì, questo è l'obiettivo, creare un piccolo ritardo con cui arriva a B rispetto a C.
[00:06:08 - 00:06:19] Ovviamente questa è una porta-end, cosa vuol dire, e nel momento in cui uno dei due segnali è 0,
[00:06:19 - 00:06:26] in uscita ci sarà 0, e sarà alto solo quando sono alti entrambi gli ingressi.
[00:06:27 - 00:06:36] Quindi, se andiamolo con il disegno che è più semplice,
[00:06:39 - 00:06:53] allora D è l'uscita della porta-end, poi abbiamo B, diciamo, e C è il risultato
[00:06:53 - 00:07:06] della porta-end, allora partiamo da A, ah, vedete, finché A è basso, cosa succede?
[00:07:06 - 00:07:21] Poche A è basso in C, che sarebbe A alla fine, C è 0, e quindi B end C fa 0, a prescindere
[00:07:21 - 00:07:29] dal valore di B, però B ovviamente essendo invertito rispetto ad A è alto, quindi veniamo
[00:07:29 - 00:07:40] da una situazione a livello, diciamo, in cui A è 0, C è 0 e B è alto, B end C è 0 anche
[00:07:40 - 00:07:51] esso, e ovviamente D è anche esso il 0. Ora, immaginiamo che a certo punto il segnale
[00:07:51 - 00:08:04] A diventa alto, quando A diventa alto, vedete, C, possiamo dire che diventa alto in contemporaneo,
[00:08:04 - 00:08:12] poi ci stiamo ritenendo il ritardo di proprio vacazione sul filo, diciamo, praticamente nulla
[00:08:12 - 00:08:17] e questo è accettabile, perché non c'è niente in mezzo, se invece mette il filo,
[00:08:17 - 00:08:25] meno che il filo non sia lunghissimo, il ritardo, diciamo, lo trascurabile, e quindi
[00:08:25 - 00:08:37] C, vedete, è sincronizzato con A, B invece, poi che c'è l'invertitore, A diventa alto,
[00:08:37 - 00:08:43] ora B dovrebbe diventare basso perché deve essere negato di A, però nel fattempo che
[00:08:43 - 00:08:53] il segnale A alto passa nell'invertitore e raggiunge B, c'è un piccolo intervallo di
[00:08:53 - 00:08:57] tempo, diciamo, che è il ritardo della porta. Durante questo piccolo intervallo di tempo,
[00:08:57 - 00:09:06] B si mantiene ancora alto, cioè l'uscita, o meglio, all'ingresso della porta END,
[00:09:06 - 00:09:14] scusate mi si è vado avanti e indietro, non è ancora arrivato il negato di A, c'è ancora
[00:09:14 - 00:09:19] il vecchio valore di B, scusate, io metto quello qua, per questo bilo vediamo ancora alto.
[00:09:20 - 00:09:30] In questo piccolo intervallo di tempo, delta, quindi, ci troviamo che C e B sono entrambi
[00:09:30 - 00:09:50] alti e quindi, in uscita, diciamo, della END, dobbiamo avere alto, ovviamente anche in questo
[00:09:50 - 00:09:58] caso ci sarà un piccolo ritardo finché il risultato della END arriva a D e quindi vediamo
[00:09:58 - 00:10:08] di leggermente spasato rispetto a questo B END C, però poi non appena passa questo delta che
[00:10:08 - 00:10:14] immaginiamolo come tempo, come ritardo, di tutte queste porte coinvolte, quindi sia dell'invertitore
[00:10:14 - 00:10:23] che della END, che succede, che B finalmente si accorge che A è diventato alto e quindi B va
[00:10:23 - 00:10:38] a zero e ovviamente adesso la END, la negazione, diciamo, tra B e END C va a zero e quindi va a
[00:10:38 - 00:10:47] zero con un piccolo delta poi effettivamente D va a zero anche lui e quindi il risultato finale
[00:10:47 - 00:10:58] qual è? Che il segnale D risulta essere un segnale, vedete, impulsivo, che cioè che per lo più è
[00:10:58 - 00:11:06] a livello basso, tranne questo piccolo delta, ingurisciamo ad farlo diventare alto, si parla
[00:11:06 - 00:11:15] dei, ci vedete, circa, cioè, meno di 5 nanosecondi, quindi per realizzare, diciamo, questo segnale
[00:11:15 - 00:11:22] impulsivo non abbiamo introdotto nuove porte semplicemente, si sfrutta il ritardo delle porte
[00:11:22 - 00:11:31] stesse. Che ci facciamo con questo segnale? Ora ricordiamo, vedete, questa configurazione che poi
[00:11:31 - 00:11:40] è quella che abbiamo anche incontrato la volta scorsa nell'HD, questa cosa la andiamo a usare per
[00:11:40 - 00:11:51] abilitare il LCD dell'altra volta. Vedete, anche l'avevamo l'invertitore che negava il segnale per
[00:11:51 - 00:11:57] mandare questo, il LCD, se ricordate l'abbiamo introdotto per evitare la configurazione vietata 1.1.
[00:11:57 - 00:12:05] Questo invertitore e questa NEND, invece, connessi in questo modo che abbiamo visto oggi, abbiamo
[00:12:05 - 00:12:13] detto, realizza un impulso. Quindi io, in ingresso, diciamo, il segnale di clock, in generale, il
[00:12:13 - 00:12:23] segnale di abilitazione del circuito è un segnale a livello. Però, nei momenti in cui, diciamo,
[00:12:23 - 00:12:32] passa da un livello all'altro, produce in uscita un segnale impulsivo di questo tipo, come questo
[00:12:32 - 00:12:43] di. Quindi il segnale che arriva qui ad abilitare il LCD è impulsivo e noi abbiamo visto anche l'altra
[00:12:43 - 00:12:51] volta, una volta, in cui andiamo ad abilitare il LCD, siamo semplicemente campionando il valore di D.
[00:12:51 - 00:13:01] Quindi, se D è 1, prendiamo il valore 1 e lo andiamo a ammettere, diciamo, in questo circuito di
[00:13:01 - 00:13:10] memoria, quindi lo stato diventerà 1. Se il valore di D è 0, vuol dire che andiamo a memorizzare 0.
[00:13:10 - 00:13:20] Ovviamente, nel momento in cui questo impulso che abbiamo generato torna a 0, si disabilita
[00:13:20 - 00:13:32] il LCD, nel senso che viene forzato in ingresso all'HSR che si trova all'estrema destra, diciamo,
[00:13:32 - 00:13:39] di questo circuito, il che vuol dire mantieni lo stato che abbiamo adesso campionato. Quindi,
[00:13:39 - 00:13:45] siamo mettendo insieme i vari pezzetti che abbiamo visto fino ad oggi, quindi, scusatemi,
[00:13:46 - 00:13:56] l'HSR, la configurazione del LCD per abilitare il circuito ed evitare la configurazione 1.1, più
[00:13:56 - 00:14:04] questo circuito che mi rende il segnale di abitazione impulsivo mi realizza appunto un circuito,
[00:14:04 - 00:14:13] il circuito totale, diciamo, che è un circuito che mi va a memorizzare un'informazione binaria che
[00:14:13 - 00:14:21] posso abilitare in maniera impulsiva, diciamo, sul fronte, ad esempio, di salita di questo segnale
[00:14:21 - 00:14:41] di abilitazione. E questo, diciamo, è il circuito per generare, diciamo, un flip flop. Abbiamo detto,
[00:14:41 - 00:14:50] però, che, diciamo, dallo schema, diciamo, dal simbolo che vediamo vicino a segnale di
[00:14:50 - 00:14:59] abitazione possiamo capire che tipologia di circuito è. Alla fine abbiamo detto tra
[00:14:59 - 00:15:13] l'Hatch e il flip flop cambia solo il modo in cui viene abilitato, nel momento in cui noi qui
[00:15:13 - 00:15:20] abbiamo visto con l'abilitazione sul fronte di salita, no, di tipo impulsivo, però in genere
[00:15:20 - 00:15:28] voi potete trovare questi simboli dei flip flop che vedete hanno sul segnale di abitazione diverse
[00:15:28 - 00:15:35] tipologie di simboli. Quando c'è il triangolo, come abbiamo visto prima, è il classico
[00:15:35 - 00:15:47] circuito, diciamo, abilitato sul fronte di salita. Se, vicino all'altriangolo, c'è anche il pallino,
[00:15:47 - 00:15:55] vuol dire che invece sul fronte di discesa. Se invece non c'è il triangolo, vuol dire che quel
[00:15:55 - 00:16:04] segnale, cioè che fu il circuito, è abilitato sul livello del segnale, quindi nel primo caso vedete
[00:16:04 - 00:16:10] c'è solo il filo, vuol dire che di quando quel segnale è alto il circuito è abilitato, quando è
[00:16:10 - 00:16:19] basso è disabilitato. Se invece c'è il pallino è il contrario, quindi è abilitato sul livello basso
[00:16:19 - 00:16:30] e quindi abbiamo queste quattro combinazioni possibili. Ovviamente quando abbiamo l'abilitazione
[00:16:30 - 00:16:38] sul livello non è altro che un latch di temporizzato, come abbiamo visto la volta scorsa. Se invece abbiamo
[00:16:38 - 00:16:45] il triangolino, quindi un'abilitazione sul fronte di salita o di discesa, lo chiameremo flip flop.
[00:16:49 - 00:16:52] C'è uno lavoro sul livello o l'altro sul fronte?
[00:16:54 - 00:17:05] Sì, è come questo circuito qui, se il livello viene mandato direttamente qua, senza questo circuito
[00:17:05 - 00:17:12] che abbiamo visto oggi, sarà un latch di temporizzato. Se introduciamo questa parte per fare il fronte di salita
[00:17:13 - 00:17:21] o lo colleghiamo diversamente per farvi il fronte di discesa, diciamo comunque, realizziamo il flip flop.
[00:17:21 - 00:17:28] Quindi stiamo sempre parlando di circuiti di memoria, a questo punto li possiamo chiamare a un bit
[00:17:28 - 00:17:37] in cui con queste configurazioni particolari evitiamo la configurazione 1.1 e abilitiamo il circuito
[00:17:37 - 00:17:46] a memorizzare o meglio a campionare il valore di interesse, quindi questo D in ingresso,
[00:17:46 - 00:17:53] a salvarlo e poi quando disabilitiamo il circuito intendiamo che andiamo a forzare
[00:17:53 - 00:18:03] lo stato S00 e quindi mantieni lo stato. Cioè questi circuiti di memoria in che sono alimentati
[00:18:03 - 00:18:13] mantendono il valore memorizzato e poiché l'ingresso di ulteriori valori, il salvataccio,
[00:18:13 - 00:18:20] diciamo ulteriori valori disabilitato, viene abilitato solo quando ci arriva il segnale
[00:18:21 - 00:18:30] un livello alto nel caso di latch di temporizzato oppure un fronte di salita di un clock o di un
[00:18:30 - 00:18:34] altro segnale, diciamo, sul fronte di salita nel caso di flip flop.
[00:18:44 - 00:18:52] Come detto prima questo qua sulla destra c'è il semplice segnale di abilitazione l'abbiamo
[00:18:52 - 00:18:59] visto la volta scorsa quando è alto e abilitato quando è basso memorizza. Se mettiamo il pallino
[00:18:59 - 00:19:06] semplicemente funziona al contrario, come meglio questi sono, diciamo, se trovate questi simboli
[00:19:06 - 00:19:13] dovete capire che in indiano questi due sono due latch temporizzati con abilitazione sul fronte
[00:19:13 - 00:19:20] alto oppure quello in giù, diciamo, con il pallino sul fronte, sul livello basso, scusate.
[00:19:20 - 00:19:31] Invece nel caso di simboli col triangolo sono ad abilitazione sul fronte di salita o di discesa
[00:19:31 - 00:19:40] a seconda del simbolo, diciamo, il ragionamento di come viene memorizzata l'informazione più o
[00:19:40 - 00:19:53] meno resta quello che abbiamo già visto varie volte. Il flip flop come quelli che abbiamo
[00:19:53 - 00:20:00] visto tipicamente hanno entrambi le uscite, quindi sia il valore Q che il complementare.
[00:20:01 - 00:20:11] Possiamo trovare il flip flop con ulteriori input aggiuntivi per forzare il valore dello
[00:20:11 - 00:20:17] stato, il set o il reset, quindi indimendentemente dalla linea di ingresso a cui sono collegate
[00:20:17 - 00:20:26] che ovviamente aumenta la versatilità del circuito, ma si complica, diciamo, la circuiteria.
[00:20:26 - 00:20:37] In differenza, abbiamo visto varie volte divente dal tipo di transizione sul clock,
[00:20:37 - 00:20:46] questo segnale di abilitazione, andiamo avanti. Vediamo adesso i registri. Con lo stesso ragionamento
[00:20:46 - 00:20:52] che ovviamente abbiamo fatto quando abbiamo visto l'alu per esempio in cui noi abbiamo ragionato
[00:20:52 - 00:20:58] su il single of bit, operazioni sul single of bit, quindi abbiamo visto come collegare
[00:20:58 - 00:21:07] opportunamente, diciamo, i circuiti fondamentali per realizzare, diciamo, un circuito che lavora
[00:21:07 - 00:21:15] sotto bit, su un byte o su più byte, sono diciamo generalizzabili le cose che stiamo vedendo a più
[00:21:15 - 00:21:22] byte, a una string di byte, di bit, scusate me. Allo stesso modo, abbiamo detto che il flip
[00:21:22 - 00:21:36] flop è... C'è un refuso nella slide. Dove? O3, O3. O3 non c'è. No, I3 manca. Sì,
[00:21:36 - 00:21:47] quello là in atto al destra è I3. Giusto? Sì, dovrebbe essere I3, quel D. Sì, perché c'è D.
[00:21:47 - 00:21:55] C'è D, vuol dire che è l'ingresso, quindi immaginiamo da avere una stringa di bit, di 8-bit,
[00:21:55 - 00:22:04] fare un registro, diciamo, di 8-bit, un registro di memoria di 8-bit, vuol dire collegare, diciamo,
[00:22:04 - 00:22:16] ogni linea di input questi 0, i1, i2, i3, come giustamente suggerisci, ha dei corrispondenti,
[00:22:16 - 00:22:23] diciamo, di uno di essi, ha un flip flop di... come quelli che abbiamo visto prima. Qui,
[00:22:23 - 00:22:31] queste sono 8 flip flops tutti uguali, vedete, che hanno semplicemente un uscita Q, qui non c'è
[00:22:31 - 00:22:39] Q negato. L'ingresso D lo vado a collegare alla linea l'ingresso che devo andare a memorizzare.
[00:22:45 - 00:22:53] Poi il clock, vedete, sono tutti impostati, cioè sono tutti impostati sul fronte di discesa,
[00:22:53 - 00:23:07] che vedete, c'è il triangolo e il pallino. Però, vedete, il clock generale. Abbiamo un
[00:23:07 - 00:23:15] segnale di clear, abbiamo detto che è collegato a tutti i flip flops, nel caso si voglia alzerare
[00:23:15 - 00:23:23] l'intero registro, collegato col pallino, quindi quando questo segnale clear si trova a livello
[00:23:23 - 00:23:35] basso, si attive, quindi a zero questi flip flops. Dicevo, il clock, vedete, piuttosto che farlo con
[00:23:35 - 00:23:46] questo registro di 8 bit, invece di farlo con dei flip flops attivati sul fronte di salita
[00:23:47 - 00:23:56] collegati al clock, sono stati collegati. In questa figura ha 8 flip flops abilitati sul fronte
[00:23:56 - 00:24:07] di discesa e il clock, però, non è collegato direttamente a questi flip flops, ma passa
[00:24:07 - 00:24:18] per una negazione, un invertitore. Questo vuol dire che quindi alla fine non è vero che si
[00:24:18 - 00:24:25] attiveranno sul fronte di discesa del clock, perché quando il clock va sul fronte di discesa
[00:24:26 - 00:24:35] il inverter genererà un segnale che invece va sul fronte di salita e quindi non abiliterà
[00:24:35 - 00:24:42] i registri. Quando invece il clock va sul fronte di, si trova sul fronte di salita,
[00:24:43 - 00:24:48] l'invertitore genererà un fronte di discesa che andrà ad abilitare i registri.
[00:24:49 - 00:24:55] Quindi alla fine tutto questo registro di memoria si abilita sul fronte di salita,
[00:24:57 - 00:25:02] quindi e a che serve? Perché è stata inserita questa doppia negazione alla fine?
[00:25:04 - 00:25:14] Questo è un approccio che viene spesso utilizzato, perché immaginate che questo è un segnale
[00:25:14 - 00:25:22] di clock collegato su tutta la macchina o comunque su molti dispositivi, quindi è molto
[00:25:22 - 00:25:29] lontano da dove è stato generato. E allora un approccio di più che si utilizza è quello
[00:25:29 - 00:25:37] di amplificarlo mandandolo dentro un invertitore, perché questo invertitore ovviamente sarà
[00:25:37 - 00:25:48] alimentato, oltre a negare il valore dell'ingresso lo alimenterà, cioè lo amplificará, scusate,
[00:25:48 - 00:25:57] quindi lo riporterà a un livello accettabile in uscita. E quindi questa forzatura di mettere
[00:25:57 - 00:26:02] questo invertitore quando poi, diciamo, potevo collegare dietro del clock al developer clock
[00:26:02 - 00:26:07] di topologia diverso, viene fatto per introdurre, perché si sfruttano, diciamo,
[00:26:08 - 00:26:18] degli invertitori per, diciamo, ritare forza al segnale, per amplificare il segnale che
[00:26:18 - 00:26:22] potrebbe arrivare, diciamo, un po' attenuato rispetto a dove è stato generato.
[00:26:22 - 00:26:24] Stabilizza il segnale?
[00:26:24 - 00:26:28] Si, lo amplifiche effettivamente.
[00:26:38 - 00:26:44] E questo abbiamo detto, il tanzenero del clock, ovviamente, quando quindi il fronte di salita
[00:26:44 - 00:26:56] del clock, tutti, diciamo, i registri vengono abilitati e quindi viene acquisita l'intera
[00:26:56 - 00:27:08] stringa di 8-bit. Dopo quel delta che abbiamo visto prima, i flip-flop vengono disabilitati,
[00:27:08 - 00:27:14] disabilitati nel senso che passano nello stato di memorizzazione, quindi il valore che sta
[00:27:14 - 00:27:18] campionato, che è stato letto, di questi 8-bit, vuole, resta in memoria.
[00:27:24 - 00:27:29] Ecco qua, la cosa che vi accendavo prima, il invertitore è stato introdotto proprio per
[00:27:29 - 00:27:32] amplificare il segnale del clock.
[00:27:32 - 00:27:45] Il clear abbiamo detto semplicemente a cancellare veramente tutti i flip-flop,
[00:27:45 - 00:27:55] cioè forzarli a zero, indipendentemente quindi di dove si trovi il clock.
[00:27:55 - 00:28:01] Infatti il clear, vedete, sono a livello, sono dei semplici segnali a livello,
[00:28:01 - 00:28:07] negati, quindi quando il clear viene forzato, cioè arriva, si trova nello stato a zero,
[00:28:08 - 00:28:13] abilita il clear di tutti i flip-flop che non fa un altro che settare a zero Q.
[00:28:21 - 00:28:27] Ovviamente, come abbiamo visto sempre, quando abbiamo fatto i sommatori, le alu,
[00:28:27 - 00:28:33] questo discorso può essere steso a più-bit, possiamo realizzare una memoria,
[00:28:33 - 00:28:39] un registro, le scusate mi ha 32-bit, come abbiamo visto
[00:28:41 - 00:28:49] così, collegato fino a 32-bit, oppure si possono usare degli approcci gerarchici,
[00:28:49 - 00:28:56] nel senso che se abbiamo dei registri a 8-bit li possiamo combinare per creare un registro
[00:28:56 - 00:29:04] a 16-bit, oppure se abbiamo un registro a 32-bit li possiamo nire e fare dei registri a 16-bit,
[00:29:04 - 00:29:12] quindi sono modulari, cioè i miei amori, i registri si possono realizzare in maniera modulare
[00:29:12 - 00:29:20] unendo componenti persistenti più piccole oppure facendole, come abbiamo visto ora,
[00:29:21 - 00:29:28] alla fine questo è comunque un registro a 1-bit che sto usando in maniera modulare,
[00:29:28 - 00:29:36] se i registri che ho a disposizione sono già di loro, soccustato dei registri a più-bit,
[00:29:36 - 00:29:46] li posso unire e combinare a creare una memoria più grande, ovviamente devo sempre ricordarmi
[00:29:46 - 00:29:52] o comunque stare attento, diciamo, a unire poi opportunamente i clock e i clear,
[00:29:52 - 00:29:57] cioè perché il clock deve essere unico per tutti i registri coinvolti e ovviamente il clear
[00:29:57 - 00:30:03] lo stesso e se ci sono altri segnali, non abbiamo detto se c'è il set o altri input,
[00:30:03 - 00:30:10] ci deve essere un unico segnale che va ad alimentare contemporaneamente tutti i registri coinvolti.
[00:30:17 - 00:30:18] Ci sono domande.
[00:30:37 - 00:30:41] Lascio questa figura che assume tutto.
[00:30:42 - 00:30:51] Questo c'è stato veloce, ovviamente è sempre preso dal libro che dovresti sempre poter vedere
[00:30:51 - 00:30:56] tutti quanti. Capito l'ultra di questa, no?
[00:31:41 - 00:31:49] Beh, se io ho terminato, se non ci sono domande potete anche allontanar,
[00:31:49 - 00:31:58] diciamo, lascio comunque la lezione attiva in modo che possiamo raggiungere il tempo
[00:31:58 - 00:32:02] che vi serve a voi per la presenza, però potete allontanarvi o sono in attesa,
[00:32:02 - 00:32:08] cioè resto qui in linea se avete bisogno di informazioni di qualunque tipo.
[00:32:12 - 00:32:15] Grazie prof.
[00:32:15 - 00:32:20] Grazie prof, io avrei una domanda al di fuori di questa lezione,
[00:32:20 - 00:32:29] siccome per motivi di lavoro non sono riuscito a seguire tutte le altre lezioni,
[00:32:29 - 00:32:36] dopo il mese di marzo si ripete lezioni per recuperarle?
[00:32:37 - 00:32:43] Dovrebbero ripetersi, diciamo, nell'arco dell'anno, però non so dirti quando,
[00:32:43 - 00:32:46] non so quando è prevista la prossima ripetizione.
[00:32:51 - 00:32:54] Io da quello che avevo capito, da maggio, può essere?
[00:32:55 - 00:32:56] Sì, può essere.
[00:32:56 - 00:33:01] C'era tipo priv' di pausa e poi da maggio.
[00:33:01 - 00:33:10] Ho la stessa informazione, so che dovrebbero esserci un altro ciclo prima dell'estate,
[00:33:10 - 00:33:17] quindi maggio, giugno, luglio e probabile, però non mi è stata letta la fascia di giorni.
[00:33:19 - 00:33:24] Ok, va bene, perché tanto io l'esame ce l'ho autobre, quindi vado che bene.
[00:33:24 - 00:33:28] Però ecco, solo per seguire le lezioni ho mancato
[00:33:29 - 00:33:31] nelle settimane precedenti.
[00:33:32 - 00:33:39] Io ho capito che quando la buona introdotta questa didattica qui,
[00:33:39 - 00:33:46] e dovrà essere due barra tre cicli, giustamente non sono due, ma ci sarà anche il terzo.
[00:33:48 - 00:33:53] Cioè, perché comunque, ma non credo che siano più di tre.
[00:33:54 - 00:34:02] Io so, anche io due barra tre, però non ho un calendario che mi dice tutto l'anno,
[00:34:02 - 00:34:03] quando devo fare le lezioni.
[00:34:06 - 00:34:13] Ho capito, va bene, altanto, ecco, ripeto, io per esempio l'appello ce l'ho autobre,
[00:34:13 - 00:34:20] quindi va più che bene se a maggio, giugno, luglio vengono ripetute le lezioni,
[00:34:20 - 00:34:23] in senso stompi a mienteni tempi, senza problemi.
[00:34:23 - 00:34:30] No, l'informazione è che ci dovrebbe essere un'altra ripetizione, per avere del taglio,
[00:34:30 - 00:34:35] diciamo, precisione quando, forse in secretaria, possono darti qualche informazione in più.
[00:34:36 - 00:34:37] Ok, grazie mille.
[00:34:37 - 00:34:41] Mi sfugge, adesso, mi sembra che non mi è stato comunicato.
[00:34:43 - 00:34:44] Va bene, grazie.
[00:35:21 - 00:35:25] Diciamo che, come materiale a spiegare, c'era di più su latch,
[00:35:25 - 00:35:30] perché forse era tutto pre-pedeutico, questo qui del flip-flop c'è un po' più...
[00:35:32 - 00:35:38] Sì, in più abbiamo introdotto solo questo circuito per capire l'impurso come viene generato.
[00:35:39 - 00:35:45] L'invertitore, la parte invertente che fa da...
[00:35:45 - 00:35:50] Sì, diciamo, la logica che poi si mettono insieme e si fanno memorie più grandi,
[00:35:50 - 00:35:52] penso sia abbastanza semplice.
[00:36:00 - 00:36:05] Sì, sì, agiscono tutti in parallelo, che prendono lo stesso segnale di clock e di clear,
[00:36:05 - 00:36:08] quindi sono sincronizzati dal clock.
[00:36:08 - 00:36:13] Questa è l'idea di avere, diciamo, il clock che dà il via a tutti i flip-flops e dice...
[00:36:15 - 00:36:22] Memorizzate, diciamo, campionate e poi, quando passa l'abilitazione, memorizzate.
[00:36:29 - 00:36:30] La volta scorsa c'era molto...
[00:36:30 - 00:36:35] A questo flip-flop c'era molto più materiale, è andato abbastanza più spedito,
[00:36:36 - 00:36:41] c'era probabilmente più slide, adesso non so le quante slide c'era, però...
[00:36:42 - 00:36:44] Sono andato troppo veloce oggi.
[00:36:45 - 00:36:54] Ah, oppure oggi, ok, oppure oggi è andato troppo veloce, ok, è giunto a 35, ho visto che l'ho già finito.
[00:36:57 - 00:37:00] Sì, ma hai qualche dubbio sulla lezione precedente?
[00:37:00 - 00:37:01] No.
[00:37:01 - 00:37:02] Possiamo parlare di quello?
[00:37:03 - 00:37:12] No, no, no, non ho una domanda, ma se questo registro lo volessimo, diciamo,
[00:37:12 - 00:37:18] tramutare in un oggetto fisico, tutti gli ingressi e gli usciti sarebbero i pin dei chip che vanno poi
[00:37:18 - 00:37:22] assemblati insieme o avrebbe una forma differente?
[00:37:27 - 00:37:29] C'è gli ingressi e gli usciti?
[00:37:30 - 00:37:37] Gli ingressi e gli usciti devono essere pin del circuito sicuramente, poi se effettivamente
[00:37:37 - 00:37:42] vengono disposti così o con una forma geometrica diversa interna,
[00:37:44 - 00:37:54] questo poi dipende da condizioni fisiche, il cipro puoi anche vedere così fisicamente,
[00:37:54 - 00:38:00] con i quattro pin sopra e sotto, però poi dentro se sono organizzati così vabbè visto
[00:38:01 - 00:38:07] o cambiano come il discorso dell'interfaccia e dell'implementazione, sicuramente il circuito
[00:38:07 - 00:38:14] avrà un'interfaccia con tutti questi pin, poi effettivamente dentro può essere così,
[00:38:14 - 00:38:21] cioè didatticamente è così, ma nella realtà probabilmente vengono disposti in maniera
[00:38:21 - 00:38:28] per migliorare, cioè per ridurre la dissipazione, ridurre lo spazio, cose di questo tipo.
[00:38:51 - 00:39:10] Considera poi che tutti questi registri di memoria, se sono i immagini dei registri del
[00:39:10 - 00:39:17] processore, la luca abbiamo visto altra volta, nei processori moderni dove di solo,
[00:39:18 - 00:39:22] cioè non si vedono neanche più i pin per come sono densi e vicini tra di loro,
[00:39:26 - 00:39:34] quindi capire che incontro e dire ci sono i pin che poi si collegano a questi circuiti,
[00:39:34 - 00:39:44] ma poi ci sono così tanti circuiti integrati tra loro che sicuramente il processore non
[00:39:44 - 00:39:50] sono disposti così come li vediamo in figura, però il concetto è chiaro.
[00:39:50 - 00:40:15] Vabbè, potete allontanarvi, lascio aperto ancora un po' però ci possiamo salutare. Ci vediamo la
[00:40:15 - 00:40:22] prossima lezione. Grazie, buona giornata. Grazie anche voi, buona giornata. Grazie.
[00:40:33 - 00:40:36] Professore, posso farle una domanda ma più che altro, una curiosità?
[00:40:37 - 00:40:45] Vimmi. Se si avesse voglia per esempio di provare a costruire questo tipo di circuiteri e non
[00:40:45 - 00:40:51] so tramite una basetta, acquistando dei componenti ma proprio così a livello amatoriale,
[00:40:51 - 00:40:59] entendo, esistono in commercio luoghi o comunque materiali acquistabili con cui,
[00:40:59 - 00:41:05] non so, metto insieme due porte, tre porte in hand per fare questi, diciamo,
[00:41:05 - 00:41:08] questi tipi di circuiti che stiamo vedendo insieme a lei.
[00:41:08 - 00:41:20] Sì, nel senso che esistono delle basette che si possono comprare in cui andare a inserire delle
[00:41:20 - 00:41:29] board, diciamo, di andare inserire dei circuiti, diciamo, più semplici di ogni un processore per
[00:41:29 - 00:41:36] andare a fare cose elementari, però di cercare nel campo dell'elettronica in generale, capito?
[00:41:36 - 00:41:47] Ci dovrebbero essere dei circuiti integrati che implementano esattamente questo registro
[00:41:47 - 00:41:57] a 8-bit. Le avevo scritto in chat. Ah, mi hai scritto in chat? Sì. Guarda, io non l'ho mai
[00:41:57 - 00:42:12] cercato sinceramente. Sì, ricordo bene. Ho visto tante volte che nel campo dell'elettronica si
[00:42:13 - 00:42:20] vendono, detto, delle board in cui andare a mettere i circuiti integrati, ma quali circuiti,
[00:42:20 - 00:42:30] non occupandomi di elettronica, non ti saprei indicare. Sì, il 3.7.4 ha proprio ingressi
[00:42:30 - 00:42:37] uscite mescolati insieme. Il 5.7.4 dovrebbe avere gli ingressi tutti da un lato e le uscite dall'altro
[00:42:37 - 00:42:48] lato del chip. Sì, sono proprio che registri a 8-bit? Esatto. Ok, quindi... Sì, questa cosa,
[00:42:48 - 00:42:54] io la confermo qualche rimaniscenza delle superiori di elettronica che ho fatto quasi 20 anni fa.
[00:42:54 - 00:43:05] Ma già c'erano queste cose, quindi sì. Grazie a tutti per le risposte. No, fico, la
[00:43:05 - 00:43:12] diciamo, scopriamo insieme quello che ormai oggi si può fare qualunque cosa, quindi penso
[00:43:12 - 00:43:15] che puoi trovare molti circuiti che vanno a implementare queste cose.
[00:44:24 - 00:44:25] Sì.
[00:44:54 - 00:45:22] Ok, io chiudo allora, vi saluto. Grazie profa, la prossima lezione.
[00:45:25 - 00:45:28] Grazie, buona giornata.
[00:45:34 - 00:45:36] Buona giornata, grazie.
