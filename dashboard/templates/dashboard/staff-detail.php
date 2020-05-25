{% include 'dashboard/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>{{ restaurant.name|title }}</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <div class="order-details-pop">
                                    <div class="order-detail-mainttl">
                                    </div>
                                    <div class="customer-info-pop">
                                        <div class="customer-name-prnt">
                                        <h2>{{ restaurant.owner }}</h2>
                                        <h3>{{ restaurant.registration_number }}</h3>
                                        </div>
                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-phone" aria-hidden="true"></i>{{ restaurant.contact }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-map-marker" aria-hidden="true"></i>{{ restaurant.street }}, {{ restaurant.town }}, {{ restaurant.state }}- {{ restaurant.zip_code }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-envelope-open-o" aria-hidden="true"></i>{{ restaurant.email }}</span>
                                        </div>

                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-clock-o"></i>Opens at: {{ restaurant.opening_time }} & Closes at: {{ restaurant.closing_time }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-calendar-check-o" aria-hidden="true"></i>Joined at {{ restaurant.joined_date }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-credit-card"></i>Delivery charge: ${{ restaurant.delivery_charge }}</span>
                                        </div>
                                    </div>

                                    <div class="customer-instructions-pop">
                                        <h2>Location</h2>
                                        <div class="fm-ls sm-mb">
                                            <div id="map" style="height: 500px; width: 1100px;"></div>
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
    {% include 'dashboard/footer.php' %}

  </body>
</html>
