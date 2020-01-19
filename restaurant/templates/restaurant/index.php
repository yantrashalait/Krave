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
                                <form method="post" action=".">
                                    {% csrf_token %}
                                    <div class="fm-ls sm-mb">
                                        <label>Food Item Name</label>
                                        {{ food_form.name }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td">
                                            <div class="up-im">
                                                <input type='file' id="imgInp" name="image" />
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
                                                <img id="blah" src="{% static 'restaurant/images/upload__prv.jpg' %}" alt="your image" />
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Description</label>
                                        {{ food_form.description }}
                                    </div>
                                    <div class="fm-ls sm-mb">
                                        <label>Ingredients</label>
                                        {{ food_form.ingredients }}
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Old Price</label>
                                                {{ food_form.old_price }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>New Price</label>
                                                {{ food_form.new_price }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Calories</label>
                                                {{ food_form.calories }}
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Modifier Group (Required) Note: Some notes for Restaurant Owner</label>
                                        <div class="md-gp">
                                            <div class="md-gp-ls-rd" id="md-gp-ls-rd-id">
                                                <div class="md-gp-in">
                                                    <div class="md-gp-in-ls">
                                                        <label>Modifier Name</label>
                                                        <input type="text">
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Modifier Price</label>
                                                        <input type="text">
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Modifier Calories</label>
                                                        <input type="text">
                                                    </div>
                                                    <div class="md-gp-in-ls">
                                                        <label>Select</label>
                                                        <select class="fd-ct">
                                                            <option>Required</option>
                                                            <option>Optional</option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                            <button class="md-gp-bt" id="cl-bt-rd">Add More Modifier</button>
                                        </div>
                                    </div>
                                    <!-- form list -->

                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Choose Category</label>
                                                {{ food_form.category }}
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Preparation Time</label>
                                                {{ food_form.preparation_time }}
                                            </div>
                                        </div>
                                    </div>
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