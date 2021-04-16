#!/usr/bin/python
import pgdb
from sys import argv
from datetime import datetime
class DBContext:
    """DBContext is a small interface to a database that simplifies SQL.
    Each function gathers the minimal amount of information required and executes the query."""

    def __init__(self): #PG-connection setup
        print("AUTHORS NOTE: If you submit faulty information here, I am not responsible for the consequences.")

        print("The idea is that you, the authorized database user, log in.")
        print ("Then the interface is available to employees whos should only be able to enter shipments as they are made.")
        params = {'host':'nestor2.csc.kth.se', 'user':'fmatz', 'database':'fmatz', 'password':'hAAIUMMBhbkm'}
        self.conn = pgdb.connect(**params)
        self.menu = ["Record a shipment","Show stock", "Show shipments", "Exit"]
        self.cur = self.conn.cursor()
    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i,x in enumerate(self.menu):
            print("%i. %s"%(i+1,x))
        return self.get_int()

    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError,ValueError, TypeError,SyntaxError):
                print("That was not a number, genious.... :(")
 
    def makeShipments(self):
        
        #THESE INPUT LINES  ARE NOT GOOD ENOUGH    
        # YOU NEED TO TYPE CAST/ESCAPE THESE AND CATCH EXCEPTIONS
        try:
            CID = int(pgdb.escape_string(raw_input("CustomerID: ")))
        except(NameError,ValueError,TypeError,SyntaxError):
            print("Customer ID Invalid")
            return
        try:
            SID = int(pgdb.escape_string(raw_input("ShipmentID: ")))
        except(NameError,ValueError,TypeError,SyntaxError):
            print("Shipment ID Invalid")
            return
        try:
            Sisbn= str(pgdb.escape_string(raw_input("isbn: ").strip()))
        except(NameError,ValueError,TypeError,SyntaxError):
            print("Shipment ISBN Invalid")
            return
        try:
            timeFormat = '%Y-%m-%d %H:%M:%S'
            Sdate= "%s"%(datetime.strftime(datetime.strptime(pgdb.escape_string(str(raw_input("Ship date (yyyy-mm-dd hh:mm:ss) ").strip().strip('\''))),timeFormat),timeFormat))
        except(NameError,ValueError,TypeError,SyntaxError):
            print("Shipment Date Invalid")
            return
        # THIS IS NOT RIGHT  YOU MUST FORM A QUERY THAT HELPS
        query ="SELECT stock FROM stock WHERE isbn='%s'"%(Sisbn)
        print(query)
        # HERE YOU SHOULD start a transaction    
        
        #YOU NEED TO Catch exceptions ie bad queries
        try:
            self.cur.execute(query)
        except (pgdb.DatabaseError, pgdb.OperationalError):
            print("  Exception encountered while modifying table data." )
            self.conn.rollback ()
            return   
        #HERE YOU NEED TO USE THE RESULT OF THE QUERY TO TEST IF THER ARE 
        #ANY BOOKS IN STOCK 
        # YOU NEED TO CHANGE THIS TO SOMETHING REAL
        try:
            cnt=int(self.cur.fetchone()[0])
            if cnt < 1:
                print("No more books in stock.")
                return
            else:
                print ("WE have the book in stock")
        except(TypeError):
            print('Book not found')
            return
        query="""UPDATE stock SET stock=stock-1 WHERE isbn='%s';"""%(Sisbn)
        print (query)
        #YOU NEED TO Catch exceptions  and rollback the transaction
        try:
            self.cur.execute(query)
        except (pgdb.DatabaseError, pgdb.OperationalError):
            print ("  Exception encountered while modifying table data." )
            self.conn.rollback ()
            return   
        self.cur.execute(query)
        print ("stock decremented" )
        
        query="""INSERT INTO shipments VALUES (%i, %i, '%s','%s');"""%(SID,CID,Sisbn,Sdate)
        print (query)
        #YOU NEED TO Catch exceptions and rollback the transaction
        try:
            self.cur.execute(query)
        except(pgdb.DatabaseError, pgdb.OperationalError):
            print('Could not insert shipment.')
            return
        print ("shipment created") 
        # This ends the transaction (and starts a new one)    
        self.conn.commit()



    def showStock(self):
        query="""SELECT * FROM stock;"""
        print (query)
        try:
            self.cur.execute(query)
        except (pgdb.DatabaseError, pgdb.OperationalError):
            print ("  Exception encountered while modifying table data." )
            self.conn.rollback ()
            return   
        self.print_answer()
    def showShipments(self):
        query="""SELECT * FROM shipments;"""
        print (query)
        try:
            self.cur.execute(query)
        except (pgdb.DatabaseError, pgdb.OperationalError):
            print ("  Exception encountered while modifying table data." )
            self.conn.rollback ()
            return   
        self.print_answer()
    def exit(self):    
        self.cur.close()
        self.conn.close()
        exit()

    def print_answer(self):
        print("\n".join([", ".join([str(a) for a in x]) for x in self.cur.fetchall()]))

    # we call this below in the main function.
    def run(self):
        """Main loop.
        Will divert control through the DBContext as dictated by the user."""
        actions = [self.makeShipments, self.showStock, self.showShipments, self.exit]
        while True:
            try:
                actions[self.print_menu()-1]()
            except IndexError:
                print("Bad choice")
                continue

if __name__ == "__main__":
    db = DBContext()
    db.run()
