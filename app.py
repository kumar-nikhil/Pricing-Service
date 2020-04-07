# from models.item import Item
# from models.alert import Alert
# # URL = "https://www.johnlewis.com/2018-apple-ipad-pro-12-9-inch-a12x-bionic-ios-wi-fi-cellular-64gb/p3834601"
# # TAG = "p"
# # QUERY = {'class': "price price--large"}
# #
# #
# # item = Item(URL, TAG, QUERY)
# # # item.save_to_mongo()
# #
# # items_loaded = Item.get_by_id("097f71de59b442b594391d0764b188ad")
# # # print(items_loaded)
# # # print(items_loaded[0].load_price())
# # print(items_loaded)
#
# alert = Alert("097f71de59b442b594391d0764b188ad", 2000)
# alert.save_to_mongo()

import os
from flask import Flask, render_template
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix='/users')

if __name__ == "__main__":
    app.run(debug=True)
