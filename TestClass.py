
# class named as the table name in the database 'candy'
class TestClass(object):
    area = 100

    # constructor
    def __init__(self, h, w):
        self.h = h
        self.w = w


    # add self as parameter indicates the the method is a class method, not a free function
    def testMethod(self):
        area = self.h * self.w
        print(area, ' test method invoked')

        
        
