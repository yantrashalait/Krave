{% include 'restaurant/header.php' %}
    <div class="it-ad-hl pd-tb-md">
        <div class="rb-pd-rl">
            <div class="it-ac-hd">
                <div class="sc-hd">
                    <h1>Add Order</h1>
                </div>
            </div>
            <!-- heading -->
            <div class="ad-fd-fm pd-tb-md">
                <form method="post" action=".">
                    {% csrf_token %}
                    <div class="fm-ls sm-mb" id="foods">
                        <label>Food Name</label>
                        <select name="food" class="fd-ct" id="food-select">
                          {% for food in foods %}
                            <option value="{{ food.id }}">{{ food.name }}</option>
                          {% endfor %}
                        </select>

                    </div>
                    <div class="fm-ls sm-mb">
                      <label>Quantity</label>
                      <input type="number" name="qty" required>
                    </div>

                    <div class="fm-ls sm-mb">
                      <label>Select Style(choose any one of the following)</label>
                      <div id="styles">

                      </div>
                    </div>
                    <div class="fm-ls sm-mb">
                      <label>Select Extras</label>
                      <div id="extras">

                      </div>
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
    {% include 'restaurant/footer.php' %}
    <script>
      $(document).ready(function(){
        var food_id = $("#food-select").children("option:selected").val();
        $.ajax({
          url: "{% url 'core:get-food-detail' %}",
          data: {
            'food_id': food_id,
          },
          dataType: 'json',
          success: function(result){
            var data = result;

            $("#styles").html("");
            var styles = [];
            styles = data.styles;
            styles = jQuery.parseJSON(styles);

            styles.forEach(function(style){
              var style_content = '<div class="radio__wrapper"><div class="radio__wrapper__content"><input type="radio" name="radio3" value="'+ style.fields.name_of_style.split(' ').join('_') +'"><span> '+ style.fields.name_of_style +' </span></div><div class="radio__price"><span>$'+ style.fields.cost +'</span></div></div>'
              $("#styles").append(style_content);
            });

            $("#extras").html("");
            var extras = [];
            extras = data.extras;
            extras = jQuery.parseJSON(extras);

            extras.forEach(function(extra){
              var extra_content = '<div class="checkbox__wrapper__new"><div class="checkbox__wrapper__content"><input name="extras" type="checkbox" value="'+ extra.fields.name_of_extra.split(' ').join('_') +'"><span> '+ extra.fields.name_of_extra +'</span></div><div class="checkbox__price"><span>$5</span></div></div>'
              $("#extras").append(extra_content);
            });

          }
        })
      });
      $('#food-select').on('change', function(){
        var food_id = $(this).children("option:selected").val();
        $.ajax({
          url: "{% url 'core:get-food-detail' %}",
          data: {
            'food_id': food_id,
          },
          dataType: 'json',
          success: function(result){
            var data = result;

            $("#styles").html("");
            var styles = [];
            styles = data.styles;
            styles = jQuery.parseJSON(styles);

            styles.forEach(function(style){
              var style_content = '<div class="radio__wrapper"><div class="radio__wrapper__content"><input type="radio" name="radio3" value="'+ style.fields.name_of_style.split(' ').join('_') +'"><span> '+ style.fields.name_of_style +' </span></div><div class="radio__price"><span>$'+ style.fields.cost +'</span></div></div>'
              $("#styles").append(style_content);
            });

            $("#extras").html("");
            var extras = [];
            extras = data.extras;
            extras = jQuery.parseJSON(extras);

            extras.forEach(function(extra){
              var extra_content = '<div class="checkbox__wrapper__new"><div class="checkbox__wrapper__content"><input name="extras" type="checkbox" value="'+ extra.fields.name_of_extra.split(' ').join('_') +'"><span> '+ extra.fields.name_of_extra +'</span></div><div class="checkbox__price"><span>$5</span></div></div>'
              $("#extras").append(extra_content);
            });

          }
        })
      });
    </script>

  </body>
  </html>
