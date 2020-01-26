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
                                        <input type="text" name="name" placeholder="Item Name" value="{{ request.restaurant.name }}" >
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
                                                <img id="blah" src="{{ request.restaurant.logo.url }}" alt="your image" />
                                            
                                            {% else %}
                                                <img id="blah" src="{% static 'restaurant/images/rest_logo.jpg' %}" alt="your image" />
                                            {% endif  %}

                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Location</label>
                                        <input type="text" name="town" placeholder="Item Name" value="{{ request.restaurant.town }}">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Contact Number</label>
                                        <input type="text" name="contact" placeholder="Item Name" value="{{ request.restaurant.contact }}">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Email Address</label>
                                        <input type="text" name="email" placeholder="Item Name" value="{{ request.restaurant.email }}">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Registration Number</label>
                                        <input type="text" name="registration_number" placeholder="Item Name" value="{{ request.restaurant.registration_number }}">
                                    </div>
                                    <!-- form list -->                                    
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Opening Time</label>
                                                <input type="time" name="opening_time" value="{{ request.restaurant.opening_time|time:'H:i' }}">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Closing TIme</label>
                                                <input type="time" name="closing_time" value="{{ request.restaurant.closing_time|time:'H:i' }}">
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Delivery Time</label>
                                                <input type="text" name="delivery_time" value="{{ request.restaurant.delivery_time }}" placeholder="20-30">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Delivery Charge</label>
                                                <input type="text" name="delivery_charge" value= "{{ request.restaurant.delivery_charge }}">
                                            </div>
                                        </div>
                                    </div>   
                                    {% if rest_cuisine %} 
                                    <div class="fm-ls sm-mb">
                                        <label>Selected Cuisines</label>
                                        
                                        {% for item in rest_cuisine.cuisine.all %}
                                        <p>
                                            <span>{{ item.name }}</span>
                                        </p>
                                        {% endfor %}
                                        
                                    </div>
                                    {% endif %}
                                    <!-- form list -->                               
                                    <div class="fm-ls sm-mb">
                                        <label>Types of Cuisines</label>
                                        
                                            <select name="cuisines" class="fd-ct" multiple="multiple">
                                                <option></option>
                                                {% for item in cuisine %}
                                                <option>{{ item.name }}</option>
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