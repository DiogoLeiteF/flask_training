


###################################
####     ADD DATA to DB      ######
##################################


def add_dummy_data(db, User, Sale, Product):

    user1 = User(email='admin@gmail.com', first_name='Antonio', last_name='José',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e', user_type='admin')
    user2 = User(email='supplier1@gmail.com', first_name='Manuel', last_name='Antonio',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e', user_type='supplier')
    user3 = User(email='supplier2@gmail.com', first_name='David', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e', user_type='supplier')
    user4 = User(email='user1@gmail.com', first_name='Ricardo', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user5 = User(email='user2@gmail.com', first_name='Ricardo', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user6 = User(email='user3@gmail.com', first_name='Ricardo', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user7 = User(email='user4@gmail.com', first_name='Ricardo', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user8 = User(email='user5@gmail.com', first_name='Ricardo', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user9 = User(email='user6@gmail.com', first_name='Ricardo', last_name='Leonel',
                 password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user10 = User(email='user7@gmail.com', first_name='Ricardo', last_name='Leonel',
                  password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user11 = User(email='user8@gmail.com', first_name='Ricardo', last_name='Leonel',
                  password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user12 = User(email='user9@gmail.com', first_name='Ricardo', last_name='Leonel',
                  password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user13 = User(email='user10@gmail.com', first_name='Ricardo', last_name='Leonel',
                  password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')
    user14 = User(email='user11@gmail.com', first_name='Ricardo', last_name='Leonel',
                  password='sha256$KzmxWcp65OIqQ37C$88a3a43ab774f0584de9e8b7ca6c960a630d575e68181c096b74b1e490478a9e')

    db.session.add_all([user1, user2, user3, user4, user5, user6,
                       user7, user8, user9, user10, user11, user12, user13, user14])

    p1 = Product(name='PC 1', supplier='supplier1', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p2 = Product(name='PC 2', supplier='supplier1', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p3 = Product(name='PC 3', supplier='supplier1', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p4 = Product(name='PC 4', supplier='supplier1',
                 supplier_price=50, retail_price=125, stock=8, stock_prev=100)
    p5 = Product(name='PC 5', supplier='supplier2', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p6 = Product(name='PC 6', supplier='supplier2', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p7 = Product(name='PC 7', supplier='supplier2',
                 supplier_price=50, retail_price=125, stock=9, stock_prev=100)
    p8 = Product(name='PC 8', supplier='supplier2', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p9 = Product(name='PC 9', supplier='supplier2', supplier_price=50,
                 retail_price=125, stock=50, stock_prev=100)
    p10 = Product(name='PC 10', supplier='supplier2',
                  supplier_price=50, retail_price=125, stock=50, stock_prev=100)
    p11 = Product(name='PC 11', supplier='supplier2',
                  supplier_price=50, retail_price=125, stock=50, stock_prev=100)
    p12 = Product(name='PC 12', supplier='supplier2',
                  supplier_price=50, retail_price=125, stock=50, stock_prev=100)

    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])

    db.session.commit()
