# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:28:48 2020

@author: Paul Payumo (011344905) and Mike Lin (011001445)
"""

from random import randint

class Global:
    operatingRooms = 4
    beds = 400
    nurses = 200
    doctors = 50
    medicalEquipment = 100
    medication = 200
    patients = []
    time = 5
    waiting = 0

class Patient:
    def __init__(self, time):
        self.time = time
        self.waitingTime = 0
        self.operatingRoom = False
        self.specialEquipment = False
        self.medication = False
    
def checkCapacity(patient):
    if(Global.medication == 0):
        if(patient.medication == True):
            patient.waitingTime = minimumTime() + 2
    if(Global.operatingRooms == 0):
        if(patient.operatingRoom == True):
            if(24 - Global.time > patient.waitingTime):
                patient.waitingTime = 24 - Global.time
    if(Global.medicalEquipment == 0):
        if(patient.specialEquipment == True):
            if(patient.waitingTime < minimumEquipmentTime()):
                patient.waitingTime = minimumEquipmentTime()
    if(Global.nurses == 0 or Global.beds == 0 or Global.doctors < (1/8)):
        if(patient.waitingTime < minimumTime()):
            patient.waitingTime = minimumTime()
    return patient.waitingTime
    
def minimumTime():
    minTime = 9
    for i in range(len(Global.patients)):
        if(Global.patients[i].time < minTime):
            minTime = Global.patients[i].time
    return minTime

def minimumEquipmentTime():
    minTime = 9
    equipment = []
    for i in range(len(Global.patients)):
        if(Global.patients[i].specialEquipment == True):
            equipment.append(Global.patients[i])
    for i in range(len(equipment)):
        if(equipment[i].time < minTime):
            minTime = equipment[i].time
    return minTime
            
def addPatient():
    p = Patient(randint(1,8))
    if(input("Does the patient need surgery? 'Yes' or 'No' ") == "Yes"):
        p.operatingRoom = True
    if(input("Does the patient need special equipment? 'Yes' or 'No' " ) == "Yes"):
        p.specialEquipment = True
    if(input("Does the patient need medication? 'Yes' or 'No' ") == "Yes"):
        p.medication = True
    waitingTime = checkCapacity(p)
    if(waitingTime == 0):
        Global.beds += -1
        Global.nurses += -0.25
        Global.doctors += -1/8
        if(p.operatingRoom == True):
            Global.operatingRooms += -1
        if(p.specialEquipment == True):
            Global.medicalEquipment += -1
        if(p.medication == True):
            Global.medication += -1
        Global.patients.append(p)
        print("\nYou will be admitted now for", p.time, "hours.")
    else:
        if(p.operatingRoom == False and p.specialEquipment == False and p.medication == True and Global.medication == 0 and Global.beds > 0 and Global.nurses > 0 and Global.doctors > 0):
            print("\nYou will be admitted now for", p.time, "plus 2 additional hours due to lack of medication.")
            p.time += 2
            Global.patients.append(p)
            Global.beds += -1
            Global.nurses += -0.25
            Global.doctors += -1/8
        else:
            if(p.medication == True):
                waitingTime += -2
            print("\n\nWaiting time is", waitingTime, "hours.\n")
            
            
def wait():
    newPatients = []
    Global.time += 1
    if(Global.time == 24):
        Global.time = 0
        Global.operatingRooms = 4
        Global.medication = 2
    print("It is {}:00 in military time.".format(Global.time))
    if(len(Global.patients) >= 1):
        for i in range(len(Global.patients)):
            Global.patients[i].time += -1
            if(Global.patients[i].time == 0):
                Global.beds += 1
                Global.nurses += 0.25
                Global.doctors += 1/8
                if(Global.patients[i].specialEquipment == True):
                    Global.medicalEquipment += 1
    for i in range(len(Global.patients)):
        if(not Global.patients[i].time == 0):
            newPatients.append(Global.patients[i])
    Global.patients = newPatients
    
            
def main():
    print("It is {}:00 in military time.".format(Global.time))
    while(1):
        action = int(input("\nWhat would you like to do?\n'1' for admit a patient\n'2' for wait one hour.\n'3' to check availability.\n'4' to see when the next patient is leaving.\n\n"))
        if(action == 1):
            addPatient()
        elif(action == 2):
            wait()
        elif(action == 3):
            print("\nNumber of operating rooms available: ", Global.operatingRooms)
            print("Number of beds available: ", Global.beds)
            print("Nurses can see", Global.nurses * 4, "patients")
            print("Doctors can see", Global.doctors * 8, "patients")
            print("Number of equipment available: ", Global.medicalEquipment)
            print("Number of medication available: ", Global.medication)
        elif(action == 4):
            if(len(Global.patients) == 0):
                print("\nThere are no patients.")
            else:
                print("\nThe next patient will be leaving in", minimumTime(), "hours.")
        else:
            print("\nInvalid command.")
    
main()