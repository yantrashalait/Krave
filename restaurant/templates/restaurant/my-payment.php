{% include 'restaurant/header.php' %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>My Earnings</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                               <table id="fd-it-ls-dt" class="display">
                                    <thead>
                                        <tr>
                                            <th>Order ID</th>
                                            <th>Date</th>
                                            <th>Amount</th>
                                            <th>Payment Type</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in earnings %}
                                        <tr>
                                            <td>
                                                <a href="{% url 'restaurant:order-detail' request.restaurant.id item.order.id %}">#{{ item.order.id_string }}</a>
                                            </td>
                                            <td>{{ item.date }}</td>
                                            <td>
                                                ${{ item.payment_amount }}
                                            </td>
                                            <td>
                                                {{ item.order.get_payment_display }}
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
