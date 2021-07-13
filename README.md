# xeonsoft_project

A feladatom egy univerzális, adaptálható neurális hálózatot használó, bármilyen felhasználó által könnyen kezelhető alkalmazás létrehozása, mely rendkívül olcsó hardveren is képes
futni, és segítségével bármilyen, a felhasználó által megadott termékről eldönthető, hogy hibás-e.

Ennek megvalósításához a Google Colab számítási kapacitását fogom használni, melynek segítségével már meglévő neurális hálózatokat fogok "áttanítani", ráilleszteni a felhasználó 
által kívánt termékre.
A felhasználónak csupán meg kell adnia valamennyi (kb. 100-100) képet a "jó", illetve a "rossz" termékekről, az ezek alapján a Google Colab segítségével betanított neurális 
hálózatot akár egy Raspberry Pi szintű hardver is képes használni.

Az éles rendszer élő kameraképből fog bemenetet küldeni a hálózatnak, mely a kimenet függvényében más-más jelzést fog adni. Az alkalmazás egyszerre több kamerát is támogat majd,
ezeket az IP címük megadásával lesz majd lehetőség hozzáadni.
