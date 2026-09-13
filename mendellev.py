import json
import random
import re
from pathlib import Path

from colorama import Fore, Style, init

init(autoreset=True)

raw_elements = [
	("Водород", "H"), ("Гелий", "He"), ("Литий", "Li"), ("Бериллий", "Be"),
	("Бор", "B"), ("Углерод", "C"), ("Азот", "N"), ("Кислород", "O"),
	("Фтор", "F"), ("Неон", "Ne"), ("Натрий", "Na"), ("Магний", "Mg"),
	("Алюминий", "Al"), ("Кремний", "Si"), ("Фосфор", "P"), ("Сера", "S"),
	("Хлор", "Cl"), ("Аргон", "Ar"), ("Калий", "K"), ("Кальций", "Ca"),
	("Скандий", "Sc"), ("Титан", "Ti"), ("Ванадий", "V"), ("Хром", "Cr"),
	("Марганец", "Mn"), ("Железо", "Fe"), ("Кобальт", "Co"), ("Никель", "Ni"),
	("Медь", "Cu"), ("Цинк", "Zn"), ("Галлий", "Ga"), ("Германий", "Ge"),
	("Мышьяк", "As"), ("Селен", "Se"), ("Бром", "Br"), ("Криптон", "Kr"),
	("Рубидий", "Rb"), ("Стронций", "Sr"), ("Иттрий", "Y"), ("Цирконий", "Zr"),
	("Ниобий", "Nb"), ("Молибден", "Mo"), ("Технеций", "Tc"), ("Рутений", "Ru"),
	("Родий", "Rh"), ("Палладий", "Pd"), ("Серебро", "Ag"), ("Кадмий", "Cd"),
	("Индий", "In"), ("Олово", "Sn"), ("Сурьма", "Sb"), ("Теллур", "Te"),
	("Йод", "I"), ("Ксенон", "Xe"), ("Цезий", "Cs"), ("Барий", "Ba"),
	("Лантан", "La"), ("Церий", "Ce"), ("Празеодим", "Pr"), ("Неодим", "Nd"),
	("Прометий", "Pm"), ("Самарий", "Sm"), ("Европий", "Eu"), ("Гадолиний", "Gd"),
	("Тербий", "Tb"), ("Диспрозий", "Dy"), ("Гольмий", "Ho"), ("Эрбий", "Er"),
	("Тулий", "Tm"), ("Иттербий", "Yb"), ("Лютеций", "Lu"), ("Гафний", "Hf"),
	("Тантал", "Ta"), ("Вольфрам", "W"), ("Рений", "Re"), ("Осмий", "Os"),
	("Иридий", "Ir"), ("Платина", "Pt"), ("Золото", "Au"), ("Ртуть", "Hg"),
	("Таллий", "Tl"), ("Свинец", "Pb"), ("Висмут", "Bi"), ("Полоний", "Po"),
	("Астат", "At"), ("Радон", "Rn"), ("Франций", "Fr"), ("Радий", "Ra"),
	("Актиний", "Ac"), ("Торий", "Th"), ("Протактиний", "Pa"), ("Уран", "U"),
	("Нептуний", "Np"), ("Плутоний", "Pu"), ("Америций", "Am"), ("Кюрий", "Cm"),
	("Берклий", "Bk"), ("Калифорний", "Cf"), ("Эйнштейний", "Es"), ("Фермий", "Fm"),
	("Менделевий", "Md"), ("Нобелий", "No"), ("Лоуренсий", "Lr"), ("Резерфордий", "Rf"),
	("Дубний", "Db"), ("Сиборгий", "Sg"), ("Борий", "Bh"), ("Хассий", "Hs"),
	("Мейтнерий", "Mt"), ("Дармштадтий", "Ds"), ("Рентгений", "Rg"), ("Коперниций", "Cn"),
	("Нихоний", "Nh"), ("Флеровий", "Fl"), ("Московий", "Mc"), ("Ливерморий", "Lv"),
	("Теннессин", "Ts"), ("Оганесон", "Og"),
]

special_details = {
	1: ("Самый распространённый элемент во Вселенной.", "Бесцветный, самый лёгкий и очень горючий газ.", "Производство аммиака, топлива и ракетных технологий."),
	7: ("Азот составляет примерно 78% земной атмосферы.", "Бесцветный газ, который при обычных условиях малоактивен.", "Производство удобрений, аммиака и создание инертной среды."),
	6: ("На основе углерода построены все известные живые организмы.", "Имеет несколько форм, включая графит и алмаз.", "Карандаши, фильтры, сталь, топливо и пластмассы."),
	8: ("Около 21% земной атмосферы составляет кислород.", "Бесцветный газ, поддерживает дыхание и горение.", "Медицина, сварка, металлургия и очистка воды."),
	14: ("Кремний — второй по распространённости элемент в земной коре.", "Твёрдый полупроводник с серо-металлическим блеском.", "Микросхемы, солнечные панели, стекло и силиконы."),
	17: ("Хлор получил название от греческого слова «хлорос» — зелёный.", "Жёлто-зелёный токсичный газ с резким запахом.", "Обеззараживание воды, производство ПВХ и отбеливателей."),
	19: ("Калий назван от арабского слова, связанного со щёлочью.", "Мягкий серебристый металл, бурно реагирует с водой.", "Удобрения, производство стекла и химическая промышленность."),
	20: ("Кальций назван от латинского слова calx — известь.", "Серебристо-белый активный металл, важен для костей.", "Цемент, известь, металлургия и производство сплавов."),
	22: ("Титан назван в честь титанов из древнегреческой мифологии.", "Лёгкий, прочный металл, устойчивый к коррозии.", "Самолёты, медицинские импланты, краски и сплавы."),
	24: ("Соединения хрома могут иметь яркие зелёные, жёлтые и красные цвета.", "Твёрдый блестящий металл, устойчивый к коррозии.", "Нержавеющая сталь, покрытия, пигменты и сплавы."),
	26: ("Железо является важной частью гемоглобина в крови.", "Прочный магнитный металл, ржавеет во влажном воздухе.", "Сталь, здания, мосты, машины и инструменты."),
	28: ("Никель входит в состав многих метеоритов.", "Серебристо-белый прочный металл, устойчивый к коррозии.", "Нержавеющая сталь, монеты, аккумуляторы и покрытия."),
	29: ("Медь была одним из первых металлов, освоенных человеком.", "Красноватый металл с высокой электропроводностью.", "Электрические провода, трубы, монеты и электроника."),
	30: ("Цинк необходим организму в небольших количествах.", "Синевато-белый металл, защищает железо от коррозии.", "Оцинковка, батарейки, латуни и лекарства."),
	35: ("Бром — единственный неметалл, жидкий при комнатной температуре.", "Красно-бурая летучая жидкость с резким запахом.", "Огнезащитные материалы, водоочистка и химический синтез."),
	47: ("Серебро лучше всех металлов проводит электрический ток.", "Блестящий мягкий металл с антибактериальными свойствами.", "Ювелирные изделия, электроника, зеркала и медицина."),
	50: ("Олово использовали ещё в бронзовом веке.", "Мягкий серебристый металл с низкой температурой плавления.", "Пайка, защитные покрытия, бронза и производство стекла."),
	53: ("Йод получил название от греческого слова «фиолетовый».", "Тёмный блестящий кристалл, пары имеют фиолетовый цвет.", "Антисептики, медицина, фотография и йодированная соль."),
	78: ("Платина встречается в природе значительно реже золота.", "Плотный благородный металл, устойчивый к большинству кислот.", "Катализаторы, ювелирные изделия, медицина и электроника."),
	80: ("Ртуть — единственный металл, жидкий при комнатной температуре.", "Серебристая тяжёлая токсичная жидкость.", "Научные приборы, лампы и химическая промышленность."),
	79: ("Практически всё добытое за историю золото всё ещё существует.", "Мягкий, ковкий и очень устойчивый к коррозии металл.", "Ювелирные изделия, электроника, медицина и инвестиции."),
	82: ("Свинец использовали в письменных табличках ещё в Древнем Риме.", "Тяжёлый мягкий токсичный металл.", "Аккумуляторы, защита от излучения и специальные сплавы."),
	88: ("Радий открылся благодаря исследованиям Марии и Пьера Кюри.", "Редкий радиоактивный щёлочноземельный металл.", "Научные исследования и лучевая терапия в прошлом."),
	94: ("Плутоний назван в честь карликовой планеты Плутон.", "Радиоактивный тяжёлый металл.", "Ядерная энергетика, космические источники энергии и исследования."),
	92: ("Уран назван в честь планеты Уран.", "Тяжёлый радиоактивный металл.", "Ядерная энергетика и научные исследования."),
}

gas_symbols = {"H", "He", "N", "O", "F", "Ne", "Cl", "Ar", "Kr", "Xe", "Rn", "Og"}
category_symbols = {
	"Щелочные металлы": {"Li", "Na", "K", "Rb", "Cs", "Fr"},
	"Галогены": {"F", "Cl", "Br", "I", "At", "Ts"},
	"Благородные газы": {"He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"},
}


def get_category(symbol):
	for category, symbols in category_symbols.items():
		if symbol in symbols:
			return category
	return "Другие элементы"


def make_element(item):
	name, symbol = item
	number = raw_elements.index(item) + 1
	if number in special_details:
		fact, properties, uses = special_details[number]
	elif 57 <= number <= 71:
		fact = f"{name} относится к лантаноидам — редкоземельным элементам, важным для современной техники."
		properties = "Серебристый металл, обычно мягкий и химически довольно активный."
		uses = "Электроника, магниты, лазеры, аккумуляторы и специальные сплавы."
	elif 89 <= number <= 103:
		fact = f"{name} относится к актинидам — радиоактивным элементам тяжёлого атомного ядра."
		properties = "Тяжёлый радиоактивный металл; многие изотопы имеют короткий период полураспада."
		uses = "Ядерные исследования, энергетика и получение новых элементов."
	elif number > 103:
		fact = f"{name} получают в лабораториях в очень малых количествах."
		properties = "Сверхтяжёлый радиоактивный элемент, существующий недолгое время."
		uses = "Фундаментальные исследования строения атомного ядра."
	elif symbol in gas_symbols:
		fact = f"{name} при обычных условиях находится в газообразном состоянии."
		properties = "Газ с характерными свойствами; некоторые представители группы почти не реагируют с другими веществами."
		uses = "Освещение, сварка, медицина, промышленность и научные исследования."
	else:
		fact = f"{name} встречается в минералах и соединениях, которые изучают и используют в химии."
		properties = "Химический элемент с характерными физическими и химическими свойствами."
		uses = "Промышленность, производство материалов, научные исследования или специальные технологии."
	return {
		"name": name,
		"symbol": symbol,
		"number": number,
		"category": get_category(symbol),
		"fact": fact,
		"properties": properties,
		"uses": uses,
	}


elements = [make_element(item) for item in raw_elements]
stats_path = Path(__file__).with_name("element_stats.json")
try:
	stats = json.loads(stats_path.read_text(encoding="utf-8"))
except (FileNotFoundError, json.JSONDecodeError):
	stats = {}
stats.setdefault("correct", 0)
stats.setdefault("wrong", 0)

nonmetal_symbols = {"B", "C", "P", "S", "Se", "Br", "I", "At", "Ts"}


def element_color(element):
	if element["symbol"] in gas_symbols:
		return Fore.CYAN
	if element["symbol"] in nonmetal_symbols:
		return Fore.YELLOW
	return Fore.GREEN


def print_element(element):
	color = element_color(element)
	print("\n" + color + "=" * 56)
	print(color + f"{element['name']} ({element['symbol']}), атомный номер {element['number']}")
	print(Fore.WHITE + f"Категория: {element['category']}")
	print(Fore.WHITE + f"Факт: {element['fact']}")
	print(Fore.WHITE + f"Свойства: {element['properties']}")
	print(Fore.WHITE + f"Применение: {element['uses']}")
	print(color + "=" * 56 + Style.RESET_ALL)


def save_stats():
	stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def show_random_element():
	element = random.choice(elements)
	stats[element["symbol"]] = stats.get(element["symbol"], 0) + 1
	save_stats()
	print_element(element)


def find_element(query):
	query = query.strip().casefold()
	return next((element for element in elements if element["name"].casefold() == query or element["symbol"].casefold() == query), None)


def search_element():
	query = input("Введите название или символ элемента: ")
	element = find_element(query)
	if element is None:
		print(Fore.RED + "Элемент не найден.")
		return
	print_element(element)


def replace_whole_word(text, value, replacement):
	pattern = rf"(?<!\w){re.escape(value)}(?!\w)"
	return re.sub(pattern, replacement, text, flags=re.IGNORECASE)


def hide_answer(text, element):
	text = replace_whole_word(text, element["name"], "***")
	return replace_whole_word(text, element["symbol"], "***")


last_guess_signature = None


def guess_element(hard=False):
	global last_guess_signature
	for _ in range(100):
		element = random.choice(elements)
		signature = replace_whole_word(element["fact"], element["name"], "<name>").casefold()
		if signature != last_guess_signature:
			break
	last_guess_signature = signature
	print("\nСложный режим:" if hard else "\nУгадайте элемент по интересному факту:")
	if hard:
		print(Fore.YELLOW + element["properties"])
	else:
		print(Fore.YELLOW + hide_answer(element["fact"], element))
	for attempt in range(1, 4):
		answer = input(f"Попытка {attempt}/3. Ваш ответ: ").strip().casefold()
		if answer in {element["name"].casefold(), element["symbol"].casefold()}:
			stats["correct"] += 1
			save_stats()
			print(Fore.GREEN + f"Правильно! Это {element['name']} ({element['symbol']}).")
			return
		stats["wrong"] += 1
		save_stats()
		if hard and attempt == 1:
			print(Fore.YELLOW + f"Подсказка: {hide_answer(element['fact'], element)}")
		elif attempt == 1:
			print(Fore.YELLOW + f"Подсказка: {element['properties']}")
		elif attempt == 2:
			print(Fore.YELLOW + f"Ещё подсказка: {element['uses']}")
	print(Fore.RED + f"Попытки закончились. Правильный ответ: {element['name']} ({element['symbol']}).")


def show_stats():
	used = [(element, stats.get(element["symbol"], 0)) for element in elements if stats.get(element["symbol"], 0)]
	print("\nСтатистика:")
	print(f"Правильных ответов: {stats['correct']}")
	print(f"Неправильных ответов: {stats['wrong']}")
	if not used:
		print("Случайные элементы пока не выпадали.")
		return
	print("\nСтатистика случайных выпадений:")
	for element, count in sorted(used, key=lambda pair: (-pair[1], pair[0]["name"])):
		print(f"{element['name']} ({element['symbol']}): {count}")


def show_category():
	category = input("Категория (щелочные металлы, галогены, благородные газы): ").strip().casefold()
	selected = next((name for name in category_symbols if name.casefold() == category), None)
	if selected is None:
		print(Fore.RED + "Такой категории нет.")
		return
	print(f"\n{selected}:")
	for element in elements:
		if element["category"] == selected:
			print(f"{element['name']} ({element['symbol']})")


print(Fore.CYAN + "Случайные элементы таблицы Менделеева")
while True:
	try:
		command = input("\nслучайный элемент | поиск | угадай | сложный | категории | статистика | выход: ").strip().casefold()
	except EOFError:
		print("\nВвод завершён.")
		break
	if command in {"выход", "выхода", "exit", "q"}:
		print("До встречи!")
		break
	elif command in {"", "случ", "рандом", "случайный"}:
		show_random_element()
	elif command in {"поиск", "найти", "search"}:
		search_element()
	elif command in {"угадай", "игра", "guess"}:
		guess_element()
	elif command in {"сложный", "hard"}:
		guess_element(hard=True)
	elif command in {"категории", "категория", "categories"}:
		show_category()
	elif command in {"статистика", "стата", "stats"}:
		show_stats()
	else:
		print("че ты ввел попробуй: поиск, угадай, статистика или выход.")