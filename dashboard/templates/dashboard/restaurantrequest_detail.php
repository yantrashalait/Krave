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
                                      <h2>{{ req.name_of_owner }}</h2>
                                      <h3>{{ req.registration_number }}</h3>
                                      </div>
                                      <div class="customer-inftxt">
                                          <span class="cus-inf-attributes"><i class="fa fa-phone" aria-hidden="true"></i>{{ req.contact }}</span>
                                          <span class="cus-inf-attributes"><i class="fa fa-map-marker" aria-hidden="true"></i>{{ req.street }}, {{ req.town }}, {{ req.state }}- {{ req.zip_code }}</span>
                                          <span class="cus-inf-attributes"><i class="fa fa-envelope-open-o" aria-hidden="true"></i>{{ req.email_of_owner }}</span>
                                      </div>

                                      <div class="customer-inftxt">
                                          <span class="cus-inf-attributes"><i class="fa fa-calendar-check-o" aria-hidden="true"></i>Requested at {{ req.requested_date }}</span>
                                      </div>
                                  </div>
                                  <div class="customer-instructions-pop">
                                      <h2>Message</h2>
                                      <div class="fm-ls sm-mb">
                                          {{ req.message }}
                                      </div>
                                      <p>Does this restaurant provide delivery service?<span><b>{% if req.does_your_restaurant_staff_deliver_order %} Yes{% else %} No{% endif %}</b></span></p>
                                  </div>
                                  <a href="{% url 'dashboard:accept-request' req.id %}" class="btn btn-success">Accept</a>
                                  <a href="{% url 'dashboard:decline-request' req.id %}" class="btn btn-danger">Decline</a>
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
