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
                                <form>
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Name</label>
                                        <input type="text" placeholder="Item Name" value="Restaurant Name">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td">
                                            <div class="up-im">
                                                <input type='file' id="imgInp" />
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
                                                <img id="blah" src="{% static 'restaurant/images/rest_logo.jpg' %}" alt="your image" />
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Location</label>
                                        <input type="text" placeholder="Item Name" value="Restaurant Location">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Contact Number</label>
                                        <input type="text" placeholder="Item Name" value="12352625">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Email Address</label>
                                        <input type="text" placeholder="Item Name" value="test@gmail.com">
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Restaurant Registration Number</label>
                                        <input type="text" placeholder="Item Name" value="NB 125362">
                                    </div>
                                    <!-- form list -->                                    
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Opening Time</label>
                                                <input type="text" value="6:00 am">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Closing TIme</label>
                                                <input type="text" value="9:00 pm">
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Delivery Time</label>
                                                <input type="text" value="10 - 40 min">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Delivery Charge</label>
                                                <input type="text" value="$2">
                                            </div>
                                        </div>
                                    </div>    
                                    <!-- form list -->                               
                                    <div class="fm-ls sm-mb">
                                        <label>Types of Cuisines</label>
                                                <select class="fd-ct" multiple="multiple">
                                                    <option></option>
                                                    <option>Chef's Special</option>
                                                    <option>Shakes & desert</option>
                                                    <option>Snakers</option>
                                                    <option>Drinks</option>
                                                    <option>Chef's Special</option>
                                                    <option>Shakes & desert</option>
                                                    <option>Snakers</option>
                                                    <option>Drinks</option>
                                                    <option>Chef's Special</option>
                                                    <option>Shakes & desert</option>
                                                    <option>Snakers</option>
                                                    <option>Drinks</option>
                                                </select>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                      <button class="sb-bt mx-auto d-flex">Update Restaurant Details</button>
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