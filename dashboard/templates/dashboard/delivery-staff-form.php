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
                                    <h1>Add Staff</h1>
                                </div>
                                <!-- <div class="ac-bt-hl">
                                      <button class="ac-bt">Save</button>
                                    </div> -->
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <form method="post" enctype="multipart/form-data" action="{% url 'dashboard:delivery-person-create' %}">
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
                                        {% if name_empty %}
                                          <p style="color:red;">First name and last name should not be empty.</p>
                                        {% endif %}
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                              <label>First Name *</label>
                                              <input name="first_name" type="text" id="first_name" class="form-control" required />
                                            </div>
                                            <div class="fm-hf-ls">
                                              <label>Last Name *</label>
                                              <input name="last_name" type="text" id="last_name" class="form-control" required />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                              <label>Username *</label>
                                              <input name="username" type="text" id="username" class="form-control" required />
                                              {% if username_empty %}
                                                <p style="color:red;">This field is required.</p>
                                              {% endif %}
                                              {% if username_error %}
                                                <p style="color:red;">User with this username already exists.</p>
                                              {% endif %}
                                            </div>
                                            <div class="fm-hf-ls">
                                              <label>Email *</label>
                                              <input name="email" type="email" id="email" class="form-control" required />
                                              {% if email_empty %}
                                                <p style="color:red;">This field is required.</p>
                                              {% endif %}
                                              {% if email_error %}
                                                <p style="color:red;">User with this email already exists.</p>
                                              {% endif %}
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->

                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Contact</label>
                                        <input name="contact" type="text" id="contact" class="form-control" />
                                    </div>
                                    <div class="fm-ls sm-mb">
                                        <label>Address</label>
                                        <input name="address" type="text" id="address" class="form-control" />
                                    </div>
                                    <!-- form list -->

                                    <div class="fm-ls sm-mb">
                                      <button class="sb-bt mx-auto d-flex">Add Staff</button>
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
    <script>
      $(document).ready(function(){
        if ("{{ username }}"){
          $("#username").val("{{ username }}")
        }
        if ("{{ email }}"){
          $("#email").val("{{ email }}")
        }
        if ("{{ first_name }}"){
          $("#first_name").val("{{ first_name }}")
        }
        if ("{{ last_name }}"){
          $("#last_name").val("{{ last_name }}")
        }
        if ("{{ contact }}"){
          $("#contact").val("{{ contact }}")
        }
        if ("{{ address }}"){
          $("#address").val("{{ address }}")
        }
      });
    </script>
  </body>
</html>
