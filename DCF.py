
import numpy as np
import pandas as pd
import BloombergDataGrab as BDG


tickerInput = input("Please enter a ticker: ")
dateInput = input("Please enter a date in YYYYMMDD: ")

times = 5
YoYSteps = -0.01
GPMarginSteps = -0.001
EBITDASteps = -0.001
DepreciationSteps = -0.001
ARSteps = 0.1
InventorySteps = 0.1
APSteps = 0.1
CapexSteps = 0.001

#This pulls all the data

WACC, ETR, Revenue, COGS, GP, EBITDA, DA, EBIT, NWC, Capex, AR, Inventory, AP, Cash, EM, Shares = BDG.BloombergDataGrab(tickerInput + " US Equity", dateInput)

#print(Revenue.iloc[-1])


#This does the actual calculation of the DCF
def DCF():
    
#This is the actual calculation, I will add the repeating part later
    #This is the initialization for all the variables 
    CurrentRevenue = Revenue.iloc[-1]
    YoYGrowth = CurrentRevenue/Revenue.iloc[-1]
    
    CurrentCOGS = COGS.iloc[-1]
    
    GPMargin = (CurrentRevenue - CurrentCOGS) / CurrentRevenue
    DepreciationPercent = DA.iloc[-1]/CurrentRevenue
    EBITDAMargin = EBITDA.iloc[-1]/CurrentRevenue
    
    DSO = AR.iloc[-1]/(CurrentRevenue/365)
    DIO = Inventory.iloc[-1]/(CurrentCOGS/365)
    DPO = AP.iloc[-1]/(CurrentCOGS/365)
   
    CurrentEBIT = EBIT.iloc[-1] * (1-(ETR/100))
    NWC = AR.iloc[-1] + Inventory.iloc[-1] - AP.iloc[-1]
    ChangeNWC = NWC - (AR.iloc[-2] + Inventory.iloc[-2] - AP.iloc[-2])
    
    CapexPercent = Capex.iloc[-1]/CurrentRevenue
    
    FCFtoFirm = CurrentEBIT + DA.iloc[-1] - (ChangeNWC + Capex.iloc[-1])
    
    #I am now simulating the future years
    for i in range(times):
        #Calculate the Revenue Growth
        YoYGrowth += YoYSteps
        CurrentRevenue *= YoYGrowth
        
        
        #Calculate the EBIT Growth
        EBITDAMargin += EBITDASteps
        DepreciationPercent += DepreciationSteps
        NewDepreciation = DepreciationPercent * CurrentRevenue
        NewEBIT = (CurrentRevenue * EBITDAMargin) - (CurrentRevenue * DepreciationPercent) * (1-(ETR/100))
        
        #Calculate the rest to calculate the FCF Firm Value for that years
        DSO += ARSteps
        NewAR = DSO * (CurrentRevenue/365)
        
        GPMargin += GPMarginSteps
        NewCOGS = (1-GPMargin) * CurrentRevenue
        
        DIO += InventorySteps
        NewInventory = DIO * (CurrentCOGS/365)
        
        DPO += APSteps
        NewAP = DPO * (NewCOGS/365)
        
        OldNWC = NWC
        NWC = NewAR + NewInventory - NewAP
        NewChangeNWC = NWC - OldNWC
        
        CapexPercent += CapexSteps
        NewCapex = CapexPercent * CurrentRevenue
        
        FCFtoFirm = NewEBIT + NewDepreciation - (NewChangeNWC + NewCapex)
        
        FCFPresentValue = FCFtoFirm * (1/((1 + WACC/100)**(i+1)))
        
        
        
        
        
        
        
        
        
        
        
        
    
    
