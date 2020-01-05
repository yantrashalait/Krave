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
                                <form>
                                    <div class="fm-ls sm-mb">
                                        <label>Food Item Name</label>
                                        <input type="text" placeholder="Item Name">
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
                                                <img id="blah" src="{% static 'restaurant/images/upload__prv.jpg' %}" alt="your image" />
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Description</label>
                                        <textarea placeholder="Keep it more descriptive in less words"></textarea>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <div class="fm-ls-td js-sb">
                                            <div class="fm-hf-ls">
                                                <label>Price</label>
                                                <input type="text" placeholder="Price">
                                            </div>
                                            <div class="fm-hf-ls">
                                                <label>Calories</label>
                                                <input type="text" placeholder="Calories">
                                            </div>
                                        </div>
                                    </div>
                                    <!-- form list -->
                                    <div class="fm-ls sm-mb">
                                        <label>Modifier Group (Required) Note: Some notes for Restaurant Owner</label>
                                        <div class="md-gp">
                                            <div class="md-gp-ls" id="md-gp-ls-id">
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
                                                </div>
                                            </div>
                                            <button class="md-gp-bt" id="cl-bt">Add More Modifier</button>
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
                                            <div class="fm-hf-ls">
                                                <label>Preparation Time</label>
                                                <input type="text" placeholder="Eg (10-20)">
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