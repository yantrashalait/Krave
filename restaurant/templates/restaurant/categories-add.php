{% load static %}
{% include 'restaurant/header.php' %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Add Category</h1>
                                </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <form method="post" enctype="multipart/form-data" action="{% if form.instance.pk %}{% url 'restaurant:category-edit' request.restaurant.id restaurantfoodcategory.id %}{% else %}{% url 'restaurant:category-add' request.restaurant.id %}{% endif %}">
                                    {% csrf_token %}
                                    <div class="fm-ls sm-mb">
                                        <label>Category Name</label>
                                        {{ form.category }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td">
                                            <div class="up-im">
                                                <input type='file' name="image" id="id_cat_image" />
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
                                                <img id="cat_image_blah" src="{{ form.instance.image.url }}" alt="your image" />

                                            {% else %}
                                                <img id="cat_image_blah" src="{% static 'restaurant/images/rest_logo.jpg' %}" alt="your image" />
                                            {% endif  %}

                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                      {% if form.instance.pk %}
                                      <button class="sb-bt mx-auto d-flex">Edit Category</button>
                                      {% else %}
                                      <button class="sb-bt mx-auto d-flex">Add Category</button>
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

  </body>
</html>
