{% load static %}
{% include 'restaurant/header.php' %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Categories</h1>
                                    <a class="btn btn-success" href="{% url 'restaurant:category-add' request.restaurant.id %}"><i class="fa fa-plus"></i> Add Category</a>
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
                                            <th>Category Name</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                      {% for category in categories %}
                                        <tr>
                                            <td>{{ category.category }}</td>
                                            <td class="ac-bt-hl-fd-ls">
                                              <a href="{% url 'restaurant:category-edit' request.restaurant.id category.id %}" class="btn btn-primary">Edit</a>
                                              <a href="{% url 'restaurant:category-delete' request.restaurant.id category.id %}" class="btn btn-danger">Delete</a>
                                            </td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
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
