# lezione3

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\lezione3.mp4`
- Durata: 00:46:07
- Trascrizione: `03_lezione3.json`

## Argomenti probabili
- porte_logiche (240): and, or, not, nor, nand, sop
- conversioni (19): binario, base
- mips_assembly (10): registri, sb, addi
- memoria_bus (3): memoria, ram
- microarchitettura (2): alu

## Trascrizione

[00:00:00 - 00:00:23] In questo momento, due minuti e cominciamo.
[00:00:23 - 00:00:25] Buon appetito!
[00:00:53 - 00:00:55] Buon appetito!
[00:01:23 - 00:01:25] Buon appetito!
[00:01:53 - 00:02:18] Allora, oggi vediamo qualcosa sull'artematica binaria.
[00:02:18 - 00:02:30] Se vi ricordate, abbiamo detto che nei Calcolatori, i sistemi di numerazioni sono sistemi a precisione finita,
[00:02:30 - 00:02:39] proprio perché abbiamo un numero finito di bit di registri di memoria,
[00:02:39 - 00:02:52] e questo comporta delle limitazioni o comunque delle differenze rispetto alla rettamedica classica.
[00:02:52 - 00:03:04] Abbiamo parlato del fatto che alcune proprietà della rettamedica che vagano in generale sono ancora validi nei sistemi di numerazione,
[00:03:04 - 00:03:10] a codifica ad esempio binaria, o in generale quando passiamo da una base all'altra,
[00:03:10 - 00:03:13] se un numero abbiamo detto è divisibile per un altro,
[00:03:13 - 00:03:18] oppure se un numero è periodico in una base, quando poi passiamo in un'altra base,
[00:03:18 - 00:03:25] queste proprietà cambiano, possono non più persistere, tipicamente non persistono diciamo.
[00:03:26 - 00:03:32] Oggi vediamo alcune operazioni rettemediche fondamentali, molto semplici,
[00:03:32 - 00:03:36] potremmo usare l'addizione ad attrazione alla moltiplicazione.
[00:03:39 - 00:03:47] Per quanto riguarda l'addizione, vediamo che quando effettiamo queste operazioni rettemediche,
[00:03:47 - 00:04:08] e in questo caso con l'addizione, tutto sommato possiamo seguire le regole, le proprietà che valgono nelle operazioni classiche,
[00:04:08 - 00:04:16] nel senso che approcciamo queste operazioni seguendo regole abbastanza simili.
[00:04:16 - 00:04:23] Quindi quando andiamo a fare la somma tra i due numeri binari useremo un procedimento molto simile
[00:04:23 - 00:04:32] a quello che usiamo normalmente nel sistema decimale, quindi si parte dalle scifre meno significative,
[00:04:32 - 00:04:39] si va a effettuare la somma tra le scifre corrispondenti in base alla posizione,
[00:04:39 - 00:04:48] la prima cosa è mettere in colon secondo il peso le scifre dei due numeri da sommare,
[00:04:48 - 00:04:57] e poi valerò il stesso ragionamento sul riporto, come nel decimale quando la somma tra due numeri
[00:04:57 - 00:05:04] dà un valore teorico che supera il valore della singola scifra, che tipicamente,
[00:05:04 - 00:05:10] se vi ricordate quando abbiamo visto i vari sistemi di operazione su base genetiche abbiamo sempre detto
[00:05:10 - 00:05:17] le scifre disponibili sono quelle che vanno da zero a i meno uno, quindi nel decimale,
[00:05:17 - 00:05:21] se abbiamo un ministro quelle scifre sono da zero a nove e in tutto sono dieci,
[00:05:21 - 00:05:27] nel binario ovviamente le scifre sono due, sono zero e uno, sempre minore di b e meno uno,
[00:05:27 - 00:05:33] quindi quando la somma di due scifre dà un valore che teoricamente non vuol essere rappresentato
[00:05:33 - 00:05:41] sulla singola scifra si genera un riporto che si propaga alla sinistra delle scifre che lo hanno generato.
[00:05:45 - 00:05:52] Nel caso in cui dobbiamo fare la somma tra due numeri, tra due scifre binari,
[00:05:52 - 00:06:04] soltanto, perché come al solito nel mondo binario noi abbiamo che possiamo calcolare o meglio definire
[00:06:04 - 00:06:09] tutte le possibili combinazioni, in tutti i casi possibili, facilmente perché alla fine
[00:06:09 - 00:06:15] se abbiamo due scifre da sommare a più un b e ogni scifre può assumere il valore o zero o uno
[00:06:15 - 00:06:21] alla fine, converrete che le sono quattro e possibili casi che ci possiamo trovare e quindi
[00:06:21 - 00:06:28] possiamo scrivere una tabella dei possibili risultati e quindi sappiamo che se devo fare la somma
[00:06:28 - 00:06:35] tra zero e zero, quindi tra due scifre a b e valore o zero entrambe, il risultato sarà zero, così come faremmo
[00:06:35 - 00:06:43] nel sistema decimale, zero più uno è risultato fa uno, uno più zero risultato fa uno, quello che cambia
[00:06:43 - 00:06:50] che dobbiamo stare attenti nella dizione e quando facciamo la somma tra uno e uno,
[00:06:50 - 00:06:58] perché ovviamente nel decimale faremmo due, perché il valore teorico è due, ma nel binario
[00:06:58 - 00:07:08] ovviamente due, non c'abbiamo la scifra due, superiamo di meno uno, quindi questo genera un riporto
[00:07:08 - 00:07:16] e quindi il risultato della somma uno più uno in binario è zero col riporto di uno,
[00:07:17 - 00:07:25] riporto che va alla sinistra, alla prima scifra diciamo, a sinistra delle scifre che generano questa situazione.
[00:07:27 - 00:07:36] Ad esempio facciamo l'analogia prima col decimale e poi col binario, per vedere che le regole sono le stesse
[00:07:36 - 00:07:44] e cambiano le scifre a disposizione, i simboli a disposizione, quindi nel decimale banalmente mettiamo
[00:07:44 - 00:07:51] in ordine i due numeri 9 e 13 che dobbiamo sommare, li mettiamo incolonati secondo il peso, quindi le unità con le unità
[00:07:51 - 00:08:01] le decine, con le decine e così via, in questo caso vedete 9 più 3 va 12, non abbiamo la scifra 12 nel decimale
[00:08:01 - 00:08:10] quindi dobbiamo scrivere due con il resto di uno che si propaga, in questo caso nella colonna delle decine
[00:08:11 - 00:08:19] e si va a sommare con le scifre attualmente presenti in quella colonna, quindi 0 e 1 fa 1 più il riporto di 1 fa 2,
[00:08:19 - 00:08:28] 2 ce l'abbiamo e quindi il risultato è 22, nel binario in maniera analoga quanto dobbiamo fare la somma tra due numeri,
[00:08:28 - 00:08:35] in questo caso nelle sempre numeri sono 1, 0, 0, 1 e 1, 1, 0, 1, cosa facciamo?
[00:08:35 - 00:08:45] banalmente li mettiamo in ordine secondo il peso delle scifre e poi partendo dalla scifra meno significativa, cioè dalla scifra più a destra
[00:08:45 - 00:09:00] cominciamo a sommare, quindi 1 più 1 abbiamo detto prima fa 0 il riporto di 1, il riporto di 1 lo andiamo a mettere nella prima colonna a sinistra
[00:09:00 - 00:09:14] quindi nelle scifre di peso due alla uno, le scifre di peso due alla uno abbiamo 0 più 0, riporto fa 1, quindi ci spostiamo nella terza colonna
[00:09:14 - 00:09:27] qui non abbiamo riporti 0, quindi facciamo semplicemente dalla somma, 0 più 1 fa 1, nella quarta colonna di nuovo non abbiamo riporti
[00:09:27 - 00:09:40] facciamo semplicemente la somma tra le due scifre presenti nei numeri originali, 1 più 1 fa 0 con riporto di 1, il riporto si fa sommare
[00:09:41 - 00:09:56] cioè va a creare una nuova colonna alla fine e quindi abbiamo un ulteriore bit 1, quindi il risultato della somma tra 1, 0, 1 e 1, 1, 0, 1 è il numero in binario 1, 0, 1, 1, 0
[00:09:57 - 00:10:10] già qui potete osservare un concetto che tornerà spesso il fatto che vedete abbiamo due numeri su 4 bit, la somma è un numero a 5 bit
[00:10:10 - 00:10:18] che non è detto che noi possiamo rappresentare, se abbiamo ulteriore bit a disposizione lo riusciremo a rappresentare
[00:10:18 - 00:10:24] altrimenti si genererà quello che abbiamo visto la volta scorsa un errore di overflow
[00:10:24 - 00:10:34] il fatto che servirebbe teoricamente ulteriore bit per rappresentare l'informazione si deve scontrare con il numero di bit a dislosizione
[00:10:34 - 00:10:46] se noi abbiamo, siamo lavorando ragionando su un sistema di codifica a binario su 4 bit, vuol dire che tutti i numeri che si rappresentano a 5 bit non sono rappresentabili
[00:10:47 - 00:10:59] e quindi torniamo al concetto che i sistemi in numerazione a predecesione finita come ad esempio il sistema binario su 4 bit
[00:10:59 - 00:11:10] questo succede che un numero, se due numeri appartengono all'insieme non è detto che il risultato della somma appartenga, ok? non è che il suo rispetto alla somma
[00:11:11 - 00:11:20] qua banalmente qualche altro semplice esempio di somma tra numeri binari
[00:11:20 - 00:11:28] vedete quando abbiamo numeri che hanno diverso numero di bit a disloszione, che sono composti da un numero di bit diverso
[00:11:28 - 00:11:38] semplicemente li andiamo a mettere in colonna e se preferite potete aggiungere degli zeri a sinistra per riempire
[00:11:38 - 00:11:50] diciamo le colonne mancanti, come nel sistema decimale anche nel sistema binario ovviamente aggiungere zeri a sinistra non austerà il numero
[00:11:50 - 00:12:05] quindi in questo caso 1 0 1 0 0 più 1 1 1, ok? mettiamo in colonna e vediamo le prime colonne sono, cioè le prime due colonne sono banalmente 0 più 1 fa 1
[00:12:05 - 00:12:15] la terza colonna ci troviamo nel caso critico da analizzare con attenzione 1 più 1 fa 0 con riporto di 1
[00:12:15 - 00:12:24] questo riporto va a finire nella quarta colonna dove ci sono solo gli zeri quindi lo abbiamo come risultato 1
[00:12:24 - 00:12:41] e l'ultima colonna 1 più 0 fa 1 quindi c'è un unico riporto che si propaga dalla terza la quarta colonna e il risultato finale 1 1 0 1 1
[00:12:41 - 00:12:58] altro esempio sempre addizioni sempre molto semplice quindi avere numeri contatti in bit diventa solo più lungo da fare però è sempre molto semplice non aggiunge complessità reticolare
[00:12:59 - 00:13:14] anche qua abbiamo un numero da 7 bit da sommare il numero a 5 bit, nel secondo caso vedete ho aggiunto gli zeri per riempire per aver lo stesso numero di colonne
[00:13:15 - 00:13:27] non è fondamentale, allora 0 più 1 fa 1, 1 più 1 fa 0 con riporto di 1, questo riporto si va a sommare con i zeri presenti della terza colonna e quindi abbiamo 1
[00:13:28 - 00:13:38] 1 più 1 fa 0 con riporto di 1, il riporto si va a sommare all'uno già presente e quindi fa 1 più 1 0 con riporto di 1
[00:13:39 - 00:13:47] l'ultimo riporto si va a sommare nella colonna, qui ci sono solo zeri quindi risultate 1 e poi 1 più 0 fa 1
[00:13:47 - 00:13:53] quindi il risultato di questa somma è 1 1 0 0 1 0 1
[00:13:58 - 00:14:17] indora che solo detto sommare negli esempi non era specificato il numero di bit, rappresentare il risultato quindi quando non è specificato
[00:14:17 - 00:14:22] quindi possiamo aggiungere ulteriori bit se necessario, non ci sono limiti
[00:14:22 - 00:14:34] invece una traccia di questo tipo, vedete rappresentare su un byte il risultato, questo viene fissato, si sta fissando un limite
[00:14:34 - 00:14:40] che sta chiedendo che il risultato di questa operazione debba essere rappresentato su un byte
[00:14:40 - 00:14:47] e quindi quando abbiamo un vincolo di questo tipo è il caso in cui dobbiamo fare attenzione e chiederci
[00:14:47 - 00:14:55] ma il risultato è effettivamente rappresentabile su un byte quindi non possiamo aggiungere bit in questo caso
[00:14:55 - 00:15:03] intendo nel caso in cui sia specificato che risultato essere su un byte, ma se non ci riusciamo allora una risposta
[00:15:03 - 00:15:10] ad un'esercizia di questo tipo può essere appunto per l'oridiografo come accendiamo prima
[00:15:10 - 00:15:22] in questo particolare esempio il problema non si verifica perché noi abbiamo 1 1 0 1 0 che fa sommare 1 0 1 0 1 0
[00:15:22 - 00:15:29] il risultato vedete sotto bit, quindi il problema non ce l'abbiamo qui, come ci chiediamo arrivati
[00:15:29 - 00:15:39] 0 più 0 fa 0, 1 più 1 fa 0 col riporto di 1, 1 più 0 fa 1, 1 più 1 fa 0 col riporto di 1
[00:15:39 - 00:15:46] il riporto di un 1 già presente fa 0 col riporto di 1, 1 più 1 fa 0 col riporto di 1
[00:15:46 - 00:15:52] e quindi andiamo a un risultato che 1 0 0 0 1 0 0
[00:15:52 - 00:15:59] il terriore cosa quando viene specificato di rappresentare su un numero di bit definito il risultato
[00:15:59 - 00:16:06] non solo bisogna essere attenti che il risultato non va da oltre il numero di bit presenti
[00:16:06 - 00:16:15] ma bisogna anche andare a specificare quali sono i bit completi, questo voglio dire il risultato qui ha 7 bit
[00:16:15 - 00:16:27] però io voglio la codifica su 8 bit quindi banalmente andiamo a esplicitare i g0 in più
[00:16:28 - 00:16:37] quindi il risultato non sarà 1 0 0 0 1 0 0 ma sarà 0 1 0 0 0 1 0 0
[00:16:37 - 00:16:47] cioè rendiamo espliciti tutti gli eventuali zeri per riempire a punto di avere un risultato composto da 8 bit
[00:16:48 - 00:17:05] ulteriore esempio, sempre su 1 byte quindi su 8 bit vuol dire voglio una stringa di 8 bit come risultato
[00:17:06 - 00:17:13] dobbiamo sommare 1 0 1 1 0 1 0 1 1 1 0
[00:17:13 - 00:17:22] anche qua ho messo lo 0 per avere lo stesso, cioè valorati a tutte le colonne però non è necessario
[00:17:22 - 00:17:30] allora facciamo 0 più 0 fa 0, 1 più 1 fa 0 con riporto di 1, 1 più 1 fa 0 con riporto di 1
[00:17:30 - 00:17:34] ora qui vedete abbiamo 2 1 che si vanno a sommare al riporto
[00:17:34 - 00:17:47] 1 più 1 fa 0 con riporto di 1, 0 più ulteriore 1 fa 1 quindi nella quarta colonna abbiamo 1 con riporto di 1
[00:17:49 - 00:17:56] 1 più 1 fa 0 con riporto di 1, 1 più 1 fa 0 con riporto di 1, 1 più 1 fa 0 con riporto di 1
[00:17:57 - 00:18:09] anche qua il risultato entra ancora negli 8 bit a disposizione, già il risultato di suo ha 8 bit quindi non devo aggiungere 0
[00:18:09 - 00:18:12] ed è 1 0 0 1 0 0 0
[00:18:12 - 00:18:31] questo invece è un esempio in cui vedete il risultato non lo dovete dare nel senso che non è quello che verrebbe aggiungendo il bit
[00:18:31 - 00:18:43] ma deve essere overflow, perché? perché è specificato su un byte se invece la traccia è chiesto soltanto di calcolare il risultato
[00:18:43 - 00:18:49] allora il risultato era quello specificato con il bit ulteriore come arriviamo
[00:18:49 - 00:18:56] allora 1 1 0 1 1 0 1 1 più 1 0 1 1 0 1 0
[00:18:56 - 00:19:03] andiamo a fare 1 0 1 1 più 1 0 con riporto di 1 1 1 più 1 0 con riporto di 1
[00:19:03 - 00:19:12] più gli altri due che già ci sono fa 1 con riporto di 1 1 più 0 fa 1 1 più 1 fa 0 con riporto di 1
[00:19:12 - 00:19:21] ecco qua questo riporto che dovrebbe andarmi ad aggiungere al 9 bit alla nona con on
[00:19:21 - 00:19:35] teoricamente nei momenti in cui specifico e voglio risultato sotto bit allora la risposta è overflow proprio perché servirebbe un ulteriore bit per rappresentare il risultato
[00:19:35 - 00:19:42] ma c'è solo un byte di spruzione non c'è questo bit
[00:19:42 - 00:19:58] allora come abbiamo fatto diciamo all'addizione anche nel caso della sottrazione possiamo seguire regole molto simili alla sottrazione nei numeri decimali
[00:19:58 - 00:20:10] l'unica cosa che cambia è che il numero di cifre e i simboli di sottrazione è diverso e minore e quindi ne dobbiamo tener conto quando applichiamo le regole della sottrazione
[00:20:10 - 00:20:26] nelle regole della sottrazione quali sono ovviamente noi diciamo in questi esempi ci soffermiamo nei casi in cui il minuendo è maggiore del sottraendo
[00:20:26 - 00:20:36] cioè il risultato è maggiore quale di zero o che non analizziamo operazioni che danno diciamo risultati negativi
[00:20:36 - 00:20:42] stiamo ragionando su un sistema binario più lo classico numeri compressi tra zero
[00:20:42 - 00:20:56] e poi alla l, diciamo i numeri 2 l-1 dove l è il numero di bit di spruzione quindi solo valori maggiore quale di zero
[00:20:57 - 00:21:14] come si fa? si parte dalle cifre meno significative si vanno a sottrarre e in maniera analoga all'addizione anche qui quando il risultato della sottrazione tra due cifre
[00:21:14 - 00:21:30] non lo possiamo fare perché la cifra minuendo e minore della cifra sottrendo in questo caso avremo qualcosa che si propaga non sarà un riporto
[00:21:30 - 00:21:35] ma sarà un valore che viene prestato dalle cifre a sinistra
[00:21:36 - 00:21:42] anche qua possiamo volendo creare la tabella dei possibili casi
[00:21:42 - 00:21:49] cioè cosa può accadere quando facciamo la sottrazione tra due cifre
[00:21:49 - 00:21:59] come al solito noi sappiamo che i valori possibili sono zero e uno basta fare le combinazioni sono quattro possibili casi in cui ci possiamo trovare
[00:22:00 - 00:22:08] devo fare la sottrazione tra a e b ovviamente se a e b valgono zero la differenza sarà zero
[00:22:08 - 00:22:17] se a e maggiore di b quindi ho uno meno zero la differenza è banalmente uno se a e uguale b la differenza è zero
[00:22:17 - 00:22:26] il caso critico da più attenti è il secondo in cui vedete il minuendo e minore del sottrendo
[00:22:26 - 00:22:29] cioè a e minore di b
[00:22:29 - 00:22:36] se nel caso in cui devo fare zero meno uno non posso farlo
[00:22:36 - 00:22:47] ma per poterlo fare la cifra deve chiedere diciamo un prestito alla cifra più a sinistra alla sua sinistra diciamo
[00:22:47 - 00:22:55] e in questo caso il risultato sarà uno con un prestito di uno
[00:22:55 - 00:23:10] come ci arriviamo a questa cosa ci possiamo notare però dopo lo vediamo meglio con gli esempi che nel momento in cui viene prestata una cifra
[00:23:10 - 00:23:14] ad a diventa uno zero
[00:23:15 - 00:23:28] che in decimale ovviamente noi siamo obbetto a fare quando facciamo la la sottrazione decimale siamo abituati che il prestito mi fa aumentare di una decina il valore
[00:23:29 - 00:23:41] qua ovviamente non è non aumenta di una decina il valore diciamo della cifra che riceve il prestito ma aumenterà non di dieci alla uno ma di due alla uno
[00:23:41 - 00:23:55] quindi questo equivale ad affiancare la cifra uno a quella che la riceve uno zero ma uno zero sarebbe un aumento di due e proprio uno zero proprio due
[00:23:55 - 00:24:08] per questo motivo quando poi la cifra che ha ricevuto il prestito quando vado a sottrarre b ad a per prestito effettivamente quello che vado a fare uno zero meno uno
[00:24:08 - 00:24:26] cioè è uno e il risultato è uno per questo zero meno uno fa uno perché quando ha riceve il prestito di una cifra riceve un due elevato a uno
[00:24:26 - 00:24:37] cioè a diventa due meno b che vale uno risultate uno vediamo sempre il raffronto tra decimale e binario no?
[00:24:37 - 00:24:46] immaginiamo che dobbiamo fare dodici meno cinque in decimale sapete benissimo che in questo caso due meno cinque non lo posso fare
[00:24:46 - 00:25:11] due due riceve il prestito di una cifra e sarebbe aggiungere uno zero cioè dieci alla uno al due e il due diventa dodici oppure se preferite lo potete immaginare come affiancare al due la cifra uno quindi uno due dodici meno cinque fa sette
[00:25:11 - 00:25:24] uno ovviamente acceduto quando poi mi sposto nella colonna fianco uno acceduto con la cifra diventa zero quindi non aggiunge ulteriori contributi
[00:25:24 - 00:25:36] con lo stesso modo se io devo fare uno zero uno meno uno zero cosa faccio la prima colonna uno meno zero fa uno non ci sono problemi
[00:25:36 - 00:25:51] la seconda colonna o zero meno uno zero non ce la fa a bisogno di un prestito di una cifra dalla dalla sua sinistra stare una cifra allo zero lo fa diventare due
[00:25:52 - 00:26:14] perché vuol dire prestare uno zero cioè due alla uno a zero e passa da zero a due due meno uno fa uno la terza colonna l'uno avendo prestato una unità vale a zero e quindi zero meno zero fa zero e quindi posso dire che uno zero uno meno uno zero fa uno uno
[00:26:15 - 00:26:25] vediamo qualche esempio uno zero zero zero meno uno uno
[00:26:27 - 00:26:34] parto dalla prima colonna sempre si parte sempre dalle cifre meno significative quindi quelle più a destra
[00:26:35 - 00:26:54] qui nella prima riga ho evidenziato diciamo i prestiti forniti dalle varie colonne quindi cosa vuol dire che zero nella prima colonna zero meno uno non lo posso fare quindi bisogna chiedere un prestito
[00:26:55 - 00:27:04] alla seconda colonna la seconda colonna non ce la lo chiede a sua volta alla terza la terza non ce la lo chiede a sua volta alla quarta
[00:27:06 - 00:27:23] ora stiamo attenti qua la quarta colonna c'è uno lo presta alla terza colonna o la quarta colonna ovviamente quando cede una cifra diciamo diventa zero quindi vedete la quarta colonna
[00:27:24 - 00:27:33] come risultato finale avrà zero perché poi resta zero meno zero questo uno che presta la quarta colonna lo mettiamo quindi nella terza colonna
[00:27:35 - 00:27:51] quando lo mettiamo nella terza colonna diventa uno zero ok uno zero cioè due questo due però non rasterà due perché una volta che diventa due deve prestare uno uno alla seconda colonna
[00:27:52 - 00:28:05] restando due e un con unità scusatemi alla seconda colonna la terza colonna era diventata due adesso diventa uno e quindi nella terza colonna dopo aver ricevuto il prestito
[00:28:06 - 00:28:16] e dopo avermi fatto uno a sua volta verso la seconda colonna la terza colonna il valore di a è uno uno meno b che vale zero fa uno
[00:28:17 - 00:28:32] la seconda colonna ha ricevuto l'uno dalla terza colonna ed è diventato due a source però cede una cifra alla prima colonna e quindi nella seconda colonna il valore di a è uno
[00:28:33 - 00:28:49] uno meno uno che il valore di b fa zero nella prima colonna arriva il prestito finalmente e quindi a della prima colonna vale due due meno uno fa uno
[00:28:50 - 00:28:58] e quindi uno zero zero zero meno uno uno diventa uno zero uno cioè fa uno zero uno
[00:29:01 - 00:29:03] vi trovate tutto chiaro?
[00:29:04 - 00:29:06] sì più bene
[00:29:09 - 00:29:29] ricordate che come nella diciamo sottrazione nel sistema decimale ovviamente un prestito se poi viene fatto a sua volta quindi che si propaga ovviamente altera il valore finale della cifra che ha chiesto il prestito e poi l'ha fatto a sua volta
[00:29:33 - 00:29:43] facciamo qualche altro esempio uno zero uno zero zero zero uno meno uno zero uno zero uno zero uno
[00:29:44 - 00:29:58] partiamo dalla prima colonna uno meno uno facile zero zero meno zero zero zero meno uno non lo posso fare la cifra abbiamo bisogno di un prestito alla sinistra
[00:29:59 - 00:30:06] zero non ce la chiede a quella alla sua sinistra zero non ce la chiede a quella alla sinistra
[00:30:07 - 00:30:22] chi può effettivamente erogare il primo prestito è la sesta colonna questo uno qui questo uno qui nel momento in cui da un prestito diventa zero quindi a meno b nella sesta colonna ha come valore zero
[00:30:23 - 00:30:41] l'uno dato in prestito alla quinta colonna fa diventare il valore dia due due che però scende a uno perché uno lo dà in prestito alla quarta colonna quindi il valore finale dia è la quinta colonna e uno
[00:30:41 - 00:30:58] uno meno b della quinta colonna cioè uno meno uno fa zero quarta colonna riceve un uno quindi diventa diventa due però anche lui ha ricevuto una richiesta di prestito quindi cede
[00:30:58 - 00:31:11] uno uno alla sua destra e quindi nella quarta colonna a diventa uno uno meno zero che il valore di b nella quinta colonna della quarta colonna fa uno
[00:31:12 - 00:31:21] a terza colonna ha ricevuto uno diventa due lo cede a destra diventa uno uno meno uno
[00:31:24 - 00:31:40] no scusate mi sto sbagliando qua non c'è nulla richiesta perché qua non c'era quindi in terza colonna riceve l'uno diventa due però basta se lo tiene non deve cedere nient'altro quindi questo due meno uno fa uno
[00:31:42 - 00:32:02] quindi torniamo adesso alla settima colonna zero meno uno ed è un prestito a sinistra diventa due due meno uno fa uno nell'ultima colonna non c'è più l'uno perché è stato prestato e fa zero meno zero zero e quindi risultato in alle zero uno zero zero uno uno zero zero
[00:32:03 - 00:32:05] e
[00:32:08 - 00:32:15] andiamo l'importante è tenere traccia dei prestiti e come si si propagano poi ve li potete diciamo segnare o tenere a mente
[00:32:16 - 00:32:21] con la convenzione che volete basta che vi ricordate i valori
[00:32:21 - 00:32:23] e
[00:32:27 - 00:32:31] altro esempio uno zero uno zero uno uno uno zero
[00:32:33 - 00:32:37] meno uno zero zero zero uno uno uno
[00:32:40 - 00:32:47] allora zero meno uno chiede un prestito lo riceve immediatamente diventa due meno uno fa uno
[00:32:48 - 00:32:59] la seconda colonna avendo dato uno in prestito non vale più uno vale zero zero meno uno non riesco a farlo devo chiedere un prestito a sinistra
[00:33:00 - 00:33:07] lo ricevo quindi il valore di a in seconda colonna diventa due meno uno uno
[00:33:08 - 00:33:14] in terza colonna il valore di a non è più uno per diventato zero quindi deve chiedere un prestito
[00:33:14 - 00:33:18] lo riceve diventa due meno uno fa uno
[00:33:19 - 00:33:28] nella quarta colonna il valore di a non è più uno ma è zero perché è dato acceduto un prestito a destra quindi zero meno zero zero
[00:33:29 - 00:33:31] quinta colonna è zero meno zero zero
[00:33:32 - 00:33:34] stessa colonna uno meno zero uno
[00:33:35 - 00:33:42] settima colonna zero meno uno non lo posso fare chiedo il prestito a sinistra diventa due meno uno uno
[00:33:42 - 00:33:49] ultima colonna l'uno è diventato zero perché ha dato il prestito e quindi zero meno zero zero
[00:33:50 - 00:33:54] quindi risultato finale zero uno uno zero zero uno uno
[00:33:58 - 00:34:02] voi potete sempre fare diciamo queste operazioni che stiamo facendo
[00:34:03 - 00:34:09] potete sempre fare la controprova tradurre cioè convertire i numeri binari in decimale
[00:34:09 - 00:34:15] fare le operazioni e vedere se vi trovate con un risultato che effettivamente
[00:34:18 - 00:34:26] in valore numerico cioè se convertite il risultato dell'operazione in decimale ovviamente vi dovete trovare un valore decimale
[00:34:27 - 00:34:32] che coincide con il risultato dell'operazione svolta nel decimale ok
[00:34:32 - 00:34:37] diciamo se non ci sono errori di ovverlo i due con risultati di uno coincide
[00:34:38 - 00:34:45] sarà importante capire come svolge le operazioni direttamente in binario senza convertirli in decimale
[00:34:49 - 00:34:54] altro esempio uno zero zero uno uno meno uno zero uno zero
[00:34:55 - 00:35:01] e qua uno zero facile fa uno uno meno uno zero facile zero zero zero zero
[00:35:02 - 00:35:06] zero meno uno non lo posso fare chiedo il prestito diventa due due meno uno uno
[00:35:07 - 00:35:13] risultato è uno zero zero uno che poi porto su otto bit aggiungendo i quattro zero
[00:35:14 - 00:35:21] per esempio uno zero uno uno zero uno zero meno uno zero uno zero
[00:35:22 - 00:35:30] metto in colonna zero uno zero zero meno uno chiedo il prestito diventa due meno uno uno
[00:35:31 - 00:35:35] terza colonna adesso vale zero
[00:35:35 - 00:35:42] vero meno uno posso farlo devo chiedere un prestito prestito si propaga c'è la richiesta di prestito si propaga a sinistra
[00:35:43 - 00:35:50] finché chi procedere è la quinta colonna la quinta colonna da uno diventa due in quarta colonna
[00:35:51 - 00:35:55] questo due diventa uno perché uno viene dato in prestito a destra
[00:35:55 - 00:36:02] uno meno zero fa uno nella terza colonna ho ricevuto l'uno mi fa diventare il valore due due meno uno fa uno
[00:36:02 - 00:36:07] dove ero arrivato qui la quinta colonna poi vado in cesta
[00:36:08 - 00:36:19] in cesta c'è sempre una quinta colonna
[00:36:19 - 00:36:34] dove era arrivato qui la quinta colonna, poi vado in cesta, in quinta colonna che aveva
[00:36:34 - 00:36:41] dato il prestito e diventato 0, quindi lo chiede a sinistra e diventa 2, 2, 1, 1. La
[00:36:41 - 00:36:50] sexta colonna è diventato 0, 0 meno 0, 0. Settima colonna chiede il prestito diventa 2, 2 meno 1,
[00:36:50 - 00:36:58] ultima colonna l'uno diventa 0, quindi 0 meno 0, 0. Quindi, facciamo attenti a non
[00:36:58 - 00:37:05] imbrogliarsi tra i valori nuovi e quelli vecchi, non dovrebbe essere, diciamo, complicato.
[00:37:05 - 00:37:16] Allora, ultima operazione, che vediamo la moltipliazione, anche qua un banale, diciamo,
[00:37:16 - 00:37:23] recap di come funziona la moltipliazione, nel decimale, come la facciamo, mettiamo sempre in
[00:37:23 - 00:37:33] ordine le cifre, in modo da far coincidere, diciamo, le cifre dello stesso peso, le incoloniamo e poi
[00:37:33 - 00:37:39] andiamo a svolgere le operazioni tra moltiplicando e moltiplicatore. Come lo facciamo? La tecnica
[00:37:39 - 00:37:47] che, tebicamente, si usa è quello di fare i prodotti parziali sfasati, man mano, che ci sono
[00:37:47 - 00:37:57] cifre del moltiplicatore. Quindi, 2 per 26 faccio 52, 1 per 26 fa 26, però sfasato e poi andiamo a
[00:37:57 - 00:38:06] fare la somma, 312, ok? Stessa tecnica, stessa procedura, ovviamente, la possiamo usare tra
[00:38:06 - 00:38:15] numeri binari, col vantaggio che nella moltipliazione, diciamo, nel mondo binario è molto semplice perché
[00:38:15 - 00:38:23] noi abbiamo solo due cifre, o 0 e o 1, è la moltipliazione per 0 a nulla tutto, la moltipliazione per
[00:38:23 - 00:38:31] 1, ripete la cifra, quindi sarà facilissimo fare le moltipliazioni. Anche qua possiamo
[00:38:31 - 00:38:38] costruire la tabella di tutti i casi possibili sulla singola cifra, cioè se devo fare a per
[00:38:38 - 00:38:49] b, i casi che posso avere sono questi 4, 0 per 0, 0 per 1, 0, 1 per 0, 0, 1 per 1, 1, quindi, come vedete
[00:38:49 - 00:38:56] anche da questa tabella, il capitolo della locazione sarà sempre 0, appena c'è uno 0 in mezzo, e
[00:38:56 - 00:39:06] sarà la replica, diciamo, della cifra nel momento in cui per l'1, c'è entrambi, sono 1. Facciamo,
[00:39:06 - 00:39:16] per esempio, 1, 0, 1 per 1, 0, 1. Incoloniamo e come facciamo, abbiamo 3 cifre al moltiplicatore,
[00:39:17 - 00:39:25] quindi andremo a fare 3 prodotti parziali spasati, quindi il primo replica la è moltiplicando,
[00:39:25 - 00:39:34] quindi 1, 0, 0, 1, il secondo a 0 tutto, quindi 4, 0, il terzo replica è moltiplicando di nuovo 1,
[00:39:34 - 00:39:44] 0, 0, 1 spasati, e poi andiamo a fare le somme come abbiamo imparato a fare, 1, 0, 1, 1, 1, 0, 1 e quindi
[00:39:44 - 00:39:57] il risultato di questa moltiplicazione è banalmente 1, 0, 1, 1, 0, 1. Una cosa che potete fare se vi
[00:39:57 - 00:40:07] torniamo utile farlo è evitare proprio di mettere gli zeri proprio perché sappiamo che dovremo mettere
[00:40:08 - 00:40:14] tutti i zeri e quindi possiamo semplicemente concentrarci su le moltiplicazioni della cifra 1,
[00:40:14 - 00:40:23] sopparlando del moltiplicatore, quando dobbiamo fare una moltiplicazione tra due numeri binari e devo
[00:40:23 - 00:40:28] andare a calcolare tutti i prodotti parziali, posso evitare di calcolare i prodotti parziali per
[00:40:28 - 00:40:37] 0, l'importante è che poi mi ricordo di mettere i valori spasati in maniera opportuna, cioè quando
[00:40:37 - 00:40:44] vado a calcolare solo i prodotti parziali della cifra 1, ovviamente il primo resta 1, 0, 0, 1,
[00:40:44 - 00:40:53] il secondo l'altro 1, 0, 0, 1, però mi devo ricordare spasarlo non di 1 ma di 2, ok? Perché
[00:40:53 - 00:41:05] ovviamente lista 2 dall'altro e ovviamente il risultato è lo stesso, diciamo, è una semplificazione che potete usare o meno.
[00:41:05 - 00:41:31] L'altro esempio, 1, 0, 1, 0, 0, 0, 1, per 1, 0, 1, ovviamente conviene sempre mettere come
[00:41:31 - 00:41:41] moltiplicatore, diciamo, il numero che ha meno cifre, che qua faccio la moltiplicazione per 1,
[00:41:41 - 00:41:53] semplicemente ripetendo le cifre del moltiplicando, la moltiplicazione per 0 è sempre 0 e di nuovo
[00:41:53 - 00:42:02] metto il moltiplicando spasato e quindi ottengo queste tre risultati parziali che devo andare
[00:42:02 - 00:42:15] a sommare, quindi faccio l'addizione come visto prima, 1, 0, 0, 0, 0, 0, 1, fa 1, 0, 0, 1, 0, qui ovviamente se genera il riporto 1 più 1 fa 0
[00:42:16 - 00:42:27] riporto il riporto di 1 e qui 1, quindi il risultato sarà 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, se li è comodo potrete
[00:42:27 - 00:42:36] fare direttamente il calculo solo sui 1 spasando però di due i termini di i prodotti parziali.
[00:42:36 - 00:42:47] altro risultato di nuovo qui sto fissando il numero di bit e deve contenere il risultato
[00:42:47 - 00:42:57] 8 bit 1 0 1 0 1 per 1 0 0 1 come lo vado a fare vedete qua ho fatto semplicemente i prodotti
[00:42:57 - 00:43:11] degli 1 soltanto quindi 1 0 1 0 1 più 1 0 1 0 1 sfasato però di 3 perché i 2 bit 2 1 sono
[00:43:11 - 00:43:20] distanti 3 bit vado a svolgere le attenzioni e quindi mi trovo 1 0 1 1 1 1 0 1
[00:43:20 - 00:43:32] ulteriore esempio il caso lì che abbiamo già parlato dell'overflow in cui anche qua nella
[00:43:32 - 00:43:39] possibilizzazione come in qualunque diciamo operazione che svolgete tra numeri può causare un
[00:43:39 - 00:43:45] errore di overflow perché in questo caso vediamo servire però più bit di quelli a
[00:43:45 - 00:43:52] disposizione noi abbiamo 8 bit di disposizione quando deve fare la multipliazione anche qua
[00:43:52 - 00:44:00] vedete prodotte parziali ho ripartato solo quelli degli 1 sfasati di 2 perché gli 1 soltanto
[00:44:00 - 00:44:08] distanti di 2 vedete il primo già lo sfasato di 1 perché ci sarebbe lo 0 che non ho ripartato
[00:44:08 - 00:44:18] quindi 1 1 0 1 0 1 0 1 0 sfasato di 2 1 1 0 1 0 sfasato di 2 quindi semplicemente andiamo a
[00:44:18 - 00:44:26] replicare il moltiplicando tante volte quanti sono gli 1 nel moltiplicatore spasando opportunamente
[00:44:26 - 00:44:34] i valori vada a svolgere le somme e abbiamo 0 0 1 0 1 col riporto c'è 0 col riporto di 1
[00:44:34 - 00:44:45] 1 più 1 fa 1 più 1 fa 0 col riporto di 1 che si va ad adizionare quest'altro 1 quindi di nuovo
[00:44:45 - 00:44:52] 0 col riporto di 1 1 più 1 più riporto fa 1 col riporto di 1 1 più 0 più 1 che di riporto fa
[00:44:52 - 00:44:59] 0 col riporto di 1 1 più il riporto fa 0 col riporto di 1 1 più riporto fa 0 col riporto di 1
[00:44:59 - 00:45:06] quindi questo riporto che si sta propagando sempre più a sinistra la richiede mi va a richiedere
[00:45:06 - 00:45:20] un totale di 6 9 11 bit teoricamente che mi servirebbero per rappresentare il risultato di
[00:45:20 - 00:45:27] questa operazione e quindi ovviamente un un overflow molto pronunciato perché addirittura
[00:45:27 - 00:45:33] su tre bit oltre quelli che ha disposizione quindi risultato e banalmente overflow non si può
[00:45:33 - 00:45:42] calcolare o meglio non si può rappresentare domande dubbi
[00:45:50 - 00:46:01] ok allora se non ci sono dubbi con questo concludo vi saluto allora ci vediamo al
[00:46:01 - 00:46:06] mezzogiorno per la un'altra ora di lezione ok a dopo
