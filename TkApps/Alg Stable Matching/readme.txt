StableMatching.py
* egyszerű felhasználási módja a Gayle-Shapley algoritmusnak, eredetileg játékosok és csapatok összepárosításának indult
- lásd a kódban használt elnevezések -, de végül is általánosan is felhasználhatóvá tettem a kis projektet: Tkinter GUI-
t kapott, semmi extra, minimális dizájn. Két bármely - azonos méretű - csoportot párosít össze optimálisan a megadott
preferencia-listák alapján.

* a simple implementation of the Stable Matching algorithm. Originally made for matching players with teams - hence the
variable names of the code -, then decided to be made for various uses. The program has a simple, easy to use TK GUI,
minimalist in design. Function: to pair two equal sized groups according to given preferences. It uses stable matching
algorithm to ensure the best possible outcome that is optimal for both groups..

========================================================================================================================
Használat:
Group1 és Group2: a két csoport, tagjait szóközök nélkül, vesszővel elválasztva kell megadni.
Pref1 és Pref2: preferencia-listák, szóköz nélkül, vesszővel, csoport elemenként új sort kezdeni!
További elemek megadása ennek alapján...

//Help gomb/button//
Instructions:
Group1 / Group2 --> Comma-separated, no spaces!
Prefs1 / Prefs2 --> Comma-separated, no spaces, line breaks (new rows per Group members)
Add more inputs accordingly!

========================================================================================================================
Hasznos információk a témáról (Gayle-Shapley), az algoritmus logikájának áttekintése:
For more details on the Gayle-Shapley Algorithm and to learn the basics of "stable matching":

https://www.geeksforgeeks.org/stable-marriage-problem/
https://www.youtube.com/watch?v=FhRf0j068ZA

A folyamat lépései:
A GIF for visualization of the whole process:
https://en.wikipedia.org/wiki/Stable_marriage_problem#/media/File:Gale-Shapley.gif
