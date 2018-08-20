import csv

def assign():
  seeds = []
  allSixThousand = []

  for i in range(0,10):
    seeds.append(set())

  for j in range(0,6000):
    allSixThousand.append([])
    for k in range(0,10):
      allSixThousand[j].append(0)


  with open('Seed.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      pid = int(row[0])
      label = int(row[1])
      seeds[label].add(pid)

  similarity_g = []
  for i in range(0,6000):
    similarity_g.append(set())

  with open('Graph.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      num1 = int(row[0])
      num2 = int(row[1])
      similarity_g[num1-1].add(num2-1)
      for i in range(0,10):
        seed = seeds[i]
        if (num1 in seed):
          allSixThousand[num2-1][i] = allSixThousand[num2-1][i] + 1
          break

  temp_assignments = []
  for i in range(0,10):
    temp_assignments.append(set())

  for i in range(0,6000):
    for j in range(0,10):
      if allSixThousand[i][j] > 0:
        temp_assignments[j].add(i)

  for i in range(0,10):
    for num in seeds[i]:
      temp_assignments[i].add(num-1)

  assignments = []
  for i in range(0,6000):
    highestCount = -1
    index = -1
    for j in range(0,10):
      if i in temp_assignments[j]:
        counter = 0
        for k in temp_assignments[j]:
          if k in similarity_g[i]:
            counter = counter + 1
        if counter > highestCount:
          highestCount = counter
          index = j
    assignments.append(index)


  for m in range(0,10):
    seed = seeds[m]
    for num in seed:
      assignments[num-1] = m



  for i in range(0,6000):
    if assignments[i] == -1:
      highestCount = -1
      index = -1
      for j in range(0,10):
        counter = 0
        for k in temp_assignments[j]:
          if k in similarity_g[i]:
            counter = counter + 1
        if counter > highestCount:
          highestCount = counter
          index = j
      assignments[i] = index

  return assignments

if __name__ == '__main__':
  assignments = assign()
  with open('similarities_3.csv','w') as csv_file:
    writer = csv.writer(csv_file, delimiter = ',',lineterminator='\n')
    for a in assignments:
        writer.writerow([a])
