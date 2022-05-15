##This ia where I will make the calls to the terminal to input to the DCF


import blpapi
import sys
import pdblp


def BloombergDataGrab(security, date):

    testCon = pdblp.BCon(debug=False, port=8194, timeout=5000)

    testCon.start()
    
    #This is where I will get all the data from BloombergDataGrab
    WACC = testCon.bdh(security, 'VM011', str(int(date) - 30000), date).iloc[-1, 0] #WACC
    ETR = testCon.bdh(security, 'RR037', str(int(date) - 30000), date).iloc[-1, 0] #Effective Tax Rate
    
    #Main Section
    Revenue = testCon.bdh(security, 'IS010', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Revenue in Millions
    #print(Revenue)
    COGS = testCon.bdh(security, 'IS021', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Cost of Revenue in Millions
    GP = testCon.bdh(security, 'RR861', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Gross Profit in Millions
    EBITDA = testCon.bdh(security, 'RR009', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #EBITDA in Millions
    DA = testCon.bdh(security, 'A0122', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Depreciation/Amortization in Millions
    EBIT = testCon.bdh(security, 'RR002', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #EBIT in Millions
    NWC = testCon.bdh(security, 'F0918',  str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #NWC in Millions
    Capex = testCon.bdh(security, 'RR014', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] # Capex in Millions
    
    
    #Section used to calculate the Drivers of Growth in the Main Section
    AR = testCon.bdh(security, 'BS496', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Accounts Receivable in Millions
    Inventory = testCon.bdh(security, 'BS013', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Inventory in Millions
    AP = testCon.bdh(security, 'BS036', str(int(date) - 30000), date).iloc[[False, False, False, False, True, True, True, True, True, True, True, True], 0] #Accounts Payable in Millions
    
    #Section where we do the final calculations to help calculate the final values of the DCF
    Cash = testCon.bdh(security, 'BS010', str(int(date) - 30000), date).iloc[-1, 0] #Cash in Millions
    EM = testCon.bdh(security, 'F1129', str(int(date) - 30000), date).iloc[-1, 0] #Exit Multiple
    NetDebt = testCon.bdh(security, 'RR208', str(int(date) - 30000), date).iloc[-1, 0] #Net Debt
    Shares = testCon.bdh(security, 'BS081', str(int(date) - 30000), date).iloc[-1, 0] #Number of Outstanding Shares in Millions
    
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
    
    return WACC, ETR, RevenuePrevious, RevenueCurrent, COGSCurrent, GPCurrent, EBITDACurrent, DACurrent, EBITCurrent, NWCPrevious, NWCCurrent, CapexCurrent, ARPrevious, ARCurrent, InventoryPrevious, InventoryCurrent, APPrevious, APCurrent, Cash, EM, NetDebt, Shares

BloombergDataGrab('AAPL US Equity', '20220412')
#print(BloombergDataGrab('AAPL US Equity', '20220412'))