{% include 'dashboard/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>{{ staff.username|title }}</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <div class="order-details-pop">
                                    <div class="order-detail-mainttl">
                                    </div>
                                    <div class="customer-info-pop">
                                        <div class="customer-name-prnt">
                                          <h2>{{ staff.first_name|title }} {{ staff.last_name|title }}</h2>
                                          <h3>Last login: {{ staff.last_login }}</h3>
                                        </div>
                                        <div class="pv-im-hl">
                                            <img src="{{ staff.profile.image.url }}">
                                        </div>
                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-phone" aria-hidden="true"></i>{{ staff.profile.contact }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-map-marker" aria-hidden="true"></i>{{ staff.profile.address }}</span>
                                            <span class="cus-inf-attributes"><i class="fa fa-envelope-open-o" aria-hidden="true"></i>{{ staff.email }}</span>
                                        </div>

                                        <div class="customer-inftxt">
                                            <span class="cus-inf-attributes"><i class="fa fa-calendar-check-o" aria-hidden="true"></i>Joined at {{ staff.date_joined }}</span>
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
