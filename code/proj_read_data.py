import snap
import csv
from collections import *
import os

def read_alliance_data():
  cc1 = open("ccode1.txt")
  cc2 = open("ccode2.txt")
  n1 = open("state_names1.txt")
  n2 = open("state_names2.txt")

  names1 = [line.rstrip() for line in n1]
  names2 = [line.rstrip() for line in n2]

  cnames = {}

  cc1s = []
  i = 0
  for line in cc1:
    cc1s.append(float(line))
    cnames[float(line)] = names1[i]
    i += 1

  cc2s = []
  i = 0
  for line in cc2:
    cc2s.append(float(line))
    cnames[float(line)] = names2[i]
    i += 1

  #Get labels
  labels = snap.TIntStrH()
  for key in cnames:
    labels[key] = cnames[key]

  graph = snap.TUNGraph.New()
  for cc in cc1s:
    if not graph.IsNode(cc):
      graph.AddNode(cc)

  for cc in cc2s:
    if not graph.IsNode(cc):
      graph.AddNode(cc)

  for i in range(len(cc1s)):
    if not graph.IsEdge(cc1s[i], cc2s[i]):
      graph.AddEdge(cc1s[i], cc2s[i])

  print graph.GetNodes(), graph.GetEdges()
  return graph, labels

def read_trade_data():
  f = open("dyadic_trade_3.0.csv", "rU")
  reader = csv.reader(f)
  #Map of (cc1, cc2) to trade 
  trade = Counter()
  for row in reader:
    #Ignore row if not in proper format
    if row[0] == "ccode1":
      continue

    #Use data from 1989 only
    if int(row[2]) != 1989:
      continue

    cc1 = float(row[0])
    cc2 = float(row[1])
    tradeFlow = max(0.0, float(row[5]) + float(row[6]))
    trade[(cc1, cc2)] += tradeFlow
    trade[(cc2, cc1)] += tradeFlow

  return trade

def read_contiguity_data():
  f = open("contdird.csv", "rU")
  reader = csv.reader(f)
  contiguity = Counter()
  for row in reader:
    #Ignore row if not in proper format
    if row[0] == "dyad":
      continue

    #Use data from 1989 only
    if int(row[5]) != 1989:
      continue

    cc1 = float(row[1])
    cc2 = float(row[3])
    cont = float(row[6])
    contiguity[(cc1, cc2)] += cont

  return contiguity

def religion_data():
  print os.getcwd()

  f = open("Religion.csv", "rU")
  reader = csv.reader(f)
  religion_raw = {}
  for row in reader:
    cc = float(row[0])
    top_relig = (row[1])
    religion_raw[cc] = top_relig
  religion_map = Counter()
  for cc1 in religion_raw:
    for cc2 in religion_raw:
      if cc1 != cc2:
        if religion_raw[cc1] == religion_raw[cc2]:
          religion_map[(cc1,cc2)] = 1
        else:
          religion_map[(cc1,cc2)] = 0
  return religion_map

def read_dispute_data():
  f = open("MIDDyadic_v3.10.csv", "rU")
  reader = csv.reader(f)
  disputes = Counter()
  for row in reader:
    #Ignore row if not in proper format
    if row[0] == "DispNum":
      continue

    cc1 = float(row[2])
    cc2 = float(row[3])
    hostility = float(row[12]) + float(row[13])
    disputes[(cc1, cc2)] = max(disputes[(cc1, cc2)], hostility)
    disputes[(cc2, cc1)] = max(disputes[(cc2, cc1)], hostility)

  return disputes
#graph, labels = read_data()
#print read_trade_data()
#print "\n\n\n"
#print read_contiguity_data()
print read_dispute_data()
snap.DrawGViz(graph, snap.gvlDot, "output.png", " ", labels)
snap.SaveGViz(graph, "Graph1.dot", "Undirected Alliance Graph", True, labels)

