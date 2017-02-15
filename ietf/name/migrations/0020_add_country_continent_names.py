# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def insert_initial_country_continent_names(apps, schema_editor):
    ContinentName = apps.get_model("name", "ContinentName")
    africa, _ = ContinentName.objects.get_or_create(slug="africa", name="Africa")
    antarctica, _ = ContinentName.objects.get_or_create(slug="antarctica", name="Antarctica")
    asia, _ = ContinentName.objects.get_or_create(slug="asia", name="Asia")
    europe, _ = ContinentName.objects.get_or_create(slug="europe", name="Europe")
    north_america, _ = ContinentName.objects.get_or_create(slug="north-america", name="North America")
    oceania, _ = ContinentName.objects.get_or_create(slug="oceania", name="Oceania")
    south_america, _ = ContinentName.objects.get_or_create(slug="south-america", name="South America")

    CountryName = apps.get_model("name", "CountryName")
    CountryName.objects.get_or_create(slug="AD", name=u"Andorra", continent=europe)
    CountryName.objects.get_or_create(slug="AE", name=u"United Arab Emirates", continent=asia)
    CountryName.objects.get_or_create(slug="AF", name=u"Afghanistan", continent=asia)
    CountryName.objects.get_or_create(slug="AG", name=u"Antigua and Barbuda", continent=north_america)
    CountryName.objects.get_or_create(slug="AI", name=u"Anguilla", continent=north_america)
    CountryName.objects.get_or_create(slug="AL", name=u"Albania", continent=europe)
    CountryName.objects.get_or_create(slug="AM", name=u"Armenia", continent=asia)
    CountryName.objects.get_or_create(slug="AO", name=u"Angola", continent=africa)
    CountryName.objects.get_or_create(slug="AQ", name=u"Antarctica", continent=antarctica)
    CountryName.objects.get_or_create(slug="AR", name=u"Argentina", continent=south_america)
    CountryName.objects.get_or_create(slug="AS", name=u"American Samoa", continent=oceania)
    CountryName.objects.get_or_create(slug="AT", name=u"Austria", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="AU", name=u"Australia", continent=oceania)
    CountryName.objects.get_or_create(slug="AW", name=u"Aruba", continent=north_america)
    CountryName.objects.get_or_create(slug="AX", name=u"Åland Islands", continent=europe)
    CountryName.objects.get_or_create(slug="AZ", name=u"Azerbaijan", continent=asia)
    CountryName.objects.get_or_create(slug="BA", name=u"Bosnia and Herzegovina", continent=europe)
    CountryName.objects.get_or_create(slug="BB", name=u"Barbados", continent=north_america)
    CountryName.objects.get_or_create(slug="BD", name=u"Bangladesh", continent=asia)
    CountryName.objects.get_or_create(slug="BE", name=u"Belgium", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="BF", name=u"Burkina Faso", continent=africa)
    CountryName.objects.get_or_create(slug="BG", name=u"Bulgaria", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="BH", name=u"Bahrain", continent=asia)
    CountryName.objects.get_or_create(slug="BI", name=u"Burundi", continent=africa)
    CountryName.objects.get_or_create(slug="BJ", name=u"Benin", continent=africa)
    CountryName.objects.get_or_create(slug="BL", name=u"Saint Barthélemy", continent=north_america)
    CountryName.objects.get_or_create(slug="BM", name=u"Bermuda", continent=north_america)
    CountryName.objects.get_or_create(slug="BN", name=u"Brunei", continent=asia)
    CountryName.objects.get_or_create(slug="BO", name=u"Bolivia", continent=south_america)
    CountryName.objects.get_or_create(slug="BQ", name=u"Bonaire, Sint Eustatius and Saba", continent=north_america)
    CountryName.objects.get_or_create(slug="BR", name=u"Brazil", continent=south_america)
    CountryName.objects.get_or_create(slug="BS", name=u"Bahamas", continent=north_america)
    CountryName.objects.get_or_create(slug="BT", name=u"Bhutan", continent=asia)
    CountryName.objects.get_or_create(slug="BV", name=u"Bouvet Island", continent=antarctica)
    CountryName.objects.get_or_create(slug="BW", name=u"Botswana", continent=africa)
    CountryName.objects.get_or_create(slug="BY", name=u"Belarus", continent=europe)
    CountryName.objects.get_or_create(slug="BZ", name=u"Belize", continent=north_america)
    CountryName.objects.get_or_create(slug="CA", name=u"Canada", continent=north_america)
    CountryName.objects.get_or_create(slug="CC", name=u"Cocos (Keeling) Islands", continent=asia)
    CountryName.objects.get_or_create(slug="CD", name=u"Congo (the Democratic Republic of the)", continent=africa)
    CountryName.objects.get_or_create(slug="CF", name=u"Central African Republic", continent=africa)
    CountryName.objects.get_or_create(slug="CG", name=u"Congo", continent=africa)
    CountryName.objects.get_or_create(slug="CH", name=u"Switzerland", continent=europe)
    CountryName.objects.get_or_create(slug="CI", name=u"Côte d'Ivoire", continent=africa)
    CountryName.objects.get_or_create(slug="CK", name=u"Cook Islands", continent=oceania)
    CountryName.objects.get_or_create(slug="CL", name=u"Chile", continent=south_america)
    CountryName.objects.get_or_create(slug="CM", name=u"Cameroon", continent=africa)
    CountryName.objects.get_or_create(slug="CN", name=u"China", continent=asia)
    CountryName.objects.get_or_create(slug="CO", name=u"Colombia", continent=south_america)
    CountryName.objects.get_or_create(slug="CR", name=u"Costa Rica", continent=north_america)
    CountryName.objects.get_or_create(slug="CU", name=u"Cuba", continent=north_america)
    CountryName.objects.get_or_create(slug="CV", name=u"Cabo Verde", continent=africa)
    CountryName.objects.get_or_create(slug="CW", name=u"Curaçao", continent=north_america)
    CountryName.objects.get_or_create(slug="CX", name=u"Christmas Island", continent=asia)
    CountryName.objects.get_or_create(slug="CY", name=u"Cyprus", continent=asia, in_eu=True)
    CountryName.objects.get_or_create(slug="CZ", name=u"Czech Republic", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="DE", name=u"Germany", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="DJ", name=u"Djibouti", continent=africa)
    CountryName.objects.get_or_create(slug="DK", name=u"Denmark", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="DM", name=u"Dominica", continent=north_america)
    CountryName.objects.get_or_create(slug="DO", name=u"Dominican Republic", continent=north_america)
    CountryName.objects.get_or_create(slug="DZ", name=u"Algeria", continent=africa)
    CountryName.objects.get_or_create(slug="EC", name=u"Ecuador", continent=south_america)
    CountryName.objects.get_or_create(slug="EE", name=u"Estonia", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="EG", name=u"Egypt", continent=africa)
    CountryName.objects.get_or_create(slug="EH", name=u"Western Sahara", continent=africa)
    CountryName.objects.get_or_create(slug="ER", name=u"Eritrea", continent=africa)
    CountryName.objects.get_or_create(slug="ES", name=u"Spain", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="ET", name=u"Ethiopia", continent=africa)
    CountryName.objects.get_or_create(slug="FI", name=u"Finland", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="FJ", name=u"Fiji", continent=oceania)
    CountryName.objects.get_or_create(slug="FK", name=u"Falkland Islands  [Malvinas]", continent=south_america)
    CountryName.objects.get_or_create(slug="FM", name=u"Micronesia (Federated States of)", continent=oceania)
    CountryName.objects.get_or_create(slug="FO", name=u"Faroe Islands", continent=europe)
    CountryName.objects.get_or_create(slug="FR", name=u"France", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="GA", name=u"Gabon", continent=africa)
    CountryName.objects.get_or_create(slug="GB", name=u"United Kingdom", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="GD", name=u"Grenada", continent=north_america)
    CountryName.objects.get_or_create(slug="GE", name=u"Georgia", continent=asia)
    CountryName.objects.get_or_create(slug="GF", name=u"French Guiana", continent=south_america)
    CountryName.objects.get_or_create(slug="GG", name=u"Guernsey", continent=europe)
    CountryName.objects.get_or_create(slug="GH", name=u"Ghana", continent=africa)
    CountryName.objects.get_or_create(slug="GI", name=u"Gibraltar", continent=europe)
    CountryName.objects.get_or_create(slug="GL", name=u"Greenland", continent=north_america)
    CountryName.objects.get_or_create(slug="GM", name=u"Gambia", continent=africa)
    CountryName.objects.get_or_create(slug="GN", name=u"Guinea", continent=africa)
    CountryName.objects.get_or_create(slug="GP", name=u"Guadeloupe", continent=north_america)
    CountryName.objects.get_or_create(slug="GQ", name=u"Equatorial Guinea", continent=africa)
    CountryName.objects.get_or_create(slug="GR", name=u"Greece", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="GS", name=u"South Georgia and the South Sandwich Islands", continent=antarctica)
    CountryName.objects.get_or_create(slug="GT", name=u"Guatemala", continent=north_america)
    CountryName.objects.get_or_create(slug="GU", name=u"Guam", continent=oceania)
    CountryName.objects.get_or_create(slug="GW", name=u"Guinea-Bissau", continent=africa)
    CountryName.objects.get_or_create(slug="GY", name=u"Guyana", continent=south_america)
    CountryName.objects.get_or_create(slug="HK", name=u"Hong Kong", continent=asia)
    CountryName.objects.get_or_create(slug="HM", name=u"Heard Island and McDonald Islands", continent=antarctica)
    CountryName.objects.get_or_create(slug="HN", name=u"Honduras", continent=north_america)
    CountryName.objects.get_or_create(slug="HR", name=u"Croatia", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="HT", name=u"Haiti", continent=north_america)
    CountryName.objects.get_or_create(slug="HU", name=u"Hungary", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="ID", name=u"Indonesia", continent=asia)
    CountryName.objects.get_or_create(slug="IE", name=u"Ireland", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="IL", name=u"Israel", continent=asia)
    CountryName.objects.get_or_create(slug="IM", name=u"Isle of Man", continent=europe)
    CountryName.objects.get_or_create(slug="IN", name=u"India", continent=asia)
    CountryName.objects.get_or_create(slug="IO", name=u"British Indian Ocean Territory", continent=asia)
    CountryName.objects.get_or_create(slug="IQ", name=u"Iraq", continent=asia)
    CountryName.objects.get_or_create(slug="IR", name=u"Iran", continent=asia)
    CountryName.objects.get_or_create(slug="IS", name=u"Iceland", continent=europe)
    CountryName.objects.get_or_create(slug="IT", name=u"Italy", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="JE", name=u"Jersey", continent=europe)
    CountryName.objects.get_or_create(slug="JM", name=u"Jamaica", continent=north_america)
    CountryName.objects.get_or_create(slug="JO", name=u"Jordan", continent=asia)
    CountryName.objects.get_or_create(slug="JP", name=u"Japan", continent=asia)
    CountryName.objects.get_or_create(slug="KE", name=u"Kenya", continent=africa)
    CountryName.objects.get_or_create(slug="KG", name=u"Kyrgyzstan", continent=asia)
    CountryName.objects.get_or_create(slug="KH", name=u"Cambodia", continent=asia)
    CountryName.objects.get_or_create(slug="KI", name=u"Kiribati", continent=oceania)
    CountryName.objects.get_or_create(slug="KM", name=u"Comoros", continent=africa)
    CountryName.objects.get_or_create(slug="KN", name=u"Saint Kitts and Nevis", continent=north_america)
    CountryName.objects.get_or_create(slug="KP", name=u"North Korea", continent=asia)
    CountryName.objects.get_or_create(slug="KR", name=u"South Korea", continent=asia)
    CountryName.objects.get_or_create(slug="KW", name=u"Kuwait", continent=asia)
    CountryName.objects.get_or_create(slug="KY", name=u"Cayman Islands", continent=north_america)
    CountryName.objects.get_or_create(slug="KZ", name=u"Kazakhstan", continent=asia)
    CountryName.objects.get_or_create(slug="LA", name=u"Laos", continent=asia)
    CountryName.objects.get_or_create(slug="LB", name=u"Lebanon", continent=asia)
    CountryName.objects.get_or_create(slug="LC", name=u"Saint Lucia", continent=north_america)
    CountryName.objects.get_or_create(slug="LI", name=u"Liechtenstein", continent=europe)
    CountryName.objects.get_or_create(slug="LK", name=u"Sri Lanka", continent=asia)
    CountryName.objects.get_or_create(slug="LR", name=u"Liberia", continent=africa)
    CountryName.objects.get_or_create(slug="LS", name=u"Lesotho", continent=africa)
    CountryName.objects.get_or_create(slug="LT", name=u"Lithuania", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="LU", name=u"Luxembourg", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="LV", name=u"Latvia", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="LY", name=u"Libya", continent=africa)
    CountryName.objects.get_or_create(slug="MA", name=u"Morocco", continent=africa)
    CountryName.objects.get_or_create(slug="MC", name=u"Monaco", continent=europe)
    CountryName.objects.get_or_create(slug="MD", name=u"Moldova", continent=europe)
    CountryName.objects.get_or_create(slug="ME", name=u"Montenegro", continent=europe)
    CountryName.objects.get_or_create(slug="MF", name=u"Saint Martin (French part)", continent=north_america)
    CountryName.objects.get_or_create(slug="MG", name=u"Madagascar", continent=africa)
    CountryName.objects.get_or_create(slug="MH", name=u"Marshall Islands", continent=oceania)
    CountryName.objects.get_or_create(slug="MK", name=u"Macedonia", continent=europe)
    CountryName.objects.get_or_create(slug="ML", name=u"Mali", continent=africa)
    CountryName.objects.get_or_create(slug="MM", name=u"Myanmar", continent=asia)
    CountryName.objects.get_or_create(slug="MN", name=u"Mongolia", continent=asia)
    CountryName.objects.get_or_create(slug="MO", name=u"Macao", continent=asia)
    CountryName.objects.get_or_create(slug="MP", name=u"Northern Mariana Islands", continent=oceania)
    CountryName.objects.get_or_create(slug="MQ", name=u"Martinique", continent=north_america)
    CountryName.objects.get_or_create(slug="MR", name=u"Mauritania", continent=africa)
    CountryName.objects.get_or_create(slug="MS", name=u"Montserrat", continent=north_america)
    CountryName.objects.get_or_create(slug="MT", name=u"Malta", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="MU", name=u"Mauritius", continent=africa)
    CountryName.objects.get_or_create(slug="MV", name=u"Maldives", continent=asia)
    CountryName.objects.get_or_create(slug="MW", name=u"Malawi", continent=africa)
    CountryName.objects.get_or_create(slug="MX", name=u"Mexico", continent=north_america)
    CountryName.objects.get_or_create(slug="MY", name=u"Malaysia", continent=asia)
    CountryName.objects.get_or_create(slug="MZ", name=u"Mozambique", continent=africa)
    CountryName.objects.get_or_create(slug="NA", name=u"Namibia", continent=africa)
    CountryName.objects.get_or_create(slug="NC", name=u"New Caledonia", continent=oceania)
    CountryName.objects.get_or_create(slug="NE", name=u"Niger", continent=africa)
    CountryName.objects.get_or_create(slug="NF", name=u"Norfolk Island", continent=oceania)
    CountryName.objects.get_or_create(slug="NG", name=u"Nigeria", continent=africa)
    CountryName.objects.get_or_create(slug="NI", name=u"Nicaragua", continent=north_america)
    CountryName.objects.get_or_create(slug="NL", name=u"Netherlands", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="NO", name=u"Norway", continent=europe)
    CountryName.objects.get_or_create(slug="NP", name=u"Nepal", continent=asia)
    CountryName.objects.get_or_create(slug="NR", name=u"Nauru", continent=oceania)
    CountryName.objects.get_or_create(slug="NU", name=u"Niue", continent=oceania)
    CountryName.objects.get_or_create(slug="NZ", name=u"New Zealand", continent=oceania)
    CountryName.objects.get_or_create(slug="OM", name=u"Oman", continent=asia)
    CountryName.objects.get_or_create(slug="PA", name=u"Panama", continent=north_america)
    CountryName.objects.get_or_create(slug="PE", name=u"Peru", continent=south_america)
    CountryName.objects.get_or_create(slug="PF", name=u"French Polynesia", continent=oceania)
    CountryName.objects.get_or_create(slug="PG", name=u"Papua New Guinea", continent=oceania)
    CountryName.objects.get_or_create(slug="PH", name=u"Philippines", continent=asia)
    CountryName.objects.get_or_create(slug="PK", name=u"Pakistan", continent=asia)
    CountryName.objects.get_or_create(slug="PL", name=u"Poland", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="PM", name=u"Saint Pierre and Miquelon", continent=north_america)
    CountryName.objects.get_or_create(slug="PN", name=u"Pitcairn", continent=oceania)
    CountryName.objects.get_or_create(slug="PR", name=u"Puerto Rico", continent=north_america)
    CountryName.objects.get_or_create(slug="PS", name=u"Palestine, State of", continent=asia)
    CountryName.objects.get_or_create(slug="PT", name=u"Portugal", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="PW", name=u"Palau", continent=oceania)
    CountryName.objects.get_or_create(slug="PY", name=u"Paraguay", continent=south_america)
    CountryName.objects.get_or_create(slug="QA", name=u"Qatar", continent=asia)
    CountryName.objects.get_or_create(slug="RE", name=u"Réunion", continent=africa)
    CountryName.objects.get_or_create(slug="RO", name=u"Romania", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="RS", name=u"Serbia", continent=europe)
    CountryName.objects.get_or_create(slug="RU", name=u"Russia", continent=europe)
    CountryName.objects.get_or_create(slug="RW", name=u"Rwanda", continent=africa)
    CountryName.objects.get_or_create(slug="SA", name=u"Saudi Arabia", continent=asia)
    CountryName.objects.get_or_create(slug="SB", name=u"Solomon Islands", continent=oceania)
    CountryName.objects.get_or_create(slug="SC", name=u"Seychelles", continent=africa)
    CountryName.objects.get_or_create(slug="SD", name=u"Sudan", continent=africa)
    CountryName.objects.get_or_create(slug="SE", name=u"Sweden", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="SG", name=u"Singapore", continent=asia)
    CountryName.objects.get_or_create(slug="SH", name=u"Saint Helena, Ascension and Tristan da Cunha", continent=africa)
    CountryName.objects.get_or_create(slug="SI", name=u"Slovenia", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="SJ", name=u"Svalbard and Jan Mayen", continent=europe)
    CountryName.objects.get_or_create(slug="SK", name=u"Slovakia", continent=europe, in_eu=True)
    CountryName.objects.get_or_create(slug="SL", name=u"Sierra Leone", continent=africa)
    CountryName.objects.get_or_create(slug="SM", name=u"San Marino", continent=europe)
    CountryName.objects.get_or_create(slug="SN", name=u"Senegal", continent=africa)
    CountryName.objects.get_or_create(slug="SO", name=u"Somalia", continent=africa)
    CountryName.objects.get_or_create(slug="SR", name=u"Suriname", continent=south_america)
    CountryName.objects.get_or_create(slug="SS", name=u"South Sudan", continent=africa)
    CountryName.objects.get_or_create(slug="ST", name=u"Sao Tome and Principe", continent=africa)
    CountryName.objects.get_or_create(slug="SV", name=u"El Salvador", continent=north_america)
    CountryName.objects.get_or_create(slug="SX", name=u"Sint Maarten (Dutch part)", continent=north_america)
    CountryName.objects.get_or_create(slug="SY", name=u"Syria", continent=asia)
    CountryName.objects.get_or_create(slug="SZ", name=u"Swaziland", continent=africa)
    CountryName.objects.get_or_create(slug="TC", name=u"Turks and Caicos Islands", continent=north_america)
    CountryName.objects.get_or_create(slug="TD", name=u"Chad", continent=africa)
    CountryName.objects.get_or_create(slug="TF", name=u"French Southern Territories", continent=antarctica)
    CountryName.objects.get_or_create(slug="TG", name=u"Togo", continent=africa)
    CountryName.objects.get_or_create(slug="TH", name=u"Thailand", continent=asia)
    CountryName.objects.get_or_create(slug="TJ", name=u"Tajikistan", continent=asia)
    CountryName.objects.get_or_create(slug="TK", name=u"Tokelau", continent=oceania)
    CountryName.objects.get_or_create(slug="TL", name=u"Timor-Leste", continent=asia)
    CountryName.objects.get_or_create(slug="TM", name=u"Turkmenistan", continent=asia)
    CountryName.objects.get_or_create(slug="TN", name=u"Tunisia", continent=africa)
    CountryName.objects.get_or_create(slug="TO", name=u"Tonga", continent=oceania)
    CountryName.objects.get_or_create(slug="TR", name=u"Turkey", continent=europe)
    CountryName.objects.get_or_create(slug="TT", name=u"Trinidad and Tobago", continent=north_america)
    CountryName.objects.get_or_create(slug="TV", name=u"Tuvalu", continent=oceania)
    CountryName.objects.get_or_create(slug="TW", name=u"Taiwan", continent=asia)
    CountryName.objects.get_or_create(slug="TZ", name=u"Tanzania", continent=africa)
    CountryName.objects.get_or_create(slug="UA", name=u"Ukraine", continent=europe)
    CountryName.objects.get_or_create(slug="UG", name=u"Uganda", continent=africa)
    CountryName.objects.get_or_create(slug="UM", name=u"United States Minor Outlying Islands", continent=oceania)
    CountryName.objects.get_or_create(slug="US", name=u"United States of America", continent=north_america)
    CountryName.objects.get_or_create(slug="UY", name=u"Uruguay", continent=south_america)
    CountryName.objects.get_or_create(slug="UZ", name=u"Uzbekistan", continent=asia)
    CountryName.objects.get_or_create(slug="VA", name=u"Holy See", continent=europe)
    CountryName.objects.get_or_create(slug="VC", name=u"Saint Vincent and the Grenadines", continent=north_america)
    CountryName.objects.get_or_create(slug="VE", name=u"Venezuela", continent=south_america)
    CountryName.objects.get_or_create(slug="VG", name=u"Virgin Islands (British)", continent=north_america)
    CountryName.objects.get_or_create(slug="VI", name=u"Virgin Islands (U.S.)", continent=north_america)
    CountryName.objects.get_or_create(slug="VN", name=u"Vietnam", continent=asia)
    CountryName.objects.get_or_create(slug="VU", name=u"Vanuatu", continent=oceania)
    CountryName.objects.get_or_create(slug="WF", name=u"Wallis and Futuna", continent=oceania)
    CountryName.objects.get_or_create(slug="WS", name=u"Samoa", continent=oceania)
    CountryName.objects.get_or_create(slug="YE", name=u"Yemen", continent=asia)
    CountryName.objects.get_or_create(slug="YT", name=u"Mayotte", continent=africa)
    CountryName.objects.get_or_create(slug="ZA", name=u"South Africa", continent=africa)
    CountryName.objects.get_or_create(slug="ZM", name=u"Zambia", continent=africa)
    CountryName.objects.get_or_create(slug="ZW", name=u"Zimbabwe", continent=africa)

class Migration(migrations.Migration):

    dependencies = [
        ('name', '0019_continentname_countryname'),
    ]

    operations = [
        migrations.RunPython(insert_initial_country_continent_names, migrations.RunPython.noop)
    ]
