from datetime import datetime, timedelta
import calendar

class Finyear:
    ''' 
    It Returns the start date and end date of a month for a given financial year and month.
    also set financial_month_start_month
    year = "2023-24" and month as int (e.g., 4 for April)
    month_start_date returns a date like "01-04-2023"
    month_end_date returns a date like "30-04-2023"
    month_list returns all months of the financial year from "04-2023" to "03-2024"
    '''

    def __init__(self, year: str, **kwargs) -> None:
        '''
            year : 2023-24 as str or 2023 str
            **kwargs: financial_month_start_month:str  
        '''
        self.finyear = year
        self.financial_month_start_month = str(kwargs.get('month_start_date', 4))     
        self.year = year[:4]
   
    def month_start_date(self, month: int) -> str:
        ''' return datetime object 
            return month first date
        '''
        if month >= int(self.financial_month_start_month) and month <= 12:
            # print('first')
            return datetime.strptime(f"01-{month:02d}-{self.year[:4]}", '%d-%m-%Y').date()
        elif month > 0 and month < int(self.financial_month_start_month):
            # print('second')
            next_year = (datetime.strptime(f"01-{month:02d}-{self.year[:4]}", '%d-%m-%Y').date()+timedelta(days=395)).year
            return datetime.strptime(f"01-{month:02d}-{next_year}", '%d-%m-%Y').date()
        else:
            raise Exception('Please enter Correct Month')
        # return datetime.strptime(f"01-{month:02d}-{self.year[:4]}", '%d-%m-%Y').date()

    def month_end_date(self, month: int) -> str:
        # Get the last day of the month
        start_date = self.month_start_date(month=month)
        month = start_date.month
        year = start_date.year
        total_month = calendar.monthcalendar(year=year, month=month)
        last_date = 0
        for day in total_month[len(total_month)-1]:
            if day > last_date:
                last_date = day
        
        return datetime.strptime(f"{last_date}-{month}-{year}", "%d-%m-%Y").date()
    
    def previous_month_dates(self, month:int):
        end_date_ = self.month_start_date(month=month)-timedelta(days=1)
        month = end_date_.month
        year = end_date_.year
        first_date_ = datetime.strptime(f"01-{month}-{year}", "%d-%m-%Y").date()
        return first_date_, end_date_


    def month_list(self) -> list:

        # Construct a list of month-year strings for the financial year
        start_date = datetime.strptime(f"01-04-{self.year}", "%d-%m-%Y").date()
        end_date = datetime.strptime(f"31-03-{int(self.year)+1}", "%d-%m-%Y").date()
        # print(start_date, end_date)
        month_list = []
        while start_date < end_date:
            month_list.append(start_date.strftime("%m-%Y"))
            start_date += timedelta(days=30)
        return month_list


