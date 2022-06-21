#This ia where I will make the calls to the terminal to input to the DCF


import blpapi
import sys
import pdblp
import pandas as pd
import numpy as np


def BloombergDataGrab(security, date):

    testCon = pdblp.BCon(debug=False, port=8194, timeout=5000)

    testCon.start()
    
    # #This is where I will get all the data from BloombergDataGrab
    WACC = testCon.bdh(security, 'VM011', str(int(date) - 30000), date) #WACC
    if (WACC.empty or WACC.iloc[-1, 0] == 0):
        WACC = 7.5
    else:
        WACC = WACC.iloc[-1, 0]

    ETR = testCon.bdh(security, 'RR037', str(int(date) - 30000), date) #Effective Tax Rate
    if (ETR.empty or ETR.iloc[-1, 0] == 0):
        ETR = 20
    else:
        ETR = ETR.iloc[-1, 0]
    
    #Main Section
    Revenue = testCon.bdh(security, 'IS010', str(int(date) - 30000), date)
    if (Revenue.empty):
        Revenue = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        Revenue = Revenue.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Revenue in Millions
    COGS = testCon.bdh(security, 'IS021', str(int(date) - 30000), date) #Cost of Revenue in Millions
    if (COGS.empty):
        COGS = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        COGS = COGS.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0]
    GP = testCon.bdh(security, 'RR861', str(int(date) - 30000), date)
    if (GP.empty):
        GP = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        GP = GP.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Gross Profit in Millions
    EBITDA = testCon.bdh(security, 'RR009', str(int(date) - 30000), date)
    if (EBITDA.empty):
        EBITDA = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        EBITDA = EBITDA.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #EBITDA in Millions
    DA = testCon.bdh(security, 'A0122', str(int(date) - 30000), date)
    if (DA.empty):
        DA = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        DA = DA.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Depreciation/Amortization in Millions
    EBIT = testCon.bdh(security, 'RR002', str(int(date) - 30000), date)
    if (EBIT.empty):
        EBIT = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        EBIT = EBIT.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #EBIT in Millions
    NWC = testCon.bdh(security, 'F0918',  str(int(date) - 30000), date)
    if (NWC.empty):
        NWC = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        NWC = NWC.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #NWC in Millions
    Capex = testCon.bdh(security, 'RR014', str(int(date) - 30000), date)
    if (Capex.empty):
        Capex = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        Capex.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] # Capex in Millions
    
    
    #Section used to calculate the Drivers of Growth in the Main Section
    AR = testCon.bdh(security, 'BS496', str(int(date) - 30000), date)
    if (AR.empty):
        AR = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        AR = AR.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Accounts Receivable in Millions
    Inventory = testCon.bdh(security, 'BS013', str(int(date) - 30000), date)
    if(Inventory.empty):
        Inventory = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        Inventory = Inventory.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Inventory in Millions  
    AP = testCon.bdh(security, 'BS036', str(int(date) - 30000), date)
    if (AP.empty):
        AP = pd.DataFrame(np.zeros(shape=(8,1)))
    else:
        AP = AP.iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Accounts Payable in Millions
    
    #Section where we do the final calculations to help calculate the final values of the DCF
    Cash = testCon.bdh(security, 'BS010', str(int(date) - 30000), date)#Cash in Millions
    if (Cash.empty or Cash.iloc[-1, 0] == 0):
        Cash = 0
    else:
        Cash = Cash.iloc[-1, 0]

    EM = testCon.bdh(security, 'F1129', str(int(date) - 30000), date)#.iloc[-1, 0] #Exit Multiple
    if (EM.empty or EM.iloc[-1,0] == 0):
        EM = 17.12
    else:
        EM = EM.iloc[-1, 0]
    
    NetDebt = testCon.bdh(security, 'RR208', str(int(date) - 30000), date)
    if (NetDebt.empty or NetDebt.iloc[-1, 0] == 0):
        NetDebt = 0
    else:
        NetDebt = NetDebt.iloc[-1, 0] #Net Debt\
    Shares = testCon.bdh(security, 'BS081', str(int(date) - 30000), date).iloc[-1, 0] #Number of Outstanding Shares in Millions

    LastPrice = testCon.bdh(security, 'PX_LAST', str(int(date)-1), date).iloc[-1, 0] #Last Price in Dollars
    print(LastPrice)
    
    RevenuePrevious = 0
    RevenueCurrent = 0
    COGSCurrent = 0
    GPCurrent = 0
    EBITDACurrent = 0
    DACurrent = DA.iloc[-1] * 2
    EBITCurrent = 0
    NWCPrevious = 0
    NWCCurrent = 0
    CapexCurrent = 0
    ARPrevious = AR.iloc[-2]
    ARCurrent = AR.iloc[-1]
    InventoryPrevious = Inventory.iloc[-2]
    InventoryCurrent = Inventory.iloc[-1]
    APPrevious = AP.iloc[-2]
    APCurrent = AP.iloc[-1]
    
    for i in range(2,8):
        if (i < 4):
            RevenuePrevious += Revenue.iloc[i]
            #ARPrevious += AR.iloc[i]
            #InventoryPrevious += Inventory.iloc[i]
            #APPrevious += AP.iloc[i]
            NWCPrevious += NWC.iloc[i]
        elif (i >= 4 and i < 6):
            RevenuePrevious += Revenue.iloc[i]
            NWCPrevious += NWC.iloc[i]
            RevenueCurrent += Revenue.iloc[i]
            COGSCurrent += COGS.iloc[i]
            GPCurrent += GP.iloc[i]
            EBITDACurrent += EBITDA.iloc[i]
            EBITCurrent += EBIT.iloc[i]
            NWCCurrent += NWC.iloc[i]
            CapexCurrent += Capex.iloc[i]
        else:
            RevenueCurrent += Revenue.iloc[i]
            COGSCurrent += COGS.iloc[i]
            GPCurrent += GP.iloc[i]
            EBITDACurrent += EBITDA.iloc[i]
            #DACurrent += DA.iloc[i]
            EBITCurrent += EBIT.iloc[i]
            NWCCurrent += NWC.iloc[i]
            CapexCurrent += Capex.iloc[i]
            #ARCurrent += AR.iloc[i]
            #InventoryCurrent += Inventory.iloc[i]
            #APCurrent += AP.iloc[i]
    
    #print(RevenueCurrent)
    #print(RevenuePrevious)
    #print(DACurrent)
    
    #return WACC, ETR, RevenuePrevious, RevenueCurrent, COGSCurrent, GPCurrent, EBITDACurrent, DACurrent, EBITCurrent, NWCPrevious, NWCCurrent, CapexCurrent, ARPrevious, ARCurrent, InventoryPrevious, InventoryCurrent, APPrevious, APCurrent, Cash, EM, NetDebt, Shares, LastPrice

#WACC, ETR, RevenuePrevious, RevenueCurrent, COGSCurrent, GPCurrent, EBITDACurrent, DACurrent, EBITCurrent, NWCPrevious, NWCCurrent, CapexCurrent, ARPrevious, ARCurrent, InventoryPrevious, InventoryCurrent, APPrevious, APCurrent, Cash, EM, NetDebt, Shares = BloombergDataGrab('AAPL US Equity', '20220412')

#RevenueRandom = np.random.normal(RevenueCurrent, 0.1, size=100)
#print(np.around(RevenueRandom, decimals=2))
print(BloombergDataGrab('AMZN US Equity', '20220618'))