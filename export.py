import xlsxwriter
import datetime

class Table():

    col = 0
    alphavite = ["A","B","C","D","E","F","G","I","J","K"]

    def __init__(self, tableName : str):
        now = datetime.datetime.now()
        self.doc = xlsxwriter.Workbook(tableName+"_"+now.strftime("%Y-%m-%d")+".xlsx")
        self.sheet = self.doc.add_worksheet()


    def addColumn(self, data : list, title : str):
        row = 0
        self.sheet.write(row, self.col, title)
        row+=1
        for item in data:
            self.sheet.write(row, self.col, item)
            row+=1
        self.col+=1

    def addChart(self, title : str, xLabels : list, legends : list, dataCoordinates : dict):
        chart = self.doc.add_chart({"type" : "line"})
        for key in dataCoordinates.keys(): 
            chart.add_series({"values" : f"=Sheet1!{key}:{dataCoordinates[key]}"})
        self.sheet.insert_chart(self.alphavite[self.col-1]+"1",chart)
        #chart.set_x_axis({'text_axis' : True, 'name' : "titile"})

    def close(self):
        self.doc.close()
