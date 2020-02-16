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
