import urllib.request

for years in range(2012, 2022):
    for months in range(4, 12):
        if months < 10:
            months = '0' + str(months)
        else:
            months = str(months)

        for days in range(28, 32):
            years = str(years)
            if days < 10:
                days = '0' + str(days)
            else:
                days = str(days)
            try:
                urllib.request.urlretrieve(f'http://sci-vega.ru/press/fire/obzor{years}/{years+months+days}_obzor.pdf',
                                           f"{years+months+days}.pdf")
            except:
                print(years + months + days)
                continue
