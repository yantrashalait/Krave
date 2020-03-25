{% include 'restaurant/header.php' %}
    <div class="it-ad-hl pd-tb-md">
        <div class="rb-pd-rl">
            <div class="it-ac-hd">
                <div class="sc-hd">
                    <h1>Place Order</h1>
                </div>
            </div>
            <!-- heading -->
            <div class="ad-fd-fm pd-tb-md">
                <form method="post" action="#">
                    {% csrf_token %}
                    <div class="fm-ls sm-mb">
                        <label>First Name*</label>
                        <input type="text" class="form-control" name="first_name" required>
                    </div>
                    <div class="fm-ls sm-mb">
                        <div class="fm-ls-td js-sb">
                            <div class="fm-hf-ls">
                                <label>Middle Name</label>
                                <input type="text" class="form-control" name="middle_name">
                            </div>
                            <div class="fm-hf-ls">
                                <label>Last Name*</label>
                                <input type="text" class="form-control" name="last_name" required>
                            </div>
                        </div>
                    </div>
                    <div class="fm-ls sm-mb">
                        <div class="fm-ls-td js-sb">
                            <div class="fm-hf-ls">
                                <label>Email*</label>
                                <input type="text" class="form-control" name="email" required>
                            </div>
                            <div class="fm-hf-ls">
                                <label>Contact Number*</label>
                                <input type="text" class="form-control" name="contact" required>
                            </div>
                        </div>
                    </div>
                    <div class="fm-ls sm-mb">
                        <div class="fm-ls-td js-sb">
                            <div class="fm-hf-ls">
                                <label>Address Line 1*</label>
                                <input type="text" class="form-control" name="address1" required>
                            </div>
                            <div class="fm-hf-ls">
                                <label>Address Line 2*</label>
                                <input type="text" class="form-control" name="address2" required>
                            </div>
                        </div>
                    </div>
                    <div class="fm-ls sm-mb">
                        <div class="fm-ls-td js-sb">
                            <div class="fm-hf-ls">
                                <label>City*</label>
                                <input type="text" class="form-control" name="city" required>
                            </div>
                            <div class="fm-hf-ls">
                                <label>State*</label>
                                <input type="text" class="form-control" name="state" required>
                            </div>
                        </div>
                    </div>
                    <div class="fm-ls sm-mb">
                        <div class="fm-ls-td js-sb">
                            <div class="fm-hf-ls">
                                <label>Zip Code*</label>
                                <input type="text" class="form-control" name="zip" required>
                            </div>
                        </div>
                    </div>
                    <div class="fm-ls sm-mb" id="foods">
                        <label>Leave a note...</label>
                        <textarea class="form-control" name="comment" placeholder="Leave a note..." rows="4"></textarea>
                    </div>
                    <button type="submit" class="sb-bt mx-auto d-flex">Place Order</button>
                  </form>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    </section>
    {% include 'restaurant/footer.php' %}

  </body>
  </html>
