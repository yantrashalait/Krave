{% include 'restaurant/header.php' %}
                    <!-- right top menu -->
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>List of Orders</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                               <table id="fd-it-ls-dt" class="display">
                                    <thead>
                                        <tr>
                                            <th>Order ID</th>
                                            <th>Date</th>
                                            <th>Transaction</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    {% for order in orders %}
                                        <tr>
                                            <td>
                                                <a href="{% url 'restaurant:order-detail' request.restaurant.id order.id %}">#{{ order.id_string }}</a>
                                            </td>
                                            <td>{{ order.added_date }}</td>
                                            <td>
                                                {{ order.user.username }}<br/>${{ order.total_price }} - {{ order.get_payment_display }}
                                            </td>
                                            <td>
                                                {{ order.get_status_display }}
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                    </div>
                </div>
            </div>
            <!-- right body part -->
        </div>
        </div>

    </section>
    {% include 'restaurant/footer.php' %}

  </body>
</html>