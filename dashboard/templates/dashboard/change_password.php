{% include 'dashboard/header.php' %}
<div class="it-ad-hl pd-tb-md">
    <div class="rb-pd-rl">
        <div class="it-ac-hd">
            <div class="sc-hd">
                <h1>Change Password</h1>
            </div>
            <!-- <div class="ac-bt-hl">
                  <button class="ac-bt">Save</button>
                </div> -->
        </div>
        <!-- heading -->
        <div class="ad-fd-fm pd-tb-md">
            <form method="post">
                {% csrf_token %}
                <div>
                    <p>
                        {{ form.helptext }}
                    </p>
                </div>
                <div class="fm-ls sm-mb">
                    <label for="id_old_password">{{ form.old_password.label }}</label>
                    {{ form.old_password }}
                    {% if form.old_password.errors %}
                        <span style="color:red;">Your old password is incorrect.</span>
                    {% endif %}
                </div>


                <div class="fm-ls sm-mb">
                    <label for="id_new_password1">{{ form.new_password1.label }}</label>
                    {{ form.new_password1 }}
                    {% if form.new_password1.errors %}
                        {% for error in form.new_password1.errors %}
                            <span style="color:red;">{{ error }}</span>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="fm-ls sm-mb">
                    <label for="id_new_password2">{{ form.new_password2.label }}</label>
                    {{ form.new_password2 }}
                    {% if form.new_password2.errors %}
                        {% for error in form.new_password2.errors %}
                            <span style="color:red;">{{ error }}</span>
                        {% endfor %}
                    {% endif %}
                </div>
                <div class="fm-ls sm-mb">
                    <button type="submit" class="sb-bt mx-auto d-flex">Update Password</button>
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
