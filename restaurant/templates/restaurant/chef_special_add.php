{% include 'restaurant/header.php' %}
    <div class="it-ad-hl pd-tb-md">
        <div class="rb-pd-rl">
            <div class="it-ac-hd">
                <div class="sc-hd">
                    <h1>Add to Chef Special</h1>
                </div>
            </div>
            <!-- heading -->
            <div class="ad-fd-fm pd-tb-md">
                <form method="post" action="{% url 'restaurant:chef-special-add' %}">
                    {% csrf_token %}
                    <div class="fm-ls sm-mb" id="foods">
                        <label>Select Food</label>
                        <select name="food" class="fd-ct" id="food-select">
                          {% for food in foods %}
                            <option value="{{ food.id }}">{{ food.name }}</option>
                          {% endfor %}
                        </select>
                    </div>
                    <button type="submit" class="sb-bt mx-auto d-flex">Proceed</button>
                  </form>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    </section>
  </body>
  </html>
