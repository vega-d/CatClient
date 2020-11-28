a = [float(i) for i in
     ("4 2 4 6 3 3 5 2 4 5 4 3 6 5 4 2 4 3 5 3")
     .split(' ')]
sum = 0
not_repeated = []

print('var vib:', len(a))
for i in a:
    if i not in not_repeated:
        not_repeated.append(i)
print(not_repeated)
overall = 0.0
for i in not_repeated:
    print(i, 'is in quantity of', a.count(i))
    overall+=float(a.count(i))
print('\n', overall, '\n')
for i in not_repeated:
    print(i, 'is in quantity of', (float(a.count(i))/overall)*100, '%')
for i in not_repeated:
    sum += (int(i))*(a.count(i))
print(sum)




# "5 9 4 8 6 8 6 8 5 9 4 4 5 4 9 8 6 6 8 9 4"

#"4 3 2 3 4 3 3 5 3 4 3 4 3 4 3 3 5 4 3 3 "+
#"4 2 4 4 4 3 4 4 4 5 3 3 4 3 3 4 3 5 2 4 "+
#"3 4 3 3 4 4 4 4 5 4"
