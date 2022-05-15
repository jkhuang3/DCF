
import numpy as np
import pandas as pd
import BloombergDataGrab as BDG


tickerInput = input("Please enter a ticker: ")
dateInput = input("Please enter a date in YYYYMMDD: ")
modeInput = input("Please enter a mode (Perpetuity or Exit Multiple): ")
times = input("Please specify a time period: ")

PerpetualGrowthRate = 0.03

mode = "Perpetuity"

#This pulls all the data

WACC, ETR, RevenuePrevious, RevenueCurrent, COGSCurrent, GPCurrent, EBITDACurrent, DACurrent, EBITCurrent, NWCPrevious, NWCCurrent, CapexCurrent, ARPrevious, ARCurrent, InventoryPrevious, InventoryCurrent, APPrevious, APCurrent, Cash, EM, NetDebt, Shares = BDG.BloombergDataGrab(tickerInput.upper() + " US Equity", dateInput)


#This does the actual calculation of the DCF
def DCF(mode, times):

    RevenueSteps = -0.01
    GPMarginSteps = -0.001
    EBITDASteps = -0.001
    DepreciationSteps = -0.001
    ARSteps = 0.1
    InventorySteps = 0.1
    APSteps = 0.1
    CapexSteps = 0.001
    
    FCFMaxYearsPerpetuity = 0
    FCFMaxYearsExitMultiple = 0
    
    #This is the actual calculation, I will add the repeating part later
    #This is the initialization for all the variables 
    YoYGrowth = (RevenueCurrent/RevenuePrevious) - 1
    
    GPMargin = (RevenueCurrent - COGSCurrent) / RevenueCurrent
    DepreciationPercent = DACurrent/RevenueCurrent
    EBITDAMargin = EBITDACurrent/RevenueCurrent
    
    DSO = ARCurrent/(RevenueCurrent/365)
    DIO = InventoryCurrent/(COGSCurrent/365)
    DPO = APCurrent/(COGSCurrent/365)
   
    CurrentEBIT = EBITCurrent * (1-(ETR/100))
    NWC = ARCurrent + InventoryCurrent - APCurrent
    OldNWC = NWC
    ChangeNWC = NWC - (ARPrevious + InventoryPrevious - APPrevious)
    CapexPercent = (CapexCurrent/RevenueCurrent) * -1
   
    
    FCFtoFirm = CurrentEBIT + DACurrent - (ChangeNWC + CapexCurrent)
    
    FCFs = 0
    
    NewRevenue = RevenueCurrent
    CurrentCOGS = COGSCurrent
    
    #I am now simulating the future years
    for i in range(times):
        
        #Calculate the Revenue Growth
        YoYGrowth += RevenueSteps
        NewRevenue *= (1 + YoYGrowth)
        
        
        
        #Calculate the EBIT Growth
        EBITDAMargin += EBITDASteps
        DepreciationPercent += DepreciationSteps
        NewDepreciation = NewRevenue * DepreciationPercent
        
        NewEBITDA = NewRevenue * EBITDAMargin
        NewEBIT = (NewRevenue * EBITDAMargin) - (NewRevenue * DepreciationPercent)
        NewForwardEBIT = NewEBIT - (NewEBIT * ETR/100)
        
        #Calculate the rest to calculate the FCF Firm Value for that years
        DSO += ARSteps
        NewAR = DSO * (NewRevenue/365)
        
        GPMargin += GPMarginSteps
        NewCOGS = (1 - GPMargin) * NewRevenue
        
        DIO += InventorySteps
        NewInventory = DIO * (NewCOGS/365)
        
        DPO += APSteps
        NewAP = DPO * (NewCOGS/365)
        
        
        NewNWC = NewAR + NewInventory - NewAP
        NewChangeNWC = NewNWC - OldNWC
        OldNWC = NewNWC
        
        CapexPercent += CapexSteps
        NewCapex = CapexPercent * NewRevenue
        
        
        FCFtoFirm = NewForwardEBIT + NewDepreciation - NewChangeNWC - NewCapex
        FCFMaxYearsPerpetuity = FCFtoFirm
        
        FCFPresentValue = FCFtoFirm/((1 + WACC/100)**(i+1))
        FCFs += FCFPresentValue
        
        FCFMaxYearsExitMultiple = NewEBITDA
      
    if(mode == "Perpetuity"):
        TerminalValue = FCFMaxYearsPerpetuity * (1 + PerpetualGrowthRate)/(WACC/100 - PerpetualGrowthRate)
    else:
        TerminalValue = EM * FCFMaxYearsExitMultiple
   
    PresentTerminalValue = TerminalValue * (1/((1 + WACC/100)**(times)))
    
    FirmValue = PresentTerminalValue + FCFs
    
    EquityValue = FirmValue - NetDebt + Cash
    
    IntrinsicValue = EquityValue/Shares
    
    return "Intrinsic Value: " + str(round(IntrinsicValue, 2))
    

#DCF(mode)
print(DCF(modeInput, int(times)))
    
    
    
    
        
        
        
        
        
        
        
        
    
    
