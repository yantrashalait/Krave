{% load static %}
{% include 'restaurant/header.php' %}
                    <div class="rh-bd-tp-m-hl">
                        <div class="rb-pd-rl">
                            <div class="tp-m">
                                <!-- <div class="fr-u">
                                    <ul>
                                        <li>
                                            <a href="#">Overview</a>
                                        </li>
                                        <li>
                                            <a href="#">Menus</a>
                                        </li>
                                        <li>
                                            <a href="#">Categories</a>
                                        </li>
                                        <li class="active">
                                            <a href="#">Items</a>
                                        </li>
                                        <li>
                                            <a href="#">Modifier Groups</a>
                                        </li>
                                    </ul>
                                </div> -->
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
                                                    <img id="blah" src="{{ form.instance.image.url }}" alt="your image" />
                                                {% else %}
                                                    <img id="blah" src="{% static 'restaurant/images/upload__prv.jpg' %}" alt="your image" />
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
                                            <div class="fm-hf-ls">
                                                <label>Calories</label>
                                                {{ form.calories }}
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
                                    {{ modifierform.management_form }}
                                    {% for modifier_single in modifierform.forms %}
                                    <div class="fm-ls sm-mb">
                                        <label>Modifier Group (Required) Note: Some notes for Restaurant Owner</label>
                                        <div class="md-gp">
                                            <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                <div style="display: none;">
                                                    {{ modifier_single.id }}
                                                </div>
                                                <div class="md-gp-in">
                                                    <div class="md-gp-in-ls">
                                                        <label>Modifier Name</label>
                                                        {{ modifier_single.name_of_ingredient }}
                                                        {% if modifier_single.name_of_ingredient.errors %}
                                                        {{ modifier_single.name_of_ingredient.errors }}
                                                        {% endif %}
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Modifier Price</label>
                                                        {{ modifier_single.cost_of_addition }}
                                                        {% if modifier_single.cost_of_addition.errors %}
                                                        {{ modifier_single.cost_of_addition.errors }}
                                                        {% endif %}
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Modifier Calories</label>
                                                        {{ modifier_single.calories }}
                                                        {% if modifier_single.calories.errors %}
                                                        {{ modifier_single.calories.errors }}
                                                        {% endif %}
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Type Of Modifier</label>
                                                        {{ modifier_single.type }}
                                                        {% if modifier_single.type.errors %}
                                                        {{ modifier_single.type.errors }}
                                                        {% endif %}
                                                    </div>
                                                </div>
                                            </div>
                                            {% for error in modifier_single.errors %}
                                            <p>{{ error }}</p>
                                            {% endfor %}
                                            {% with modifierform.empty_form as form %}
                                            <div id="modifierempty_form" style="display:none">
                                                <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                    <div class="md-gp-in">
                                                        <div style="display: none;">
                                                            {{ form.id }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Modifier Name</label>
                                                            {{ form.name_of_ingredient }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Modifier Price</label>
                                                            {{ form.cost_of_addition }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Modifier Calories</label>
                                                            {{ form.calories }}
                                                        </div>
                                                        <div class="md-gp-in-ls">
                                                            <label>Type Of Modifier</label>
                                                            {{ form.type }}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            {% endwith %}
                                            <button class="md-gp-bt" id="cl-bt-rd">Add More Modifier</button>
                                        </div>
                                    </div>
                                    {% endfor %}
                                    
                                    <!-- form list -->

                                    <div class="fm-ls sm-mb">
                                      <button class="sb-bt mx-auto d-flex">Add Food Item</button>
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
            var form_idx = $('#id_modifierform-TOTAL_FORMS').val();
            var cloneIndexrd = $(".md-gp-ls-rd").length;
            $self.before($('#modifierempty_form').html().replace(/__prefix__/g, form_idx));
            $('#id_modifierform-TOTAL_FORMS').val(parseInt(form_idx) + 1);
        });
    </script>
  </body>
</html>
