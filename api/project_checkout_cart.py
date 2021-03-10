from collections import defaultdict
from tabulate import tabulate
from flask_restful import Resource, request
import logging as logger


class ShoppingCart(Resource):
    """
    ShoppingCart class implements the functionality to add the
    items into the cart by validating whether if there is any offer
    that applies for the selected item and calculates the total price
    of all the items after applying all the applicable discounts.
    """
    def __init__(self):
        self.cart = list()
        self.item_count = defaultdict(int)
        self.total_cart_price = 0
        self.product_details = {'CH1': 3.11, 'AP1': 6.00, 'CF1': 11.23,
                                'MK1': 4.75, 'OM1': 3.69}
        self.apple_price = self.product_details['AP1']

    def applicable_offer(self, item):
        """
        Applies if there is any applicable offer for the given item.
        :param item:
        :return: ['', offer_code, offer_price]
        """
        if item == 'AP1' and \
                item in self.item_count.keys() and \
                self.item_count[item] >= 3:
            if self.apple_price == self.product_details['AP1']:
                self.apple_price -= 1.50
            offer_code = 'APPL'
            offer_price = -1.50
            return ['', offer_code, offer_price]

        elif item == 'MK1' and \
                'CH1' in self.item_count.keys() and \
                self.item_count['CH1'] == 1:
            self.item_count['CH1'] -= 1
            offer_code = 'CHMK'
            offer_price = -4.75
            return ['', offer_code, offer_price]

        elif item == 'CF1' and \
                item in self.item_count.keys() and \
                self.item_count[item] == 2:
            self.item_count[item] = 0
            offer_code = 'BOGO'
            offer_price = -11.23
            return ['', offer_code, offer_price]

        elif item == 'OM1' and \
                item in self.item_count.keys() and \
                self.item_count['OM1'] == 1:
            offer_code = 'APOM'
            offer_price = -float(self.apple_price/2)
            return ['', offer_code, offer_price]

        else:
            return

    def add_to_cart(self, data, offer_applicable=False, item=None):
        """
        Add item details to the cart. Items with and without
        applicable offers will be considered to be added to the cart.
        :param data: ['', offer_code, offer_price] if offer is applicable
               data: [item, '', item_price]
        :param offer_applicable: True or False
        :param item:
        :return: None
        """
        if not offer_applicable:
            self.cart.append(data)
            self.total_cart_price += data[-1]
        else:
            bogo_count = 0
            for index, product in enumerate(self.cart):
                if product[0] == item:
                    if item == 'CF1':
                        bogo_count += 1
                        if bogo_count % 2 == 0 and \
                                ((index+1 >= len(self.cart)) or
                                 (index+1 < len(self.cart) and
                                  data != self.cart[index+1])):
                            self.cart.insert(index + 1, data)
                            self.total_cart_price += data[-1]

                    elif item == 'AP1' and \
                            'OM1' in self.item_count.keys() and \
                            ((index+2 >= len(self.cart)) or
                             (index+2 < len(self.cart) and
                              data != self.cart[index+2])):
                        self.item_count['OM1'] -= 1
                        self.cart.insert(index + 2, data)
                        self.total_cart_price += data[-1]
                        break

                    elif 'OM1' not in self.item_count.keys() and \
                            ((index+1 >= len(self.cart)) or
                             (index+1 < len(self.cart) and
                              data != self.cart[index+1])):
                        self.cart.insert(index+1, data)
                        self.total_cart_price += data[-1]

    def checkout_shopping_cart(self, shopping_items):
        """
        From the list of shopping items, each time an item is picked
        and validates whether any offer is applicable for the
        selected item and adds the item to the cart.
        :param shopping_items: list of items
        :return: $total_cart_price
        """
        for item in shopping_items:
            self.item_count[item] += 1
            offer_details = self.applicable_offer(item)
            self.add_to_cart([item, '', self.product_details[item]])
            if offer_details:
                if item == 'OM1':
                    self.add_to_cart(offer_details, offer_applicable=True,
                                     item='AP1')
                else:
                    self.add_to_cart(offer_details, offer_applicable=True,
                                     item=item)
            self.print_cart_data()
        return self.total_cart_price

    def print_cart_data(self):
        # Prints the cart details
        print('```')
        self.cart.append(['------', '------', '------'])
        self.cart.append(['', '', self.total_cart_price])
        self.cart.append(['```', '', ''])
        print(tabulate(self.cart, headers=["Item", "offer", "Price"]))
        self.cart = self.cart[:len(self.cart)-3]

    def get(self):
        logger.debug("Started running ShoppingCart App")
        try:
            items = request.args.get['items']
            total_cart_price = self.checkout_shopping_cart(
                items.strip().split())
            return {"message": "Total price expected: "
                               "${0}".format(total_cart_price),
                    "return_code": 200}
        except Exception as e:
            logger.error("Failed to get the total cart price of the "
                         "shopping cart: {0}".format(str(e)))
            raise Exception("Failed to get the total cart price "
                            "of the shopping cart")
