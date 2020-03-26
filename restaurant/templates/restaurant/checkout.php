{% include 'restaurant/header.php' %}
<div class="it-ad-hl pd-tb-md">
    <div class="rb-pd-rl">
        <div class="it-ac-hd">
            <div class="sc-hd">
                <h1>Your Orders</h1>
                <a class="btn btn-success" href="{% url 'restaurant:manual-order' %}"><i class="fa fa-plus"></i> Add More Foods</a>
            </div>
            <!-- <div class="ac-bt-hl">
                  <button class="ac-bt">Save</button>
                </div> -->
        </div>
        <!-- heading -->
        <div class="ad-fd-fm pd-tb-md">
            <table id="fd-it-ls-dt" class="display">
                <thead>
                    <tr>
                        <th>Food Name</th>
                        <th>Quantity</th>
                        <th>Extras</th>
                        <th>Total Price</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                  {% for cart in carts %}
                    <tr>
                      <td>{{ cart.food.name }}{% if cart.style %} - {{ cart.style.name_of_style }}{% endif %}</td>
                      <td>{{ cart.number_of_food }}</td>
                      <td>
                        {% for extra in cart.extras.all %}
                          {{ extra.name_of_extra }} - ${{ extra.cost }}<br>
                        {% endfor %}
                      </td>
                      <td>${{ cart.get_total }}</td>
                      <td class="ac-bt-hl-fd-ls">
                        <a href="{% url 'restaurant:cart-delete' cart.pk %}" class="btn btn-danger">Delete</a>
                      </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <a href="{% url 'restaurant:add-to-order' %}"><button class="sb-bt mx-auto d-flex">Proceed to order</button></a>
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
