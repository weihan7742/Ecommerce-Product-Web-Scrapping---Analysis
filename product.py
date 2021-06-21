class Product: 
    def __init__(self,name,desc,rating,no_rating,no_sold) -> None:
        self.name = name
        self.desc = desc
        self.rating = rating
        self.no_rating = no_rating
        self.no_sold = no_sold

    def __str__(self) -> str:
        return "Product: " + self.name

class Seller: 
    def __init__(self,name,rating,no_products,response_rate,response_time,follower,joined):
        self.name = name
        self.rating = rating
        self.no_products = no_products
        self.response_rate = response_rate
        self.response_time = response_time
        self.follower = follower
        self.joined = joined

    def __str__(self):
        return "Seller: " + self.name

 