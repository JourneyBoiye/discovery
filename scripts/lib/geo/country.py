import enum

_CANNONICAL_FORMS = {
    'usa': 'united states',
    'united states of america': 'united states',
    'uk': 'united kingdom',
    'united kingdom of great britain and northern ireland': 'united kingdom',
    'the bahamas': 'bahamas',
    'myanmar (burma)': 'myanmar',
    'czechia': 'czech republic',
    'macedonia (fyrom)': 'macedonia',
    'cabo verde': 'cape verde',
    'democratic people\'s republic of korea': 'north korea',
    'congo': 'republic of the congo',
    'democratic republic of the congo': 'the democratic republic of the congo',
    'russian federation': 'russia',
    'united republic of tanzania': 'tanzania',
    'viet nam': 'vietnam',
    'venezuela (bolivarian republic of)': 'venezuela',
    'korea': 'south korea',
    'republic of korea': 'south korea',
    'republic of moldova': 'moldova',
    'iran (islamic republic of)': 'iran',
    'bolivia (plurinational state of)': 'bolivia',
    'lao people\'s democratic republic': 'laos',
    'syrian arab republic': 'syria',
    'tfyr of macedonia': 'macedonia',
    'china hong kong sar': 'hong kong',
    'china, hong kong sar': 'hong kong',
    'china macao sar': 'macao',
    'china, macao sar': 'macao',
    'macau': 'macao',
    'state of palestine': 'palestine',
    'republic of south sudan': 'south sudan',
    'brunei darussalam': 'brunei',
    'faeroe islands': 'faroe islands',
    'federated states of micronesia': 'micronesia',
    'wallis and futuna islands': 'wallis and futuna',
    'saint helena ex. dep.': 'saint helena',
    'curacao': 'curaçao',
    'saint barthelemy': 'saint barthélemy',
    'são tomé': 'sao tome and principe',
    'são tomé and príncipe': 'sao tome and principe',
    'east timor': 'timor-leste',
    'ivory coast': 'côte d\'ivoire',
    'vatican city': 'holy see',
    'u.s. virgin islands': 'united states virgin islands',
    'pitcairn islands': 'pitcairn',
    'saint martin': 'sint maarten',
    'reunion': 'réunion',
    'saint helena, ascension and tristan da cunha': 'saint helena',
}

def create(name):
    try:
        return Country(_CANNONICAL_FORMS[name])
    except KeyError:
        return Country(name)

class Country(enum.Enum):
    AFGHANISTAN = 'afghanistan'
    ALAND_ISLANDS = 'åland islands'
    ALBANIA = 'albania'
    ALGERIA = 'algeria'
    AMERICAN_SAMOA = 'american samoa'
    ANDORRA = 'andorra'
    ANGOLA = 'angola'
    ANGUILLA = 'anguilla'
    ANTARCTICA = 'antarctica'
    ANTIGUA_AND_BARBUDA = 'antigua and barbuda'
    ARGENTINA = 'argentina'
    ARMENIA = 'armenia'
    ARUBA = 'aruba'
    AUSTRALIA = 'australia'
    AUSTRIA = 'austria'
    AZERBAIJAN = 'azerbaijan'
    BAHAMAS = 'bahamas'
    BAHRAIN = 'bahrain'
    BANGLADESH = 'bangladesh'
    BARBADOS = 'barbados'
    BELARUS = 'belarus'
    BELGIUM = 'belgium'
    BELIZE = 'belize'
    BENIN = 'benin'
    BERMUDA = 'bermuda'
    BHUTAN = 'bhutan'
    BOLIVIA = 'bolivia'
    BOSNIA_AND_HERZEGOVINA = 'bosnia and herzegovina'
    BOTSWANA = 'botswana'
    BOUVET_ISLAND = 'bouvet island'
    BRAZIL = 'brazil'
    BRITISH_INDIAN_OCEAN_TERRITORY = 'british indian ocean territory'
    BRUNEI = 'brunei'
    BULGARIA = 'bulgaria'
    BURKINA_FASO = 'burkina faso'
    BURUNDI = 'burundi'
    CAMBODIA = 'cambodia'
    CAMEROON = 'cameroon'
    CANADA = 'canada'
    CAPE_VERDE = 'cape verde'
    CAYMAN_ISLANDS = 'cayman islands'
    CENTRAL_AFRICAN_REPUBLIC = 'central african republic'
    CHAD = 'chad'
    CHILE = 'chile'
    CHINA = 'china'
    CHRISTMAS_ISLAND = 'christmas island'
    COCOS_KEELING_ISLANDS = 'cocos (keeling) islands'
    COLOMBIA = 'colombia'
    COMOROS = 'comoros'
    REPUBLIC_OF_THE_CONGO = 'republic of the congo'
    THE_DEMOCRATIC_REPUBLIC_OF_THE_CONGO = 'the democratic republic of the congo'
    COOK_ISLANDS = 'cook islands'
    COSTA_RICA = 'costa rica'
    COTE_DIVOIRE = 'côte d\'ivoire'
    CROATIA = 'croatia'
    CUBA = 'cuba'
    CYPRUS = 'cyprus'
    CZECH_REPUBLIC = 'czech republic'
    CURACAO = 'curaçao'
    DENMARK = 'denmark'
    DJIBOUTI = 'djibouti'
    DOMINICA = 'dominica'
    DOMINICAN_REPUBLIC = 'dominican republic'
    ECUADOR = 'ecuador'
    EGYPT = 'egypt'
    EL_SALVADOR = 'el salvador'
    EQUATORIAL_GUINEA = 'equatorial guinea'
    ERITREA = 'eritrea'
    ESTONIA = 'estonia'
    ETHIOPIA = 'ethiopia'
    FALKLAND_ISLANDS = 'falkland islands'
    FAROE_ISLANDS = 'faroe islands'
    FIJI = 'fiji'
    FINLAND = 'finland'
    FRANCE = 'france'
    FRENCH_GUIANA = 'french guiana'
    FRENCH_POLYNESIA = 'french polynesia'
    FRENCH_SOUTHERN_TERRITORIES = 'french southern territories'
    GABON = 'gabon'
    GAMBIA = 'gambia'
    GEORGIA = 'georgia'
    GERMANY = 'germany'
    GHANA = 'ghana'
    GIBRALTAR = 'gibraltar'
    GREECE = 'greece'
    GREENLAND = 'greenland'
    GRENADA = 'grenada'
    GUADELOUPE = 'guadeloupe'
    GUAM = 'guam'
    GUATEMALA = 'guatemala'
    GUERNSEY = 'guernsey'
    GUINEA = 'guinea'
    GUINEA_BISSAU = 'guinea-bissau'
    GUYANA = 'guyana'
    HAITI = 'haiti'
    HEARD_ISLAND_AND_MCDONALD_ISLANDS = 'heard island and mcdonald islands'
    HOLY_SEE = 'holy see'
    HONDURAS = 'honduras'
    HONG_KONG = 'hong kong'
    HUNGARY = 'hungary'
    ICELAND = 'iceland'
    INDIA = 'india'
    INDONESIA = 'indonesia'
    IRAN = 'iran'
    IRAQ = 'iraq'
    IRELAND = 'ireland'
    ISLE_OF_MAN = 'isle of man'
    ISRAEL = 'israel'
    ITALY = 'italy'
    JAMAICA = 'jamaica'
    JAPAN = 'japan'
    JERSEY = 'jersey'
    JORDAN = 'jordan'
    KAZAKHSTAN = 'kazakhstan'
    KENYA = 'kenya'
    KIRIBATI = 'kiribati'
    KOSOVO = 'kosovo'
    NORTH_KOREA = 'north korea'
    SOUTH_KOREA = 'south korea'
    KUWAIT = 'kuwait'
    KYRGYZSTAN = 'kyrgyzstan'
    LAOS = 'laos'
    LATVIA = 'latvia'
    LEBANON = 'lebanon'
    LESOTHO = 'lesotho'
    LIBERIA = 'liberia'
    LIBYA = 'libya'
    LIECHTENSTEIN = 'liechtenstein'
    LITHUANIA = 'lithuania'
    LUXEMBOURG = 'luxembourg'
    MACAO = 'macao'
    MACEDONIA = 'macedonia'
    MADAGASCAR = 'madagascar'
    MALAWI = 'malawi'
    MALAYSIA = 'malaysia'
    MALDIVES = 'maldives'
    MALI = 'mali'
    MALTA = 'malta'
    MARSHALL_ISLANDS = 'marshall islands'
    MARTINIQUE = 'martinique'
    MAURITANIA = 'mauritania'
    MAURITIUS = 'mauritius'
    MAYOTTE = 'mayotte'
    MEXICO = 'mexico'
    MICRONESIA = 'micronesia'
    MOLDOVA = 'moldova'
    MONACO = 'monaco'
    MONGOLIA = 'mongolia'
    MONTENEGRO = 'montenegro'
    MONTSERRAT = 'montserrat'
    MOROCCO = 'morocco'
    MOZAMBIQUE = 'mozambique'
    MYANMAR = 'myanmar'
    NAMIBIA = 'namibia'
    NAURU = 'nauru'
    NEPAL = 'nepal'
    NETHERLANDS = 'netherlands'
    CARIBBEAN_NETHERLANDS = 'caribbean netherlands'
    NEW_CALEDONIA = 'new caledonia'
    NEW_ZEALAND = 'new zealand'
    NICARAGUA = 'nicaragua'
    NIGER = 'niger'
    NIGERIA = 'nigeria'
    NIUE = 'niue'
    NORFOLK_ISLAND = 'norfolk island'
    NORTHERN_MARIANA_ISLANDS = 'northern mariana islands'
    NORWAY = 'norway'
    OMAN = 'oman'
    PAKISTAN = 'pakistan'
    PALAU = 'palau'
    PALESTINE = 'palestine'
    PANAMA = 'panama'
    PAPUA_NEW_GUINEA = 'papua new guinea'
    PARAGUAY = 'paraguay'
    PERU = 'peru'
    PHILIPPINES = 'philippines'
    PITCAIRN = 'pitcairn'
    POLAND = 'poland'
    PORTUGAL = 'portugal'
    PUERTO_RICO = 'puerto rico'
    QATAR = 'qatar'
    REUNION = 'réunion'
    ROMANIA = 'romania'
    RUSSIA = 'russia'
    RWANDA = 'rwanda'
    SAINT_BARTHELEMY = 'saint barthélemy'
    SAINT_HELENA = 'saint helena'
    SAINT_KITTS_AND_NEVIS = 'saint kitts and nevis'
    SAINT_LUCIA = 'saint lucia'
    SINT_MAARTEN = 'sint maarten'
    SAINT_PIERRE_AND_MIQUELON = 'saint pierre and miquelon'
    SAINT_VINCENT_AND_THE_GRENADINES = 'saint vincent and the grenadines'
    SAMOA = 'samoa'
    SAN_MARINO = 'san marino'
    SAO_TOME_AND_PRINCIPE = 'sao tome and principe'
    SAUDI_ARABIA = 'saudi arabia'
    SENEGAL = 'senegal'
    SERBIA = 'serbia'
    SEYCHELLES = 'seychelles'
    SIERRA_LEONE = 'sierra leone'
    SINGAPORE = 'singapore'
    SLOVAKIA = 'slovakia'
    SLOVENIA = 'slovenia'
    SOLOMON_ISLANDS = 'solomon islands'
    SOMALIA = 'somalia'
    SOUTH_AFRICA = 'south africa'
    SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS = 'south georgia and the south sandwich islands'
    SOUTH_SUDAN = 'south sudan'
    SPAIN = 'spain'
    SRI_LANKA = 'sri lanka'
    SUDAN = 'sudan'
    SURINAME = 'suriname'
    SVALBARD_AND_JAN_MAYEN = 'svalbard and jan mayen'
    SWAZILAND = 'swaziland'
    SWEDEN = 'sweden'
    SWITZERLAND = 'switzerland'
    SYRIA = 'syria'
    TAIWAN = 'taiwan'
    TAJIKISTAN = 'tajikistan'
    TANZANIA = 'tanzania'
    THAILAND = 'thailand'
    TIMOR_LESTE = 'timor-leste'
    TOGO = 'togo'
    TOKELAU = 'tokelau'
    TONGA = 'tonga'
    TRINIDAD_AND_TOBAGO = 'trinidad and tobago'
    TUNISIA = 'tunisia'
    TURKEY = 'turkey'
    TURKMENISTAN = 'turkmenistan'
    TURKS_AND_CAICOS_ISLANDS = 'turks and caicos islands'
    TUVALU = 'tuvalu'
    UGANDA = 'uganda'
    UKRAINE = 'ukraine'
    UNITED_ARAB_EMIRATES = 'united arab emirates'
    UNITED_KINGDOM = 'united kingdom'
    UNITED_STATES = 'united states'
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = 'united states minor outlying islands'
    URUGUAY = 'uruguay'
    UZBEKISTAN = 'uzbekistan'
    VANUATU = 'vanuatu'
    VENEZUELA = 'venezuela'
    VIETNAM = 'vietnam'
    VIRGIN_ISLANDS_BRITISH = 'british virgin islands'
    VIRGIN_ISLANDS_US = 'united states virgin islands'
    WALLIS_AND_FUTUNA = 'wallis and futuna'
    WESTERN_SAHARA = 'western sahara'
    YEMEN = 'yemen'
    ZAMBIA = 'zambia'
    ZIMBABWE = 'zimbabwe'
