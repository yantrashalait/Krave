{% load static %}
{% include 'restaurant/header.php' %}
                    <div class="rh-bd-tp-m-hl">
                        <div class="rb-pd-rl">
                            <div class="tp-m">
                                <div class="fr-pr">
                                    <ul>
                                        <li>
                                            <a href="#"><i class="fa fa-eye" aria-hidden="true"></i>View Online</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- right top menu -->
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Add Food Item</h1>
                                </div>
                                <!-- <div class="ac-bt-hl">
                                      <button class="ac-bt">Save</button>
                                    </div> -->
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <form method="post" enctype="multipart/form-data" action="{% if form.instance.name %}{% url 'restaurant:menu-edit' request.restaurant.id foodmenu.id %}{% else %}{% url 'restaurant:dashboard' request.restaurant.id %}{% endif %}">
                                    {% csrf_token %}
                                    <div class="fm-ls sm-mb">
                                        <label>Food Item Name</label>
                                        {{ form.name }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td">
                                            <div class="up-im">
                                                <input type='file' id="id_img" name="image" />
                                                <div class="up-im-bt">
                                                    <div class="up-im-cn">
                                                        <div class="up-im-bt-tl">
                                                            <p>Drop image here to upload</p>
                                                        </div>
                                                        <div class="up-im-bt-dv">
                                                            <p>or</p>
                                                        </div>
                                                        <div class="up-im-bt-bw">
                                                            Browse File
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="pv-im-hl">
                                                {% if form.instance.image %}
                                                    <img id="food_blah" src="{{ form.instance.image.url }}" alt="your image" />
                                                {% else %}
                                                    <img id="food_blah" src="{% static 'restaurant/images/upload__prv.jpg' %}" alt="your image" />
                                                {% endif %}
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Description</label>
                                        {{ form.description }}
                                    </div>
                                    <div class="fm-ls sm-mb">
                                        <label>Ingredients</label>
                                        {{ form.ingredients }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Old Price</label>
                                                {{ form.old_price }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>New Price</label>
                                                {{ form.new_price }}
                                            </div>
                                        </div>
                                    </div>

                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Choose Category</label>
                                                {{ form.category }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Preparation Time</label>
                                                {{ form.preparation_time }}
                                            </div>
                                        </div>
                                    </div>
                                    {% for error in form.errors %}
                                    <p>{{ error }}</p>
                                    {% endfor %}
                                    <!-- form list -->

                                    <!-- form list -->
                                    {{ styleform.management_form }}
                                    <div class="fm-ls sm-mb">
                                        <label>Styles that can come with the food item.</label>
                                            <div class="md-gp">
                                    {% for style_single in styleform.forms %}
                                            <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                <div style="display: none;">
                                                    {{ style_single.id }}
                                                </div>
                                                <div class="md-gp-in">
                                                    <div class="md-gp-in-ls">
                                                        <label>Name of style*</label>
                                                        {{ style_single.name_of_style }}
                                                        {% if style_single.name_of_style.errors %}
                                                        {{ style_single.name_of_style.errors }}
                                                        {% endif %}
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Price</label>
                                                        {{ style_single.cost }}
                                                        {% if style_single.cost.errors %}
                                                        {{ style_single.cost.errors }}
                                                        {% endif %}
                                                    </div>
                                                </div>
                                            </div>
                                            {% for error in style_single.errors %}
                                            <p>{{ error }}</p>
                                            {% endfor %}
                                            {% with styleform.empty_form as form %}
                                            <div id="styleempty_form" style="display:none">
                                                <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                    <div class="md-gp-in">
                                                        <div style="display: none;">
                                                            {{ form.id }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Name of style*</label>
                                                            {{ form.name_of_style }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Price</label>
                                                            {{ form.cost }}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            {% endwith %}

                                    {% endfor %}
                                    <button class="md-gp-bt" id="cl-bt-rd">Add More Styles</button>
                                    </div>
                                  </div>


                                    <!-- form list -->

                                    {{ extraform.management_form }}
                                    <div class="fm-ls sm-mb">
                                        <label>Extras that can come with the food item.</label>
                                        <div class="md-gp">
                                    {% for extra_single in extraform.forms %}
                                            <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                <div style="display: none;">
                                                    {{ extra_single.id }}
                                                </div>
                                                <div claid_logoss="md-gp-in">
                                                    <div class="md-gp-in-ls">
                                                        <label>Name of extra*</label>
                                                        {{ extra_single.name_of_extra }}
                                                        {% if extra_single.name_of_extra.errors %}
                                                        {{ extra_single.name_of_extra.errors }}
                                                        {% endif %}
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Price</label>
                                                        {{ extra_single.cost }}
                                                        {% if extra_single.cost.errors %}
                                                        {{ extra_single.cost.errors }}
                                                        {% endif %}
                                                    </div>
                                                </div>
                                            </div>
                                            {% for error in extra_single.errors %}
                                            <p>{{ error }}</p>
                                            {% endfor %}
                                            {% with extraform.empty_form as form %}
                                            <div id="extraempty_form" style="display:none">
                                                <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                    <div class="md-gp-in">
                                                        <div style="display: none;">
                                                            {{ form.id }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Name of extra*</label>
                                                            {{ form.name_of_extra }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Price</label>
                                                            {{ form.cost }}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            {% endwith %}

                                    {% endfor %}
                                    <button class="md-gp-bt" id="cl-bt-rd-et">Add More Extras</button>
                                  </div>
                                </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                      {% if form.instance.pk %}
                                      <button class="sb-bt mx-auto d-flex">Edit Food Item</button>
                                      {% else %}
                                      <button class="sb-bt mx-auto d-flex">Add Food Item</button>
                                      {% endif %}
                                    </div>
                                </form>
                            </div>
                    </div>
                </div>
            </div>
            <!-- right body part -->
        </div>
        </div>

    </section>

    {% include 'restaurant/footer.php' %}
    <script>
        $("#cl-bt-rd").click(function (e) {
            e.preventDefault();
            var $self = $(this);
            var form_idx = $('#id_styleform-TOTAL_FORMS').val();
            var cloneIndexrd = $(".md-gp-ls-rd").length;
            $self.before($('#styleempty_form').html().replace(/__prefix__/g, form_idx));
            $('#id_styleform-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        });

        $("#cl-bt-rd-et").click(function (e) {
            e.preventDefault();
            var $self = $(this);
            var form_idx = $('#id_extraform-TOTAL_FORMS').val();
            var cloneIndexrd = $(".md-gp-ls-rd").length;
            $self.before($('#extraempty_form').html().replace(/__prefix__/g, form_idx));
            $('#id_extraform-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        });
    </script>
  </body>
</html>
