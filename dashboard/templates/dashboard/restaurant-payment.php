{% include 'dashboard/header.php' %}
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
                                            <th>Date</th>
                                            <th>Amount</th>
                                            <th>Payment Type</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in earnings %}
                                        <tr>
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
    {% include 'dashboard/footer.php' %}

  </body>
</html>
