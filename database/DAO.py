from database.DB_connect import DBConnect
from model.arco import Arco
from model.product import Product


class DAO():
    def __init__(self):
        pass



    @staticmethod
    def getAllColors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()

        res = []
        query = """SELECT  DISTINCT gp.Product_color
                    FROM go_products gp 
                    order by gp.Product_color"""

        cursor.execute(query)

        for row in cursor:
            res.append(row[0])
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodes(color):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        res = []
        query = """SELECT *
                    FROM go_products gp 
                    WHERE gp.Product_color =%s"""

        cursor.execute(query, (color,))

        for row in cursor:
            res.append(Product(**row))
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdges(color, year, idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        res = []
        query = """SELECT   gds.Product_number AS P1, gds2.Product_number AS P2, COUNT(DISTINCT gds.Date) AS peso
            FROM (SELECT gp.Product_number
                 FROM go_products gp 
                 WHERE gp.Product_color =%s) t1,
                 (SELECT gp.Product_number
                 FROM go_products gp 
                 WHERE gp.Product_color = %s) t2,
                 go_daily_sales gds , go_daily_sales gds2 
            WHERE
            YEAR(gds.`Date`) = %s and  YEAR(gds2.`Date`) = %s and gds.`Date` = gds2.`Date`
            and gds.Product_number = t1.Product_number and gds2.Product_number = t2.Product_number
            and gds.Retailer_code = gds2.Retailer_code and gds.Product_number < gds2.Product_number
            GROUP BY P1, P2"""

        cursor.execute(query, (color, color, year, year))

        #for row in cursor:
            #res.append((idMap[row['P1']], idMap[row['P2']], row['peso']))

        for row in cursor:
            res.append(Arco(
                idMap[row['P1']],
                idMap[row['P2']],
                row['peso']
            ))
        cursor.close()
        cnx.close()
        return res



