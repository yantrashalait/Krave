{% include 'dashboard/header.php' %}
                    <div class="it-ad-hl pd-tb-md">
                        <div class="rb-pd-rl">
                            <div class="it-ac-hd">
                                <div class="sc-hd">
                                    <h1>List of Delivery Persons</h1>
                                </div>
                                <div class="ac-bt-hl">
                                      <a href="{% url 'dashboard:delivery-person-create' %}"><button class="ac-bt"><i class="fa fa-plus"></i> Add Delivery Person</button></a>
                                    </div>
                            </div>
                            <!-- heading -->
                            <div class="ad-fd-fm pd-tb-md">
                               <table id="fd-it-ls-dt" class="display">
                                    <thead>
                                        <tr>
                                            <th>Username</th>
                                            <th>Full name</th>
                                            <th>Email</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in staffs %}
                                        <tr>
                                            <td>{{ item.username }}</td>
                                            <td>
                                                {{ item.first_name }} {{ item.last_name }}
                                            </td>
                                            <td>
                                                {{ item.email }}
                                            </td>
                                            <td class="ac-bt-hl-fd-ls">
                                                <a href="{% url 'dashboard:delivery-person-detail' item.pk %}" class="btn btn-success">View detail</a>
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
    {% include 'dashboard/footer.php' %}

  </body>
</html>
