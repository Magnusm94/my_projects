import pandas as pd

with open('test.txt') as file:
    content = file.read()
    file.close()

arr = content.split('\n')

counter = 0
new_invoice = []
reminders = []

for i in arr:
    if str(i).isdigit() or str(i) in ['Purring', 'PÃ¥minnelse']:
        new_invoice.append(counter)
    if str(i) == 'Purring':
        reminders.append(counter)
    if str(i) == 'PÃ¥minnelse':
        reminders.append(counter)
    counter += 1

fakturainfo = {}
counter = 0
for i in range(len(new_invoice) - 2):
    temp = arr[new_invoice[i]:new_invoice[i + 1]]

    fakturainfo[str(counter)] = {}

    while True:
        if '\ue002' in temp:
            temp.remove('\ue002')
        elif '\ue417' in temp:
            temp.remove('\ue417')
        else:
            break

    email = False
    for item in temp:
        if '@' in item:
            fakturainfo[str(counter)]['email'] = item.split(' ')[-1]

    if 'Purre' in temp[1] or 'PÃ¥minnelse' in temp[1]:
        fakturainfo[str(counter)]['purregebyr'] = float(temp[1].split(' ')[-1].replace(',', '.'))
        fakturainfo[str(counter)]['renter'] = float(temp[2].split(' ')[-1].replace(',', '.'))

    else:
        fakturainfo[str(counter)]['kunde'] = temp[1]
    last_element = temp[-1].split(' ')
    fakturainfo[str(counter)]['dato'] = last_element[0]

    if len(last_element) == 5:

        if len(last_element[1]) > 9:
            fakturainfo[str(counter)]['eksl mva'] = float(last_element[-3].replace(',', '.'))
            fakturainfo[str(counter)]['inkl mva'] = float(last_element[-2].replace(',', '.'))
            fakturainfo[str(counter)]['utestÃ¥ende'] = float(last_element[-1].replace(',', '.'))

        else:
            fakturainfo[str(counter)]['inkl mva'] = float(str(last_element[1] + last_element[2]).replace(',', '.'))
            fakturainfo[str(counter)]['utestÃ¥ende'] = float(str(last_element[3] + last_element[4]).replace(',', '.'))

    elif len(last_element) == 6:

        try:
            fakturainfo[str(counter)]['eksl mva'] = float(str(last_element[2]).replace(',', '.'))
            fakturainfo[str(counter)]['inkl mva'] = float(str(last_element[3] + last_element[4]).replace(',', '.'))
            fakturainfo[str(counter)]['utestÃ¥ende'] = float(str(last_element[5] + last_element[6]).replace(',', '.'))

        except ValueError:
            pass

    elif len(last_element) == 8:
        fakturainfo[str(counter)]['eksl mva'] = float(str(last_element[2] + last_element[3]).replace(',', '.'))
        fakturainfo[str(counter)]['inkl mva'] = float(str(last_element[4] + last_element[5]).replace(',', '.'))
        fakturainfo[str(counter)]['utestÃ¥ende'] = float(str(last_element[6] + last_element[7]).replace(',', '.'))

    elif len(last_element) == 3:
        fakturainfo[str(counter)]['inkl mva'] = float(str(last_element[1]).replace(',', '.'))
        fakturainfo[str(counter)]['utestÃ¥ende'] = float(str(last_element[2]).replace(',', '.'))

    elif len(last_element) == 7:
        fakturainfo[str(counter)]['eksl mva'] = float(str(last_element[2]).replace(',', '.'))
        fakturainfo[str(counter)]['inkl mva'] = float(str(last_element[3] + last_element[4]).replace(',', '.'))
        fakturainfo[str(counter)]['utestÃ¥ende'] = float(str(last_element[5] + last_element[6]).replace(',', '.'))

    counter += 1

counter = 0
emails = []
for x, z in fakturainfo.items():
    try:
        if z['utestÃ¥ende'] > 0:
            try:
                emails.append(z['email'])
            except KeyError:
                pass
    except KeyError:
        pass

with open('Tapere_uten_penger.txt', 'w') as file:
    for i in list(set(emails)):
        file.write(i)
        file.write('\n')
file.close()

df = pd.DataFrame(data=fakturainfo)
df.to_excel('abc.xlsx')
