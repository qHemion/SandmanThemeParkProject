# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:56:53 2018

@author: home
"""

from random import randint
from copy import deepcopy

class Parc():
    
    def __init__(self):
        self.layout = None
        self.entree = None
        self.scoreTotal = None
        self.scoreIndividuel = None
    
    def testParc(self):
        self.entree = [0, 0] 
        self.layout = [["B", "A", "R", "B"], ["R", "Tree", "B", "A"], ["A", "Tree", "Tree", "A"], ["B", "R", "A", "B"]]
        
    def simulation(self, dayLength, basePopulation):
        self.scoreTotal = 0
        self.scoreIndividuel=[[0 for i in range(len(self.layout[0]))] for j in range(len(self.layout))]
        taillePop = basePopulation
        for i in self.layout:
            for j in i:
                if (j == "Tree"):
                    taillePop += 10
        pop = []
        for i in range(taillePop):
            pop.append(customer(self.entree, i))
        
        for turn in range(dayLength):
            for i in pop:
                print(i.toString())
                if(i.alive):
                    if (not i.isVeryTired() or randint(0, 2)==1):
                        self.playTurn(i)
                        if(i.alive and i.isVeryHappy() and randint(0, 2)==1):
                            self.playTurn(i)
        return pop
    
    def currentBuilding(self, i):
        return self.layout[i.pos[0]][i.pos[1]]
                    
    def choosePath(self, i):
        dirPossible=[]
        if(i.lastMove!="R" and i.pos[0]>0 and self.layout[i.pos[0]-1][i.pos[1]]!="Tree"):
            dirPossible.append("L")
            if(i.isHungry()):
                dirPossible.append("L")
                dirPossible.append("L")
        if(i.lastMove!="L" and i.pos[0]<len(self.layout)-1 and self.layout[i.pos[0]+1][i.pos[1]]!="Tree"):
            dirPossible.append("R")
            if(not i.isHungry()):
                dirPossible.append("R")
                dirPossible.append("R")
        if(i.lastMove!="D" and i.pos[1]>0 and self.layout[i.pos[0]][i.pos[1]-1]!="Tree"):
            dirPossible.append("U")
            if(i.isTired()):
                dirPossible.append("U")
                dirPossible.append("U")
        if(i.lastMove!="U" and i.pos[1]<len(self.layout[0])-1 and self.layout[i.pos[0]][i.pos[1]+1]!="Tree"):
            dirPossible.append("D")
            if(not i.isTired()):
                dirPossible.append("D")
                dirPossible.append("D")
            
        if(len(dirPossible)==0):
            if(i.lastMove==None):
                i.kill()
                return None
            else :
                return i.lastMove
        else :
            return dirPossible[randint(0, len(dirPossible)-1)]
            
    def useBuilding(self, i):
        building = self.currentBuilding(i)
        if(building == "B"):
            i.rest += 20
            i.hunger -= 15
            i.log +="Used Bench \n"
            
        if(building == "A"):
            i.rest-= 15
            i.joy+=20
            self.scoreTotal+=100
            self.scoreIndividuel[i.pos[0]][i.pos[1]]+=100
            i.log +="Used Attraction \n"
            
        if(building == "R"):
            if(i.isVeryHungry()):
                self.scoreTotal+=100
                self.scoreIndividuel[i.pos[0]][i.pos[1]]+=100
            i.hunger += 20
            i.joy -= 15
            self.scoreTotal+=100
            self.scoreIndividuel[i.pos[0]][i.pos[1]]+=100
            i.log +="Used Restaurant \n"
            
            
    def playTurn(self, i):
        
        direc = self.choosePath(i)
        if(direc == None): return None

        i.lastMove = direc            
        if(direc=="L"):
            i.pos[0]  -= 1
            i.log +="Moved Left \n"
        if(direc=="U"):
            i.pos[1] -= 1
            i.log +="Moved Up \n"
        if(direc=="R"):
            i.pos[0] += 1
            i.log +="Moved Right \n"
        if(direc=="D"):
            i.pos[1] += 1
            i.log +="Moved Down \n"
            
        i.log += "Now in " + str(i.pos[0]) + "," + str(i.pos[1])+ "\n"
        if(not i.pos in i.visited): 
            self.useBuilding(i)
            i.visited.append([i.pos[0], i.pos[1]])
            if(len(i.visited)>=4):
                i.visited.pop(0)
        else:
            i.log+=("Did not visit, already visited recently \n")
        i.checkVivant()
        
    def reproduction(self, parc2, initLayout):
        fils = Parc()
        fils.entree = self.entree
        fils.layout = initLayout
        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                fils.layout[i][j]="Tree"
                
        
        
        
        
            
            
            
    
    
    
    
class customer():
    
    def __init__(self, posInit, idC):
        self.idC = idC
        self.alive = True
        self.pos = [posInit[0], posInit[1]]
        self.hunger = randint(30, 70)
        self.rest = randint(30, 70)
        self.joy = randint(30, 70)
        self.lastMove = None
        self.visited = []
        self.log="logs for customer " + str(self.idC) + "\n"
        
    def toString(self):
        L = "customer " + str(self.idC) + "\n"
        if(self.alive==False):
            L+="customer left"
        else:
            L+="pos : " + str(self.pos[0]) + " ," + str(self.pos[1]) + "\n"
            L+="hunger : " + str(self.hunger) + " \nrest : " + str(self.rest) + " \njoy : " + str(self.joy) + "\n" 
        return L
            

    def kill(self):
        self.alive = False   
        self.log += "customer left"
        
    def checkVivant(self):
        self.hunger = min(100, self.hunger)
        self.rest = min(100, self.rest)
        self.joy = min(100, self.joy)
        if(self.hunger<=0 or self.joy<=0 or self.rest<=0):
            self.kill()
        
    def isTired(self):
        return (self.rest<=50)
    
    def isHungry(self):
        return (self.hunger<=50)
        
    def isVeryHungry(self):
        return (self.hunger<=20)
    
    def isVeryTired(self):
        return (self.rest<=20)
    
    def isVeryHappy(self):
        return (self.joy>80)
        
        
        