from collections import defaultdict
import matplotlib.pyplot as plt

class Chart():
    '''
    create pie charts
    '''
    def __init__(self,amounts:list,search_result:list, categories:list=None, dates:list=None, xlabel:str=None, ylabel=None):
        self.categories=categories
        self.amounts=amounts
        self.dates=dates
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.search_result=search_result
        
    def pie(self):
        category_totals=defaultdict(float)
        for t in self.search_result:
            category_totals[t['category']] += float(t['amount'])

        self.categories=list(category_totals.keys())
        self.amounts=list(category_totals.values())
        max_value=max(self.amounts)
        max_index=self.amounts.index(max_value)
        explode=[0.2 if i==max_index else 0 for i in range(len(self.amounts))]
        return plt.pie(self.amounts, labels=self.categories, explode=explode, shadow=True, autopct="%1.1f%%")