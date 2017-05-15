# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-20 14:21
from __future__ import unicode_literals

from django.db import migrations

new_addresses = {
'mrose@twg.com': 2455, # Marshall Rose (1085)
'mrose@psi.com': 2455, # Marshall Rose (1187)
'jpo@cs.nott.ac.uk': 3564, # Julian P. Onions (1086)
'case@utkux1.utk.edu': 2331, # Dr. Jeff D. Case (1089)
'sollins@xx.lcs.mit.edu': 3029, # Dr. Karen R. Sollins (1107)
'cerf@a.isi.edu': 3, # Dr. Vinton G. Cerf (1109)
'vcerf@isoc.org': 3, # Vinton G. Cerf (1790)
'mckenzie@bbn.com': 53, # Alexander McKenzie (1110)
'deering@pescadero.stanford.edu': 9009, # Dr. Steve E. Deering (1112)
'deering@xerox.com': 9009, # Steve Deering (1191)
'krol@uxc.cso.uiuc.edu':  304, # Edward M. Krol (1118)
'hagens@cs.wisc.edu': 2372, # Robert Hagens (1139)
'gmalkin@proteon.com': 2412, # Gary S. Malkin (1150) 
'gmalkin@ftp.com': 2412, # Gary S. Malkin (1177) 
'mrc@tomobiki-cho.cac.washington.edu': 3346, # Mark Crispin (1176)
'utf9@lingling.panda.com': 3346, # Mark Crispin (4042)
'april@nic.ddn.mil': 4356, # April Marine (1177)
'april@nisc.sri.com': 4356, # April N. Marine (1325)
'ferrari@ucbvax.berkeley.edu': 3599, # Dr. Domenico Ferrari (1193)
'dave@sabre.bellcore.com': 2775, # David M. Piscitello (1209) 
'sob@harvard.harvard.edu': 2324, # Scott O. Bradner (1242)
'craig@sics.se': 1307, # Dr. Craig Partridge (1257) 
'topolcic@nri.reston.va.us': 2828, # Claudio M. Topolcic (1367)
'jwong@garage.att.com': 8198, # Jeff A. Wong (1433)
'chim@relito.medeng.wfu.edu': 118803, # William Chimiak (1453)
'housley.mclean_csd@xerox.com': 5376, # Russ Housley (1457)
'mohta@cc.titech.ac.jp': 11038, # Dr. Masataka Ohta (1554)
'3858921@mcimail.com': 10836, # Robert G. Moskowitz (1597)
'rgm3@is.chrysler.com': 10836, # Robert G. Moskowitz (1918) 
'mpullen@cs.gmu.edu': 14437, # Dr. Mark Pullen(1667)
'phill_gross@mcimail.com': 2791, # Phillip G. Gross (1719)
'gnc@ginger.lcs.mit.edu': 2662, # J. Noel Chiappa (1992)
'hallam@w3.org': 110217, # Phillip Hallam-Baker (2069)
'guerin@watson.ibm.com': 6128, # Dr. Roch Guerin (2212)
'sri@att.com': 8225, # Dr. Srinivas R. Sataluri (2247)
'rdaniel@acl.lanl.gov': 17304, # Dr. Ron Daniel (2288)
'ted_kuo@baynetworks.com': 13252, # Ted Kuo (2320)
'c.perkins@cs.ucl.ac.uk': 20209, # Dr. Colin Perkins (2354)
'mjs@securify.com': 17237, # Mark J. Schertler (2408)
'corson@isr.umd.edu': 19037, # Dr. Scott M. Corson (2501)
'mday@vinca.com': 101325, # Michael D. Day (2608)
'michael.mealling@rwhois.net': 9497, # Michael H. Mealling (2651)
'walshp@lucent.com': 103289, # Pat Walsh (2989)
'chopps@nexthop.com': 22933, # Christian Hopps (2991)
'robart@nortelnetworks.com': 102393, # Lewis C. Robart (2995)
'fredette@photonex.com': 21059, # Dr. Andre N. Fredette (3036)
'pcain@bbn.com': 20713, # Patrick Cain (3161)
'kawano@core.ecl.net': 20826, # Dr. Tetsuo Kawano (3186)
'yves.tjoens@alcatel.be': 102145, # Yves T'Joens (3203)
'muckai@atoga.com': 101632,#  Dr. Muckai K. Girish (3213)
'schooler@research.att.com': 5439, # Eve M. Schooler (3261)
'jh@song.fi': 4319, # Dr. Juha Heinanen (3270)
'pat_thaler@agilent.com': 112851, # Patricia Thaler (3385)
'burcak@juniper.net': 101833, # Burcak N. Beser (3495)
'mstewart1@nc.rr.com': 104837, # Mark Stewart (3591)
'dan.grossman@motorola.com': 6564, # Daniel B. Grossman (3819)
'hbbeykirch@web.de': 104273, # Hans Beykirch (3867)
'coar@apache.org': 100988, # Ken A.L. Coar (3875)
'dvenable@crt.xerox.com': 22957, # Dr. Dennis L. Venable (3949)
'hannsjuergen.schwarzbauer@siemens.com': 103471, # Dr. HannsJuergen Schwarzbauer (4165)
'dmaltz@microsoft.com': 101236, # Dave A. Maltz (4728)
'yihchun@uiuc.edu': 101395, # Yih-Chun Hu (4728)
'yakov@juniper.com': 10535, # Yakov Rekhter (4760)
'hong-yon.lach@motorola.com': 104527, # Hong Lach(4885)
'bgp-confederations@st04.pst.org': 6819, # Paul S. Traina (5065)
'dhaval@moowee.tv': 21770, # Dhaval Shah (5140)
'hsalama@citexsoftware.com': 102549, # Dr. Hussein F. Salama (5140)
'steve.vogelsang@alcatel-lucent.com': 104509, # Stephen Vogelsang (5143)
'fredi@entel.upc.es': 106027, # Fredric Raspall (5475)
'mjl@caida.org': 106174, # Matthew J. Luckie (7514)

'kzm@hplabs.hp.com': 2731, #,Keith McCloghrie (1155)
'mathis@faraday.ece.cmu.edu': 2674, # Matt Mathis (1164)
'ariel@relay.prime.com': 4418, # Robert Ullman (1183)
'pvm@isi.edu': 1310, # Dr. Paul V. Mockapetris (1183)
'craig_everhart@transarc.com': 2867, # Craig Everhart (1183)
'louie@sayshell.umd.edu': 2413, # Louis A. Mamakos (1183)
'jcl@sabre.bellcore.com': 2883, # Joe L. Lawrence (1209)
'colella@osi3.ncsl.nist.gov': 2738, # Richard P. Colella (1237)
'callon@bigfut.enet.dec.com': 2723, # Ross Callon (1237)
'scottw@diis.ddn.mil': 5263, # Scott Williamson (1261)
'tbradley@wellfleet.com': 4040, # Terry Bradley (1293)
'weider@ans.net': 3428, # Chris Weider (1309)
'cohen@isi.edu': 184, # Dr. Danny Cohen (1357)
'boss@sunet.se': 3733, # Bernhard Stockman (1404)
'kannan@sejour.lkg.dec.com': 5794, # Kannan Alagappan (1412)
'klensin@infoods.unu.edu': 106911, # John C. Klensin (1425)
'vcerf@cnri.reston.va.us': 3, # Dr. Vinton G. Cerf (1430)
'jsq@tic.com': 1674, # John S. Quarterman (1432)
'linn@gza.com': 3385, # John Linn (1508)
'vinton_cerf@mcimail.com': 3, # Dr. Vinton G. Cerf (1607)
'bcole@cisco.com': 10341, # Bruce A. Cole (1664)
'iana@isi.edu': 105716, # IANA (1797)
'yee@atlas.arc.nasa.gov': 113428, # Peter Yee (1803)
'getchell@es.net': 4504, # Arlene Getchell (1803)
'frederic@parc.xerox.com': 8677, # Ron Frederick (1889)
'tli@skat.usc.edu': 4475, # Dr. Tony Li (1997)
'gerry@europe.shiva.com': 10451, # Dr. Gerry Meyer (2091)
'michaelm@internic.net': 9497, # Michael H. Mealling (2168)
'christian.maciocco@intel.com': 10459, # Christian Maciocco (2429)
'thomas.r.gardos@intel.com': 101230, # Dr. Thomas R. Gardos (2429)
'gim.l.deisher@intel.com': 22906, # Gim L. Deisher (2429)
'donald.newell@intel.com': 21437, # Donald Newell (2429)
'hal@pgp.com': 100795, # Hal Finney (2440)
'rodney@unitran.com': 8663, # Rodney L. Thayer (2440)
'mark.hoy@mainbrace.com': 100841, # Mark Hoy (2442)
'tds@lucent.com': 113202, # A. DeSimone (2458)
'eric.baize@bull.com': 18674, # Eric Baize (2478)
'sanjayk@dnrc.bell-labs.com': 21758, # Sanjay Kamat (2676)
'jboyle@level3.net': 20451, # Jim Boyle (2748)
'asastry@cisco.com': 17769, # Arun Sastry (2748)
'ronc@cisco.com': 20097, # Ron Cohen (2748)
'raju@research.att.com': 19384, # Raju Rajan (2749)
'arnt@troll.no': 18315, # Arnt Gulbrandsen (2782)
'tony1@home.net': 4475, # Dr. Tony Li (2784)
'angelos@cis.upenn.edu': 18975, # Angelos D. Keromytis (2792)
'jrv@interlinknetworks.com': 2856, # John Vollbrecht (2903)
'pmoore@peerless.com': 100005, # Paul Moore (2910)
'yxu@watercove.com': 103295, # Yingchun Xu (2989)
'eyal@sanrad.com': 102526, # Eyal Felstaine (2998)
'mstevens@ellacoya.com': 102976, # Mark L. Stevens (3127)
'bklim@lge.com': 103292, # Byung-Keun Lim (3141)
'mmunson@gte.net': 102715, # Mark Munson (3141)
'charles.lo@vodafone-us.com': 102827, # Charles N. Lo (3141)
'serge@awardsolutions.com': 103296, # Serge Manning (3141)
'afredette@charter.net': 21059,# Dr. Andre N. Fredette (3212)
'pdoolan@acm.org': 20531, # Paul Doolan (3212)
'loa.andersson@utfors.se': 20682, # Loa Andersson (3212)
'mbaker@planetfred.com': 102843, # Mark Baker (3236)
'paolo.crivellari@belgacom.be': 101265, # Paolo Crivellari (3301)
'garyfishman@lucent.com': 105628, # Gary Fishman (3356)
'hain@tndh.net': 9051, # Tony L. Hain (3363)
'jeff@redback.com': 8669, # Jeff T. Johnson (3498)
'timur.friedman@lip6.fr': 104338, # Timur Friedman (3611)
'caceres@watson.ibm.com': 10929, # Ramon Caceres (3611)
'cmonia@pacbell.net': 104763, # Charles Monia (3643)
'roweber@ieee.org': 105152, # Ralph Weber (3643)
'milan.merhar@sun.com': 100798, # Milan Merhar (3643)
'konishi@jp.apan.net': 6273, # Kazunori Konishi (3743)
'bob@airespace.com': 106531L, # Bob O'Hara (3990) 
'bob.ohara@computer.org': 106531L, # Bob O'Hara (5412)
'falk@isi.edu': 21226, # Aaron Falk (4440)
'junhyuk.song@gmail.com': 105239, # Junhyuk Song (4615)
'iab@ietf.org': 104167, # IAB (4732)
'jasdips@rwhois.net': 18211, # Jasdip Singh (2167)
'audet@nortelnetworks.com': 20858, # Francois Audet (3204)
'mzonoun@nortelnetworks.com': 101819, # Mo R. Zonoun (3204)
'kasten@europa.clearpoint.com': 2706, # Frank Kastenholz (1284)
'dee@ranger.enet.dec.com': 102391, # Donald E. Eastlake (1455)

}


def forward(apps,schema_editor):

    Email=apps.get_model('person','Email')

    # Sanity check
    for addr in new_addresses.keys():
        if Email.objects.filter(address__iexact=addr).exists():
            raise Exception("%s already exists in the Email table"%addr)

    for addr in new_addresses.keys():
        Email.objects.create(address=addr,person_id=new_addresses[addr],active=False,primary=False)

def reverse(apps,schema_editor):
    Email=apps.get_model('person','Email')
    #Person=apps.get_model('person','Person')
    #print "new_addresses = {"
    #for addr in sorted(new_addresses.keys()):
    #    print "'%s': %s, # %s"%(addr,new_addresses[addr],Person.objects.get(pk=new_addresses[addr]).name) 
    #print "}"
    Email.objects.filter(address__in=new_addresses.keys()).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('person', '0017_add_email_address_from_parsed_rfcs'),
    ]

    operations = [
        migrations.RunPython(forward,reverse)
    ]
