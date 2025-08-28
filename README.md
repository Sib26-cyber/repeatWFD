An E-Commerce web application built with the Django Python Web Framework.
This project simulates an online store for running gear where customers can browse products, add them to a cart, and place orders. It also supports returns/refunds, and user management.

Tests included in the project
python manage.py test cart.tests.CartViewTests -v 2
python manage.py test payment.tests.PaymentFlowTests -v 2
python manage.py test users.tests.UserAccountTests -v 2
