# Lezione 17 - Implementazione di IJVM con Mic-1

- File: `C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI\Lezione 17 - Implementazione di IJVM con Mic-1.mp4`
- Durata: 00:33:23
- Trascrizione: `17_lezione_17_implementazione_di_ijvm_con_mic_1.json`

## Argomenti probabili
- porte_logiche (104): and, or, nand
- memoria_bus (66): memoria, indirizzo, ram
- microarchitettura (49): mic, controllo
- clock_prestazioni (20): ciclo, frequenza, prestazioni, tempo
- mips_assembly (6): registro

## Trascrizione

[00:00:00 - 00:00:07] All'interno dell'MDETER e tu fa istruzione deve essere interfetata.
[00:00:14 - 00:00:15] Allora, vediamo.
[00:00:18 - 00:00:27] Questo reciclo possiamo indicare con una sola riga del mitrolinguaggio di Malno, quindi
[00:00:28 - 00:00:37] men uno, diciamo, il ciclo principale che deve essere effettuato per recuperare ogni
[00:00:37 - 00:00:41] volta la prossima istruzione, se dire.
[00:00:42 - 00:00:49] Questo è fatto ovviamente da delle mitrooperazioni, le istruzioni che sono un incremento del proprio
[00:00:49 - 00:00:58] alcante che, ricordiamo, viene incrementato e le istruzioni dell'oliva sono sempre,
[00:00:59 - 00:01:06] criticamente, diciamo, la prossima istruzione è genere quella possessiva, quindi si incrementa
[00:01:07 - 00:01:18] il proprio alcante, si recupera la prossima istruzione con freccia e poi si fa il stato
[00:01:18 - 00:01:25] ad MBR, cioè alla prossima istruzione, perché la volta che si è fatta il prezzo,
[00:01:26 - 00:01:30] istruzioni, diciamo, è finita nell'MBR.
[00:01:34 - 00:01:42] L'MBR, diciamo, contiene già, al momento attuale, l'istruzione che deve seguire.
[00:01:42 - 00:01:54] Quindi, durante, diciamo, questo microprogramma, queste microestruzioni, poi l'MBR va aggiornato
[00:01:55 - 00:02:02] a termine verso la fase finale del ciclo.
[00:02:03 - 00:02:10] Attualmente, cioè l'MBR, in che contiene già l'istruzione, in particolare l'off code,
[00:02:10 - 00:02:17] l'off code circondice operativo che identifica l'istruzione corrente che devo seguire e poi
[00:02:18 - 00:02:25] eseguendo questo microgramma, verrà caviata, diciamo, la MBR che verrà però interpretato
[00:02:26 - 00:02:29] nel prossimo ciclo.
[00:02:30 - 00:02:39] Quello che fa, quindi, la microestruzione è effettuare un salto nel mitocodice per eseguire
[00:02:40 - 00:02:49] questa istruzione. Prelevare il byte che segue l'off code, il byte per il tip cancanto
[00:02:49 - 00:02:58] lavora sul byte, quindi incrementarlo di questa stassa il byte successivo, e il byte successivo
[00:02:59 - 00:03:06] può essere o l'istruzione successiva o, nel caso sia, una istruzione che richiede un operando,
[00:03:07 - 00:03:11] sarà l'operando di quelle istruzioni.
[00:03:11 - 00:03:26] Allora, qui sono riportate, diciamo, alcuni dei microprogrammi che realizzano le microestruzioni
[00:03:26 - 00:03:42] della, come li realizzano le istruzioni di JPM. Qui vedete, l'estruzione di livello isa ad
[00:03:43 - 00:03:53] è realizzata, vedete, da un microprogramma composto da queste varie istruzioni, microestruzioni.
[00:03:54 - 00:04:05] Quindi fa anche capire che la istruzione di livello isa ad non si esegue, non termina in
[00:04:05 - 00:04:14] un unico ciclo, ma mi equide diversi. Come ricordate, ogni riga è un ciclo, lo stesso
[00:04:15 - 00:04:21] risulto e così via. Questo è solo un estratto sul libro che trova, diciamo, la tabella
[00:04:22 - 00:04:27] completa con tutti i microprogrammi che implementano le istruzioni di livello isa della
[00:04:27 - 00:04:45] IGPM che stiamo considerando come esempio. Adesso pregiamo a ragionare su, diciamo, queste
[00:04:45 - 00:04:57] per capirci, poi vedremo più avanti un esempio in dettaglio. Allora, quella che avevamo
[00:04:58 - 00:05:06] considerato prima, quindi il TOS, abbiamo detto il topo do stack, quindi contiene il valore
[00:05:06 - 00:05:18] puntato dallo stack pointer, quindi il stack pointer è l'indirizzo, in memoria che si trova,
[00:05:19 - 00:05:24] diciamo, la cima dello stack, piuttosto invece è il dato puntato da questo indirizzo, quindi
[00:05:25 - 00:05:31] quando viene letto una parola, diciamo, dallo stack, il valore lo troveremo nel registro TOS.
[00:05:36 - 00:05:44] Ovviamente può sembrare ridondante avere questo registro per contenere il valore di questa
[00:05:45 - 00:05:53] area di memoria, perché per me la vado a recuperare quando mi serve, però ovviamente avendola
[00:05:54 - 00:06:01] già a disposizione del registro di far risparmiare un accesso in memoria.
[00:06:06 - 00:06:25] Allora, le microestruzioni, mi ha detto, non vennero eseguite sequenziamente, una dopo
[00:06:26 - 00:06:34] l'altra come nel livello ITA, ma ogni una lista si porta presso, stesso nella sua formato,
[00:06:34 - 00:06:46] nella sua istruzione, anche nel registro della prossima istruzione in maniera esplicita.
[00:06:47 - 00:06:56] Questo perché, diciamo, tutti gli indirizzi della memoria di control, in questo caso,
[00:06:56 - 00:07:02] quindi la memoria dove sono memorizzate le istruzioni, sono memorizzati i micro programmi
[00:07:03 - 00:07:12] strati, devono essere riservati per la prima parola della corrispondente istruzione dell'interprete.
[00:07:12 - 00:07:32] Allora, assomigliamo che MBR contenga il valore 0,60. 0,60 è il valore dell'instruzione
[00:07:32 - 00:07:40] stesso che non è l'indirizzo di memoria. MBR è già l'instruzione, o meglio il primo
[00:07:41 - 00:07:48] byte dell'instruzione, e il primo byte dell'instruzione di livello ITA è in genere il codice identificativo
[00:07:48 - 00:07:59] dell'instruzione ITA, che devo eseguire. Se si va a vedere quella tabella che vi ha
[00:08:00 - 00:08:09] accennato prima, dove sono riportate tutte le istruzioni, si va a vedere che il codice 0,60,
[00:08:10 - 00:08:15] in particolare subito trovate la lista di le istruzioni di livello ITA che compongono
[00:08:15 - 00:08:26] la IGDM che stiamo ragionando, il codice 0,60 è associato all'instruzione ITA, quindi
[00:08:27 - 00:08:37] nel momento in cui nel ciclo continuo si va a eseguire istruzione di livello ITA e si trova
[00:08:37 - 00:08:46] che nelle BBR è indicato dell'instruzione ITA, allora viene interpretata come eseguita
[00:08:47 - 00:09:01] questa istruzione ITA che deve essere eseguita. Alla lexico principale quindi cosa dobbiamo
[00:09:01 - 00:09:09] fare? Dobbiamo incrementare il program counter in modo che contenga poi l'indirizzo del byte
[00:09:10 - 00:09:18] successivo. Vi vedo, quello attuale l'abbiamo usato perché è stato caricato il valore
[00:09:19 - 00:09:27] del BBR, quindi lo devo incrementare in un nuovo ciclo, devo incrementare il program counter
[00:09:27 - 00:09:36] e richiedere il recupero del prossimo byte, ne ho detto non sappiamo se è un'instruzione
[00:09:37 - 00:09:43] o un'operando e qui iniziamo a parlare il prossimo byte che poi dopo un po' di tempo
[00:09:44 - 00:09:51] andrà a finire nel registro del BBR, ma finché arriva questo nuovo byte adesso nel BBR
[00:09:51 - 00:10:11] c'è l'instruzione attuale, questo IAD. Abbiamo di seguire queste istruzioni di livello ITA,
[00:10:11 - 00:10:18] però in generale durante questo ciclo in cui noi andiamo a interpretare e seguire le istruzioni
[00:10:19 - 00:10:25] livello ITA, abbiamo detto seguire le istruzioni e seguire il microprogramma che implementa
[00:10:26 - 00:10:34] con le istruzioni, ma abbiamo anche detto che poi a termine diciamo l'eseuzione deve
[00:10:34 - 00:10:41] essere caricato nell'MBR e poi la prossima istruzione deve seguire, quindi diciamo
[00:10:42 - 00:10:48] è compito di ogni microprogramma che imprementa una istruzione di livello ITA andare anche
[00:10:49 - 00:10:58] a preoccuparsi di caricare nell'MBR l'off-code della prossima istruzione di livello ITA.
[00:10:58 - 00:11:05] Ok, quindi diciamo questo richiamo a questo microprogramma main1 che qui abbiamo indicato
[00:11:06 - 00:11:13] con la etiquetta main1, lo troveremo a termine di ogni altro microprogramma che realizza
[00:11:14 - 00:11:23] le istruzioni livello ITA, vediamo se da quasi in c'è, vedete? Se io identifico con main1
[00:11:23 - 00:11:38] questa microprogramma che incrementa, recupera e salta a MBR, faccio manca la MBR, scusate
[00:11:39 - 00:11:49] questo è goto MBR, vedete? Poi il microprogramma che imprementa la istruzione di livello ITA
[00:11:49 - 00:11:57] IAD, vedete? Alla fine ha goto main1 proprio per dire che quando ha terminato quella, diciamo,
[00:11:58 - 00:12:06] le microprogramma che incrementano IAD, poi deve caricare l'MBR con l'uovo, con l'uovo
[00:12:07 - 00:12:13] BITE, con la nuova istruzione e quindi troviamo sempre questo goto main1, goto main1 che il salto
[00:12:13 - 00:12:20] al ciclo principale che alimenta appunto l'esecuzione stessa delle istruzioni livello ITA, quindi
[00:12:21 - 00:12:33] anche a MBR e così via, vedete? Ad ogni microprogramma contiene anche, diciamo, il microprogramma
[00:12:33 - 00:12:52] del main1, e incluso in ognuna delle istruzioni. In questo microprogramma, questo ciclo principale,
[00:12:53 - 00:13:02] abbiamo quelle i microstruzioni che abbiamo detto. La prima incrementa il programmante, in modo
[00:13:03 - 00:13:08] incrementale il programmante vuol dire puntare al BITE successivo. Il programmante lavora,
[00:13:09 - 00:13:20] indirizza la memoria in BITE, se vi contate quando abbiamo visto invece il registro di memory address,
[00:13:20 - 00:13:29] il memoria address, il memoria data registra, il memoria address registra invece lavora,
[00:13:30 - 00:13:37] indirizzando la memoria per parole. Ok, invece il programmante è per BITE, quindi si sposta
[00:13:38 - 00:13:44] di BITE in BITE, mentre il memoria address è di parola in parola. Le parole potete comunque
[00:13:44 - 00:13:54] essere con un parculo, che sono quattro BITE o comunque un mustito dei BITE. Allora,
[00:13:55 - 00:13:59] la volta incrementato il program counter, abbiamo quindi il nuovo valore che dobbiamo prelevare
[00:14:00 - 00:14:05] e quindi iniziamo a fare la richiesta la memoria di prelevare il BITE successivo, perché lo dobbiamo
[00:14:05 - 00:14:15] andare a salvare nelle le vierre. Questo, diciamo, BITE, prima o poi, quando, diciamo, la memoria
[00:14:16 - 00:14:21] ci prenderà il suo tempo per fornirlo, una volta che arriverà, noi sappiamo già che ci
[00:14:22 - 00:14:30] sentirà o perché è un operando o perché è la prossima istuzione da seguire. Ok, ad esempio
[00:14:30 - 00:14:39] l'estuzione YAD non c'è l'operando e quindi il prossimo BITE è l'estuzione successiva.
[00:14:42 - 00:14:52] Abbiamo detto che quando effettiamo, cioè quando realizziamo un specifio principale, il valore
[00:14:52 - 00:15:04] di MBIRE è già stato settato dall'ultro programma precedente e contiene il valore
[00:15:04 - 00:15:10] dell'OPCODE che ci fa capire che istuzione di livello ISA dobbiamo osservire.
[00:15:22 - 00:15:28] Allora, il fatto che io adesso vado a richiedere il previevo del BITE successivo, ricordiamo
[00:15:28 - 00:15:38] che siamo in tempo di domenio quattro da una memoria, quindi sarà disponibile dopo varie, diciamo,
[00:15:39 - 00:15:50] migliori stazioni. Poi potrebbe anche non servire, se per il caso non saltiamo all'estuzione successiva
[00:15:50 - 00:15:59] ma a un'altra, però nel frattempo che noi stiamo accendendo atto tre settimi, viene comunque fatto
[00:15:59 - 00:16:10] partito il previevo del BITE successivo. Ora, se il BITE contenuto nell'MBIRE contiene
[00:16:10 - 00:16:24] tutto il zero, viene associato a una particolare istuzione, che è l'estuzione NOF. Questa istuzione, diciamo,
[00:16:24 - 00:16:38] si trova all'effettiva locazione zero della memoria di controllo. Queste sono, diciamo, i microprogrammi
[00:16:38 - 00:16:51] che implementano le istuzioni. Nella memoria di controllo la microstruzione NOF, che, diciamo,
[00:16:51 - 00:16:58] non esegue nulla, ha solo il SATO a menuno, si trova effettivamente memorizzata nella locazione
[00:16:58 - 00:17:08] della memoria di controllo BITE a zero. È sempre semplicemente a fare il SATO all'inizio
[00:17:08 - 00:17:16] del cibo principale, dove sarà ritretuta, diciamo, la sequenza di interpretazione di un nuovo
[00:17:16 - 00:17:23] prod-intremento con l'alcantere il piesto del BITE successivo.
[00:17:23 - 00:17:34] Sì, è passata l'istuzione successiva. Sì, è la microstruzione successiva.
[00:17:34 - 00:17:37] Quindi diciamo...
[00:17:42 - 00:17:47] Qua sempre è fatta che le microstruzioni della memoria di controllo non sono memorizzate in maniera
[00:17:47 - 00:17:58] sequenziale, ma sono memorizzate in base, diciamo, al loro agilizzo, cioè dove è necessario.
[00:17:58 - 00:18:05] Quindi la microstruzione MENU non si troverà all'indilizzo zero, perché all'indilizzo zero
[00:18:05 - 00:18:11] c'è l'istruzione che ha come conciutere a tipo zero.
[00:18:11 - 00:18:20] Proprio perché quell'oppo conto che noi andiamo a leggere nell'MDR è proprio,
[00:18:20 - 00:18:26] se ho poi una memoria di controllo dove andiamo a frellevare, la microstruzione che implementa
[00:18:26 - 00:18:31] quell'istuzione di nello ISA. Quindi se non abbiamo fatto il ciclo di nello ISA e abbiamo
[00:18:31 - 00:18:46] prelevato l'istuzione zero più di zero, nell'MDR abbiamo più di zero, quello sarà, diciamo,
[00:18:46 - 00:18:52] indicherà che vai seguito il mitro programma temorizzato nella locazione zero nella memoria
[00:18:52 - 00:18:59] di controllo. Se c'è zero sessanta IAD, vuol dire che nella memoria di controllo sarà
[00:18:59 - 00:19:04] nella locazione del sessanta IAD.
[00:19:04 - 00:19:13] Ovviamente quindi poi le microstruzioni microprogrammi, le memorie di controllo,
[00:19:13 - 00:19:20] sono mani posizionati appunto a quello, diciamo, opportunamente in base all'indizia
[00:19:20 - 00:19:24] di essere associati.
[00:19:34 - 00:19:41] Queste, diciamo, microstruzioni anche se si trovano in posizioni, diciamo,
[00:19:41 - 00:19:46] in locazioni non contigui della memoria di controllo, sono comunque collegate tra loro
[00:19:46 - 00:19:53] come se fosse una lista di quegli elementi di tutta, non l'acquitiamo, ogni elemento
[00:19:53 - 00:19:59] punto al successivo. E quindi ogni microstruzione con l'estaglio
[00:19:59 - 00:20:05] si indica appunto qual è la prossima microstruzione che compone il mitro programma che si sta
[00:20:05 - 00:20:16] presentando. Ogni microprogramma, però, comincia sempre al valore numerico dell'Occult,
[00:20:16 - 00:20:23] dell'essuzione di livello ISA. Il valore delle belle pierre, il valore delle belle pierre
[00:20:23 - 00:20:32] mi da, diciamo, la prima microstruzione del mitro programma che implementa l'essuzione
[00:20:32 - 00:20:39] di livello ISA, e quindi si comincia da questa prima microstruzione, e poi seguendo
[00:20:39 - 00:20:46] l'estaglio, così, ricostruisce, diciamo, tutto il mitro programma di quella che implementa
[00:20:46 - 00:20:51] quell'essuzione di livello ISA. Mi sento, se non avevo visto i ad, che comincia
[00:20:51 - 00:20:57] al 060, scusate, poppo, l'essuzione dell'Occult, che invece comincia al 050. Cioè,
[00:20:57 - 00:21:06] comincia, è memorizzata l'indirizzo 057 della memoria di Occult. Ovviamente è sicuro
[00:21:06 - 00:21:16] solo dove comincia, cioè, dove è la prima microstruzione, poi, diciamo, la straquenza
[00:21:16 - 00:21:24] del mitro programma, o è completamente determinata dall'estadio, se non ci sono jump nel mitro
[00:21:24 - 00:21:40] programma, oppure se ci sono salti condizionati o anche cambiare. Con questo terminato, poi,
[00:21:40 - 00:21:50] diciamo, nella l'ultima lezione, vedremo, torniamo di qua. Abbiamo detto che, per come l'abbiamo
[00:21:50 - 00:21:56] scritti questi mitro programmi, noi in cui ogni viga identifica tutta l'operazione che
[00:21:56 - 00:22:03] si svolgono nel stesso sito di TOC, quindi, cosa vuol dire questo? Che i ad, il mitro
[00:22:03 - 00:22:12] programma che implementa i ad, ci metterà quattro cicli, così, su, e così. Vedremo
[00:22:12 - 00:22:19] che una prossima lezione, che è un modo per velocizzare le prestazioni, diciamo, per
[00:22:19 - 00:22:28] gli ad, le prestazioni, è ridurre, ovviamente, il numero di cicli di TOC necessari per implementare
[00:22:28 - 00:22:35] un'estruzione. E questo lo si fa, cioè lo si può fare andando appunto a ridurre il numero
[00:22:35 - 00:22:42] di microstruzioni, invece di essere o meglio, ad accorciare il microprogramma in modo che,
[00:22:42 - 00:22:47] invece di metterci quattro cicli, ce ne mette tre, così, qui. Può essere una strategia,
[00:22:47 - 00:22:52] questa ne metterò altre, però questa può essere una strategia per prendere più veloce
[00:22:52 - 00:23:01] le secuzioni. O, ovviamente, diciamo, aumentare la frequenza di glocto, oppure, invece di andare
[00:23:02 - 00:23:09] a lavorare sull'ottinizzazione del microprogramma, cercare di fare più operazioni nello stesso
[00:23:10 - 00:23:17] intervallo di tempo. Sono domande?
[00:23:31 - 00:23:40] Allora, vi lascio i bri da uno bombando e ci vediamo all'ultima lezione di giovedì
[00:23:40 - 00:23:44] per essere. Ok.
[00:23:44 - 00:23:45] Ma, secondo me, sei qua?
[00:23:45 - 00:23:47] Grazie mille, per questo.
[00:23:47 - 00:23:48] Arrivederci, grazie.
[00:23:48 - 00:23:49] Ciao, madrinata.
[00:24:01 - 00:24:08] Grazie mille.
[00:24:31 - 00:24:38] Grazie mille.
[00:25:01 - 00:25:08] Grazie mille.
[00:25:31 - 00:25:41] Grazie mille.
[00:26:01 - 00:26:11] Grazie mille.
[00:26:31 - 00:26:41] Grazie mille.
[00:27:01 - 00:27:11] Grazie mille.
[00:27:31 - 00:27:41] Grazie mille.
[00:28:01 - 00:28:11] Grazie mille.
[00:28:31 - 00:28:41] Grazie mille.
[00:29:01 - 00:29:11] Grazie mille.
[00:29:31 - 00:29:41] Grazie mille.
[00:30:01 - 00:30:11] Grazie mille.
[00:30:11 - 00:30:21] Grazie mille.
[00:30:21 - 00:30:31] Grazie mille.
[00:30:31 - 00:30:41] Grazie mille.
[00:30:41 - 00:30:51] Grazie mille.
[00:30:51 - 00:31:01] Grazie mille.
[00:31:01 - 00:31:11] Grazie mille.
[00:31:11 - 00:31:21] Grazie mille.
[00:31:21 - 00:31:31] Grazie mille.
[00:31:31 - 00:31:41] Grazie mille.
[00:31:41 - 00:31:51] Grazie mille.
[00:31:51 - 00:32:01] Grazie mille.
[00:32:01 - 00:32:11] Grazie mille.
[00:32:11 - 00:32:21] Grazie mille.
[00:32:21 - 00:32:31] Grazie mille.
[00:32:31 - 00:32:41] Grazie mille.
[00:32:41 - 00:32:51] Grazie mille.
[00:32:51 - 00:33:01] Grazie mille.
[00:33:01 - 00:33:11] Grazie mille.
[00:33:11 - 00:33:23] Grazie mille.
