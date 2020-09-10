{% load static %}
{% include 'dashboard/header.php' %}
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
                                    <h1>Add Category</h1>
                                </div>
                                <!-- <div class="ac-bt-hl">
                                      <button class="ac-bt">Save</button>
                                    </div> -->
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <form method="post" enctype="multipart/form-data" action="{% if form.instance %}{% url 'dashboard:category-edit' form.instance.pk %}{% else %}{% url 'dashboard:category-create' %}{% endif %}">
                                    {% csrf_token %}
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
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                              <label>Name *</label>
                                              {{ form.name }}
                                            </div>
                                        </div>
                                        {% if form.name.errors %}
                                            {{ form.name.errors }}
                                        {% endif %}
                                    </div>

                                    <div class="fm-ls sm-mb">
                                      <button class="sb-bt mx-auto d-flex">Submit</button>
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

    {% include 'dashboard/footer.php' %}
  </body>
</html>
