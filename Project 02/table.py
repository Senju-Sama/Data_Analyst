
# file to write
with open('htable.txt','w') as file:
    # opening csv in txt format
    csn = input("Enter txt file name : ")
    if len(csn)<1:
        csn= 'book.txt'
    fhand = open(csn,'r',encoding='utf-8')
    data = fhand.read()
    line = data.strip().split('\n')

    count = 0
    file.write('<table border="1">\n')
    for words in line:
        word = words.split(',')
        file.write('<tr>\n')
        for tag in word:
            if count ==0:
                file.write('    'f'<th> {tag} </th>\n')
            else:
                file.write('    'f'<td> {tag} </td>\n')
        file.write('</tr>\n    ')
        print(count)
        count+=1
    file.write('</table>')