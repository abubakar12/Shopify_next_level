import numpy as np
import pandas as pd

class calculations_main:
    
    def __init__(self,revenue=0,taxes=0,shipping_cost=0,other_expenses=0,handling_fee=0,cogs=0,adspend=0,app_expenses=0,\
                 tax_rate=0,fb_adspend=0,goog_adspend=0,other_marketing_expenses=0,transaction_fees=0,miscellaneous_expense=0,\
                     price=0,quantity=0,sum_all_orders_per_customer=0,customer_count=1):
        self.revenue = revenue
        self.taxes = taxes
        self.shipping_cost=shipping_cost
        self.other_expenses=other_expenses
        self.miscellaneous_expense=miscellaneous_expense
        self.handling_fee = handling_fee
        self.cogs = cogs
        self.adspend=adspend
        self.app_expenses=app_expenses
        self.tax_rate=tax_rate
        self.fb_adspend=fb_adspend
        self.goog_adspend=goog_adspend
        self.other_marketing_expenses=other_marketing_expenses
        self.transaction_fees=transaction_fees
        self.price=price
        self.quantity=quantity
        self.sum_all_orders_per_customer=sum_all_orders_per_customer
        self.customer_count=customer_count
        
        
    def revenue_calc(self):
        revenue=self.price*self.quantity
        self.revenue=revenue
        return revenue
        
        
    def adspend_calc(self):
        total_adspend=self.fb_adspend+self.goog_adspend+self.other_marketing_expenses
        return total_adspend
    
    def taxes_calc(self,vat_flag=True):
        tax_factor=1+self.tax_rate
        vat=(self.revenue/tax_factor)*(self.tax_rate)
        if vat_flag==True:
            self.taxes=vat
        return vat
    
    def other_expenses_calc(self):
        other_expenses=self.transaction_fees+self.miscellaneous_expense
        self.other_expenses=other_expenses
        return other_expenses  
    
    def tot_expenses_calc(self,with_tax=True):
        if with_tax==False:
            expense=self.shipping_cost+self.other_expenses+self.handling_fee+self.cogs+self.adspend+self.app_expenses
        else:
            expense=self.taxes+self.shipping_cost+self.other_expenses+self.handling_fee+self.cogs+self.adspend+self.app_expenses
        
        return expense
    
        
    def net_profit_calc(self):
        net_profit=self.revenue-self.taxes-self.shipping_cost-self.other_expenses-self.handling_fee-self.cogs-self.adspend-self.app_expenses
        return net_profit
     

    def avg_order_value_calc(self):
        avg_ord_value=self.revenue+self.quantity
        return avg_ord_value
        
    def avg_order_profit_calc(self):
        avg_ord_profit= (self.revenue-self.shipping_cost-self.handling_fee-\
                self.cogs-self.adspend-self.app_expenses-self.other_expenses)/self.quantity
            
        return avg_ord_profit
    
    def ltv_calc(self):
        ltv=self.sum_all_orders_per_customer/self.quantity
        return ltv
        
    def cac_calc(self):
        cac=(self.adspend/self.customer_count)
        return cac
    
    def net_margin_calc(self):
        net_margin=((self.revenue-self.taxes-self.shipping_cost-self.transaction_fees-self.handling_fee-self.cogs-\
            self.adspend-self.app_expenses-self.other_expenses)/(self.revenue))*-100
        return net_margin
    
    def gross_margin_calc(self):
        
        num=(self.revenue-self.taxes-self.shipping_cost-self.handling_fee-self.cogs)
        den=self.revenue
        gross_margin=(num.divide(den))*(-100)
        return gross_margin
    
    def gross_profit_calc(self):
        
        gross_profit=self.revenue-self.taxes-self.shipping_cost-self.transaction_fees-self.handling_fee-self.cogs
        return gross_profit



        
        

        

        
        


    
    

    