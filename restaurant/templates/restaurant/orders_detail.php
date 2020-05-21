{% include 'restaurant/header.php' %}
{% load rest_filters %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Order Details</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <div class="order-details-pop">
                                    <div class="order-detail-mainttl">
                                    </div>
                                    <div class="customer-info-pop">
                                        <div class="customer-name-prnt">
                                        <h2>{{ order.user.first_name }} {{ order.user.last_name }}</h2>
                                        <a href="#">Print</a>
                                        </div>
                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-phone" aria-hidden="true"></i>{% if order.user %}{{ order.user.profile.contact }}{% else %}{{ order.contact_number }}{% endif %}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-map-marker" aria-hidden="true"></i>{{ order.address_line1 }}, {{ order.address_line2 }}, {{ order.city }}, {{ order.state }}- {{ order.zip_code }}</span>
                                        </div>

                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-hashtag"></i>{{ order.id_string }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-calendar-check-o" aria-hidden="true"></i>Placed at {{ order.added_date }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-credit-card"></i>${{ order.total_price }} - {{ order.get_payment_display }}</span>
                                        </div>
                                    </div>

                                    <div class="customer-instructions-pop">
                                        <h2>Customer Instructions</h2>
                                        {% if order.note %}
                                            <p>{{ order.note }}</p>
                                        {% else %}
                                            <p>No Instructions Available</p>
                                        {% endif %}
                                    </div>

                            <div class="order-pop-table">
                                <table class="table table-striped checkout-first-accor">
                                    <thead>
                                      <tr>
                                        <th>Item Names</th>
                                        <th>Quantity</th>
                                        <th>Price</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in order.cart.all %}
                                      <tr>
                                        <td>
                                            <span class="food_item_name order_det_ls">{{ item.food.name }}{% if item.style %}-{{ item.style.name_of_style }} (${{ item.style.cost }}){% else %} (${{ item.food.new_price }}){% endif %}</span>
                                            <div class="food_modified-gp">
                                                {% for extra in item.extras.all %}
                                                <div class="food_modified">
                                                    <span class="fd-md-ttl d-flex">{{ extra.name_of_extra }} (${{ extra.cost }})</span>
                                                </div>
                                                {% endfor %}
                                            </div>
                                        </td>
                                        <td>{{ item.number_of_food }}</td>
                                        <td>${{ item.get_total }}</td>
                                      </tr>
                                      {% endfor %}
                                    </tbody>
                                </table>
                                <div class="carttotal-prcbx-hl">
                                    <div class="carttotal-prcbx">
                                        <div class="rws-inf">
                                            <span class="inftxt flt-lft">Subtotal</span>
                                            <span class="inftxt-charge flt-rgt" id="total_price" data-id="{{ order.cart.all|get_total_price }}">${{ order.cart.all|get_total_price }}</span>
                                        </div>
                                        <div class="rws-inf">
                                            <span class="inftxt flt-lft">Delivery Charge</span>
                                            <span class="inftxt-charge flt-rgt" id="delivery_cost" data-id="{{ request.restaurant.delivery_charge }}">${{ request.restaurant.delivery_charge }}</span>
                                        </div>

                                        <div class="total-cartfrst-acor">
                                            <span class="totltxt flt-lft">Total</span>
                                            <span class="inftxt-charge flt-rgt" id="total"></span>
                                        </div>
                                        <div class="acpt-ord-btn-hl">
                                            <a href="{% url 'restaurant:accept-order' order.id %}" style="color:white;"><button class="acpt-ord-btn">Accept Order</button></a>
                                        </div>
                                    </div>
                                </div>
                            </div>

                                </div>
                            </div>
                    </div>
                </div>
            </div>
            <!-- right body part -->
        </div>
        </div>

    </section>
    {% include 'restaurant/footer.php' %}
    <script>
        $(document).ready(function(){
            var food_total = $("#total_price").attr("data-id");
            var delivery_cost = $("#delivery_cost").attr("data-id");
            var total = parseInt(food_total) + parseInt(delivery_cost);
            $("#total").html("$" + total);
        });
    </script>

  </body>
</html>
