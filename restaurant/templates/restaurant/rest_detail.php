{% include 'restaurant/header.php' %}
{% load static %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>Edit Your Restaurant Details</h1>
                                </div>
                                <!-- <div class="ac-bt-hl">
                                      <button class="ac-bt">Save</button>
                                    </div> -->
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                                <form method="POST" action="{% url 'restaurant:edit-restaurant' %}" enctype="multipart/form-data">
                                    {% csrf_token %}
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Name</label>
                                        <input type="text" name="name" placeholder="Item Name" value="{{ detail.name }}" >
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td">
                                            <div class="up-im">
                                                <input type='file' name="logo" id="imgInp" />
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
                                            {% if request.restaurant.logo %}
                                                <img id="blah" src="{{ detail.logo.url }}" alt="your image" />
                                            
                                            {% else %}
                                                <img id="blah" src="{% static 'restaurant/images/rest_logo.jpg' %}" alt="your image" />
                                            {% endif  %}

                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Location</label>
                                        <input type="text" name="town" placeholder="Item Name" value="{{ detail.town }}">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Contact Number</label>
                                        <input type="text" name="contact" placeholder="Item Name" value="{{ detail.contact }}">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Email Address</label>
                                        <input type="text" name="email" placeholder="Item Name" value="{{ detail.email }}">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Registration Number</label>
                                        <input type="text" name="registration_number" placeholder="Item Name" value="{{ detail.registration_number }}">
                                    </div>
                                    <!-- form list -->                                    
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Opening Time</label>
                                                <input type="time" name="opening_time" value="{{ detail.opening_time|time:'H:i' }}">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Closing TIme</label>
                                                <input type="time" name="closing_time" value="{{ detail.closing_time|time:'H:i' }}">
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Delivery Time</label>
                                                <input type="text" name="delivery_time" value="{{ detail.delivery_time }}" placeholder="20-30">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Delivery Charge</label>
                                                <input type="text" name="delivery_charge" value= "{{ detail.delivery_charge }}">
                                            </div>
                                        </div>
                                    </div>    
                                    <!-- form list -->                               
                                    <div class="fm-ls sm-mb">
                                        <label>Types of Cuisines</label>
                                        
                                                <select name="cuisines" class="fd-ct" multiple="multiple">
                                                    <option></option>
                                                    {% for item in cuisine %}
                                                    {% for selected_cuisine in rest_cuisine.cuisine.all %}
                                                    {% if item == selected_cuisine %}
                                                        <option selected>{{ item.name }}</option>
                                                    {% else %}
                                                        <option>{{ item.name }}</option>
                                                    {% endif %}
                                                    <!-- <option>Shakes & desert</option>
                                                    <option>Snakers</option>
                                                    <option>Drinks</option>
                                                    <option>Chef's Special</option>
                                                    <option>Shakes & desert</option>
                                                    <option>Snakers</option>
                                                    <option>Drinks</option>
                                                    <option>Chef's Special</option>
                                                    <option>Shakes & desert</option>
                                                    <option>Snakers</option>
                                                    <option>Drinks</option> -->
                                                    {% endfor %}
                                                    {% endfor %}
                                                </select>
                                              
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                      <button type="submit" class="sb-bt mx-auto d-flex">Update Restaurant Details</button>
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