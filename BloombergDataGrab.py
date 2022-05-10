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
    Revenue = testCon.bdh(security, 'IS010', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Revenue in Millions
    COGS = testCon.bdh(security, 'IS021', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Cost of Revenue in Millions
    GP = testCon.bdh(security, 'RR861', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Gross Profit in Millions
    EBITDA = testCon.bdh(security, 'RR009', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #EBITDA in Millions
    DA = testCon.bdh(security, 'A0122', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Depreciation/Amortization in Millions
    EBIT = testCon.bdh(security, 'RR002', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #EBIT in Millions
    NWC = testCon.bdh(security, 'F0918',  str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #NWC in Millions
    Capex = testCon.bdh(security, 'RR014', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] # Capex in Millions
    
    
    #Section used to calculate the Drivers of Growth in the Main Section
    AR = testCon.bdh(security, 'BS496', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Accounts Receivable in Millions
    Inventory = testCon.bdh(security, 'BS013', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Inventory in Millions
    AP = testCon.bdh(security, 'BS036', str(int(date) - 30000), date).iloc[[False, False, False, True, False, False, False, True, False, False, False, True], 0] #Accounts Payable in Millions
    
    #Section where we do the final calculations to help calculate the final values of the DCF
    Cash = testCon.bdh(security, 'BS010', str(int(date) - 30000), date).iloc[-1, 0] #Cash in Millions
    EM = testCon.bdh(security, 'F1129', str(int(date) - 30000), date).iloc[-1, 0] #Exit Multiple
    Shares = testCon.bdh(security, 'BS081', str(int(date) - 30000), date).iloc[-1, 0] #Number of Outstanding Shares in Millions
    
    return WACC, ETR, Revenue, COGS, GP, EBITDA, DA, EBIT, NWC, Capex, AR, Inventory, AP, Cash, EM, Shares
   
   
BloombergDataGrab('TSLA US Equity', '20220412')